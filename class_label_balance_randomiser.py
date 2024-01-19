"""
Daniel Walther
creation date (dd.mm.yyyy): 19.01.2024
purpose: Read in files, assume they have their class label name suffixed at the very end of the filename,
    determine class balance (equal number of images per class per specimen id),
    randomise selection of majority class files,
    copy only the selected files to another folder without changing anything about the files, including name.
intended use case: dataset10 creation, preparing sliced, class balanced 2dunet training images
"""


import os  # https://docs.python.org/3.10/library/os.html#os.chdir
from pathlib import Path  # https://docs.python.org/3/library/pathlib.html


import tkinter as tk
import numpy as np


#from imageProcessTif import fileHandling as fH


if __name__ == "__main__":
    print("program is running.")

    # tkinter init stuff

    # set wd dynamically (i.e., with symlink to parent folders of this file. My git repos should be organised the same way in relation to each other)
    print(f"This script's path: {__file__}")
    wd = Path(__file__).parent.absolute().parent.absolute()
    os.chdir(wd)
    print(f"Setting working dir (parent dir of my git repos): {Path(__file__).parent.absolute().parent.absolute()}")
