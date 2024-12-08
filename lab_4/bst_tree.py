class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, root, key):
        if not root:
            return Node(key)
        if key < root.key:
            root.left = self._insert(root.left, key)
        elif key > root.key:
            root.right = self._insert(root.right, key)
        return root

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, root, key):
        if not root or root.key == key:
            return root
        if key < root.key:
            return self._search(root.left, key)
        return self._search(root.right, key)

    @staticmethod
    def min_value_node(node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, key):
        self.root = self._delete_node(self.root, key)

    def _delete_node(self, root, key):
        if not root:
            return root
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
        return root

    def inorder_traversal(self):
        self._inorder_traversal(self.root)

    def _inorder_traversal(self, root):
        if root:
            self._inorder_traversal(root.left)
            print(root.key, end=" ")
            self._inorder_traversal(root.right)

    def successor(self, key):
        node = self._search(self.root, key)
        if node is None:
            return None
        if node.right:
            return self.min_value_node(node.right)
        p = self.root
        s = None
        while p:
            if p.key > key:
                s = p
                p = p.left
            elif p.key < key:
                p = p.right
            else:
                break
        return s

    def predecessor(self, key):
        node = self._search(self.root, key)
        if node is None:
            return None
        if node.left:
            return self.max_value_node(node.left)
        p = self.root
        s = None
        while p:
            if p.key < key:
                s = p
                p = p.right
            elif p.key > key:
                p = p.left
            else:
                break
        return s

    @staticmethod
    def max_value_node(node):
        current = node
        while current.right is not None:
            current = current.right
        return current


if __name__ == "__main__":
    bst = BST()

    for i in range(1, 11):
        bst.insert(i)

    print("Inorder traversal of the BST:")
    bst.inorder_traversal()
    print()

    print("Search for 5:", bst.search(5))
    print("Successor of 5:", bst.successor(5).key)
    print("Predecessor of 5:", bst.predecessor(5).key)

    bst.delete(1)
    bst.delete(5)

    print("Inorder traversal of the BST after deletion:")
    bst.inorder_traversal()
    