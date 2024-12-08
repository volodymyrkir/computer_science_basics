class WAVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.weight = 1
        self.height = 1


class WAVLTree:
    def __init__(self):
        self.root = None
        self.node_visit_count = 0
        self.rotation_count = 0

    def reset_metrics(self):
        self.node_visit_count = 0
        self.rotation_count = 0

    def height(self, root):
        if not root:
            return 0
        return root.height

    def weight(self, root):
        if not root:
            return 0
        return root.weight

    def update_height(self, root):
        root.height = 1 + max(self.height(root.left), self.height(root.right))

    def update_weight(self, root):
        root.weight = 1 + self.weight(root.left) + self.weight(root.right)

    def right_rotate(self, y):
        self.rotation_count += 1
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)
        self.update_weight(y)
        self.update_weight(x)

        return x

    def left_rotate(self, x):
        self.rotation_count += 1
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)
        self.update_weight(x)
        self.update_weight(y)

        return y

    def balance(self, root):
        if not root:
            return root

        w_balance = self.weight(root.left) - self.weight(root.right)

        if w_balance > 1:
            if self.weight(root.left.left) >= self.weight(root.left.right):
                root = self.right_rotate(root)
            else:
                root.left = self.left_rotate(root.left)
                root = self.right_rotate(root)

        elif w_balance < -1:
            if self.weight(root.right.right) >= self.weight(root.right.left):
                root = self.left_rotate(root)
            else:
                root.right = self.right_rotate(root.right)
                root = self.left_rotate(root)

        return root

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, root, key):
        self.node_visit_count += 1
        if not root:
            return WAVLNode(key)

        if key < root.key:
            root.left = self._insert(root.left, key)
        elif key > root.key:
            root.right = self._insert(root.right, key)

        self.update_height(root)
        self.update_weight(root)

        return self.balance(root)

    def min_value_node(self, node):
        current = node
        while current.left is not None:
            self.node_visit_count += 1
            current = current.left
        return current

    def delete(self, key):
        self._delete_node(self.root, key)

    def _delete_node(self, root, key):
        if not root:
            return root
        self.node_visit_count += 1
        if key < root.key:
            root.left = self._delete_node(root.left, key)
        elif key > root.key:
            root.right = self._delete_node(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.min_value_node(root.right)
            root.key = temp.key
            root.right = self._delete_node(root.right, temp.key)

        if root is None:
            return root

        self.update_height(root)
        self.update_weight(root)

        return self.balance(root)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, root, key):
        self.node_visit_count += 1
        if not root:
            return None
        if root.key == key:
            return root
        elif root.key < key:
            return self._search(root.right, key)
        else:
            return self._search(root.left, key)

    def successor(self, key):
        return self._successor(self.root, key)

    def _successor(self, root, key):
        self.node_visit_count += 1
        node = self._search(root, key)
        if node is None:
            return None

        if node.right is not None:
            return self.min_value_node(node.right)

        parent = None
        current = root
        while current is not None:
            self.node_visit_count += 1
            if current.key > key:
                parent = current
                current = current.left
            elif current.key < key:
                current = current.right
            else:
                break

        return parent

    def predecessor(self, key):
        node = self.search(key)
        if node is None:
            return None

        if node.left is not None:
            return self.max_value_node(node.left)

        parent = None
        current = self.root
        while current is not None:
            if current.key < key:
                parent = current
                current = current.right
            elif current.key > key:
                parent = current
                current = current.left
            else:
                break

        return parent

    @staticmethod
    def max_value_node(node):
        current = node
        while current.right is not None:
            current = current.right
        return current

    def inorder_walk(self):
        self._inorder_walk(self.root)

    def _inorder_walk(self, root):
        if root:
            self._inorder_walk(root.left)
            print(root.key, end=" ")
            self._inorder_walk(root.right)


if __name__ == "__main__":
    tree = WAVLTree()
    tree.insert(10)
    tree.insert(20)
    tree.insert(15)
    tree.insert(25)

    print(f"Root is {tree.root.key} after inserting 10, 20, 15, 25")
    print("Inorder traversal of the tree:")
    tree.inorder_walk()

    print("Search for 15:", tree.search(15))
    print("Successor of 15:", tree.successor(15).key)
    print("Predecessor of 25:", tree.predecessor(25).key)

    tree.delete(15)

    print("Inorder traversal of the tree after deletion:")
    tree.inorder_walk()
