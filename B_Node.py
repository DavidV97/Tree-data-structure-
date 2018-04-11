class B_Node(object):

    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.c = []

    def __str__(self):
        if self.leaf:
            return "Arbol B con {0} claves\n\tClaves:{1}\n\tPaginas:{2}\n".format(
                len(self.keys), self.keys, self.c)
        else:
            return "Pagina con {0} claves, {1} children\n\tClaves:{2}\n\n".format(
                len(self.keys), len(self.c), self.keys, self.c)
