import numpy as np


class DataObject(object):
    def __init__(self, mylist=None):
        super(DataObject, self).__init__()
        self.mylist = mylist

    def earliest_record(self):
        return np.min(self.mylist)

    def latest_record(self):
        return np.max(self.mylist)

    def range(self):
        return self.latest_record() - self.earliest_record()

    def len(self):
        return len(self.mylist)
