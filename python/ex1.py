import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ROUGE scores
rouge_scores = {
    'ROUGE-1': np.float64(0.5885123394530984),
    'ROUGE-2': np.float64(0.28745331207731445),
    'ROUGE-L': np.float64(0.5577341615099036),
    'ROUGE-Lsum': np.float64(0.5576115062042776)
}

# BLEU scores
bleu_scores = {
    'BLEU': 0.23491082351683862,
    'Precisions': [0.5994541484716157, 0.29413875598086126, 0.1761904761904762, 0.1128698224852071],
    'Brevity Penalty': 0.9653524523460961,
    'Length Ratio': 0.9659390488242118,
    'Translation Length': 9160,
    'Reference Length': 9483
}

# Convert ROUGE scores to DataFrame
rouge_df = pd.DataFrame(list(rouge_scores.items()), columns=['Metric', 'Score'])
print("ROUGE Scores Table:")
print(rouge_df.to_string(index=False))

# Convert BLEU scores to DataFrame
bleu_data = [
    ['BLEU', bleu_scores['BLEU']],
    ['Brevity Penalty', bleu_scores['Brevity Penalty']],
    ['Length Ratio', bleu_scores['Length Ratio']],
    ['Translation Length', bleu_scores['Translation Length']],
    ['Reference Length', bleu_scores['Reference Length']]
]
bleu_df = pd.DataFrame(bleu_data, columns=['Metric', 'Value'])
print("\nBLEU Scores Table:")
print(bleu_df.to_string(index=False))

# Precision scores as a table
precision_df = pd.DataFrame(
    {'N-gram': ['1-gram', '2-gram', '3-gram', '4-gram'], 'Precision': bleu_scores['Precisions']}
)
print("\nBLEU Precision Scores Table:")
print(precision_df.to_string(index=False))

# Extract keys and values
metrics = list(rouge_scores.keys())
scores = list(rouge_scores.values())

# Plot the scores
plt.figure(figsize=(8, 5))
plt.bar(metrics, scores, color=['blue', 'orange', 'green', 'red'])

# Labels and title
plt.xlabel('ROUGE Metrics')
plt.ylabel('Scores')
plt.title('ROUGE Score Comparison')
plt.ylim(0, 1)

# Display values on bars
for i, score in enumerate(scores):
    plt.text(i, score + 0.02, f'{score:.3f}', ha='center', fontsize=12)

# Show the plot
plt.show()
