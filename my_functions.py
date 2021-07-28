import numpy as np
import pandas as pd
from tabulate import tabulate


def mad_method_function(my_list, threshold):
    # MAD Method
    med = np.median(my_list)
    mad = pd.Series(my_list).mad()
    outlier_durations_list = []
    for v in my_list:
        t = np.abs((v - med) / mad)
        if t > threshold:
            outlier_durations_list.append((v,))
        else:
            continue
    return outlier_durations_list


def print_table_function(table_list, headers_list):
    print("\n", tabulate(table_list, headers=headers_list),
          "\n")  # Print out the pretty table
