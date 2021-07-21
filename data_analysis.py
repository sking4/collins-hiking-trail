from __future__ import print_function
import sys
import os
import csv
import argparse
import matplotlib.pyplot as plt
import thread_records
from list_set import analyzeThreadStats, analyzeRandom, plotting


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
            if filename_checker(file_path)[0]:
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
                    if float(row[1]) == threadObj.getThreadID():  # if the thread ID for the line in the CSV file equals
                        # the unique thread ID in question
                        threadObj.appendEntry(float(row[0]), row[2])  # add the timestamp and random number information
                        # to a list of data specific to that unique thread ID
                        foundThread = True
                        break
                if not foundThread:  # if the line from the CSV file has a thread ID not already captured by the list
                    # of unique thread IDs
                    thread_list.append(thread_records.ThreadRecords(float(row[1]), [(float(row[0]), row[2])]))  # add
                    # that thread ID to the unique list, as well as its timestamp and random number info
            except:
                next(csv_read)
    return thread_list


def main():
    thread_list = []
    # Gather file path, either from command line or from user input
    file_path = collect_filename()

    # Open file and process data
    # thread_list is a matrix with a list of all the unique thread IDs and
    # each of those holding the data for the corresponding thread
    # (timestamp and random number for each occurrence of that thread)
    thread_list = gather_data(file_path)

    # Analyze the thread data collected
    analyzeThreadStats(thread_list)

    # Analyze the random numbers
    analyzeRandom(thread_list)

    # Plot stuff
    plotting(thread_list)


if __name__ == '__main__':
    main()
