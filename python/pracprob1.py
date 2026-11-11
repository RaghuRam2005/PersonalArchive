from __future__ import annotations

import glob
import logging
import os
import random
import shutil
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import List, Tuple

from PIL import Image

import multiprocessing as mp

import torch
import flwr
from flwr.client import Client, ClientApp, NumPyClient
from flwr.server import ServerApp, ServerConfig, ServerAppComponents
from flwr.server.strategy import FedAvg
from flwr.simulation import run_simulation
from ultralytics import YOLO

# --------------------
# Default configuration
# --------------------
RAW_IMAGES_DIR = Path("/content/drive/MyDrive/object_detection_data/training/image_2")
RAW_LABELS_DIR = Path("/content/drive/MyDrive/object_detection_data/training/label_2")
OUTPUT_DIR = Path("prepared_data")
NUM_CLIENTS = 1
GLOBAL_TRAIN_RATIO = 0.8
GLOBAL_MODEL_NAME = "yolov8n.pt"
EPOCHS_GLOBAL = 1
EPOCHS_CLIENT = 2
TRAIN_IMAGE_COUNT = 500
IMAGE_EXTS = (".png", ".jpg", ".jpeg")

# Class mapping: KITTI -> YOLO
CLASS_MAP = {
    "Car": 0,
    "Truck": 1,
    "Cyclist": 2,
    "Misc": 3,
    "Pedestrian": 4,
    "Van": 5,
    "Tram": 6,
}



# --------------------
# Utilities
# --------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
logging.info(f"Training on {DEVICE}")
logging.info(f"Flower {flwr.__version__} / PyTorch {torch.__version__}")

def is_image_file(p: Path) -> bool:
    return p.suffix.lower() in IMAGE_EXTS


def count_images_in_dir(d: Path) -> int:
    if not d.exists():
        return 0
    return sum(1 for _ in d.rglob("*") if _.suffix.lower() in IMAGE_EXTS)


# --------------------
# Label conversion: KITTI -> YOLO
# --------------------

def convert_kitti_to_yolo(label_file: Path, img_w: int, img_h: int) -> List[str]:
    """Convert KITTI format labels to YOLO format.

    Returns a list of lines (strings) in YOLO format. If label_file does not exist or is empty,
    returns an empty list.
    """
    yolo_labels: List[str] = []

    if not label_file.exists():
        return yolo_labels

    try:
        with open(label_file, "r") as f:
            for line in f:
                parts = line.strip().split()
                # KITTI lines should have at least 8 fields (type, trunc, occl, alpha, x1, y1, x2, y2, ...)
                if len(parts) < 8:
                    continue

                cls_name = parts[0]
                if cls_name == "DontCare" or cls_name not in CLASS_MAP:
                    continue

                cls_idx = CLASS_MAP[cls_name]
                x1, y1, x2, y2 = map(float, parts[4:8])

                # Convert to YOLO format (center_x, center_y, width, height) normalized
                cx = (x1 + x2) / 2.0 / img_w
                cy = (y1 + y2) / 2.0 / img_h
                w = (x2 - x1) / img_w
                h = (y2 - y1) / img_h

                # Clamp to valid range
                cx = max(0.0, min(1.0, cx))
                cy = max(0.0, min(1.0, cy))
                w = max(0.0, min(1.0, w))
                h = max(0.0, min(1.0, h))

                yolo_labels.append(f"{cls_idx} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}")

    except Exception as e:
        logging.warning(f"Error processing label file {label_file}: {e}")

    return yolo_labels


# --------------------
# Single-file processing executed by workers
# --------------------

def process_single_file(args: Tuple[str, str, Path, Path, Path]) -> bool:
    """Process a single image-label pair.

    args: (img_file_name, label_file_name, img_dir, label_dir, output_label_path)
    """
    img_file, label_file, img_dir, label_dir, output_path = args

    try:
        img_path = img_dir / img_file
        label_path = label_dir / label_file

        if not img_path.exists():
            logging.warning(f"Image file not found: {img_path}")
            return False

        # Get image dimensions
        with Image.open(img_path) as img:
            img_w, img_h = img.size

        # Convert labels
        yolo_labels = convert_kitti_to_yolo(label_path, img_w, img_h)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write YOLO label file (empty file allowed)
        with open(output_path, "w") as f:
            f.write("\n".join(yolo_labels))

        # Copy image to same directory
        img_output_path = output_path.parent / img_file
        if not img_output_path.exists():
            shutil.copy2(img_path, img_output_path)

        return True

    except Exception as e:
        logging.exception(f"Error processing {img_file}: {e}")
        return False


# --------------------
# Directory structure + dataset split
# --------------------

def create_directory_structure(output_dir: Path, num_clients: int):
    # Remove previous output (be careful!)
    if output_dir.exists():
        logging.info(f"Removing existing output directory: {output_dir}")
        shutil.rmtree(output_dir)

    # Create main dirs
    (output_dir / "train").mkdir(parents=True, exist_ok=True)
    (output_dir / "val").mkdir(parents=True, exist_ok=True)

    # Create client dirs (0-based indexing to match Flower client ids)
    for i in range(num_clients):
        (output_dir / f"client_{i}" / "train").mkdir(parents=True, exist_ok=True)
        (output_dir / f"client_{i}" / "val").mkdir(parents=True, exist_ok=True)


def split_data(image_files: List[str], train_ratio: float = 0.8) -> Tuple[List[str], List[str]]:
    split_idx = int(len(image_files) * train_ratio)
    return image_files[:split_idx], image_files[split_idx:]


# --------------------
# Prepare data pipeline
# --------------------

