import datetime

import numpy as np
import tabulate
from tabulate import tabulate

from DataObject import DataObject


class DataThread(DataObject):
#     # def add_thread_metrics(self, arr, n, arr_set, data, arr_ranges, arr_records, arr_durations):
#     #     # Metrics per thread
#     #     data.append(["{:e}".format(arr_set[n]), self.len(),
#     #                  datetime.datetime.fromtimestamp(self.earliest_record()),
#     #                  datetime.datetime.fromtimestamp(self.latest_record())])
#     #
#     #     # Metrics about all threads
#     #     arr_ranges.append(self.range())
#     #     arr_records.append(self.len())
#     #     arr_durations.append(self.range())
#
#     def separate_threads(self, unix_list):
#         arr_set = sorted(set(self.mylist))
#         unique_arr_count = len(arr_set)
#
#         data = []
#         arr_ranges = []
#         arr_records = []
#         arr_durations = []
#
#         # Separating the timestamps by unique thread ID
#         for ele_base in range(0, len(arr_set)):  # For each distinct thread
#             unix_per_arr_list = []
#             test_arr = arr_set[ele_base]
#             for ele_test in range(0, len(self.mylist)):  # Go through the thread list and find the time values for each
#                 if self.mylist[ele_test] == test_arr:
#                     unix_per_arr_list.append(
#                         unix_list[ele_test])  # Add all of the timestamps for that thread to a list
#             arr = np.array(unix_per_arr_list)
#
#             self.add_thread_metrics(arr, ele_base, arr_set, data, arr_ranges, arr_records, arr_durations)
#
#         avg_per_period = sum(arr_records) / unique_arr_count
#
#         return arr_set, unique_arr_count, data, arr_ranges, arr_records, arr_durations, avg_per_period


    def output_thread_metrics(self, unix_list):
        thread_set, unique_threads, thread_data, threads_ranges, threads_records, threads_durations = self.separate_threads(
            unix_list)[0:6]
        avg_records_per_thread = sum(threads_records) / unique_threads
        print("Number of unique thread values generated: ", unique_threads)

        # Output table for metrics per thread
        headers_list = ["Thread", "Number of Records", "Earliest Record", "Latest Record"]
        print("\n")
        print(tabulate(thread_data, headers=headers_list, floatfmt=("e", "", "", "")))

        fastest_value = max(threads_records)
        fastest_index = threads_records.index(fastest_value)
        slowest_value = min(threads_records)
        slowest_index = threads_records.index(slowest_value)

        greatest_diff_value = max(threads_ranges)
        greatest_diff_index = threads_ranges.index(greatest_diff_value)
        least_diff_value = min(threads_ranges)
        least_diff_index = threads_ranges.index(least_diff_value)

        print("\nAverage numbers of records per thread:", "{:.2f}".format(avg_records_per_thread))
        print("Fastest thread:", "{:e}".format(thread_set[fastest_index]), "with", fastest_value, "records")
        print("Slowest thread:", "{:e}".format(thread_set[slowest_index]), "with", slowest_value, "records")
        print("Greatest difference in timestamps per thread: Thread {:e}, time range {} seconds".format(
            thread_set[greatest_diff_index], greatest_diff_value))
        print("Least difference in timestamps per thread: Thread {:e}, time range {} seconds".format(
            thread_set[least_diff_index], least_diff_value))
