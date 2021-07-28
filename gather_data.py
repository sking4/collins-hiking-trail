import csv
import thread_records
from data_object import ThreadObject, AnalysisObject


def gather_data(file_path):
    thread_records_list = []
    with open(str(file_path), 'r+') as csv_file:
        # Read data and separate into lists
        csv_read = csv.reader(csv_file)
        for row in csv_read:  # for each line in the csv file [timestamp, thread ID, random number]
            try:
                foundThread = False
                for threadObj in thread_records_list:  # for a unique thread that has already been added to the thread_list
                    if float(row[1]) == threadObj.getThreadID():  # if the thread ID for the line in the CSV file equals
                        # the unique thread ID in question
                        threadObj.appendEntry(float(row[0]), row[2])  # add the timestamp and random number information
                        # to a list of data specific to that unique thread ID
                        foundThread = True
                        break
                if not foundThread:  # if the line from the CSV file has a thread ID not already captured by the list
                    # of unique thread IDs
                    thread_records_list.append(
                        thread_records.ThreadRecords(float(row[1]), [(float(row[0]), row[2])]))  # add
                    # that thread ID to the unique list, as well as its timestamp and random number info
            except:
                next(csv_read)
    return thread_records_list


def create_analysis_objects(thread_list):
    # Create data object for each thread in thread_list
    thread_object_list = []
    for thread in thread_list:
        # Each ThreadObject is an object containing a thread ID, and all of the timestamps and random numbers
        # associated with that thread ID
        thread_object_list.append(ThreadObject(thread.getThreadID(),
                                               thread.getTimestamps(),
                                               thread.getRandomNumbers()))
    # ao is the Analysis Object containing all of the timestamp and thread ID information for each ThreadObject

    ao_time = AnalysisObject([(threadObject.timeObjects, threadObject.threadID) for threadObject in thread_object_list])
    ao_random = AnalysisObject([(threadObject.randObjects, threadObject.threadID) for threadObject in thread_object_list])
    return ao_time, ao_random