def prepare_data(
    raw_images_dir: Path,
    raw_labels_dir: Path,
    output_dir: Path,
    num_clients: int,
    train_image_count: int,
    global_train_ratio: float = 0.8,
) -> Tuple[int, int]:
    """Prepare datasets for global + per-client training.

    Returns: (successful_tasks, total_tasks)
    """
    logging.info("Starting data preparation...")

    if not raw_images_dir.exists() or not raw_labels_dir.exists():
        raise ValueError(f"Raw data directories not found: {raw_images_dir}, {raw_labels_dir}")

    create_directory_structure(output_dir, num_clients)

    image_files = [f for f in os.listdir(raw_images_dir) if Path(f).suffix.lower() in IMAGE_EXTS]

    if len(image_files) == 0:
        raise ValueError("No image files found in the raw images directory")

    random.seed(42)
    random.shuffle(image_files)

    # Global dataset -- first TRAIN_IMAGE_COUNT images
    global_images = image_files[:train_image_count]
    global_train_images, global_val_images = split_data(global_images, global_train_ratio)

    logging.info(f"Global dataset: {len(global_train_images)} train, {len(global_val_images)} val")

    # Clients -- each gets a disjoint slice after the global block
    client_datasets = []
    for i in range(num_clients):
        start_idx = (i + 1) * train_image_count
        end_idx = (i + 2) * train_image_count

        if start_idx >= len(image_files):
            logging.warning(f"Not enough data for client {i} (start_idx={start_idx})")
            client_images = []
        else:
            client_images = image_files[start_idx:min(end_idx, len(image_files))]

        if client_images:
            client_train_images, client_val_images = split_data(client_images, global_train_ratio)
            client_datasets.append((client_train_images, client_val_images))
            logging.info(f"Client {i} dataset: {len(client_train_images)} train, {len(client_val_images)} val")
        else:
            client_datasets.append(([], []))

    # Prepare processing tasks
    tasks: List[Tuple[str, str, Path, Path, Path]] = []

    def make_label_name(img_name: str) -> str:
        return Path(img_name).with_suffix('.txt').name

    # Global tasks
    for img_file in global_train_images:
        label_file = make_label_name(img_file)
        output_path = output_dir / "train" / label_file
        tasks.append((img_file, label_file, raw_images_dir, raw_labels_dir, output_path))

    for img_file in global_val_images:
        label_file = make_label_name(img_file)
        output_path = output_dir / "val" / label_file
        tasks.append((img_file, label_file, raw_images_dir, raw_labels_dir, output_path))

    # Client tasks
    for client_idx, (client_train_images, client_val_images) in enumerate(client_datasets):
        for img_file in client_train_images:
            label_file = make_label_name(img_file)
            output_path = output_dir / f"client_{client_idx}" / "train" / label_file
            tasks.append((img_file, label_file, raw_images_dir, raw_labels_dir, output_path))

        for img_file in client_val_images:
            label_file = make_label_name(img_file)
            output_path = output_dir / f"client_{client_idx}" / "val" / label_file
            tasks.append((img_file, label_file, raw_images_dir, raw_labels_dir, output_path))

    logging.info(f"Processing {len(tasks)} files with up to {min(mp.cpu_count(), 8)} workers...")

    successful = 0

    max_workers = min(mp.cpu_count(), 8)
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_single_file, task) for task in tasks]
        for future in as_completed(futures):
            try:
                if future.result():
                    successful += 1
            except Exception as e:
                logging.exception(f"Task failed: {e}")

    logging.info(f"Data preparation completed. Successfully processed {successful}/{len(tasks)} files.")

    # Create dataset config files (global + clients)
    create_dataset_config(output_dir, num_clients)

    return successful, len(tasks)


# --------------------
# Dataset YAML creation helper (simple, explicit YAML)
# --------------------

def create_dataset_config(output_dir: Path, num_clients: int):
    # Global dataset.yaml
    global_yaml = f"""# Global dataset configuration for YOLO training
path: {output_dir.absolute()}
train: train
val: val

# Number of classes
nc: {len(CLASS_MAP)}

# Class names
names: {list(CLASS_MAP.keys())}
"""
    (output_dir / "dataset.yaml").write_text(global_yaml.strip())
    logging.info(f"Created global dataset configuration: {output_dir / 'dataset.yaml'}")

    # Per-client
    for i in range(num_clients):
        client_dir = output_dir / f"client_{i}"
        client_yaml = f"""# Client {i} dataset configuration for YOLO training
path: {client_dir.absolute()}
train: train
val: val

# Number of classes
nc: {len(CLASS_MAP)}

# Class names
names: {list(CLASS_MAP.keys())}
"""
        client_yaml_path = client_dir / "dataset.yaml"
        client_yaml_path.write_text(client_yaml.strip())
        logging.info(f"Created client {i} dataset configuration: {client_yaml_path}")


# --------------------
# Global training helper
# --------------------

def global_model_train(data_yaml="/prepared_data/data.yaml", epochs=5, optimizer="SGD"):
    logging.info("YOLO Global model training started")
    model = YOLO('yolov8n.pt')
    try:
       results = model.train(data=data_yaml, epochs=epochs, imgsz=640, save=True, seed=42, device=-1, name="global_model", optimizer=optimizer, classes=CLASS_MAP)
       logging.info("YOLO global model training complete")
       logging.info("YOLO global model validation started")
       global_metrics = model.val(save_json=True, classes=CLASS_MAP, name="global_model", device=-1)
       logging.info("YOLO global model validation complete")
       return {
           'map50-95':global_metrics.box.map,
           'map50':global_metrics.box.map50,
           'map75':global_metrics.box.map75
       }
    except Exception as e:
        logging.error(f"Global model training failed: {e}")
        return None


