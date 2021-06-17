import numpy as np


class DataObject(object):
    def __init__(self, mylist=None):
        super(DataObject, self).__init__()
        self.mylist = mylist

    def minimum(self):
        return min(self.mylist)

    def maximum(self):
        return max(self.mylist)

    def range(self):
        return self.maximum() - self.minimum()

    def len(self):
        return len(self.mylist)

    def average(self):
        return sum(self.mylist)/len(self.mylist)
