"""
Daniel Walther
creation date (dd.mm.yyyy): 30.12.2023
purpose: read .h5 file and export to .tif format. Intended use case: Take predict3dunet output .h5 images and convert to .tif format for being able to open them with Fiji.
"""


import tkinter as tk
import numpy as np


# import skimage
import cv2  # aka opencv-python for installation
import h5py
import npy2bdv  # Nikita's h5 handling package


from imageProcessTif import fileHandling as fH


def main():

    path = fH.get_folder_path_dialog(window_title="Choose folder with .h5 file(s)")
    file_path_list = fH.get_file_path_list(parent_path=path)

    for i in range(len(file_path_list)):
        file_path_h5 = file_path_list[i]  # define input file path
        if not file_path_h5.endswith(".h5"):
            print(f"File {file_path_h5} does not end with '.h5'. Skipping file.")
            continue

        print(f"Opening file {file_path_h5}")
        hdf = h5py.File(name=file_path_h5, mode="r")  # read .h5 image to np.ndarray
        keys = list(hdf.keys())
        print(f"list hdf5 items: {keys}")
        for j in range(len(keys)):
            img_ds = hdf[keys[j]][()]
            print(f'Image Dataset info: Shape={img_ds.shape},Dtype={img_ds.dtype}')  # shape and dtype of hdf5 dataset
            img_ds: np.ndarray  # add python type hint for np. ... auto-completion
            img_ds = img_ds.astype(dtype=np.uint32)  # https://numpy.org/doc/stable/reference/generated/numpy.ndarray.astype.html
                # https://numpy.org/doc/stable/reference/arrays.scalars.html#unsigned-integer-types

            file_path_tif = file_path_h5.replace(".h5", f"-key_{keys[j]}.tif")  # define output file path
            print(f"Saving file {file_path_tif}")
            # print(hdf)
            # skimage.io.imsave(fname=file_path_tif, arr=image)  # save (.tif) file
            cv2.imwrite(file_path_tif, img_ds)
            print(f"File saved.")

    return 0


if __name__ == "__main__":

    # This puts the tkinter dialog window (for choosing inputs etc.) on top of other windows.
    window = tk.Tk()
    window.wm_attributes('-topmost', 1)
    window.withdraw()  # this suppresses the tk window

    print("\n- - - - - - - - - -\nstart program.\n")
    main()
    print("\nend program.")
