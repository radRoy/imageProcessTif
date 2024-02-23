"""
TBD: Take pytorch-3dunet prediction tif or better yet h5,
calculate series of Otsu threshold images (use Fiji wrapper for python 'pyimagej', translate working .ijm to .py here)
to calculate and converge on the highest IoU score (root finder (Nullstellensucher)),
save results in a txt file.

First TBD (22.02.2024):
Calculate the IoU for a batch of prediction threshold & label image pairs, instead of pair by pair.
- Prompt user for choosing a group (=batch) of thresholded .tif files to calculate the IoU for.
    - Ask in batches of threshold images belonging to the same input label image.
    - (Maybe also write the Intersection and Union images to an output file?
      What would they be useful for besides calculating additional model performance metrics?)
    - Write the IoU results to a separate output .txt file for each image pair (no chagnes required, there).
- - -

Read in two binary mask .tif stacks of same size (with file path dialogs or testing without),
calculate the Intersection over Union (IoU) between them,
write IoU to a text file next to the segmentation file, alongside some additional info (date, time, input file paths).
If the output file already exists, its existing contents are not overwritten but appended to with the new results.

This script works as intended.

creation date (dd.mm.yyyy): 15.02.2024
extension date: 22.02.2024
Daniel Walther
"""


import os
import datetime
import tkinter.messagebox
from tkinter import filedialog

import cv2
import numpy
import numpy as np
import yaml  # https://pyyaml.org/wiki/PyYAMLDocumentation , using yaml.safe_dump()

import fileHandling as fH




def get_label_image(home_dir: str):
    """
    Opens a file dialog prompt where the user can choose a file as the ground truth image
    for IoU batch processing.
    See https://docs.python.org/3/library/dialog.html#module-tkinter.filedialog for source information.

    Args:
        home_dir: The home directory the user prompt window is set to when being first displayed.

    Returns: Absolute file path string, including file extension, delimited with slashes.
    """

    # "...create an Open dialog and return the selected filename that correspond to existing file."
    path_label = filedialog.askopenfilename(
        title="Choose the binary mask label (ground truth) .tif file",
        initialdir=home_dir
    )

    return path_label


def get_segmentation_batch(home_dir: str):
    """
    Opens a file dialog prompt where the user can choose one or multiple files as the segmentation image(s)
    for IoU batch processing.
    See https://docs.python.org/3/library/dialog.html#module-tkinter.filedialog for source information.

    Args:
        home_dir: The home directory the user prompt window is set to when being first displayed.

    Returns: Tuple of absolute file path string(s), including file extension(s), delimited with slashes.
    """

    # "...create an Open dialog and return the selected filename(s) that correspond to existing file(s)."
    segmentation_path_batch = filedialog.askopenfilenames(
        title="Choose at least one segmentation file belonging to the previously selected ground truth."
              "The name should end with a threshold value.",
        initialdir=home_dir
    )

    return segmentation_path_batch


def assert_iou_filenames_valid(label_path: str, segmentation_path: str):
    """
    Handles input file path exceptions to do with the file name of label and segmentation input files
    (end with .tif, segmentation file should precede .tif with a number).

    Args:
        label_path: `str` - Absolute file path of the input label image.
        segmentation_path: `str` - Absolute file path of the segmentation image.

    Returns: `True` if assertions are True.
    """

    # assert that .tif files were chosen.
    assert label_path.endswith(".tif") or label_path.endswith(".tiff"),\
        f"\nGround truth file should end with '.tif' or '.tiff'." \
        f"\n {label_path=}"
    assert segmentation_path.endswith(".tif") or segmentation_path.endswith(".tiff"), \
        f"\nSegmentation file should end with '.tif' or '.tiff'." \
        f"\n {segmentation_path=}"
    assert segmentation_path.split(" ")[-1].split(".")[0].isnumeric(),\
        f"\nThe segmentation file name should end with a number (its lower threshold value)," \
        f"before the .tif(f) file extension." \
        f"\n {segmentation_path=}"

    return True


