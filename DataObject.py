import numpy as np


class DataObject(object):
    def __init__(self, mylist=None):
        super(DataObject, self).__init__()
        self.mylist = mylist

    def earliest_record(self):
        return min(self.mylist)

    def latest_record(self):
        return max(self.mylist)

    def range(self):
        return self.latest_record() - self.earliest_record()

    def len(self):
        return len(self.mylist)

    def average(self):
        return sum(self.mylist)/len(self.mylist)

    def sum_col(self, col_num):
        array = np.sum(self.mylist, 0)
        print(array)
        return array[col_num]