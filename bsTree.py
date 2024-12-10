import random
import time
import numpy as np
import matplotlib.pyplot as plt

class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = TreeNode(key)
        else:
            self._insert(self.root, key)

    def _insert(self, node, key):
        if key < node.val:
            if node.left is None:
                node.left = TreeNode(key)
            else:
                self._insert(node.left, key)
        else:
            if node.right is None:
                node.right = TreeNode(key)
            else:
                self._insert(node.right, key)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None or node.val == key:
            return node
        if key < node.val:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return node

        if key < node.val:
            node.left = self._delete(node.left, key)
            return node
        elif key > node.val:
            node.right = self._delete(node.right, key)
            return node
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        min_larger_node = self._get_min(node.right)
        node.val = min_larger_node.val
        node.right = self._delete(node.right, min_larger_node.val)
        return node

    def _get_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def preorder(self, node):
        if not node:
            return 0
        else:
            print(node.val, end=" ")
            self.preorder(node.left)
            self.preorder(node.right)

    def inorder(self, node):
        if not node:
            return 0
        else:
            self.inorder(node.left)
            print(node.val, end=" ")
            self.inorder(node.right)

    def postorder(self, node):
        if not node:
            return 0
        else:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.val, end=" ")

    def width_traversal(self, root):
        if root is None:
            return []
        queue = [root]
        result = []

        while queue:
            current_node = queue.pop(0)
            result.append(current_node.val)
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)

        return result

def get_height(node):
    if node is None:
        return 0
    left_height = get_height(node.left)
    right_height = get_height(node.right)

    return 1 + max(left_height, right_height)

tree = BinarySearchTree()

keys = [50, 60, 70, 80, 90, 100]
for key in keys:
    tree.insert(key)

print("Прямой обход:")
tree.preorder(tree.root)
print()
print("Симметричный обход:")
tree.inorder(tree.root)
print()
print("Обратный обход:")
tree.postorder(tree.root)
print()
print("Обход в ширину:")
print(tree.width_traversal(tree.root))
tree.root = None

lowBorder = 0
highBorder = 50
step = 1

heightResults = []
n = []
for i in range(lowBorder, highBorder, step):
    n.append(i)
    seed = time.time()
    random.seed(seed)
    keys = [random.uniform(1, i) for _ in range(i)]
    for key in keys:
        tree.insert(key)
    heightResults.append(get_height(tree.root))
    tree.root = None
n = np.array(n)
curve = np.polyfit(n, heightResults, 2)
plt.scatter(n, heightResults, color = 'red')
plt.title('Бинарное дерево со случайными равномерными значениями')
plt.xlabel('Количество узлов (n)')
plt.ylabel('Высота дерева (h)')
plt.grid()
plt.plot(n, np.polyval(curve, n),  color = 'red', label = 'Зависимость от случайных значений')
plt.legend()
plt.tight_layout()
plt.show()

def generate_increasing_sequence(size, lower_bound, upper_bound):
    if size > (upper_bound - lower_bound + 1):
        return 1
    random_values = random.sample(range(lower_bound, upper_bound + 1), size)
    increasing_sequence = sorted(random_values)
    return increasing_sequence

heightResults = []
n = []
for i in range(lowBorder, highBorder, step):
    n.append(i)
    seed = time.time()
    random.seed(seed)
    keys = generate_increasing_sequence(i, 1, i)
    for key in keys:
        tree.insert(key)
    heightResults.append(get_height(tree.root))
    tree.root = None
n = np.array(n)
curve = np.polyfit(n, heightResults, 2)
plt.scatter(n, heightResults, color = 'red')
plt.title('Бинарное дерево с возрастающими значениями')
plt.xlabel('Количество узлов (n)')
plt.ylabel('Высота дерева (h)')
plt.grid()
plt.plot(n, np.polyval(curve, n), color = 'red', label = 'Зависимость от возрастающих значений')
plt.legend()
plt.tight_layout()
plt.show()