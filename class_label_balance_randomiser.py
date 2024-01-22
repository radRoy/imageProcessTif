"""
Daniel Walther
creation date (dd.mm.yyyy): 19.01.2024
purpose: Read in files, assume they have their class label name suffixed at the very end of the filename,
    determine class balance (equal number of images per class per specimen id),
    randomise selection of majority class files,
    copy only the selected files to another folder without changing anything about the files, including name.
intended use case: dataset10 creation, preparing sliced, class balanced 2dunet training images

state: - UNFINISHED -
    another time another day. can do it faster the dirty easy way. way faster.

links:
- https://docs.python.org/3/library/shutil.html "The shutil module offers a number of high-level operations on files and collections of files. In particular, functions are provided which support file copying and removal. For operations on individual files, see also the os module."
"""


import os  # https://docs.python.org/3.10/library/os.html#os.chdir
from pathlib import Path  # https://docs.python.org/3/library/pathlib.html
import tkinter as tk
import numpy as np
# print(f"This script's path: {__file__}"); wd = Path(__file__).parent.absolute().parent.absolute(); os.chdir(wd); print(f"Setting working dir (parent dir of my git repos): {Path(__file__).parent.absolute().parent.absolute()}")
from imageProcessTif import fileHandling as fH


def class_balance_counter():
    """another time another day. can do it faster the dirty easy way. way faster."""

    pass


def class_label_balance_randomiser(files, file_paths, output_dir):

    # exploring The filenames for sections of easy processing
    l = [x.split("-") for x in [fH.exclude_extension_from_filename(file)[0] for file in files]]
    # fH.iterate_function_args_over_iterable(print, l)  # [ROI no. (roi name alphabetic alphabetic > slice ascending), class label] elements are str
    # print(len(l) == len(files) == len(file_paths))  # True
    trios = [(substrings[0], substrings[-2], substrings[-1]) for substrings in l]
    # fH.iterate_function_args_over_iterable(print, trios)  # [(id, roi, class), ...], strings
    correspondence_trios_files = []
    for trio, file in zip(np.array(trios), np.array(files)):
        correspondence_trios_files.append([])
        for x in trio:
            correspondence_trios_files[-1].append(x in file)
    print(f"Elements between trios and files are ordered correspondingly: {False not in correspondence_trios_files}")

    # extracting [id, roi, class] trios from the file name fragments
    trios = np.array(trios)

    # indexing all trios
    trios_indexed = []
    for i_image, trio in enumerate(trios):
        trios_indexed.append([i_image, trio[1], trio[2]])

    # create dictionary of form {id: [[trio], [trio], ...], id: [[trio], [trio], ...], ...}
    unique_ids = np.unique(trios[:, 0])  # ['id01' 'id02' 'id03' 'id04' 'id05' 'id06' 'id07']
    unique_ids_with_trios_indexed = {}
    for id in unique_ids:
        unique_ids_with_trios_indexed[id] = [trio_indexed for trio, trio_indexed in zip(trios, trios_indexed) if id in trio]

    output = unique_ids_with_trios_indexed
    return output


def main(extension_in):

    # FILE HANDLING

    file_paths = fH.get_string_list_filtered_by_wanted_ending(
        fH.get_file_path_list(), extension_in)
    files = fH.get_string_list_filtered_by_wanted_ending(
        fH.get_file_list(
            fH.extract_parent_path(file_paths[0])), extension_in)
    print(f"files and file paths are equally long: {len(files) == len(file_paths)}")
    correspondence_files_paths = []
    for file, path in zip(np.array(files), np.array(file_paths)):
        correspondence_files_paths.append(file in path)
    print(f"Elements between files and file paths are ordered correspondingly: {False not in correspondence_files_paths}")

    output_dir = fH.get_folder_path_dialog("Choose output dir")

    print(f"\ninput folder: {fH.extract_parent_path(file_paths[0])}\noutput folder: {output_dir}")

    # OPERATIONS

    class_label_balance_randomiser(files, file_paths, output_dir)

    pass


