"""
This file is for concatenating multiple (autofluorescence) channels in tif format, so that the multiple individual
(single channel) tif files from one specimen form a single RGB-like tif file containing Channel, X, Y, and Z information
instead of just X, Y, and Z, like the single channel images.

Author: Daniel Walther
creation date: 2023.08.18
"""


import fileHandling as fH
import numpy as np


def sort_tifs_by_specimen(*args):
    # TBD: same as below TBD

    pass  # some list of specimen specific file path lists, probably


def concatenate_tifs(*args):
    # TBD: determine the best way of giving the input images to this function

    pass


if __name__ == '__main__':

    exit(0)
