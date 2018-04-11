from AVL_Node import AVL_Node
from Tree import Tree


class AVLTree(Tree):

    def __init__(self):

        self.node = None
        self.height = -1
        self.balance = 0

    def add(self, data):
        try:
            n = AVL_Node(data)

            if not self.node:
                self.node = n
                self.node.left = AVLTree()
                self.node.right = AVLTree()

            elif data < self.node.data:
                self.node.left.add(data)

            elif data > self.node.data:
                self.node.right.add(data)

            self.rebalance()

            return True

        except ValueError:
            return False

    def rebalance(self):

        self.update_heights(recursive=False)
        self.update_balances(False)

        while self.balance < -1 or self.balance > 1:

            if self.balance > 1:

                if self.node.left.balance < 0:
                    self.node.left.rotate_left()
                    self.update_heights()
                    self.update_balances()

                self.rotate_right()
                self.update_heights()
                self.update_balances()

            if self.balance < -1:

                if self.node.right.balance > 0:
                    self.node.right.rotate_right()
                    self.update_heights()
                    self.update_balances()

                self.rotate_left()
                self.update_heights()
                self.update_balances()

    def update_heights(self, recursive=True):

        if self.node:
            if recursive:
                if self.node.left:
                    self.node.left.update_heights()
                if self.node.right:
                    self.node.right.update_heights()

            self.height = 1 + max(self.node.left.height,
                                  self.node.right.height)
        else:
            self.height = -1

    def update_balances(self, recursive=True):

        if self.node:

            if recursive:
                if self.node.left:
                    self.node.left.update_balances()
                if self.node.right:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height

        else:
            self.balance = 0

    def rotate_right(self):

        new_root = self.node.left.node
        new_left_sub = new_root.right.node
        old_root = self.node

        self.node = new_root
        old_root.left.node = new_left_sub
        new_root.right.node = old_root

    def rotate_left(self):

        new_root = self.node.right.node
        new_left_sub = new_root.left.node
        old_root = self.node

        self.node = new_root
        old_root.right.node = new_left_sub
        new_root.left.node = old_root

    def delete(self, data):

        try:

            if self.node is not None:
                if self.node.data == data:

                    if not self.node.left.node and not self.node.right.node:
                        self.node = None

                    elif not self.node.left.node:
                        self.node = self.node.right.node

                    elif not self.node.right.node:
                        self.node = self.node.left.node

                    else:
                        successor = self.node.right.node

                        while successor and successor.left.node:
                            successor = successor.left.node

                        if successor:
                            self.node.data = successor.data
                            self.node.right.delete(successor.data)

                elif data < self.node.data:
                    self.node.left.delete(data)

                elif data > self.node.data:
                    self.node.right.delete(data)

                self.rebalance()

                return True

        except ValueError:
            return False

    def inorder_traverse(self):

        result = []

        if not self.node:
            return result

        result.extend(self.node.left.inorder_traverse())
        result.append(self.node.data)
        result.extend(self.node.right.inorder_traverse())

        return result

    def postorder_traverse(self):

        result = []

        if not self.node:
            return result

        result.extend(self.node.left.postorder_traverse())
        result.extend(self.node.right.postorder_traverse())
        result.append(self.node.data)

        return result

    def preorder_traverse(self):

        result = []

        if not self.node:
            return result

        result.append(self.node.data)
        result.extend(self.node.left.preorder_traverse())
        result.extend(self.node.right.preorder_traverse())

        return result

    def display(self, node=None, level=0):
        if not node:
            node = self.node

        if node.right.node:
            self.display(node.right.node, level + 1)
            print('\t' * level), ('    /')

        print('\t' * level), node

        if node.left.node:
            print('\t' * level), ('    \\')
            self.display(node.left.node, level + 1)

    def __contains__(self, key):
        AVL_list = self.inorder_traverse()

        for item in AVL_list:
            if item == key:
                return True

        return False

    def __str__(self):
        s = ""
        count = 0

        if self.node:
            s = "AVL en orden: ["

            node_list = self.inorder_traverse()

            for i in node_list:
                if count == 0:
                    s += str(i)
                else:
                    s += ", " + str(i)

            s += "]"

        else:
            s = "El arbol AVL esta vacio"

        return s