if __name__ == "__main__":

    # This puts the tkinter dialog window (for choosing inputs etc.) on top of other windows.
    window = tk.Tk()
    window.wm_attributes('-topmost', 1)
    window.withdraw()  # this suppresses the tk window

    # actual work
    # main(".tif")

    # testing until script is written

    files = [
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-1-unlabeled.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-10-eye.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-11-eye.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-12-eye.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-13-eye.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-14-eye.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-15-eye.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-16-unlabeled.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-17-unlabeled.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-18-unlabeled.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-2-unlabeled.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-3-unlabeled.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-4-unlabeled.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-5-unlabeled.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-6-unlabeled.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-7-unlabeled.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-8-eye.tif',
        'id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-9-eye.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-1-unlabeled.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-10-eye.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-11-unlabeled.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-12-unlabeled.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-13-unlabeled.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-14-unlabeled.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-15-unlabeled.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-16-eye.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-17-eye.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-18-eye.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-19-unlabeled.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-2-unlabeled.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-3-unlabeled.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-4-unlabeled.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-5-unlabeled.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-6-unlabeled.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-7-unlabeled.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-8-eye.tif',
        'id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-9-eye.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-1-unlabeled.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-10-eye.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-11-unlabeled.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-12-unlabeled.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-13-unlabeled.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-14-unlabeled.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-15-unlabeled.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-16-eye.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-17-eye.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-18-eye.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-19-eye.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-2-unlabeled.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-3-unlabeled.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-4-unlabeled.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-5-unlabeled.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-6-unlabeled.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-7-eye.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-8-eye.tif',
        'id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-9-eye.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-1-unlabeled.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-10-eye.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-11-eye.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-12-unlabeled.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-13-unlabeled.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-14-unlabeled.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-15-unlabeled.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-16-unlabeled.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-17-unlabeled.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-18-eye.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-19-eye.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-2-unlabeled.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-20-eye.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-21-unlabeled.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-3-unlabeled.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-4-unlabeled.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-5-unlabeled.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-6-unlabeled.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-7-unlabeled.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-8-unlabeled.tif',
        'id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-9-eye.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-1-unlabeled.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-10-unlabeled.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-11-unlabeled.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-12-unlabeled.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-13-unlabeled.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-14-eye.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-15-eye.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-16-eye.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-17-unlabeled.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-18-unlabeled.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-2-unlabeled.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-3-unlabeled.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-4-unlabeled.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-5-eye.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-6-eye.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-7-eye.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-8-eye.tif',
        'id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-9-unlabeled.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-1-unlabeled.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-10-unlabeled.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-11-unlabeled.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-12-unlabeled.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-13-eye.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-14-eye.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-15-eye.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-16-unlabeled.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-17-unlabeled.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-18-unlabeled.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-2-unlabeled.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-3-unlabeled.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-4-eye.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-5-eye.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-6-eye.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-7-unlabeled.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-8-unlabeled.tif',
        'id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-9-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-1-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-10-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-11-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-12-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-13-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-14-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-15-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-16-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-17-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-18-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-19-eye.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-2-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-20-eye.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-21-eye.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-22-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-23-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-3-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-4-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-5-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-6-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-7-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-8-unlabeled.tif',
        'id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-9-unlabeled.tif']
    file_paths = ['Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-1-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-10-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-11-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-12-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-13-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-14-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-15-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-16-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-17-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-18-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-2-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-3-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-4-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-5-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-6-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-7-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-8-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id01-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-9-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-1-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-10-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-11-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-12-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-13-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-14-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-15-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-16-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-17-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-18-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-19-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-2-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-3-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-4-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-5-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-6-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-7-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-8-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id02-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-9-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-1-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-10-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-11-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-12-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-13-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-14-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-15-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-16-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-17-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-18-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-19-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-2-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-3-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-4-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-5-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-6-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-7-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-8-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id03-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-9-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-1-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-10-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-11-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-12-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-13-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-14-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-15-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-16-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-17-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-18-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-19-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-2-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-20-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-21-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-3-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-4-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-5-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-6-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-7-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-8-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id04-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-9-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-1-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-10-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-11-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-12-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-13-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-14-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-15-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-16-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-17-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-18-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-2-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-3-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-4-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-5-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-6-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-7-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-8-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id05-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-9-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-1-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-10-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-11-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-12-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-13-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-14-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-15-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-16-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-17-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-18-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-2-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-3-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-4-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-5-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-6-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-7-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-8-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id06-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-9-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-1-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-10-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-11-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-12-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-13-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-14-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-15-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-16-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-17-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-18-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-19-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-2-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-20-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-21-eye.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-22-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-23-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-3-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-4-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-5-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-6-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-7-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-8-unlabeled.tif',
 'Y:/Users/DWalther/Microscopy/dataset10/labels_preprocessed-substack-0.1_sampling-refined-sliced/id07-Ch638nm-bicubic-scaled-0.3458z-0.1469y-0.1469x-fluo-eye-Otsu_auto-overlay-labels_preprocessed-substack-0.1_sampling-refined-slice-9-unlabeled.tif']
    output_dir = '/Users/DWalther/Documents'
    output = class_label_balance_randomiser(files, file_paths, output_dir)
    for id in output:
        print(f"\n{id}\n{output[id]}")
