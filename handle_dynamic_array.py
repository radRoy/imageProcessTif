"""
pseudocode
author: daniel walther
creation date: 11.07.2023
"""


import numpy as np


def handle_dynamic_array_rec(a, i=0):

    l = []
    #print(f" rec depth: {i}, input array:\n{a}")

    if len(a.shape) > 1:
        print("if")
        for a_sub in a:
            l.append(handle_dynamic_array_rec(a_sub, i+1))

    # this needs some work, still... must return partial array so that every subarray eventually reaches 1-dimensionality
    #a += 1
    else:
        print("else")
        a += i+1
        for element in a:
            l.append(element)
    return l


if __name__ == "__main__":

    a_test = np.zeros((3,3,2))
    print(f"test array:\n{a_test}")

    list_out = handle_dynamic_array_rec(a_test)
    print(f"type: {type(list_out)}, list out:\n{list_out}")
    exit(0)
