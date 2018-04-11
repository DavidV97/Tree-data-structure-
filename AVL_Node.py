class AVL_Node:

    def __init__(self, data):
        self.data = data
        self.left_node = self.right_node = None
        self.height = 0
