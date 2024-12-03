import random
import time
import numpy as np
import matplotlib.pyplot as plt
class Node:
    def __init__(self, key, color='red', left=None, right=None, parent=None):
        self.key = key
        self.color = color  # 'red' or 'black'
        self.left = left
        self.right = right
        self.parent = parent

class RedBlackTree:

    def __init__(self):
        self.NIL_LEAF = Node(key=None, color='black')
        self.root = self.NIL_LEAF
        self.elements_num = 0 #!!!
        self.height = 0

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL_LEAF:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL_LEAF:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def fix_insertion(self, t):
        while t.parent is not None and t.parent.color == 'red':
            if t.parent == t.parent.parent.left:
                uncle = t.parent.parent.right
                if uncle is not None and uncle.color == 'red':
                    t.parent.color = 'black'
                    uncle.color = 'black'
                    t.parent.parent.color = 'red'
                    t = t.parent.parent
                else:
                    if t == t.parent.right:
                        t = t.parent
                        self.left_rotate(t)
                    t.parent.color = 'black'
                    t.parent.parent.color = 'red'
                    self.right_rotate(t.parent.parent)
            else:
                uncle = t.parent.parent.left
                if uncle is not None and uncle.color == 'red':
                    t.parent.color = 'black'
                    uncle.color = 'black'
                    t.parent.parent.color = 'red'
                    t = t.parent.parent
                else:
                    if t == t.parent.left:
                        t = t.parent
                        self.right_rotate(t)
                    t.parent.color = 'black'
                    t.parent.parent.color = 'red'
                    self.left_rotate(t.parent.parent)
        self.root.color = 'black'

    def insert(self, key):
        t = Node(key, 'red', self.NIL_LEAF, self.NIL_LEAF)
        if self.root == self.NIL_LEAF:
            self.root = t
            t.parent = None
        else:
            p = self.root
            q = None
            while p != self.NIL_LEAF:
                q = p
                if t.key < p.key:
                    p = p.left
                else:
                    p = p.right
            t.parent = q
            if t.key < q.key:
                q.left = t
            else:
                q.right = t

        self.fix_insertion(t)

    def fix_deletion(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.right.color == 'black':
                        w.left.color = 'black'
                        w.color = 'red'
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.right.color = 'black'
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.left.color = 'black'
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 'black'

    def delete(self, key):
        z = self.search(self.root, key)
        if z == self.NIL_LEAF:
            print("Ключ не найден в дереве.")
            return
        y = z
        y_original_color = y.color
        if z.left == self.NIL_LEAF:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.NIL_LEAF:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 'black':
            self.fix_deletion(x)

    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, node):
        while node.left != self.NIL_LEAF:
            node = node.left
        return node

    def search(self, node, key):
        while node != self.NIL_LEAF and key != node.key:
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return node

    def depth_traversal(self, node):
        if node != self.NIL_LEAF:
            print(node.key, end=" ")
            self.depth_traversal(node.left)
            self.depth_traversal(node.right)

    def width_traversal(self):
        if self.root is None:
            return []
        queue = [self.root]
        result = []
        while queue:
            current_node = queue.pop(0)
            result.append(current_node.key)
            if current_node.left and current_node.left != self.NIL_LEAF:
                queue.append(current_node.left)
            if current_node.right and current_node.right != self.NIL_LEAF:
                queue.append(current_node.right)
        return result


def get_height(node):
    if node is None or node == tree.NIL_LEAF:
        return 0
    left_height = get_height(node.left)
    right_height = get_height(node.right)

    return 1 + max(left_height, right_height)

tree = RedBlackTree()

keys = [50, 60, 70, 80, 90, 100]
for key in keys:
    tree.insert(key)

print("Обход в глубину:")
tree.depth_traversal(tree.root)
print()
print("Обход в ширину:")
print(tree.width_traversal())
tree.root = tree.NIL_LEAF

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
        tree.insert(key)
    heightResults.append(get_height(tree.root))
    tree.root = tree.NIL_LEAF
n = np.array(n)
curve = np.polyfit(n, heightResults, 2)
plt.scatter(n, heightResults, color = 'red')
plt.title('Красно-черное дерево со случайными равномерными значениями')
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
        tree.insert(key)
    heightResults.append(get_height(tree.root))
    tree.root = tree.NIL_LEAF
n = np.array(n)
curve = np.polyfit(n, heightResults, 2)
plt.scatter(n, heightResults, color = 'red')
plt.title('Красно-черное дерево с возрастающими значениями')
plt.xlabel('Количество узлов (n)')
plt.ylabel('Высота дерева (h)')
plt.grid()
plt.plot(n, np.polyval(curve, n), color = 'red', label = 'Зависимость от возрастающих значений')
plt.legend()
plt.tight_layout()
plt.show()