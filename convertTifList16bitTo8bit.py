"""
Daniel Walther
creation date (dd.mm.yyyy): 28.09.2023

purpose: convert a list of tif images (file paths) from type uint16 to uint8 and export to new files with suffix "uint8" or similar.
"""


import numpy as np

import files
import fileHandling as fH


def convertTifList16bitTo8bit(file_paths: list):
    pass


if __name__ == "__main__":

    fs = files.Filestream(input_extension=".tif")
    print(fs.__str__())

    exit()
