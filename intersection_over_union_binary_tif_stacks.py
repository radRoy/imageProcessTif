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
import tkinter.messagebox
from tkinter import filedialog

import cv2
import numpy as np

import fileHandling as fH


def intersection_over_union(label, segmentation):

    print(f"\nThe function {intersection_over_union.__name__} was called. 'label' and 'segmentation' order matters.")

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


def get_iou_filename(iou, path_segmentation):
    parent = fH.extract_parent_path(path_segmentation)  # absolute path with slashes, trailing slash
    threshold_string = path_segmentation.split("-")[-1].strip(".tif").lstrip(" ")  # 'Otsu manual 0.25'
    return f"{parent}iou {iou} - {threshold_string}.txt"


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

    output_iou = get_iou_filename(iou, path_segmentation)
    print(f"Writing to a .txt file next to the segmentation file: {output_iou=}")
    with open(output_iou, "a", encoding="utf-8") as f:
        f.writelines(f"{datetime.datetime.now()}\n")  # enter date
        f.writelines(f"{path_label=}\n")  # enter label file path
        f.writelines(f"{path_segmentation=}\n")  # enter segmentation file path
        f.writelines(f"{iou=}\n")  # enter iou
        f.writelines("\n")  # end with a newline (adds an empty line as separator between entries, should the same iou.txt file be written into multiple times)

    return 0


