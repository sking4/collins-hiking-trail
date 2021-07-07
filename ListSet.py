import pandas as pd

import DataObject
import datetime
from tabulate import tabulate


def createThreadStatsTable(thread_list):
    summary_table = []
    headers_list = ["Thread", "Number of Records", "Earliest Record", "Latest Record", "Duration"]
    for thread in thread_list:  # for each unique thread ID
        # Add that thread's info to the master table
        summary_table.append([thread.getThreadID(),
                              len(thread.timestamps()),
                              datetime.datetime.fromtimestamp(DataObject.DataObject(thread.timestamps()).minimum()),
                              datetime.datetime.fromtimestamp(DataObject.DataObject(thread.timestamps()).maximum()),
                              DataObject.DataObject(thread.timestamps()).range()])

    print("\n", tabulate(summary_table, headers=headers_list, floatfmt=("", "", "", "", ""))) # Print out the pretty table
    return pd.DataFrame(summary_table, columns=headers_list)  # Turn data table into a dataframe to analyze the columns


def getDeadThreads(df):
    duration_mad = DataObject.DataObject(df['Duration']).madMethod()  # Outputs the index in df of the outliers
    print("\nOutlier threads: ")
    for row in duration_mad:
        print("\tThread", df.loc[row, 'Thread'],
              "died after", df.loc[row, 'Duration'],
              "seconds at", df.loc[row, 'Latest Record'])


def analyzeThreadStatsTable(thread_list):
    # Create master thread table
    df = createThreadStatsTable(thread_list)

    total_threads = df['Number of Records'].sum()
    unique_threads = len(df.index)
    average_num_threads = total_threads / unique_threads
    fastest_thread_num = df['Number of Records'].max()
    fastest_thread = df.loc[df['Number of Records'].idxmax(), 'Thread']
    slowest_thread_num = df['Number of Records'].min()
    slowest_thread = df.loc[df['Number of Records'].idxmin(), 'Thread']
    greatest_duration = df['Duration'].max()
    greatest_duration_thread = df.loc[df['Duration'].idxmax(), 'Thread']
    least_duration = df['Duration'].min()
    least_duration_thread = df.loc[df['Duration'].idxmin(), 'Thread']

    print("\nTotal entries: ", total_threads)
    print("Average numbers of records per thread:", "{:.2f}".format(average_num_threads))
    print("Fastest thread: Thread", fastest_thread, "with", fastest_thread_num, "records")  # Only gets first fastest thread
    print("Slowest thread: Thread", slowest_thread, "with", slowest_thread_num, "records")  # Only gets first slowest thread
    print("Greatest difference in timestamps per thread: Thread {}, time range {} seconds".format(greatest_duration_thread, greatest_duration))
    print("Least difference in timestamps per thread: Thread {}, time range {} seconds".format(least_duration_thread, least_duration))

    # Analyze the duration column to find outliers/dead threads (somewhat arbitrary threshold)
    getDeadThreads(df)


def AnalyzeRandom(thread_set):
    for thread in thread_set:
        # Range
        randnum_max = DataObject.DataObject(thread.randomNumbers).maximum()
        randnum_min = DataObject.DataObject(thread.randomNumbers).minimum()
        print("\nRandom numbers generated from", randnum_min, "to", randnum_max)

    # Sort randomly generated numbers #FIXME stuff after this isn't integrated/updated
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
