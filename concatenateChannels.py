"""
This file is for concatenating multiple (autofluorescence) channels in tif format, so that the multiple individual
(single channel) tif files from one specimen form a single RGB-like tif file containing Channel, X, Y, and Z information
instead of just X, Y, and Z, like the single channel images.

Author: Daniel Walther
creation date: 2023.08.18
"""


import tkinter as tk
import fileHandling as fH
import numpy as np


def extract_specimen_ids_from_single_channel_paths(single_channel_paths: list):

    specimen_ids = []

    for i, single_channel_path in enumerate(single_channel_paths):
        # print('\n', i, single_channel_path)
        file = single_channel_path.split('/')[-1]  # assumes that single_channel_path is a file path
        # print(file)

        specimen_id = file.split('-')[0]  # assumes the filename starts with 'id' (i.e., contains 'id<xy>' in the first '-' delimited segment).
        # print(specimen_id)
        specimen_ids.append(specimen_id)

    return specimen_ids


def get_file_paths_grouped_by_specimen_id(single_channel_paths: list, a_specimen_ids_unique: np.ndarray):

    grouped_specimen_file_paths = []

    for i, specimen_id in enumerate(a_specimen_ids_unique):
        grouped_specimen_file_paths.append([])
        for file_path in single_channel_paths:
            if specimen_id in file_path:
                grouped_specimen_file_paths[i].append(file_path)

    return grouped_specimen_file_paths


if __name__ == '__main__':

    # INFO: when commenting: files, file paths, etc. are always with extension except when stated otherwise

    # This is supposed to put the tkinter dialog window (for choosing inputs etc.) on top of other windows (I think it works but is buggy).
    window = tk.Tk()
    window.wm_attributes('-topmost', 1)
    window.withdraw()  # this suppresses the tk window

    # get the file path list of the processed autofluorescence single channel tif images
    #file_paths = fH.get_file_path_list( path=fH.get_folder_path_dialog( window_title="Choose folder with single channel images to concatenate"))
    single_channel_paths = fH.get_file_path_list()  # assumes

    specimen_ids = extract_specimen_ids_from_single_channel_paths(single_channel_paths)

    #print(specimen_ids)
    a_specimen_ids = np.array(specimen_ids)
    a_specimen_ids_unique = np.unique(a_specimen_ids)
    #print(len(a_specimen_ids), a_specimen_ids)
    #print(len(a_specimen_ids_unique), a_specimen_ids_unique)

    # creates a list of n_specimens lists, each to be filled with a specimen's corresponding file path.
    grouped_specimen_file_paths = get_file_paths_grouped_by_specimen_id(single_channel_paths, a_specimen_ids_unique)
    print(np.array(grouped_specimen_file_paths).shape)
    print(np.array(grouped_specimen_file_paths))

    exit(0)
