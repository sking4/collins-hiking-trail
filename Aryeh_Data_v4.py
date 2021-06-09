from __future__ import print_function
from tabulate import tabulate
import sys
import os
import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np


class Unix(object): # putting object uses object inheritance?
    def __init__(self, mylist):
        super(Unix, self).__init__()
        self.mylist = mylist

    def duration(self):
        return max(self.mylist) - min(self.mylist)

    def start_time(self):
        return datetime.datetime.fromtimestamp(min(self.mylist))

    def end_time(self):
        return datetime.datetime.fromtimestamp(max(self.mylist))

    def output_unix_metrics(self):
        print("\nNumber of data points: ", len(self.mylist))
        print("Duration: ", self.duration(), "seconds")
        print("Data collected from", self.start_time(), "to", self.end_time())


class Threads(object):
    def __init__(self, mylist):
        super(Threads, self).__init__()
        self.mylist = mylist

    def num_records(self):
        return len(self.mylist)

    def earliest_record(self):
        return np.min(self.mylist)

    def latest_record(self):
        return np.max(self.mylist)

    def range(self):
        return self.latest_record() - self.earliest_record()

    def records_per(self):
        return np.count(self.mylist)

    def add_thread_metrics(self, n, arr_set, data, arr_ranges, arr_records, arr_durations):
        # Metrics per thread
        data.append(["{:e}".format(arr_set[n]), self.num_records(), None, None]) #FIXME remove Nones and fix timestamp, timestamp should be unix record at that thread location
    #                 datetime.datetime.fromtimestamp(self.earliest_record()),
     #                datetime.datetime.fromtimestamp(self.latest_record())])

        # Metrics about all threads
        arr_ranges.append(self.range())
        arr_records.append(self.num_records())
        arr_durations.append(self.range())

    def separate_threads(self):
        arr_set = sorted(list(set(self.mylist)))
        unique_arr_count = len(arr_set)

        data = []
        arr_ranges = []
        arr_records = []
        arr_durations = []

        # Separating the timestamps by unique thread ID
        for ele_base in range(0, len(arr_set)):  # For each distinct thread
            unix_per_arr_list = []
            test_arr = arr_set[ele_base]
            for ele_test in range(0, len(self.mylist)):  # Go through the thread list and find the time values for each
                if self.mylist[ele_test] == test_arr:
                    unix_per_arr_list.append(
                        self.mylist[ele_test])  # Add all of the timestamps for that thread to a list
            arr = np.array(unix_per_arr_list)

            self.add_thread_metrics(ele_base, arr_set, data, arr_ranges, arr_records, arr_durations)

        avg_per_period = sum(arr_records) / unique_arr_count

        return arr_set, unique_arr_count, data, arr_ranges, arr_records, arr_durations, avg_per_period

    def output_thread_metrics(self):
        thread_set, unique_threads, thread_data, threads_ranges, threads_records, threads_durations = self.separate_threads()[0:6]
        avg_records_per_thread = sum(threads_records) / unique_threads
        print("Number of unique thread values generated: ", unique_threads)

        # Output table for metrics per thread
        headers_list = ["Thread", "Number of Records", "Earliest Record", "Latest Record"]
        print("\n")
        print(tabulate(thread_data, headers=headers_list, floatfmt=("e", "", "", "")))

        fastest_value = max(threads_records)
        fastest_index = threads_records.index(fastest_value)
        slowest_value = min(threads_records)
        slowest_index = threads_records.index(slowest_value)

        greatest_diff_value = max(threads_ranges)
        greatest_diff_index = threads_ranges.index(greatest_diff_value)
        least_diff_value = min(threads_ranges)
        least_diff_index = threads_ranges.index(least_diff_value)

        print("\nAverage numbers of records per thread:", "{:.2f}".format(avg_records_per_thread))
        print("Fastest thread:", "{:e}".format(thread_set[fastest_index]), "with", fastest_value, "records")
        print("Slowest thread:", "{:e}".format(thread_set[slowest_index]), "with", slowest_value, "records")
        print("Greatest difference in timestamps per thread: Thread {:e}, time range {} seconds".format(
            thread_set[greatest_diff_index], greatest_diff_value))
        print("Least difference in timestamps per thread: Thread {:e}, time range {} seconds".format(
            thread_set[least_diff_index], least_diff_value))


class RandomNumbers(object):
    def __init__(self, mylist):
        super(RandomNumbers, self).__init__()
        self.mylist = mylist

    def output_randnum_metrics(self):
        # Range
        randnum_min = min(self.mylist)
        randnum_max = max(self.mylist)
        print("\nRandom numbers generated from", randnum_min, "to", randnum_max)

        # Sort randomly generated numbers
        while True:
            sorted_list_print = input("Print sorted list of randomly generated numbers? Yes or no: ")
            if sorted_list_print.lower() == "yes":
                list_formatted = ["{:e}".format(elem) for elem in self.mylist]
                print("The randomly generated numbers sorted from smallest to largest are:\t",
                      *sorted(list_formatted), sep='\n\t')
                break
            elif sorted_list_print.lower() == "no":
                break
            else:
                print("Response not recognized, try again.")

def plotting(time, randnum, threads):
    avg = Threads.separate_threads(threads)[6]

    plot1 = plt.figure(1)  # Thread value over time
    plt.plot(time, threads)
    plt.title("Thread ID Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Thread ID")

    plot2 = plt.figure(2)  # Zoomed in thread value over time
    plt.plot(time, threads)
    x_min, x_max = time[int(len(time) / 4)], time[int(len(time) / 3)]
    plt.xlim([x_min, x_max])
    plt.title("Thread ID Over Time (Snippet)")
    plt.xlabel("Time (s)")
    plt.ylabel("Thread ID")

    plot3 = plt.figure(3)  # Random numbers generated over time
    plt.plot(time, randnum)
    plt.title("Random Numbers Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Random Number")

    plt.show()

def filename_checker(file_path):
    isValid = False
    if file_path == "z":
        file_path = str(r"C:\Users\sking4\OneDrive - Raytheon Technologies\Python\AryehData.csv")
        isValid = True
    elif file_path == "":
        print("File path cannot be blank.")
    elif not os.path.exists(file_path):
        print("File not found at " + str(file_path))
    else:
        isValid = True
    return isValid


def collect_filename():
    if len(sys.argv) <= 1:
        while True:
            file_path = input("Please specify the data CSV file path: ")
            if filename_checker(file_path):
                break
    else:
        file_path = str(sys.argv[1])  # #FIXME use argeparse module, does validation
        if not filename_checker(file_path):
            sys.exit(1)  # Exits the program
    return file_path


def gather_data(file_path):
    unix_list, time_list, thread_list, randnum_list = [], [], [], []
    with open(str(file_path), 'r+') as csv_file:
        # Read data and separate into lists
        csv_read = csv.reader(csv_file)
        for row in csv_read:
            try:
                unix_list.append(float(row[0]))
                time_list.append(float(row[0]) - unix_list[0])  # FIXME Record zero is not the smallest
                thread_list.append(float(row[1]))
                randnum_list.append(float(row[2]))
            except:
                next(csv_read)
    return unix_list, time_list, thread_list, randnum_list


def main():
    # Gather file path, either from command line or from user input
    file_path = collect_filename()

    # Open file and process data
    unix_list, time_list, thread_list, randnum_list = gather_data(file_path)

    # OUTPUTS
    Unix(unix_list).output_unix_metrics()
    Threads(thread_list).output_thread_metrics()
    RandomNumbers(randnum_list).output_randnum_metrics()
    plotting(time_list, randnum_list, thread_list)





if __name__ == '__main__':
    main()
