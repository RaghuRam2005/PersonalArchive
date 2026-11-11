from collections import deque
class TreeNode:
    def __init__(self, val=0, left=None, right=None) -> None:
        self.val = val
        self.left = left
        self.right = right

def traverse(queue):
    if not queue:
        return
    
    curr, level_order = queue.popleft()
    print(curr, level_order)

def bfs(root):
    if not root:
        return
    
    queue = deque([(root, 0)])

    traverse(queue)

root = TreeNode(2)
bfs(root)
