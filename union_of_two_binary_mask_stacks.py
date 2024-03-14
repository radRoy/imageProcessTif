"""
Read in two binary mask .tif stacks of same size (with file path dialogs or testing without),
calculate the Union between them,
    if bitdepth should be a problem, try using numpy non-zero coercion calculations ~,
save the resulting file.
If the output file already exists, its existing contents are not overwritten but appended to with the new results.

creation date (dd.mm.yyyy): 13.03.2024
Daniel Walther
"""

import os
import datetime
import tkinter.messagebox
from tkinter import filedialog
import tkinter as tk

import cv2
import numpy
import numpy as np
# import yaml  # https://pyyaml.org/wiki/PyYAMLDocumentation , using yaml.safe_dump()

import fileHandling as fH


def is_numeric(s: str):
    """Returns True if input is a number (integer or float) and returns False otherwise."""
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_label_image(home_dir: str, title=""):
    """
    Opens a file dialog prompt where the user can choose a file as the ground truth image
    for IoU batch processing.
    See https://docs.python.org/3/library/dialog.html#module-tkinter.filedialog for source information.

    Args:
        title: `str` - Title of the dialog window.
        home_dir: `str` - The home directory the user prompt window is set to when being first displayed.

    Returns: Absolute file path string, including file extension, delimited with slashes.
    """

    # "...create an Open dialog and return the selected filename that correspond to existing file."
    if title == "":
        path_label = filedialog.askopenfilename(
            title="Choose the binary mask label TIFF file",
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
              " The name should end with a threshold value range: `...[0.25,1].tif` with [lower,upper] threshold.",
        initialdir=home_dir
    )

    return segmentation_path_batch


def assert_iou_filenames_valid(label_path: str, segmentation_path: str):
    """
    Handles input file path exceptions to do with the file name of label and segmentation input files
    (end with .tif, segmentation file should precede .tif with a range [<lower_threshold>,<upper_threshold>]).

    Args:
        label_path: `str` - Absolute file path of the input label image.
        segmentation_path: `str` - Absolute file path of the segmentation image.

    Returns: `True` if assertions are True.
    """

    # assert that .tif files were chosen.
    assert label_path.endswith(".tif") or label_path.endswith(".tiff"), \
        f"\nGround truth file should end with '.tif' or '.tiff'." \
        f"\n {label_path=}"
    assert segmentation_path.endswith(".tif") or segmentation_path.endswith(".tiff"), \
        f"\nSegmentation file should end with '.tif' or '.tiff'." \
        f"\n {segmentation_path=}"
    s_lower_threshold = segmentation_path.split(" ")[-1].split(".ti")[0].lstrip("[").rstrip("]").split(",")[0]
    assert is_numeric(s_lower_threshold), \
        f"\nThe segmentation file name should end with a range [<lower_threshold>,<upper_threshold>]" \
        f"(thereof, the first (lower) threshold value is relevant for this python script)," \
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

    assert label.shape == segmentation.shape, \
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
    assert len(label_unique) <= 2, \
        f"\nThe label image is not a binary mask (more than 2 unique values found), unique values:" \
        f"\n {label_unique}"
    assert len(segmentation_unique) <= 2, \
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


def extract_thresholds_from_filename(segmentation_path):
    extension = "." + segmentation_path.split(" ")[-1].split(".")[-1]
    thresholds = segmentation_path.split(" ")[-1].split(extension)[0].lstrip("[").rstrip("]").split(",")
    lower = float(thresholds[0])
    upper = float(thresholds[1])
    return lower, upper


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
        thresholds = extract_thresholds_from_filename(segmentation_path)
        print(f"{iou=}")
        print(f"{thresholds=}")
        iou_groups.append([segmentation_path, iou, thresholds[0], thresholds[1]])

    return iou_groups


def append_highscore_to_filename(output_file_path: str, iou_groups: list):

    ious = [group[1] for group in iou_groups]
    highscore = max(ious)  # max iou
    k = ious.index(highscore)  # position index of the highest scoring segmentation in the iou_groups input list
    extension = output_file_path.split(".")[-1]  # assume that output_file_path ends with .tif or so
    output_file_path = output_file_path.rstrip("." + extension)
    a_groups = np.array(iou_groups)
    output_file_path += f"-iou_highscore_{highscore}-threshold_[{a_groups[k, 2]},{a_groups[k, 3]}].{extension}"

    return output_file_path


