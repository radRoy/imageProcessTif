"""
Read in two binary mask .tif stacks of same size (with file path dialogs or testing without),
calculate the Intersection over Union (IoU) between them,
write IoU to a text file next to the segmentation file, alongside some additional info (date, time, input file paths).
If the output file already exists, its existing contents are not overwritten but appended to with the new results.

This script works as intended.

creation date (dd.mm.yyyy): 15.02.2024
Daniel Walther
"""


import os
import datetime
import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np

import fileHandling as fH


def intersection_over_union(label, segmentation):

    print(f"\nThe function {intersection_over_union.__name__} was called. 'label' and 'segmentation' order does not matter, fyi.")

    intersection = cv2.bitwise_and(label, segmentation)
    union = cv2.bitwise_or(label, segmentation)

    i_unique = np.unique(intersection)  # [0 255]
    u_unique = np.unique(union)  # [0 255]
    if len(i_unique) > 2:
        print("\nError: Intersection is not a binary mask (more than 2 unique values found), unique values:\n", i_unique)
        exit(1)
    if len(u_unique) > 2:
        print("\nError: Union is not a binary mask (more than 2 unique values found), unique values:\n", u_unique)
        exit(1)

    count_intersection = np.count_nonzero(intersection)
    count_union = np.count_nonzero(union)
    iou = count_intersection / count_union
    print("\nIoU (sample images: model chpt-240204-0, best checkpoint):\n ", iou)  # 0.8382330306295214

    return iou


def main(path_label="", path_segmentation="", custom_input=False):

    # label & segmentation image file handling in case where no file paths were given

    if custom_input:
        # This puts the tkinter dialog window (for choosing inputs etc.) on top of other windows.
        window = tk.Tk()
        window.wm_attributes('-topmost', 1)
        window.withdraw()  # this suppresses the tk window
        path_label = filedialog.askopenfilename(title="Choose the binary mask label .tif file")
        path_segmentation = filedialog.askopenfilename(title="Choose the binary mask segmentation .tif file")

    # label image file handling in case where no file path was given

    if not path_label:
        path_label = 'sample images/id01 input label.tif'
        print(f"Using sample images since no path provided: {path_label=}")
    if os.path.isfile(path_label):
        label = fH.read_tif_stack(path_label)
        fH.print_file_properties(path_label)  # zyx
    else:
        print("\nFile", path_label, "does not exist.")
        exit(1)

    # segmentation image file handling in case where no file path was given

    if not path_segmentation:
        path_segmentation = 'sample images/chpt-240204-0 dataset10.b.0 - 3D_nuclei eye autofluo - best - id01 - Otsu 0.25.tif'
        print(f"Using sample images since no path provided: {path_segmentation=}")
    if os.path.isfile(path_segmentation):
        segmentation = fH.read_tif_stack(path_segmentation)
        fH.print_file_properties(path_segmentation)  # zyx
    else:
        print("\nFile", path_segmentation, "does not exist.")
        exit(1)

    # handling image shape exception

    if label.shape != segmentation.shape:
        print("\nError: Label and segmentation images must have the same shape (dimension shape & length) but they do not:")
        print(f" label.shape", label.shape)
        print(f" segmentation.shape", segmentation.shape)

    # IoU calculation

    iou = intersection_over_union(label=label, segmentation=segmentation)  # 'label' and 'segmentation' can be switched in order. Does not matter for this metric (commutative or so).

    # saving the result to a file next to the segmentation input file

    parent = fH.extract_parent_path(path_segmentation)  # absolute path with slashes, trailing slash
    output_iou = f"{parent}iou.txt"
    print(f"Writing to a .txt file next to the segmentation file: {output_iou=}")
    with open(output_iou, "a", encoding="utf-8") as f:
        f.writelines(f"{datetime.datetime.now()}\n")  # enter date
        f.writelines(f"{path_label=}\n")  # enter label file path
        f.writelines(f"{path_segmentation=}\n")  # enter segmentation file path
        f.writelines(f"{iou=}\n")  # enter iou
        f.writelines("\n")  # end with a newline (adds an empty line as separator between entries, should the same iou.txt file be written into multiple times)

    return 0


if __name__ == "__main__":

    main(custom_input=True)
