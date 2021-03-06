from Rb_Node import Rb_Node
from Tree import Tree
BLACK = 'NEGRO'
RED = 'ROJO'
NIL = 'NIL'


class RedBlackTree(Tree):

    NIL_LEAF = Rb_Node(value=None, color=NIL, parent=None)

    def __init__(self):
        self.count = 0
        self.root = None
        self.ROTATIONS = {
            'L': self._right_rotation,
            'R': self._left_rotation
        }

    def __iter__(self):
        if not self.root:
            return list()
        yield from iter(self.root)

    def __str__(self):
        resul = iter(self)
        data = ""

        for r in resul:
            data += str(r)
        if data != "":
            return data
        else:
            return "El arbol Rojo-Negro esta vacio"

    def add(self, value):
        try:
            if not self.root:
                self.root = Rb_Node(value, color=BLACK, parent=None,
                                    left=self.NIL_LEAF, right=self.NIL_LEAF)
                self.count += 1
                return True
            parent, node_dir = self._find_parent(value)
            if node_dir is None:
                return
            new_node = Rb_Node(value=value, color=RED, parent=parent,
                               left=self.NIL_LEAF, right=self.NIL_LEAF)
            if node_dir == 'L':
                parent.left = new_node
            else:
                parent.right = new_node

            self._try_rebalance(new_node)
            self.count += 1

            return True

        except ValueError:
            return False

    def delete(self, value):
        try:
            node_to_remove = self.find_node(value)
            if node_to_remove is None:
                return False
            if node_to_remove.get_children_count() == 2:

                successor = self._find_in_order_successor(node_to_remove)
                node_to_remove.value = successor.value
                node_to_remove = successor

            self._remove(node_to_remove)
            self.count -= 1
            return True
        except ValueError:
            return False

    def __contains__(self, value) -> bool:
        return bool(self.find_node(value))

    def ceil(self, value) -> int or None:

        if self.root is None:
            return None
        last_found_val = None if self.root.value < value else self.root.value

        def find_ceil(node):
            nonlocal last_found_val
            if node == self.NIL_LEAF:
                return None
            if node.value == value:
                last_found_val = node.value
                return node.value
            elif node.value < value:
                return find_ceil(node.right)
            else:
                last_found_val = node.value

                return find_ceil(node.left)
        find_ceil(self.root)
        return last_found_val

    def floor(self, value) -> int or None:

        if self.root is None:
            return None
        last_found_val = None if self.root.value < value else self.root.value

        def find_floor(node):
            nonlocal last_found_val
            if node == self.NIL_LEAF:
                return None
            if node.value == value:
                last_found_val = node.value
                return node.value
            elif node.value < value:
                last_found_val = node.value

                return find_floor(node.right)
            else:
                return find_floor(node.left)

        find_floor(self.root)
        return last_found_val

    def _remove(self, node):
        left_child = node.left
        right_child = node.right
        not_nil_child = left_child if left_child != self.NIL_LEAF else right_child
        if node == self.root:
            if not_nil_child != self.NIL_LEAF:
                self.root = not_nil_child
                self.root.parent = None
                self.root.color = BLACK
            else:
                self.root = None
        elif node.color == RED:
            if not node.has_children():
                self._remove_leaf(node)
            else:
                raise Exception('Unexpected behavior')
        else:
            if right_child.has_children() or left_child.has_children():
                raise Exception('The red child of a black node with 0 or 1 children'
                                ' cannot have children, otherwise the black height of the tree becomes invalid! ')
            if not_nil_child.color == RED:
                node.value = not_nil_child.value
                node.left = not_nil_child.left
                node.right = not_nil_child.right
            else:
                self._remove_black_node(node)

    def _remove_leaf(self, leaf):
        if leaf.value >= leaf.parent.value:
            leaf.parent.right = self.NIL_LEAF
        else:
            leaf.parent.left = self.NIL_LEAF

    def _remove_black_node(self, node):

        self.__case_1(node)
        self._remove_leaf(node)

    def __case_1(self, node):

        if self.root == node:
            node.color = BLACK
            return
        self.__case_2(node)

    def __case_2(self, node):

        parent = node.parent
        sibling, direction = self._get_sibling(node)
        if sibling.color == RED and parent.color == BLACK and sibling.left.color != RED and sibling.right.color != RED:
            self.ROTATIONS[direction](
                node=None, parent=sibling, grandfather=parent)
            parent.color = RED
            sibling.color = BLACK
            return self.__case_1(node)
        self.__case_3(node)

    def __case_3(self, node):

        parent = node.parent
        sibling, _ = self._get_sibling(node)
        if (sibling.color == BLACK and parent.color == BLACK
                and sibling.left.color != RED and sibling.right.color != RED):
            # color the sibling red and forward the double black node upwards
            # (call the cases again for the parent)
            sibling.color = RED
            return self.__case_1(parent)  # start again

        self.__case_4(node)

    def __case_4(self, node):

        parent = node.parent
        if parent.color == RED:
            sibling, direction = self._get_sibling(node)
            if sibling.color == BLACK and sibling.left.color != RED and sibling.right.color != RED:
                parent.color, sibling.color = sibling.color, parent.color  # switch colors
                return  # Terminating
        self.__case_5(node)

    def __case_5(self, node):

        sibling, direction = self._get_sibling(node)
        closer_node = sibling.right if direction == 'L' else sibling.left
        outer_node = sibling.left if direction == 'L' else sibling.right
        if closer_node.color == RED and outer_node.color != RED and sibling.color == BLACK:
            if direction == 'L':
                self._left_rotation(
                    node=None, parent=closer_node, grandfather=sibling)
            else:
                self._right_rotation(
                    node=None, parent=closer_node, grandfather=sibling)
            closer_node.color = BLACK
            sibling.color = RED

        self.__case_6(node)

    def __case_6(self, node):

        sibling, direction = self._get_sibling(node)
        outer_node = sibling.left if direction == 'L' else sibling.right

        def __case_6_rotation(direction):
            parent_color = sibling.parent.color
            self.ROTATIONS[direction](
                node=None, parent=sibling, grandfather=sibling.parent)
            # new parent is sibling
            sibling.color = parent_color
            sibling.right.color = BLACK
            sibling.left.color = BLACK

        if sibling.color == BLACK and outer_node.color == RED:
            return __case_6_rotation(direction)  # terminating

        raise Exception('We should have ended here, something is wrong')

    def _try_rebalance(self, node):

        parent = node.parent
        value = node.value
        if (parent is None
            or parent.parent is None
                or (node.color != RED or parent.color != RED)):
            return
        grandfather = parent.parent
        node_dir = 'L' if parent.value > value else 'R'
        parent_dir = 'L' if grandfather.value > parent.value else 'R'
        uncle = grandfather.right if parent_dir == 'L' else grandfather.left
        general_direction = node_dir + parent_dir

        if uncle == self.NIL_LEAF or uncle.color == BLACK:

            if general_direction == 'LL':
                self._right_rotation(node, parent, grandfather, to_recolor=True)
            elif general_direction == 'RR':
                self._left_rotation(node, parent, grandfather, to_recolor=True)
            elif general_direction == 'LR':
                self._right_rotation(node=None, parent=node, grandfather=parent)
                self._left_rotation(node=parent, parent=node,
                                    grandfather=grandfather, to_recolor=True)
            elif general_direction == 'RL':
                self._left_rotation(node=None, parent=node, grandfather=parent)
                self._right_rotation(node=parent, parent=node,
                                     grandfather=grandfather, to_recolor=True)
            else:
                raise Exception(
                    "{} is not a valid direction!".format(general_direction))
        else:
            self._recolor(grandfather)

    def __update_parent(self, node, parent_old_child, new_parent):

        node.parent = new_parent
        if new_parent:
            if new_parent.value > parent_old_child.value:
                new_parent.left = node
            else:
                new_parent.right = node
        else:
            self.root = node

    def _right_rotation(self, node, parent, grandfather, to_recolor=False):
        grand_grandfather = grandfather.parent
        self.__update_parent(
            node=parent, parent_old_child=grandfather, new_parent=grand_grandfather)

        old_right = parent.right
        parent.right = grandfather
        grandfather.parent = parent

        grandfather.left = old_right
        old_right.parent = grandfather

        if to_recolor:
            parent.color = BLACK
            node.color = RED
            grandfather.color = RED

    def _left_rotation(self, node, parent, grandfather, to_recolor=False):
        grand_grandfather = grandfather.parent
        self.__update_parent(
            node=parent, parent_old_child=grandfather, new_parent=grand_grandfather)

        old_left = parent.left
        parent.left = grandfather
        grandfather.parent = parent

        grandfather.right = old_left
        old_left.parent = grandfather

        if to_recolor:
            parent.color = BLACK
            node.color = RED
            grandfather.color = RED

    def _recolor(self, grandfather):
        grandfather.right.color = BLACK
        grandfather.left.color = BLACK
        if grandfather != self.root:
            grandfather.color = RED
        self._try_rebalance(grandfather)

    def _find_parent(self, value):
        def inner_find(parent):

            if value == parent.value:
                return None, None
            elif parent.value < value:
                if parent.right.color == NIL:  # no more to go
                    return parent, 'R'
                return inner_find(parent.right)
            elif value < parent.value:
                if parent.left.color == NIL:  # no more to go
                    return parent, 'L'
                return inner_find(parent.left)

        return inner_find(self.root)

    def find_node(self, value):
        def inner_find(root):
            if root is None or root == self.NIL_LEAF:
                return None
            if value > root.value:
                return inner_find(root.right)
            elif value < root.value:
                return inner_find(root.left)
            else:
                return root

        found_node = inner_find(self.root)
        return found_node

    def _find_in_order_successor(self, node):
        right_node = node.right
        left_node = right_node.left
        if left_node == self.NIL_LEAF:
            return right_node
        while left_node.left != self.NIL_LEAF:
            left_node = left_node.left
        return left_node

    def _get_sibling(self, node):

        parent = node.parent
        if node.value >= parent.value:
            sibling = parent.left
            direction = 'L'
        else:
            sibling = parent.right
            direction = 'R'
        return sibling, direction
