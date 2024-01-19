"""
Daniel Walther
creation date (dd.mm.yyyy): 19.01.2024
purpose: Read in files, assume they have their class label name suffixed at the very end of the filename,
    determine class balance (equal number of images per class per specimen id),
    randomise selection of majority class files,
    copy only the selected files to another folder without changing anything about the files, including name.
intended use case: dataset10 creation, preparing sliced, class balanced 2dunet training images

links:
- https://docs.python.org/3/library/shutil.html "The shutil module offers a number of high-level operations on files and collections of files. In particular, functions are provided which support file copying and removal. For operations on individual files, see also the os module."
"""


import os  # https://docs.python.org/3.10/library/os.html#os.chdir
from pathlib import Path  # https://docs.python.org/3/library/pathlib.html
import tkinter as tk
import numpy as np
print(f"This script's path: {__file__}"); wd = Path(__file__).parent.absolute().parent.absolute(); os.chdir(wd); print(f"Setting working dir (parent dir of my git repos): {Path(__file__).parent.absolute().parent.absolute()}")
from imageProcessTif import fileHandling as fH


def main(extension_in):

    # FILE HANDLING

    file_paths = fH.get_string_list_filtered_by_wanted_ending(
        fH.get_file_path_list(), extension_in)
    files = fH.get_string_list_filtered_by_wanted_ending(
        fH.get_file_list(
            fH.extract_parent_path(file_paths[0])), extension_in)
    print(f"files and file paths are equally long: {len(files) == len(file_paths)}")
    correspondance_files_paths = []
    for file, path in zip(np.array(files), np.array(file_paths)):
        correspondance_files_paths.append(file in path)
    print(f"Input files and file paths need to be sorted: {False in correspondance_files_paths}")

    output_dir = fH.get_folder_path_dialog("Choose output dir")

    print(f"\ninput folder: {fH.extract_parent_path(file_paths[0])}\noutput folder: {output_dir}")

    # OPERATIONS

    # exploring The filenames for sections of easy processing
    l = [x.split("-") for x in [fH.exclude_extension_from_filename(file)[0] for file in files]]
    # fH.iterate_function_args_over_iterable(print, l)  # [ROI no. (alphabetic > slice), class label] elements are str
    # print(len(l) == len(files) == len(file_paths))  # True
    trios = [(substrings[0], substrings[-2], substrings[-1]) for substrings in l]
    # fH.iterate_function_args_over_iterable(print, trios)  # [(id, slice, class), ...], strings
    correspondance_trios_files = []
    for trio, file in zip(np.array(trios), np.array(files)):
        correspondance_trios_files.append([])
        for x in trio:
            correspondance_trios_files[-1].append(x in file)
    print(f"Sorting needed for trios and files: {False in correspondance_trios_files}")

    pass


if __name__ == "__main__":

    # This puts the tkinter dialog window (for choosing inputs etc.) on top of other windows.
    window = tk.Tk()
    window.wm_attributes('-topmost', 1)
    window.withdraw()  # this suppresses the tk window

    # actual work
    main(".tif")
