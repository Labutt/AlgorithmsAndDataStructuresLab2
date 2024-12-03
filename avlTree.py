import random
import time
import numpy as np
import matplotlib.pyplot as plt

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLtree:
    def get_height(self, node):
        if not node:
            return 0
        else:
            return node.height

    def get_balance(self, node):
        if not node:
            return 0
        else:
            return self.get_height(node.left) - self.get_height(node.right)

    def get_min_value_node(self, node):
        if node is None or node.left is None:
            return node
        return self.get_min_value_node(node.left)

    def right_rotation(self, node):
        leftSubTree = node.left
        rightSubTreeOfLeftSubTree = leftSubTree.right
        leftSubTree.right = node
        node.left = rightSubTreeOfLeftSubTree
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        leftSubTree.height = 1 + max(self.get_height(leftSubTree.left), self.get_height(leftSubTree.right))
        return leftSubTree

    def left_rotation(self, node):
        rightSubTree = node.right
        leftSubTreeOfRightSubTree = rightSubTree.left
        rightSubTree.left = node
        node.right = leftSubTreeOfRightSubTree
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        rightSubTree.height = 1 + max(self.get_height(rightSubTree.left), self.get_height(rightSubTree.right))
        return rightSubTree

    def insert(self, node, key):
        if not node:
            return Node(key)
        elif key < node.key:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        if balance > 1 and key < node.left.key:
            return self.right_rotation(node)
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotation(node.left)
            return self.right_rotation(node)
        if balance < -1 and key > node.right.key:
            return self.left_rotation(node)
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotation(node.right)
            return self.left_rotation(node)
        return node

    def delete(self, root, key):
        if not root:
            return root
        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.right = self.delete(root.right, temp.key)
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotation(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotation(root.left)
            return self.right_rotation(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotation(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotation(root.right)
            return self.left_rotation(root)
        return root

    def search(self, root, key):
        while root is not None and key != root.key:
            if key < root.key:
                root = root.left
            else:
                root = root.right
        return root


    def depth_traversal(self, node):
        if not node:
            return 0
        else:
            print(node.key, end=" ")
            self.depth_traversal(node.left)
            self.depth_traversal(node.right)

    def width_traversal(self, root):
        if root is None:
            return []

        queue = [root]
        result = []

        while queue:
            current_node = queue.pop(0)
            result.append(current_node.key)

            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)

        return result


tree = AVLtree()
root = None

keys = [50, 60, 70, 80, 90, 100]
for key in keys:
    root = tree.insert(root, key)

print("Обход в глубину:")
tree.depth_traversal(root)
print()
print("Обход в ширину:")
print(tree.width_traversal(root))
root = None




lowBorder = 1
highBorder = 100
step = 2

heightResults = []
n = []
for i in range(lowBorder, highBorder, step):
    n.append(i)
    seed = time.time()
    random.seed(seed)
    keys = [random.uniform(1, i) for _ in range(i)]
    for key in keys:
        root = tree.insert(root, key)
    heightResults.append(tree.get_height(root))
    root = None
n = np.array(n)
curve = np.polyfit(n, heightResults, 2)
plt.scatter(n, heightResults, color = 'red')
plt.title('AVL дерево со случайными равномерными значениями')
plt.xlabel('Количество узлов (n)')
plt.ylabel('Высота дерева (h)')
plt.grid()
plt.plot(n, np.polyval(curve, n), color = 'red', label = 'Зависимость от случайных значений')
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
        root = tree.insert(root, key)
    heightResults.append(tree.get_height(root))
    root = None
n = np.array(n)
curve = np.polyfit(n, heightResults, 2)
plt.scatter(n, heightResults, color = 'red')
plt.title('AVL дерево с возрастающими значениями')
plt.xlabel('Количество узлов (n)')
plt.ylabel('Высота дерева (h)')
plt.grid()
plt.plot(n, np.polyval(curve, n), color = 'red', label = 'Зависимость от возрастающих значений')
plt.legend()
plt.tight_layout()
plt.show()

