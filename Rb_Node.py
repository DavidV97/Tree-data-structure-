BLACK = 'NEGRO'
RED = 'ROJO'
NIL = 'NIL'


class Rb_Node():
    def __init__(self, value, color, parent, left=None, right=None):
        self.value = value
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right

    def __repr__(self):
        resul = "==============\n"
        resul += "Numero: " + str(self.value) + "\nColor:  " + self.color + "\n"
        resul += "==============\n"
        return resul

    def __iter__(self):
        if self.left.color != NIL:
            yield from self.left.__iter__()

        yield self.__repr__()

        if self.right.color != NIL:
            yield from self.right.__iter__()

    def __eq__(self, other):
        if self.color == NIL and self.color == other.color:
            return True

        if self.parent is None or other.parent is None:
            parents_are_same = self.parent is None and other.parent is None
        else:
            parents_are_same = self.parent.value == other.parent.value and self.parent.color == other.parent.color
        return self.value == other.value and self.color == other.color and parents_are_same

    def has_children(self) -> bool:
        """ Returns a boolean indicating if the node has children """
        return bool(self.get_children_count())

    def get_children_count(self) -> int:
        """ Returns the number of NOT NIL children the node has """
        if self.color == NIL:
            return 0
        return sum([int(self.left.color != NIL), int(self.right.color != NIL)])