def assert_iou_input_images_shapes_equal(label, segmentation):
    """
    Handles exceptions to do with the shape of label and segmentation images.

    Currently, the function simply checks whether the two images have the same shape
    (dimensionality & dimensions' lengths).

    Args:
        label: `numpy.ndarray` - The label .tif image opened with `skimage.io.imread()`.
        segmentation: `numpy.ndarray` - The segmentation .tif image opened with `skimage.io.imread()`.

    Returns: `True` if assertions are True.
    """

    assert label.shape == segmentation.shape,\
        f"\nError: Label and segmentation images must have the same shape (dimension shape & length) but they do not:" \
        f"\n label shape:        {label.shape}" \
        f"\n segmentation shape: {segmentation.shape}"

    return True


def assert_iou_input_images_are_binary(label, segmentation):
    """
    Checks whether both input, the label and segmentation, images are binary images
    (contain only 2 different pixel values).

    Args:
        label: `numpy.ndarray` - The label .tif image opened with `skimage.io.imread()`.
        segmentation: `numpy.ndarray` - The segmentation .tif image opened with `skimage.io.imread()`.

    Returns: `True` if assertions are True.
    """

    label_unique = np.unique(label)  # [0 255]
    segmentation_unique = np.unique(segmentation)  # [0 255]
    assert len(label_unique) <= 2,\
        f"\nThe label image is not a binary mask (more than 2 unique values found), unique values:" \
        f"\n {label_unique}"
    assert len(segmentation_unique) <= 2,\
        f"\nThe segmentation image is not a binary mask (more than 2 unique values found), unique values:" \
        f"\n {segmentation_unique}"

    return True


def intersection_over_union(label: numpy.ndarray, segmentation: numpy.ndarray):

    assert_iou_input_images_are_binary(label, segmentation)  # redundant in 'IoU_batch_processor.py' but leaving it in.

    intersection = cv2.bitwise_and(label, segmentation)
    union = cv2.bitwise_or(label, segmentation)

    count_intersection = np.count_nonzero(intersection)
    count_union = np.count_nonzero(union)
    iou = count_intersection / count_union

    return iou


def extract_threshold_from_filename(segmentation_path):

    extension = "." + segmentation_path.split(" ")[-1].split(".")[-1]
    threshold = float(segmentation_path.split(" ")[-1].split(extension)[0])

    return threshold


def process_segmentation_batch(label_path, segmentation_paths):

    iou_groups = []  # List should suffice for starters. Later, a dictionary would fit better, here.
    for i, segmentation_path in enumerate(segmentation_paths):
        print(f"\nsegmentation {i=}: {segmentation_path}")

        # filename assertions
        assert_iou_filenames_valid(label_path, segmentation_path)  # type .tif, segmentation ends with <number>.tif

        # open the label and the current segmentation files & print their basic ndarray properties
        label = fH.read_tif_stack(label_path)
        print(f"label")
        fH.print_ndarray_properties(label)  # zyx
        segmentation = fH.read_tif_stack(segmentation_path)
        print(f"segmentation")
        fH.print_ndarray_properties(segmentation)  # zyx

        # image data assertions
        assert_iou_input_images_shapes_equal(label, segmentation)  # label and segmentation must have identical shape
        assert_iou_input_images_are_binary(label, segmentation)  # label and segmentation images must be binary masks

        # calculate iou, extract threshold, append current iou pair to iou batch list
        iou = intersection_over_union(label, segmentation)
        threshold = extract_threshold_from_filename(segmentation_path)
        print(f"{iou=}")
        print(f"{threshold=}")
        iou_groups.append([iou, threshold, segmentation_path])

    return iou_groups


