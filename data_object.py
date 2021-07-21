import datetime
import numpy as np
import scipy.stats


class DataObject(object):
    def __init__(self, mylist=None):
        super(DataObject, self).__init__()
        self.mylist = mylist

    def minimum(self):
        return min(self.mylist)

    def min_minimum(self):
        return DataObject(DataObject(entry).minimum() for entry in self.mylist).minimum()

    def maximum(self):
        return max(self.mylist)

    def max_maximum(self):
        return DataObject(DataObject(entry).maximum() for entry in self.mylist).maximum()

    def range(self):
        return self.maximum() - self.minimum()

    def len(self):
        return len(self.mylist)

    def sum(self):
        return sum(self.mylist)

    def average(self):
        return sum(self.mylist) / self.len()

    def madMethod(self):
        med = np.median(self.mylist)
        mad = np.abs(scipy.stats.median_absolute_deviation(self.mylist))

        threshold = 9
        outlier_durations_list = []
        for v in self.mylist:
            t = np.abs((v - med) / mad)
            if t > threshold:
                outlier_durations_list.append((v,))
            else:
                continue
        return outlier_durations_list

    def getTotalEntries(self):
        total_entries = DataObject(len(entry.getTimestamps()) for entry in self.mylist).sum()
        print("\nNumber of threads: ", len(self.mylist))
        print("Total entries: ", total_entries)
        return total_entries

    def getAvgCountRecords(self):
        avg_count = DataObject([len(entry.getTimestamps()) for entry in self.mylist]).average()
        print("Average number of records per thread:", "{:.2f}".format(avg_count))
        return avg_count

    def getFastest(self):
        fastest_list = []
        fastest_value = DataObject(len(entry.getTimestamps()) for entry in self.mylist).maximum()
        for entry in self.mylist:
            entry_ID = entry.getThreadID()
            if len(entry.getTimestamps()) == fastest_value:
                fastest_list.append(entry_ID)
        print("Fastest thread(s): Thread(s)", fastest_list, "with", fastest_value, "records")
        return fastest_list, fastest_value

    def getSlowest(self):
        slowest_list = []
        slowest_value = DataObject(len(entry.getTimestamps()) for entry in self.mylist).minimum()
        for entry in self.mylist:
            entry_ID = entry.getThreadID()
            if len(entry.getTimestamps()) == slowest_value:
                slowest_list.append(entry_ID)
        print("Slowest thread(s): Thread(s)", slowest_list, "with", slowest_value, "records")
        return slowest_list, slowest_value

    def getMaxDuration(self):
        max_duration_list = []
        max_duration_value = DataObject(DataObject(entry.getTimestamps()).range() for entry in self.mylist).maximum()
        for entry in self.mylist:
            entry_ID = entry.getThreadID()
            if DataObject(entry.getTimestamps()).range() == max_duration_value:
                max_duration_list.append(entry_ID)
        print("Greatest difference in timestamps per thread: Thread(s) {}, time range {} seconds".format(max_duration_list, max_duration_value))
        return max_duration_list, max_duration_value
        
    def getMinDuration(self):
        min_duration_list = []
        min_duration_value = DataObject(DataObject(entry.getTimestamps()).range() for entry in self.mylist).maximum()
        for entry in self.mylist:
            entry_ID = entry.getThreadID()
            if DataObject(entry.getTimestamps()).range() == min_duration_value:
                min_duration_list.append(entry_ID)
        print("Least difference in timestamps per thread: Thread(s) {}, time range {} seconds".format(
            min_duration_list, min_duration_value))
        return min_duration_list, min_duration_value

    def getOutliers(self):
        outlier_list = DataObject([DataObject(entry.getTimestamps()).range() for entry in self.mylist]).madMethod()
        for entry in self.mylist:
            entry_ID = entry.getThreadID()
            # Outliers (Dead Threads)
            for i, outlier in enumerate(outlier_list):
                if DataObject(entry.getTimestamps()).range() == outlier[0]:
                    t = DataObject(entry.getTimestamps()).maximum()
                    outlier_list[i] = outlier + (entry_ID, t)

        print("\nOutlier thread(s): ")
        for outlier in outlier_list:
            print("\tThread", outlier[1],
                  "died after", outlier[0],
                  "seconds at", datetime.datetime.fromtimestamp(outlier[2]))
        return

    def formatScientific(self):
        for entry in self.mylist:
            print("Entry: ", entry)
        return ("{:e}".format(float(entry)) for entry in self.mylist)
