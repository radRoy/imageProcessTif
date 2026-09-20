"""
Daniel Walther
creation date (dd.mm.yyyy): 28.09.2023

purpose: convert a list of tif images (file paths) from type uint16 to uint8 and export to new files with suffix "uint8" or similar.
"""


import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

import numpy as np
import skimage.io

from convertTif16bitTo8bit import convertTifUint16ToTifUint8


if __name__ == "__main__":

    print(f"\nProgram start: {datetime.datetime.now()}")

    # This puts the tkinter dialog window (for choosing inputs etc.) on top of other windows.
    window = tk.Tk()
    window.wm_attributes('-topmost', 1)
    window.withdraw()  # this suppresses the tk window

    """ INPUT STUFF """

    # get the file path list of the processed autofluorescence single channel tif images
    input_directory = Path(filedialog.askdirectory(title='Choose input folder'))
    input_paths = sorted(p for p in input_directory.iterdir() if p.is_file() and p.suffix.lower() == ".tif")

    # print the input directory and file paths
    print(f"\nInput directory:\n{input_directory}")
    print("Input file paths:")
    for p in np.array(input_paths):  # ndarray for nicer printing
        print(p)

    """ OUTPUT STUFF """

    """ STATIC VARIABLE DEFINITION """
    suffix = "-uint8"
    """ STATIC VARIABLE DEFINITION END """

    # create output directory
    output_directory = input_directory.parent / f"{input_directory.name}{suffix}"
    output_directory.mkdir(parents=False, exist_ok=True)

    # create output file paths
    output_paths = [output_directory / f"{p.stem}{suffix}{p.suffix}" for p in input_paths]

    # print the output directory and file paths
    print(f"\nOutput directory:\n{output_directory}")
    print("Output file paths:")
    for p in np.array(output_paths):  # ndarray for nicer printing
        print(p)

    """ MAIN FILE OPERATIONS """

    # concatenate each specimen's single channel tifs
    print("\nStarting the processing steps")
    for i, file_path in enumerate(input_paths):

        # open image (uint16 tif)
        print(f"\ni: {i}, Opening image: {file_path}")
        tif_16 = skimage.io.imread(file_path)  # assumed to be a uint16 tif image, dimensions (shape) do not matter
        print(f"Opened image's shape: {tif_16.shape}, bitdepth (np.ndarray.dtype, expect np.uint16): {tif_16.dtype}")

        # convert image to uint8
        print(f"Converting image to uint8 (8bit)")
        tif_8 = convertTifUint16ToTifUint8(tif_16)  # explicitly asserts valid intensity values and np.ndarray.dtype encoding.
        assert tif_8.shape == tif_16.shape, f"Input tif's shape {tif_16.shape} is different than the output tif's shape {tif_8.shape}. Something went wrong with the program."
        print(f"Converted image's shape: {tif_8.shape}, bitdepth (np.ndarray.dtype, expect np.uint8): {tif_8.dtype}")

        # export the concatenated ndarray to an actual tif file
        print(f"Saving the converted 8bit tif image")
        skimage.io.imsave(output_paths[i], tif_8)

    print(f"\nProgram finish: {datetime.datetime.now()}\n----\t----\t----\t----")
