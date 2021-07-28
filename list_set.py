import datetime
import data_object


def outputThreadStatsTable(thread_list): #FIXME where does this go?
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


def analyzeThreadStats(ao):
    print("\nNumber of threads: ", ao.getNumThreads())
    print("Total entries: ", ao.getTotalEntries())
    print("Average number of records per thread:", "{:.2f}".format(ao.getAvgCountRecords()))

    most_records_list, most_records_value = ao.getMostRecords()
    print("Most records returned by thread(s)", most_records_list, "with", most_records_value, "records")

    least_records_list, least_records_value = ao.getLeastRecords()
    print("Fewest records returned by thread(s)", least_records_list, "with", least_records_value, "records")

    fastest_list, fastest_value = ao.getFastest()
    print("Fastest thread(s): Thread(s)", fastest_list, "with", fastest_value, "records per second")

    slowest_list, slowest_value = ao.getSlowest()
    print("Slowest thread(s): Thread(s)", slowest_list, "with", slowest_value, "records per second")

    max_duration_list, max_duration_value = ao.getMaxDuration()
    print("Greatest difference in timestamps per thread: Thread(s) {}, time range {} seconds".format(
        max_duration_list, max_duration_value))

    min_duration_list, min_duration_value = ao.getMinDuration()
    print("Least difference in timestamps per thread: Thread(s) {}, time range {} seconds".format(
        min_duration_list, min_duration_value))

    duration_outlier_list, count_outlier_list = ao.getOutliers()
    print("\nOutlier thread(s): ")
    print("\tDuration outliers:")
    for outlier in duration_outlier_list:
        print("\t\tThread", outlier[1],
              "died after", outlier[0],
              "seconds at", datetime.datetime.fromtimestamp(outlier[2]))
    print("\tRecord count outliers:")
    for outlier in count_outlier_list:
        print("\t\tThread", outlier[1],
              "has ", outlier[0],
              "records.")


def analyzeRandom(ao):
    print("\nRandom numbers generated from", ao.min(), "to", ao.max(), "\n")

