from __future__ import print_function
from tabulate import tabulate
import sys
import os
import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np


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
    DataUnix(unix_list).output_unix_metrics()
    DataThread(thread_list).output_thread_metrics()
    DataRandom(randnum_list).output_randnum_metrics()
    plotting(time_list, randnum_list, thread_list)


if __name__ == '__main__':
    main()
