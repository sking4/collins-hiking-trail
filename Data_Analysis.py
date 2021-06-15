from __future__ import print_function
import sys
import os
import csv
import matplotlib.pyplot as plt
import argparse
import DataObject
import ThreadRecords
from tabulate import tabulate
import datetime


def plotting(time, randnum, threads):
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
        file_path = str(r"C:\Users\sking4\OneDrive - Raytheon Technologies\Python\AryehData2.csv")
        isValid = True
    elif file_path == "":
        print("File path cannot be blank.")
    elif not os.path.exists(file_path):
        print("File not found at " + str(file_path))
    else:
        isValid = True
    return isValid, file_path


def collect_filename():
    if len(sys.argv) <= 1:
        while True:
            file_path = input("Please specify the data CSV file path: ")
            if filename_checker(file_path):
                file_path = filename_checker(file_path)[1]
                break
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('file_path', type=str)
        p = parser.parse_args()
        file_path = p.file_path
        if not filename_checker(file_path):
            sys.exit(1)  # Exits the program
    return file_path


def gather_data(file_path):
    unix_list, time_list, thread_list, randnum_list = [], [], [], []
    with open(str(file_path), 'r+') as csv_file:
        # Read data and separate into lists
        csv_read = csv.reader(csv_file)
        for row in csv_read:  # for each line in the csv file [timestamp, thread ID, random number]
            try:
                foundThread = False
                for threadObj in thread_list:  # for a unique thread that has already been added to the thread_list
                    if float(row[1]) == threadObj.getThreadID():  # if the thread ID for the line in the CSV file equals the unique thread ID in question
                        threadObj.appendEntry(float(row[0]), row[2])  # add the timestamp and random number information to a list of data specific to that unique thread ID
                        foundThread = True
                        break
                if not foundThread:  # if the line from the CSV file has a thread ID not already captured by the list of unique thread IDs
                    thread_list.append(ThreadRecords.ThreadRecords(float(row[1]), [float(row[0]), row[2]]))  # add that thread ID to the unique list, as well as its timestamp and random number info
            except:
                next(csv_read)

    return unix_list, time_list, thread_list, randnum_list


def main():
    # Gather file path, either from command line or from user input
    file_path = collect_filename()

    # Open file and process data
    unix_list, time_list, thread_list, randnum_list = gather_data(file_path)

    # OUTPUTS
    # DataUnix.DataUnix(unix_list).output_unix_metrics()
    # DataThread.DataThread(thread_list).output_thread_metrics(unix_list)
    summary_table = []
    headers_list = ["Thread", "Number of Records", "Earliest Record", "Latest Record"]
    total_threads = 0
    max_value = 0
    max_index = None
    min_value = 0
    min_index = None
    for thread in thread_list:  # for each unique thread ID
        summary_table.append([str(thread.getThreadID()),
                             str(len(thread.timestamps())),
                             datetime.datetime.fromtimestamp(DataObject.DataObject(thread.timestamps()).earliest_record()),
                             datetime.datetime.fromtimestamp(DataObject.DataObject(thread.timestamps()).latest_record())])

        total_threads += len(thread.timestamps())
        # Fastest and slowest threads
        if len(thread.timestamps()) > max_value:
            max_value = len(thread.timestamps())
            max_index = thread.getThreadID()
        if len(thread.timestamps()) < min_value or min_value == 0:
            min_value = len(thread.timestamps())
            min_index = thread.getThreadID()

    # print("Length of thread_list: ", total_threads)
    #
    # print("\n", tabulate(summary_table, headers=headers_list, floatfmt=("e", "", "", "")))
    # print("\nAverage numbers of records per thread:", "{:.2f}".format(total_threads/len(thread_list)))
    #
    # print("Fastest thread:", "{:e}".format(max_index), "with", max_value, "records")
    # print("Slowest thread:", "{:e}".format(min_index), "with", min_value, "records")
    # print("Greatest difference in timestamps per thread: Thread {:e}, time range {} seconds".format(
    #     thread_set[greatest_diff_index], greatest_diff_value))
    # print("Least difference in timestamps per thread: Thread {:e}, time range {} seconds".format(
    #     thread_set[least_diff_index], least_diff_value))

    # DataRandom.DataRandom(randnum_list).output_randnum_metrics()
    # plotting(time_list, randnum_list, thread_list)


if __name__ == '__main__':
    main()
