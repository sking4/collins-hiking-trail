from my_functions import mad_method_function


class ThreadObject(object):
    def __init__(self, tid=0, time_list=None, rand_list=None):
        self.threadID = tid
        self.timeObjects = DataObject(time_list)
        self.randObjects = DataObject(rand_list)


class AnalysisObject(object):
    def __init__(self, my_object_tuple=None):
        super(AnalysisObject, self).__init__()
        self.analysisTargets = {}
        for my_object_list, my_thread_ID in my_object_tuple:
            self.analysisTargets[my_thread_ID] = my_object_list

    def min(self):
        return min(self.analysisTargets[entry].minimum() for entry in self.analysisTargets)

    def max(self):
        return max(self.analysisTargets[entry].maximum() for entry in self.analysisTargets)

    def getNumThreads(self):
        num_threads = len(self.analysisTargets)
        return num_threads

    def getTotalEntries(self):
        total_entries = sum(self.analysisTargets[entry].len() for entry in self.analysisTargets)
        return total_entries

    def getAvgCountRecords(self):
        avg_count = sum(self.analysisTargets[entry].len() for entry in self.analysisTargets)/len(self.analysisTargets)
        return avg_count

    def getMostRecords(self):
        most_records_list = []
        most_records_value = max([self.analysisTargets[entry].len() for entry in self.analysisTargets])
        for entry in self.analysisTargets:
            if self.analysisTargets[entry].len() == most_records_value:
                most_records_list.append(entry)
        return most_records_list, most_records_value

    def getLeastRecords(self):
        least_records_list = []
        least_records_value = max([self.analysisTargets[entry].len() for entry in self.analysisTargets])
        for entry in self.analysisTargets:
            if self.analysisTargets[entry].len() == least_records_value:
                least_records_list.append(entry)
        return least_records_list, least_records_value

    def getFastest(self):
        fastest_list = []
        # Fastest value is determined by max velocity (values per second)
        fastest_value = max([self.analysisTargets[entry].len() /
                             self.analysisTargets[entry].range() for entry in self.analysisTargets])
        for entry in self.analysisTargets:
            if (self.analysisTargets[entry].len() / self.analysisTargets[entry].range()) == fastest_value:
                fastest_list.append(entry)
        return fastest_list, fastest_value

    def getSlowest(self):
        slowest_list = []
        # Slowest value is determined by min velocity (values per second)
        slowest_value = min([self.analysisTargets[entry].len() /
                             self.analysisTargets[entry].range() for entry in self.analysisTargets])
        for entry in self.analysisTargets:
            if (self.analysisTargets[entry].len() / self.analysisTargets[entry].range()) == slowest_value:
                slowest_list.append(entry)
        return slowest_list, slowest_value

    def getMaxDuration(self):
        max_duration_list = []
        max_duration_value = max([self.analysisTargets[entry].range() for entry in self.analysisTargets])
        for entry in self.analysisTargets:
            if self.analysisTargets[entry].range() == max_duration_value:
                max_duration_list.append(entry)
        return max_duration_list, max_duration_value

    def getMinDuration(self):
        min_duration_list = []
        min_duration_value = min([self.analysisTargets[entry].range() for entry in self.analysisTargets])
        for entry in self.analysisTargets:
            if self.analysisTargets[entry].range() == min_duration_value:
                min_duration_list.append(entry)
        return min_duration_list, min_duration_value

    def getOutliers(self):
        duration_outlier_list = mad_method_function([self.analysisTargets[entry].range()
                                                     for entry in self.analysisTargets], 9)
        count_outlier_list = mad_method_function([self.analysisTargets[entry].len()
                                                  for entry in self.analysisTargets], 9)

        for entry in self.analysisTargets:
            # Duration Outliers (Dead Threads)
            for i, outlier in enumerate(duration_outlier_list):
                if self.analysisTargets[entry].range() == outlier[0]:
                    t = self.analysisTargets[entry].maximum()
                    duration_outlier_list[i] = outlier + (entry, t)

            # Number of Records Outliers
            for i, outlier in enumerate(count_outlier_list):
                if self.analysisTargets[entry].len() == outlier[0]:
                    t = self.analysisTargets[entry].maximum()
                    count_outlier_list[i] = outlier + (entry, t)

        return duration_outlier_list, count_outlier_list


class DataObject(object):
    def __init__(self, mylist=None):
        super(DataObject, self).__init__()
        self.mylist = mylist
        # self.tid =

    def minimum(self):
        return min(self.mylist)

    def maximum(self):
        return max(self.mylist)

    def range(self):
        return self.maximum() - self.minimum()

    def len(self):
        return len(self.mylist)

    def sum(self):
        return sum(self.mylist)

    def average(self):
        return sum(self.mylist) / self.len()

    def formatScientific(self):
        for entry in self.mylist:
            print("Entry: ", entry)
        return ("{:e}".format(float(entry)) for entry in self.mylist)
