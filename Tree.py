from abc import ABC, abstractclassmethod


class Tree(ABC, object):

    @abstractclassmethod
    def add(self):
        pass

    @abstractclassmethod
    def delete(self):
        pass

    @abstractclassmethod
    def __contains__(self, key):
        pass

    @abstractclassmethod
    def __str__(self):
        pass
