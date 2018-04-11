from AVLTree import AVLTree
from BTree import BTree
from Rb_Tree import RedBlackTree

avltree = AVLTree()
btree = BTree(5)
rbtree = RedBlackTree()


class Manager:

    @classmethod
    def add_item(cls, num, struck_type):

        struckture = cls.get_struck_obj(struck_type)

        if not (num in struckture):

            if struckture.add(num):
                return "El numero se agrego de manera exitosa\n{}".format(
                    struckture)

            else:
                return "*** Se produjo un error al agregar ***"
        else:
            return"*** El numero ya existe en el arbol " + struck_type + " ***"

    @classmethod
    def delete_item(cls, num, struck_type):
        struckture = cls.get_struck_obj(struck_type)

        if num in struckture:

            if struckture.delete(num):
                return "El numero se elimino de manera exitosa\n{}".format(
                    struckture)

            else:
                return "*** Se produjo un error al eliminar ***"
        else:
            return"*** El numero no existe en el arbol " + struck_type + " ***"

    @classmethod
    def show_item(cls, struck_type):
        struckture = cls.get_struck_obj(struck_type)

        return struckture

    @classmethod
    def get_struck_obj(cls, struck_type):
        if struck_type == "B":
            return btree
        elif struck_type == "AVL":
            return avltree
        elif struck_type == "B+":
            pass
        elif struck_type == "Rojo-Negro":
            return rbtree