if __name__ == "__main__":

    # main()  # testing
    while tkinter.messagebox.askokcancel("Calculate IoU with python", "Continue?"):
        main(custom_input=True)  # application

    """parent_label_0 = "Y:/Users/DWalther/unet DW/chpt-240124-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.4 (6 steps), patience 20 - good/chpt-240131-1 - last - good/"
    parent_segmentation_0 = parent_label_0
    label_0 = "id01 input label.tif"
    main(path_label=parent_label_0 + label_0,
         path_segmentation=parent_segmentation_0 + "chpt-240124-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.125.tif")
    main(path_label=parent_label_0 + label_0,
         path_segmentation=parent_segmentation_0 + "chpt-240124-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.25.tif")
    main(path_label=parent_label_0 + label_0,
         path_segmentation=parent_segmentation_0 + "chpt-240124-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.375.tif")
    main(path_label=parent_label_0 + label_0,
         path_segmentation=parent_segmentation_0 + "chpt-240124-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.5.tif")
    main(path_label=parent_label_0 + label_0,
         path_segmentation=parent_segmentation_0 + "chpt-240124-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.625.tif")
    main(path_label=parent_label_0 + label_0,
         path_segmentation=parent_segmentation_0 + "chpt-240124-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.75.tif")
    main(path_label=parent_label_0 + label_0,
         path_segmentation=parent_segmentation_0 + "chpt-240124-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.875.tif")

    parent_label_1 = "Y:/Users/DWalther/unet DW/chpt-240204-1 -O- dataset10.b.1 - 3D_nuclei eye autofluo - very good/240209-1 best/"
    parent_segmentation_1 = parent_label_1
    label_1 = "id06 input label.tif"
    parent_label_2 = "Y:/Users/DWalther/unet DW/chpt-240204-1 -O- dataset10.b.1 - 3D_nuclei eye autofluo - very good/240209-5 last/"
    parent_segmentation_2 = parent_label_2
    label_2 = "id06 input label.tif"
    parent_label_3 = "Y:/Users/DWalther/unet DW/chpt-240204-2 -O- dataset10.b.2 - 3D_nuclei eye autofluo - very good/240209-2 best/"
    parent_segmentation_3 = parent_label_3
    label_3 = "id05 input label.tif"
    parent_label_4 = "Y:/Users/DWalther/unet DW/chpt-240204-2 -O- dataset10.b.2 - 3D_nuclei eye autofluo - very good/240209-6 last/"
    parent_segmentation_4 = parent_label_4
    label_4 = "id05 input label.tif"
    parent_label_5 = "Y:/Users/DWalther/unet DW/chpt-240204-3 -O- dataset10.b.3 - 3D_nuclei eye autofluo - very good/240209-3 best/"
    parent_segmentation_5 = parent_label_5
    label_5 = "id07 input label.tif"
    parent_label_6 = "Y:/Users/DWalther/unet DW/chpt-240204-3 -O- dataset10.b.3 - 3D_nuclei eye autofluo - very good/240209-7 last/"
    parent_segmentation_6 = parent_label_6
    label_6 = "id07 input label.tif"
    main(path_label=parent_label_1 + label_1, path_segmentation=parent_segmentation_1 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - best - id06 - Otsu manual 0.125.tif")
    main(path_label=parent_label_1 + label_1, path_segmentation=parent_segmentation_1 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - best - id06 - Otsu manual 0.25.tif")
    main(path_label=parent_label_1 + label_1, path_segmentation=parent_segmentation_1 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - best - id06 - Otsu manual 0.375.tif")
    main(path_label=parent_label_1 + label_1, path_segmentation=parent_segmentation_1 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - best - id06 - Otsu manual 0.5.tif")
    main(path_label=parent_label_1 + label_1, path_segmentation=parent_segmentation_1 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - best - id06 - Otsu manual 0.625.tif")
    main(path_label=parent_label_1 + label_1, path_segmentation=parent_segmentation_1 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - best - id06 - Otsu manual 0.75.tif")
    main(path_label=parent_label_1 + label_1, path_segmentation=parent_segmentation_1 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - best - id06 - Otsu manual 0.875.tif")
    main(path_label=parent_label_2 + label_2, path_segmentation=parent_segmentation_2 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - last - id06 - Otsu manual 0.125.tif")
    main(path_label=parent_label_2 + label_2, path_segmentation=parent_segmentation_2 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - last - id06 - Otsu manual 0.25.tif")
    main(path_label=parent_label_2 + label_2, path_segmentation=parent_segmentation_2 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - last - id06 - Otsu manual 0.375.tif")
    main(path_label=parent_label_2 + label_2, path_segmentation=parent_segmentation_2 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - last - id06 - Otsu manual 0.5.tif")
    main(path_label=parent_label_2 + label_2, path_segmentation=parent_segmentation_2 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - last - id06 - Otsu manual 0.625.tif")
    main(path_label=parent_label_2 + label_2, path_segmentation=parent_segmentation_2 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - last - id06 - Otsu manual 0.75.tif")
    main(path_label=parent_label_2 + label_2, path_segmentation=parent_segmentation_2 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - last - id06 - Otsu manual 0.875.tif")
    main(path_label=parent_label_3 + label_3, path_segmentation=parent_segmentation_3 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - best - id05 - Otsu manual 0.125.tif")
    main(path_label=parent_label_3 + label_3, path_segmentation=parent_segmentation_3 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - best - id05 - Otsu manual 0.25.tif")
    main(path_label=parent_label_3 + label_3, path_segmentation=parent_segmentation_3 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - best - id05 - Otsu manual 0.375.tif")
    main(path_label=parent_label_3 + label_3, path_segmentation=parent_segmentation_3 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - best - id05 - Otsu manual 0.5.tif")
    main(path_label=parent_label_3 + label_3, path_segmentation=parent_segmentation_3 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - best - id05 - Otsu manual 0.625.tif")
    main(path_label=parent_label_3 + label_3, path_segmentation=parent_segmentation_3 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - best - id05 - Otsu manual 0.75.tif")
    main(path_label=parent_label_3 + label_3, path_segmentation=parent_segmentation_3 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - best - id05 - Otsu manual 0.875.tif")
    main(path_label=parent_label_4 + label_4, path_segmentation=parent_segmentation_4 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - last - id05 - Otsu manual 0.125.tif")
    main(path_label=parent_label_4 + label_4, path_segmentation=parent_segmentation_4 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - last - id05 - Otsu manual 0.25.tif")
    main(path_label=parent_label_4 + label_4, path_segmentation=parent_segmentation_4 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - last - id05 - Otsu manual 0.375.tif")
    main(path_label=parent_label_4 + label_4, path_segmentation=parent_segmentation_4 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - last - id05 - Otsu manual 0.5.tif")
    main(path_label=parent_label_4 + label_4, path_segmentation=parent_segmentation_4 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - last - id05 - Otsu manual 0.625.tif")
    main(path_label=parent_label_4 + label_4, path_segmentation=parent_segmentation_4 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - last - id05 - Otsu manual 0.75.tif")
    main(path_label=parent_label_4 + label_4, path_segmentation=parent_segmentation_4 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - last - id05 - Otsu manual 0.875.tif")
    main(path_label=parent_label_5 + label_5, path_segmentation=parent_segmentation_5 + "chpt-240204-3 dataset10.b.3 - 3D_nuclei eye autofluo - best - id07 - Otsu manual 0.125.tif")
    main(path_label=parent_label_5 + label_5, path_segmentation=parent_segmentation_5 + "chpt-240204-3 dataset10.b.3 - 3D_nuclei eye autofluo - best - id07 - Otsu manual 0.25.tif")
    main(path_label=parent_label_5 + label_5, path_segmentation=parent_segmentation_5 + "chpt-240204-3 dataset10.b.3 - 3D_nuclei eye autofluo - best - id07 - Otsu manual 0.375.tif")
    main(path_label=parent_label_5 + label_5, path_segmentation=parent_segmentation_5 + "chpt-240204-3 dataset10.b.3 - 3D_nuclei eye autofluo - best - id07 - Otsu manual 0.5.tif")
    main(path_label=parent_label_5 + label_5, path_segmentation=parent_segmentation_5 + "chpt-240204-3 dataset10.b.3 - 3D_nuclei eye autofluo - best - id07 - Otsu manual 0.625.tif")
    main(path_label=parent_label_5 + label_5, path_segmentation=parent_segmentation_5 + "chpt-240204-3 dataset10.b.3 - 3D_nuclei eye autofluo - best - id07 - Otsu manual 0.75.tif")
    main(path_label=parent_label_5 + label_5, path_segmentation=parent_segmentation_5 + "chpt-240204-3 dataset10.b.3 - 3D_nuclei eye autofluo - best - id07 - Otsu manual 0.875.tif")
    main(path_label=parent_label_6 + label_6, path_segmentation=parent_segmentation_6 + "chpt-240204-3 dataset10.b.3 - 3D_nuclei eye autofluo - last - id07 - Otsu manual 0.125.tif")
    main(path_label=parent_label_6 + label_6, path_segmentation=parent_segmentation_6 + "chpt-240204-3 dataset10.b.3 - 3D_nuclei eye autofluo - last - id07 - Otsu manual 0.25.tif")
    main(path_label=parent_label_6 + label_6, path_segmentation=parent_segmentation_6 + "chpt-240204-3 dataset10.b.3 - 3D_nuclei eye autofluo - last - id07 - Otsu manual 0.375.tif")
    main(path_label=parent_label_6 + label_6, path_segmentation=parent_segmentation_6 + "chpt-240204-3 dataset10.b.3 - 3D_nuclei eye autofluo - last - id07 - Otsu manual 0.5.tif")
    main(path_label=parent_label_6 + label_6, path_segmentation=parent_segmentation_6 + "chpt-240204-3 dataset10.b.3 - 3D_nuclei eye autofluo - last - id07 - Otsu manual 0.625.tif")
    main(path_label=parent_label_6 + label_6, path_segmentation=parent_segmentation_6 + "chpt-240204-3 dataset10.b.3 - 3D_nuclei eye autofluo - last - id07 - Otsu manual 0.75.tif")
    main(path_label=parent_label_6 + label_6, path_segmentation=parent_segmentation_6 + "chpt-240204-3 dataset10.b.3 - 3D_nuclei eye autofluo - last - id07 - Otsu manual 0.875.tif")"""

    parent_label_1 = "Y:/Users/DWalther/unet DW/chpt-240204-1 -O- dataset10.b.1 - 3D_nuclei eye autofluo - very good/240209-1 best/"
    parent_segmentation_1 = parent_label_1
    label_1 = "id06 input label.tif"
    parent_label_3 = "Y:/Users/DWalther/unet DW/chpt-240204-2 -O- dataset10.b.2 - 3D_nuclei eye autofluo - very good/240209-2 best/"
    parent_segmentation_3 = parent_label_3
    label_3 = "id05 input label.tif"
    parent_label_4 = "Y:/Users/DWalther/unet DW/chpt-240204-2 -O- dataset10.b.2 - 3D_nuclei eye autofluo - very good/240209-6 last/"
    parent_segmentation_4 = parent_label_4
    label_4 = "id05 input label.tif"
    main(path_label=parent_label_1 + label_1, path_segmentation=parent_segmentation_1 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - best - id06 - Otsu manual 0.01563.tif")
    main(path_label=parent_label_1 + label_1, path_segmentation=parent_segmentation_1 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - best - id06 - Otsu manual 0.03125.tif")
    main(path_label=parent_label_1 + label_1, path_segmentation=parent_segmentation_1 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - best - id06 - Otsu manual 0.04688.tif")
    main(path_label=parent_label_1 + label_1, path_segmentation=parent_segmentation_1 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - best - id06 - Otsu manual 0.0625.tif")
    main(path_label=parent_label_1 + label_1, path_segmentation=parent_segmentation_1 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - best - id06 - Otsu manual 0.07813.tif")
    main(path_label=parent_label_1 + label_1, path_segmentation=parent_segmentation_1 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - best - id06 - Otsu manual 0.09375.tif")
    main(path_label=parent_label_1 + label_1, path_segmentation=parent_segmentation_1 + "chpt-240204-1 dataset10.b.1 - 3D_nuclei eye autofluo - best - id06 - Otsu manual 0.1094.tif")
    main(path_label=parent_label_3 + label_3, path_segmentation=parent_segmentation_3 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - best - id05 - Otsu manual 0.01563.tif")
    main(path_label=parent_label_3 + label_3, path_segmentation=parent_segmentation_3 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - best - id05 - Otsu manual 0.03125.tif")
    main(path_label=parent_label_3 + label_3, path_segmentation=parent_segmentation_3 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - best - id05 - Otsu manual 0.04688.tif")
    main(path_label=parent_label_3 + label_3, path_segmentation=parent_segmentation_3 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - best - id05 - Otsu manual 0.0625.tif")
    main(path_label=parent_label_3 + label_3, path_segmentation=parent_segmentation_3 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - best - id05 - Otsu manual 0.07813.tif")
    main(path_label=parent_label_3 + label_3, path_segmentation=parent_segmentation_3 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - best - id05 - Otsu manual 0.09375.tif")
    main(path_label=parent_label_3 + label_3, path_segmentation=parent_segmentation_3 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - best - id05 - Otsu manual 0.1094.tif")
    main(path_label=parent_label_4 + label_4, path_segmentation=parent_segmentation_4 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - last - id05 - Otsu manual 0.01563.tif")
    main(path_label=parent_label_4 + label_4, path_segmentation=parent_segmentation_4 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - last - id05 - Otsu manual 0.03125.tif")
    main(path_label=parent_label_4 + label_4, path_segmentation=parent_segmentation_4 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - last - id05 - Otsu manual 0.04688.tif")
    main(path_label=parent_label_4 + label_4, path_segmentation=parent_segmentation_4 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - last - id05 - Otsu manual 0.0625.tif")
    main(path_label=parent_label_4 + label_4, path_segmentation=parent_segmentation_4 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - last - id05 - Otsu manual 0.07813.tif")
    main(path_label=parent_label_4 + label_4, path_segmentation=parent_segmentation_4 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - last - id05 - Otsu manual 0.09375.tif")
    main(path_label=parent_label_4 + label_4, path_segmentation=parent_segmentation_4 + "chpt-240204-2 dataset10.b.2 - 3D_nuclei eye autofluo - last - id05 - Otsu manual 0.1094.tif")

    # small study (only path_segmentation differs - slightly different thresholds were chosen, Nullstellensuche in Bezug auf den besten IoU Wert)
    # => if a model is underpredicting - e.g., in this case, a boundary instead of a filled volume model was trained - the lowest possible prediction segmentation threshold is the highest scoring in IoU.
    """#main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.00001526.tif")

    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.tif")
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.01526.tif")
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.03815.tif")

    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.0763.tif")
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.1144.tif")
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.1526.tif")
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.1907.tif")

    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.2296.tif")
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.2451.tif")
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.2605.tif")
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.2759.tif")
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.2913.tif")

    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.307.tif")
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.3221.tif")
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.3375.tif")
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.3529.tif")
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.3684.tif")
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.3838.tif")
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.3992.tif")
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.4146.tif")"""

    # small study (only path_segmentation differs - slightly different thresholds were chosen, Nullstellensuche in Bezug auf den besten IoU Wert - here, a very good model of correct type was tested)
    #main(path_label="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/id01 input label.tif",
    #     path_segmentation="Y:/Users/DWalther/unet DW/chpt-240125-0 -O- dataset10.b - 3D eye autofluo - LR factor 0.413 (6 steps), patience 20 - good/chpt-240131-3 - last - good/chpt-240125-0 last - dataset10.b - 3D eye autofluo - id01 unseen - Otsu manual 0.03815.tif")

    # Y:/Users/DWalther/unet DW/chpt-231225-4 -O- dataset07.0 - 3D heart fluo (model 9) - very good/chpt-231225-5-id07
    """main(path_label="Y:/Users/DWalther/unet DW/chpt-231225-4 -O- dataset07.0 - 3D heart fluo (model 9) - very good/chpt-231225-5-id07/id07-label-dense-threshold.tif",
         path_segmentation="Y:/Users/DWalther/unet DW/chpt-231225-4 -O- dataset07.0 - 3D heart fluo (model 9) - very good/chpt-231225-5-id07/chpt-231225-4 -O- dataset07.0 - 3D heart fluo (model 9) - very good - id07 - Otsu manual 0.9155.tif")
    main(path_label="Y:/Users/DWalther/unet DW/chpt-231225-4 -O- dataset07.0 - 3D heart fluo (model 9) - very good/chpt-231225-5-id07/id07-label-dense-threshold.tif",
         path_segmentation="Y:/Users/DWalther/unet DW/chpt-231225-4 -O- dataset07.0 - 3D heart fluo (model 9) - very good/chpt-231225-5-id07/chpt-231225-4 -O- dataset07.0 - 3D heart fluo (model 9) - very good - id07 - Otsu manual 0.9569.tif")
    main(path_label="Y:/Users/DWalther/unet DW/chpt-231225-4 -O- dataset07.0 - 3D heart fluo (model 9) - very good/chpt-231225-5-id07/id07-label-dense-threshold.tif",
         path_segmentation="Y:/Users/DWalther/unet DW/chpt-231225-4 -O- dataset07.0 - 3D heart fluo (model 9) - very good/chpt-231225-5-id07/chpt-231225-4 -O- dataset07.0 - 3D heart fluo (model 9) - very good - id07 - Otsu manual 1.tif")"""