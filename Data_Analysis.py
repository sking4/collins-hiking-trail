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
        file_path = str(r"C:\Users\sking4\OneDrive - Raytheon Technologies\Python\AryehData.csv")
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
    thread_list = []
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
                    thread_list.append(ThreadRecords.ThreadRecords(float(row[1]), [(float(row[0]), row[2])]))  # add that thread ID to the unique list, as well as its timestamp and random number info
            except:
                next(csv_read)
    return thread_list


def main():
    thread_list = []
    # Gather file path, either from command line or from user input
    file_path = collect_filename()

    # Open file and process data
    thread_list = gather_data(file_path)

    # OUTPUTS
    summary_table = []
    headers_list = ["Thread", "Number of Records", "Earliest Record", "Latest Record", "Duration"]
    for thread in thread_list:  # for each unique thread ID
        summary_table.append([str(thread.getThreadID()),
                             str(len(thread.timestamps())),
                             datetime.datetime.fromtimestamp(DataObject.DataObject(thread.timestamps()).minimum()),
                             datetime.datetime.fromtimestamp(DataObject.DataObject(thread.timestamps()).maximum()),
                             DataObject.DataObject(thread.timestamps()).range()])
    total_threads = sum(len(thread.timestamps()) for thread in thread_list)
    print("Total entries: ", total_threads)
    print("\n", tabulate(summary_table, headers=headers_list, floatfmt=("", "", "", "", "")))
    print("\nAverage numbers of records per thread:", "{:.2f}".format(total_threads/len(thread_list)))

    max_value = max(len(thread.timestamps()) for thread in thread_list)
    min_value = min(len(thread.timestamps()) for thread in thread_list)
    greatest_range_value = max(DataObject.DataObject(thread.timestamps()).range() for thread in thread_list)
    least_range_value = min(DataObject.DataObject(thread.timestamps()).range() for thread in thread_list)

    max_index = []
    min_index = []
    greatest_range_index = []
    least_range_index = []
    # For finding indexes, there has to be a better way
    for thread in thread_list:
        if len(thread.timestamps()) == max_value:
            max_index.append(thread.getThreadID())
        if len(thread.timestamps()) == min_value:
            min_index.append(thread.getThreadID())
        if DataObject.DataObject(thread.timestamps()).range() == greatest_range_value:
            greatest_range_index = thread.getThreadID()
        if DataObject.DataObject(thread.timestamps()).range() == least_range_value:
            least_range_index = thread.getThreadID()


    # max_index = max(thread.getThreadID() for thread in thread_list)  # FIXME this is just getting the maximum thread ID, not the index
    # min_index = min(thread.getThreadID() for thread in thread_list) #FIXME this is just getting the minimum thread ID, not the index
    #greatest_range_index = max((DataObject.DataObject(thread.timestamps()).range()).getThreadID #FIXME

    print("Fastest thread:", max_index, "with", max_value, "records")
    print("Slowest thread:", min_index, "with", min_value, "records")
    print("Greatest difference in timestamps per thread: Thread {}, time range {} seconds".format(greatest_range_index, greatest_range_value))
    print("Least difference in timestamps per thread: Thread {}, time range {} seconds".format(least_range_index, least_range_value))

    # DataRandom.DataRandom(randnum_list).output_randnum_metrics()
    # plotting(time_list, randnum_list, thread_list)


if __name__ == '__main__':
    main()