def main(default_dialog_home="Y:/Users/DWalther/unet DW", testing=False):

    iou_dict_list = []  # Can ignore this for now.

    # Starting the main IoU batch processing loop

    fH.tkinter_window_init()  # This puts the tkinter dialog window (for choosing inputs etc.) on top of other windows when a pop-up is created.
    while tkinter.messagebox.askokcancel(
            "Intersection over Union batch processor",
            "This process will ask for a batch of segmented model pytorch-3dunet model predictions files with the same ground truth and calculate the IoU between the respective pairs."
            "\n\nDo you want to continue?"
    ):
        print("\n---------------------------------------"
              "\nStarting IoU batch processor main loop.")

        # File selection (one input label (ground truth) image, >= 1 segmented pytorch-3dunet prediction image)

        # input label file
        label_path = get_label_image(default_dialog_home)
        if not label_path:
            print("\nNo ground truth file selected. Restarting main loop.")
            continue  # repeats main loop
        print(f"\nGround truth image path:"
              f"\n {label_path=}")

        # segmentation file batch
        segmentation_batch = get_segmentation_batch(default_dialog_home)
        if not segmentation_batch:
            print("\nNo segmentation file(s) selected. Restarting main loop.")
            continue  # repeats main loop
        print(f"\nSegmentation image path(s):"
              f"\n python's {type(segmentation_batch)=} (containing the chosen file path(s))")
        fH.iterate_function_args_over_iterable(print, segmentation_batch)

        # Starting the batch processor for one ground truth image and its selected threshold segmentation batch

        iou_groups = process_segmentation_batch(label_path=label_path, segmentation_paths=segmentation_batch)
        print("\niou_groups unsorted:")
        fH.iterate_function_args_over_iterable(print, iou_groups)

        iou_groups_dict = {group[0]: group for group in iou_groups}
        #print("\nunsorted dict:")
        #print(iou_groups_dict)

        iou_groups_dict_keys_sorted = sorted(iou_groups_dict)  # sorting by descending IoU
        #print("\nsorted dict keys:")
        #print(iou_groups_dict_keys_sorted)

        iou_groups_sorted = [iou_groups_dict[key] for key in iou_groups_dict_keys_sorted]
        print("\nsorted list:")
        print(iou_groups_sorted)

        thresholds = np.array(iou_groups)[:, 1]
        threshold_min, threshold_max = min(thresholds), max(thresholds)  # print(f"test:\n {threshold_min}\n {threshold_max}")
        label_extension = "." + label_path.split(".")[-1]
        output_yaml_file_path = f"{label_path.strip(label_extension)} - iou_batch - lower threshold value range [{threshold_min}, {threshold_max}].yml"

        # write the data to a yaml file. see cloud/yamlHandling.py for my first encounters with yaml coding/comprehension in python.

        test_output_file_path = "H:/imageProcessTif/test_yaml_iou.yml"
        output_file_path = test_output_file_path if testing else output_yaml_file_path
        while os.isfile(output_file_path):
            output_file_path += ".yml"
        with open(output_file_path, 'w') as yaml_out:
            # data sorted by IoU (because that's the key value, here)
            iou_dict = {group[0]: [{"threshold": group[1]}, {"segmentation_path": f'{group[2]}'}] for group in iou_groups_sorted}
            data = {"date": datetime.datetime.now(),
                    "label_path": label_path,
                    "threshold_segmentation_by_IoU": iou_dict}

            # converting the dictionary into a string and writing it to the output file
            output = yaml.safe_dump(data=data, width=293)  # line length of >256 should suffice (Win. path length limit)
            yaml_out.write(output)

        iou_dict_list.append(data)

    # main loop cancel message
    print("\n-----------------------------------------------------------"
          "\nIoU batch processor main loop was cancelled / has finished."
          "\n-----------------------------------------------------------")

    return iou_dict_list


if __name__ == "__main__":

    user_home_dir = "Y:/Users/DWalther/unet DW"
    batch_testing_home_dir = "H:/imageProcessTif/sample images/batch_processing"
    # main(default_dialog_home=batch_testing_home_dir, testing=True)
    main()
