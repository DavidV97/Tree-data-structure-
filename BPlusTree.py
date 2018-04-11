import bisect
import itertools
import operator
import _BPlusLeaf


class BPlusTree(object):
    LEAF = _BPlusLeaf()

    def _get(self, key):
        node, index = self._path_to(key)[-1]

        if index == len(node.contents):
            if node.next:
                node, index = node.next, 0
            else:
                return

        while node.contents[index] == key:
            yield node.data[index]
            index += 1
            if index == len(node.contents):
                if node.next:
                    node, index = node.next, 0
                else:
                    return

    def _path_to(self, item):
        path = super(BPlusTree, self)._path_to(item)
        node, index = path[-1]
        while hasattr(node, "children"):
            node = node.children[index]
            index = bisect.bisect_left(node.contents, item)
            path.append((node, index))
        return path

    def get(self, key, default=None):
        try:
            return self._get(key).next()
        except StopIteration:
            return default

    def getlist(self, key):
        return list(self._get(key))

    def insert(self, key, data):
        path = self._path_to(key)
        node, index = path.pop()
        node.insert(index, key, data, path)

    def remove(self, key):
        path = self._path_to(key)
        node, index = path.pop()
        node.remove(index, path)

    __getitem__ = get
    __setitem__ = insert
    __delitem__ = remove

    def __contains__(self, key):
        for item in self._get(key):
            return True
        return False

    def iteritems(self):
        node = self._root
        while hasattr(node, "children"):
            node = node.children[0]

        while node:
            for pair in itertools.izip(node.contents, node.data):
                yield pair
            node = node.next

    def iterkeys(self):
        return itertools.imap(operator.itemgetter(0), self.iteritems())

    def itervalues(self):
        return itertools.imap(operator.itemgetter(1), self.iteritems())

    __iter__ = iterkeys

    def items(self):
        return list(self.iteritems())

    def keys(self):
        return list(self.iterkeys())

    def values(self):
        return list(self.itervalues())

    def _build_bulkloaded_leaves(self, items):
        minimum = self.order // 2
        leaves, seps = [[]], []

        for item in items:
            if len(leaves[-1]) >= self.order:
                seps.append(item)
                leaves.append([])
            leaves[-1].append(item)

        if len(leaves[-1]) < minimum and seps:
            last_two = leaves[-2] + leaves[-1]
            leaves[-2] = last_two[:minimum]
            leaves[-1] = last_two[minimum:]
            seps.append(last_two[minimum])

        leaves = [self.LEAF(
            self,
            contents=[p[0] for p in pairs],
            data=[p[1] for p in pairs])
            for pairs in leaves]

        for i in range(len(leaves) - 1):
            leaves[i].next = leaves[i + 1]

        return leaves, [s[0] for s in seps]
