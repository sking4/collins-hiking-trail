import datetime
from tabulate import tabulate
import DataObject


def outputThreadStatsTable(thread_list):
    summary_table = []
    headers_list = ["Thread", "Number of Records", "Earliest Record", "Latest Record", "Duration"]
    for thread in thread_list:  # for each unique thread ID
        # Add that thread's info to the master table
        summary_table.append([thread.getThreadID(),
                              len(thread.getTimestamps()),
                              datetime.datetime.fromtimestamp(DataObject.DataObject(thread.getTimestamps()).minimum()),
                              datetime.datetime.fromtimestamp(DataObject.DataObject(thread.getTimestamps()).maximum()),
                              DataObject.DataObject(thread.getTimestamps()).range()])

    print("\n", tabulate(summary_table, headers=headers_list, floatfmt=("", "", "", "", "")), "\n") # Print out the pretty table
    return


def analyzeThreadStats(thread_list):
    outputThreadStatsTable(thread_list)
    threadObj = DataObject.DataObject(thread_list)

    threadObj.getAvgCountRecords()
    threadObj.getTotalEntries()
    threadObj.getFastest()
    threadObj.getSlowest()
    threadObj.getMaxDuration()
    threadObj.getMinDuration()
    threadObj.getOutliers()

def analyzeRandom(thread_list):
    rand_list = []
    randObj = DataObject.DataObject(rand_list)

    for thread in thread_list:
        rand_list.append(thread.getRandomNumbers())

    print("\nRandom numbers generated from", randObj.min_minimum(), "to", randObj.max_maximum())

    # FIXME start here

    # # Sort randomly generated numbers
    # while True:
    #     sorted_list_print = input("Print sorted list of randomly generated numbers? Yes or no: ")
    #     if sorted_list_print.lower() == "yes":
    #         list_formatted = ["{:e}".format(elem) for elem in thread_list.randomNumbers]
    #         print("The randomly generated numbers sorted from smallest to largest are:\t",
    #               *sorted(list_formatted), sep='\n\t')
    #         break
    #     elif sorted_list_print.lower() == "no":
    #         break
    #     else:
    #         print("Response not recognized, try again.")