def binary_mask_union(label_a_path, label_b_path):

    union = cv2.bitwise_or()

    return union


def main(default_dialog_home="Y:/Users/DWalther/Microscopy", testing=False):

    # Starting the main loop

    fH.tkinter_window_init()  # This puts the tkinter dialog window (for choosing inputs etc.) on top of other windows when a pop-up is created.
    while tkinter.messagebox.askokcancel(
            "Binary Mask Union",
            "This process will ask for two binary mask images to be merged into one image (all TIFF files)."
            "\n\nDo you want to continue?"):
        print("\n-------------------------------------"
              "\nStarting binary mask union main loop.")

        # File selection, input and output stuff

        # input: 1st label image file
        label_a_path = get_label_image(default_dialog_home)
        if not label_a_path:
            print("\nNo image (.tif(f)) selected for 1st binary mask label image to be merged. Restarting main loop.")
            continue  # repeats main loop
        print(f"\n1st binary mask label image path:"
              f"\n {label_a_path=}")
        # input: 2nd label image file
        label_a_parent_path = os.path.dirname(label_a_path)  # https://stackoverflow.com/questions/2860153/how-do-i-get-the-parent-directory-in-python
        label_b_path = get_label_image(label_a_parent_path)
        if not label_b_path:
            print("\nNo image (.tif(f)) selected for 2nd binary mask label image to be merged. Restarting main loop.")
            continue  # repeats main loop
        print(f"\n2nd binary mask label image path:"
              f"\n {label_b_path=}")

        # output folder
        output_folder = filedialog.askdirectory(initialdir=label_a_parent_path, title="Choose the output folder")  # absolute folder path with slashes, without trailing slash
        # outpu file name
        output_file_name = tkinter.simpledialog.askstring(title="Output file name",
                                                         prompt=f"These are the two input file names:\n"
                                                                f"- {os.path.basename(label_a_path)}\n"
                                                                f"- {os.path.basename(label_b_path)}\n"
                                                                f"\n"
                                                                f"Enter the desired output filename\n"
                                                                f"(extension '.tif' will be forced - if the name contains dots '.', end the name with a dot '.' or a file extension like '.tif'):")
                                                                # f"- {os.path.splitext(os.path.basename(label_a_path))[0]}\n"
                                                                # f"- {os.path.splitext(os.path.basename(label_b_path))[0]}\n"
        print(f"\nGiven {output_file_name=}")
        output_file_name = os.path.splitext(os.path.basename(output_file_name))[0]
        print(f"Clean {output_file_name=}")
        # output file path
        output_file_path = output_folder + "/" + output_file_name + ".tif"
        print(f"\nDesired {output_file_path=}")
        while os.path.isfile(output_file_path):
            output_file_path += ".tif"
        print(f"\nAvailable {output_file_path=}")

        # Merge (union (Vereinigung)) the two binary mask label images;

        print(f"\nStarting binary mask union image processing.\n"
              f"...")
        label_a_image = fH.read_tif_stack(tif_stack_filepath=label_a_path)
        fH.print_ndarray_properties(label_a_image, label_a_path)
        label_b_image = fH.read_tif_stack(tif_stack_filepath=label_b_path)
        fH.print_ndarray_properties(label_b_image, label_b_path)
        union = cv2.bitwise_or(label_a_image, label_b_image)             # only returns the first image (src1)
        # union = cv2.bitwise_or(label_a_image, label_b_image, dst=union)  # only returns the first image (src1)
        # cv2.bitwise_or(label_a_image, label_b_image, dst=union)  # TBD: test it
        fH.print_ndarray_properties(union, output_file_path)

        # Saving the merged binary mask label image file

        fH.export_ndarray_to_file_path(image=union, file_path=output_file_path)

    # main loop cancel message
    print("\n---------------------------------------------------------"
          "\nBinary mask union main loop was cancelled / has finished."
          "\n---------------------------------------------------------")

    pass


if __name__ == "__main__":

    user_home_dir = "Y:/Users/DWalther/unet DW"
    batch_testing_home_dir = "H:/imageProcessTif/sample images/batch_processing_1.1"

    dataset11_eye_kidney_merge_dataset_home_dir = "Y:/Users/Dwalther/Microscopy/dataset11/"
    dataset11 = dataset11_eye_kidney_merge_dataset_home_dir

    # main(default_dialog_home=batch_testing_home_dir, testing=True)
    main(dataset11)
