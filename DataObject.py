import numpy as np
import pandas as pd
import datetime
from scipy import stats
from tabulate import tabulate

import DataObject


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
        med = np.median(self.mylist)
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

    def maxMinIndex(self):
        max_value = self.maximum()
        min_value = self.minimum()  # FIXME is it still the slowest thread if it dies early or is there actually a velocity to threads?
        max_index, min_index = [], []

        for i, v in enumerate(self.mylist):
            # Finding index row for max and min values
            if v == max_value:
                max_index.append(i)
            if v == min_value:
                min_index.append(i)
        return max_index, min_index