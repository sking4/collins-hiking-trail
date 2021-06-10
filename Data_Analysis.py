from __future__ import print_function
import sys
import os
import csv
import matplotlib.pyplot as plt
import argparse

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
        for row in csv_read:
            try:
                foundThread = False
                for threadObj in threadList:
                    if row[1] == threadObj.getThreadID()
                        threadObj.appendEntry(float(row[0]), int(row[2]))
                        foundThread = True
                        break
                if not foundThread:
                    thread_list.append(ThreadRecords.ThreadRecords(row[1], [ (float(row[0]),
                                                                              int(row[2]))] ))
                randnum_list.append(float(row[2]))
                unix_list.append(float(row[0]))
                time_list.append(float(row[0]) - min(unix_list))
            except:
                next(csv_read)
    return unix_list, time_list, thread_list, randnum_list


def main():
    # Gather file path, either from command line or from user input
    file_path = collect_filename()

    # Open file and process data
    unix_list, time_list, thread_list, randnum_list = gather_data(file_path)

    # OUTPUTS
    DataUnix.DataUnix(unix_list).output_unix_metrics()
    #DataThread.DataThread(thread_list).output_thread_metrics(unix_list)
    for thread in thread_list:
        print(thread.getThreadID() + "\tmin time:\t" + np.min(thread.timestamps())
        print(thread.getThreadID() + "\tmax time:\t" + np.max(thread.timestamps())
    DataRandom.DataRandom(randnum_list).output_randnum_metrics()
    plotting(time_list, randnum_list, thread_list)


if __name__ == '__main__':
    main()            
