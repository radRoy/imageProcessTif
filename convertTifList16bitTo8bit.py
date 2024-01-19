"""
Daniel Walther
creation date (dd.mm.yyyy): 28.09.2023

purpose: convert a list of tif images (file paths) from type uint16 to uint8 and export to new files with suffix "uint8" or similar.
"""


import tkinter as tk
import numpy as np
import datetime

# import files
import fileHandling as fH
from convertTif16bitTo8bit import convertTifUint16ToTifUint8


if __name__ == "__main__":

    print(f"\nProgram start: {datetime.datetime.now()}")

    # This puts the tkinter dialog window (for choosing inputs etc.) on top of other windows.
    window = tk.Tk()
    window.wm_attributes('-topmost', 1)
    window.withdraw()  # this suppresses the tk window

    """ INPUT STUFF """

    # get the file path list of the processed autofluorescence single channel tif images
    input_directory = fH.get_folder_path_dialog(window_title='Choose input folder')
    input_paths = fH.get_file_path_list(input_directory)
    # filter input paths by file type
    input_extension = ".tif"
    input_paths = fH.get_string_list_filtered_by_wanted_ending(input_paths, input_extension)
    # print the input directory and file paths
    print(f"\nInput directory:\n{input_directory}")
    print("Input file paths:")
    fH.iterate_function_args_over_iterable(print, np.array(input_paths))

    """ OUTPUT STUFF """

    # get input filenames to be renamed for output file export
    input_filenames = fH.get_file_list(input_directory)
    input_filenames = fH.get_string_list_filtered_by_wanted_ending(input_filenames, input_extension)

    """ STATIC VARIABLE DEFINITION """
    suffix = "-uint8"
    """ STATIC VARIABLE DEFINITION END """

    # create output directory
    output_directory = fH.create_sibling_dir(path=input_directory, suffix=suffix)
    # create output file names
    output_filenames = []
    for filename in input_filenames:
        output_filenames.append(fH.rename_file(filename, suffix))
    # create output file paths from output dir and output filenames
    output_paths = [output_directory + filename for filename in output_filenames]
    # print the output directory and file paths
    print(f"\nOutput directory:\n{output_directory}")
    print("Output file paths:")
    fH.iterate_function_args_over_iterable(print, np.array(output_paths))

    """ MAIN FILE OPERATIONS """

    # concatenate each specimen's single channel tifs
    print("\nStarting the processing steps")
    for i, file_path in enumerate(input_paths):

        # open image (uint16 tif)
        print(f"\ni: {i}, Opening image: {file_path}")
        tif_16 = fH.read_tif_stack(tif_stack_filepath=file_path)  # assumed to be a uint16 tif image, dimensions (shape) do not matter
        print(f"Opened image's shape: {tif_16.shape}, bitdepth (np.ndarray.dtype, expect np.uint16): {tif_16.dtype}")

        # convert image to uint8
        print(f"Converting image to uint8 (8bit)")
        tif_8 = convertTifUint16ToTifUint8(tif_16)  # explicitly asserts valid intensity values and np.ndarray.dtype encoding.
        assert tif_8.shape == tif_16.shape, f"Input tif's shape {tif_16.shape} is different than the output tif's shape {tif_8.shape}. Something went wrong with the program."
        print(f"Converted image's shape: {tif_8.shape}, bitdepth (np.ndarray.dtype, expect np.uint8): {tif_8.dtype}")

        # export the concatenated ndarray to an actual tif file
        print(f"Saving the converted 8bit tif image")
        fH.export_ndarray_to_file_path(tif_8, output_paths[i])

    print(f"\nProgram finish: {datetime.datetime.now()}\n----\t----\t----\t----")
