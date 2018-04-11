from B_Node import B_Node
from Tree import Tree


class BTree(Tree):
    def __init__(self, t):
        self.root = B_Node(leaf=True)
        self.t = t

    def add(self, k):
        try:
            r = self.root
            if len(r.keys) == (2 * self.t) - 1:
                s = B_Node()
                self.root = s

                s.c.add(0, r)
                self._split_child(s, 0)
                self._insert_nonfull(s, k)
            else:
                self._insert_nonfull(r, k)
            return True

        except ValueError:
            return False

    def _insert_nonfull(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:

            x.keys.append(0)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:

            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.c[i].keys) == (2 * self.t) - 1:
                self._split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_nonfull(x.c[i], k)

    def _split_child(self, x, i):

        t = self.t
        y = x.c[i]
        z = B_Node(leaf=y.leaf)

        x.c.add(i + 1, z)
        x.keys.add(i, y.keys[t - 1])

        z.keys = y.keys[t:(2 * t - 1)]
        y.keys = y.keys[0:(t - 1)]

        if not y.leaf:
            z.c = y.c[t:(2 * t)]
            y.c = y.c[0:(t - 1)]

    def delete(self, item, page=None):

        if isinstance(page, B_Node):
            i = 0
            while i < len(page.keys) and item > page.keys[i]:
                i += 1
            if item == page.keys[i]:
                page.keys.pop(i)
                return True
            elif page.leaf:
                return False
            else:
                return self.delete(item, page.c[i])
        else:
            return self.delete(item, self.root)

    def __contains__(self, k, x=None):

        if isinstance(x, B_Node):
            i = 0
            while i < len(x.keys) and k > x.keys[i]:
                i += 1
            if i < len(x.keys) and k == x.keys[i]:
                return True
            elif x.leaf:
                return False
            else:
                return self.__contains__(k, x.c[i])
        else:
            return self.__contains__(k, self.root)

    def __str__(self):
        r = self.root

        return r.__str__() + '\n'.join([child.__str__() for child in r.c])
