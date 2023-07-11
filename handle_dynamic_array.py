"""
pseudocode
author: daniel walther
creation date: 11.07.2023
"""


import numpy as np


def handle_dynamic_array_rec(a):

    l = []

    if len(a.shape) > 1:
        for a_sub in a:
            l.append(handle_dynamic_array_rec(a_sub))

    # this needs some work, still... must return partial array so that every subarray eventually reaches 1-dimensionality
    return list(a)


if __name__ == "__main__":

    a_test = np.zeros((2,1,3))
    print(f"test array:\n{a_test}")

    list_out = handle_dynamic_array_rec(a_test)
    exit(0)
