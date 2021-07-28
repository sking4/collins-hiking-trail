from __future__ import print_function
import argparse
from gather_data import gather_data, create_analysis_objects
from list_set import analyzeThreadStats, analyzeRandom, outputThreadStatsTable
from my_functions import print_table_function
from plotting import plotting


def collect_filename():
    parser = argparse.ArgumentParser(description='Process file name')
    parser.add_argument('file_path',
                        nargs='?',
                        type=str,
                        default=r"C:\Users\sking4\OneDrive - Raytheon Technologies\Python\AryehData.csv")
    p = parser.parse_args()
    file_path = p.file_path
    return file_path


def main():
    # Gather file path, either from command line or from user input
    file_path = collect_filename()

    # Open file and process data
    # thread_list is a matrix with a list of all the unique thread IDs and
    # each of those holding the data for the corresponding thread
    # (timestamp and random number for each occurrence of that thread)
    thread_list = gather_data(file_path)

    # Print the pretty table if you want it
    thread_stats_table, headers_list = outputThreadStatsTable(thread_list)
    print_table_function(thread_stats_table, headers_list)

    # ao is the Analysis Object containing all of the timestamp and thread ID information for each ThreadObject
    ao_time, ao_random = create_analysis_objects(thread_list)

    # Analyze the thread time data collected
    analyzeThreadStats(ao_time)

    # Analyze the random numbers
    analyzeRandom(ao_random)

    # Plot stuff
    plotting(thread_list)


if __name__ == '__main__':
    main()
