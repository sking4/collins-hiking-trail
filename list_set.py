import datetime
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
import data_object


def outputThreadStatsTable(thread_list):
    thread_stats_table = []
    headers_list = ["Thread", "Number of Records", "Earliest Record", "Latest Record", "Duration"]
    for thread in thread_list:  # for each unique thread ID
        # Add that thread's info to the master table
        thread_stats_table.append([thread.getThreadID(),
                                   len(thread.getTimestamps()),
                                   datetime.datetime.fromtimestamp(data_object.DataObject(thread.getTimestamps()).minimum()),
                                   datetime.datetime.fromtimestamp(data_object.DataObject(thread.getTimestamps()).maximum()),
                                   data_object.DataObject(thread.getTimestamps()).range()])
    return thread_stats_table, headers_list


def analyzeThreadStats(thread_list):
    thread_stats_table, headers_list = outputThreadStatsTable(thread_list)
    print("\n", tabulate(thread_stats_table, headers=headers_list, floatfmt=("", "", "", "", "")),
          "\n")  # Print out the pretty table

    threadObj = data_object.DataObject(thread_list)

    threadObj.getAvgCountRecords()
    threadObj.getTotalEntries()
    threadObj.getFastest()
    threadObj.getSlowest()
    threadObj.getMaxDuration()
    threadObj.getMinDuration()
    threadObj.getOutliers()


def analyzeRandom(thread_list):
    rand_list = []
    randObj = data_object.DataObject(rand_list)

    for thread in thread_list:
        rand_list.append(thread.getRandomNumbers())

    print("\nRandom numbers generated from", randObj.min_minimum(), "to", randObj.max_maximum(), "\n")


def plotting(thread_list):
    plot_matrix = np.array(outputThreadStatsTable(thread_list)[0])
    threadID = plot_matrix[:, 0]
    duration = plot_matrix[:, 4]
    entry_count = plot_matrix[:, 1]

    plt.rcdefaults()
    fig, ax = plt.subplots(2)
    fig.tight_layout(pad=5)

    # Thread Deaths
    ax[0].scatter(duration, threadID)
    ax[0].set_xlabel('Duration (s)')
    ax[0].set_ylabel('Thread ID')
    ax[0].set_title('Thread Deaths')

    # Entries Per Thread
    ax[1].scatter(entry_count, threadID)
    ax[1].set_xlabel('Number of Entries')
    ax[1].set_ylabel('Thread ID')
    ax[1].set_title('Entry Count per Thread')

    # plot1 = plt.figure(1)  # Thread value over time
    # plt.plot(time, threads)
    # plt.title("Thread ID Over Time")
    # plt.xlabel("Time (s)")
    # plt.ylabel("Thread ID")
    #
    # plot2 = plt.figure(2)  # Zoomed in thread value over time
    # plt.plot(time, threads)
    # x_min, x_max = time[int(len(time) / 4)], time[int(len(time) / 3)]
    # plt.xlim([x_min, x_max])
    # plt.title("Thread ID Over Time (Snippet)")
    # plt.xlabel("Time (s)")
    # plt.ylabel("Thread ID")
    #
    # plot3 = plt.figure(3)  # Random numbers generated over time
    # plt.plot(time, randnum)
    # plt.title("Random Numbers Over Time")
    # plt.xlabel("Time (s)")
    # plt.ylabel("Random Number")

    plt.show()
