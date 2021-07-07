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
    duration_list = df['Duration'].tolist
    duration_mad = DataObject.DataObject.madMethod(duration_list)  # Outputs the index in df of the outliers
    print("Outlier threads: ")
    for row in duration_mad:
        print("\tThread", df.loc[row, 'Thread'],
              "died after", df.loc[row, 'Duration'],
              "seconds at", df.loc[row, 'Latest Record'])


def analyzeThreadStatsTable(df):
    fastest_thread_index, slowest_thread_index, greatest_duration_index, least_duration_index = [], [], [], []

    total_threads = df['Number of Records'].sum()
    unique_threads = len(df.columns)
    print("unique: ", unique_threads)
    average_num_threads = total_threads / unique_threads

    # Finding the number of records for the fastest and slowest threads
    fastest_thread_value = max(df['Number of Records'])
    slowest_thread_value = min(df['Number of Records']) #FIXME is it still the slowest thread if it dies early or is there actually a velocity to threads?
    greatest_duration = max(df['Duration'])
    least_duration = min(df['Duration'])

    # Find the threads for which the max's and min's occur
    for index, row in df.iterrows():
        number_of_records = df.loc[row, 'Number of Records']
        duration = df.loc[row, 'Duration']

        # Finding the threads with the fastest and slowest rates
        if number_of_records == fastest_thread_value:
            fastest_thread_index.append(df.loc[row, 'Thread'])
        if number_of_records == slowest_thread_value:
            slowest_thread_index.append(df.loc[row, 'Thread'])

        # Finding the threads with the greatest and least duration
        if duration == greatest_duration:
            greatest_duration_index.append(df.loc[row, 'Thread'])
        if duration == least_duration:
            least_duration_index.append(df.loc[row, 'Thread'])

    print("Total entries: ", total_threads)
    print("\nAverage numbers of records per thread:", "{:.2f}".format(average_num_threads))
    print("Fastest thread:", fastest_thread_index, "with", fastest_thread_value, "records")
    print("Slowest thread:", slowest_thread_index, "with", slowest_thread_value, "records")
    print("Greatest difference in timestamps per thread: Thread {}, time range {} seconds".format(greatest_duration_index, greatest_duration))
    print("Least difference in timestamps per thread: Thread {}, time range {} seconds".format(least_duration_index, least_duration))

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
