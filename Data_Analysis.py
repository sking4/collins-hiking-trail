from __future__ import print_function
import sys
import os
import csv
import matplotlib.pyplot as plt
import argparse
import numpy as np

import DataRandom
import DataThread
import DataUnix
import ThreadRecords


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
    unix_list, time_list, thread_list, randnum_list = [], [], [], []
    with open(str(file_path), 'r+') as csv_file:
        # Read data and separate into lists
        csv_read = csv.reader(csv_file)
        for row in csv_read:  # for each line in the csv file [timestamp, thread ID, random number]
            try:
                foundThread = False
                for threadObj in thread_list:  # for a unique thread that has already been added to the thread_list
                    if float(row[1]) == threadObj.getThreadID():  # if the thread ID for the line in the CSV file equals the unique thread ID in question
                        print("Test: " + str(test))
                        print("Row: " + str(row[1]))
                        threadObj.appendEntry(float(row[0]), row[2])  # add the timestamp and random number information to a list of data specific to that unique thread ID
                        foundThread = True
                        break
                if not foundThread:  # if the line from the CSV file has a thread ID not already captured by the list of unique thread IDs
                    print("FOUND THREAD")
                    thread_list.append(ThreadRecords.ThreadRecords(float(row[1]), [float(row[0]), row[2]])) # add that thread ID to the unique list, as well as its timestamp and random number info
                    print("Thread list: " + str(thread_list))
                randnum_list.append(float(row[2]))
                unix_list.append(float(row[0]))
                time_list.append(float(row[0]) - min(unix_list))
            except:
                next(csv_read)

    for ele in thread_list:
        print(str(ele))
    return unix_list, time_list, thread_list, randnum_list


def main():
    # Gather file path, either from command line or from user input
    file_path = collect_filename()

    # Open file and process data
    unix_list, time_list, thread_list, randnum_list = gather_data(file_path)

    # OUTPUTS
    DataUnix.DataUnix(unix_list).output_unix_metrics()
    # DataThread.DataThread(thread_list).output_thread_metrics(unix_list)
    print(thread_list)
    for thread in thread_list:
        print(str(thread.getThreadID()) + "\tmin time:\t" + str(np.min(thread.timestamps())))
        print(str(thread.getThreadID()) + "\tmax time:\t" + str(np.max(thread.timestamps())))
    DataRandom.DataRandom(randnum_list).output_randnum_metrics()
    # plotting(time_list, randnum_list, thread_list)


if __name__ == '__main__':
    main()
