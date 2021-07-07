import numpy as np
import pandas as pd
import datetime
from scipy import stats
from tabulate import tabulate

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
        return sum(self.mylist) / len(self.mylist)

    def madMethod(self):
        med = np.median(self.mylist, axis=0)
        mad = np.abs(stats.median_absolute_deviation(self.mylist))
        threshold = 9
        outlier = []
        for i, v in enumerate(self.mylist):
            t = np.abs((v - med) / mad)
            if t > threshold:
                outlier.append(i)
            else:
                continue
        return outlier
