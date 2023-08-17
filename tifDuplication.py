"""
This file is for formatting hdf5 files the right way, so that 3D U-Net can handle the multi-channel images.
Fiji's default is to save RGB images in the order zyxC, but U-Net takes multi-channel input as Czyx.

This script is for creating duplicate arrays of the (label) tif image data, then saving that to Czyx formatted tif.
Since fiji forces 16bit grey scale data into 8bit per channel data when converting to RGB, I have to do this in python,
because, apparently, 3d unet wants the label data (in the given hdf5's /label path) in uint16 format.
3dunet also wants one target channel per input channel, i.e., if there are 4 input channels and the same
solution (label) for all of them, 3dunet wants a C=4,Z,Y,X formatted target data set.

This can only be achieved in python (i.e., not in Fiji, or at least not in .ijm macros).

Author: Daniel Walther
creation date: 2023.07.07
"""


import numpy as np
import os.path
import fileHandling as fH


def duplicate_tif_stack(file_path, n_channels):
    greyscale_image = fH.read_tif_stack(file_path)
    print(f"input shape: {greyscale_image.shape}")

    duplicated_array_stack = np.repeat([greyscale_image], n_channels, axis=0)  # [n_channels,Z,Y,X]
    print(f"output shape: {duplicated_array_stack.shape}")

    return duplicated_array_stack


def main(file_path, output_file_path, n_channels):

    # if <'file' exists>
    if os.path.isfile(file_path):
        print("\nFile", file_path, "exists and is a file.")

        image_formatted = duplicate_tif_stack(file_path, n_channels)
        fH.export_file(image_formatted, output_file_path)
        return 0

    # else
    print("\nFile", file_path, "does not exist or is not a file. exit.")
    return 1


if __name__ == "__main__":

    # input parameters
    suffix = "-czyx"
    extension = "tif"
    n_channel_duplicates = 3

    # input file paths
    path = fH.get_folder_path_dialog()  # str: path with slashes and trailing slash
    files = fH.get_file_list(path)  # list: of the filenames (with extension) contained in the given path

    # tif file paths - assume these are formatted correctly (czyx)
    file_paths = [path + file for file in files]

    # output file paths, directories, etc.
    path_out = path.strip("/") + suffix + "/"  # str: path with appended suffix
    created_path = fH.create_dir(path_out)  # (str output, not required) create output path if it doesn't exist yet
    # print(path_out == created_path)  # testing (prints True)
    output_file_paths = []
    for i, file in enumerate(files):
        output_file_path = fH.rename_file(file, suffix=suffix, extension=extension)
        output_file_paths.append(path_out + output_file_path)

    for i, file_path in enumerate(file_paths):
        main(file_path, output_file_paths[i], n_channel_duplicates)
        print("")  # testing, add a newline between data sets for readability of output messages
