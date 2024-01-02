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
    # https://nvladimus.github.io/npy2bdv/npy2bdv.html#npy2bdv.npy2bdv.BdvWriter is especially useful


from imageProcessTif import fileHandling as fH


def main():

    path = fH.get_folder_path_dialog(window_title="Choose folder with .h5 file(s)")
    file_path_list = fH.get_file_path_list(parent_path=path)

    for i in range(len(file_path_list)):
        print("")  # output newline separator between files in file path list.

        file_path_h5 = file_path_list[i]  # define input file path
        if not file_path_h5.endswith(".h5"):
            print(f"File {file_path_h5} does not end with '.h5'. Skipping file.")
            continue

        print(f"Opening file {file_path_h5}")
        hdf = h5py.File(name=file_path_h5, mode="r")  # read .h5 image to np.ndarray
        keys = list(hdf.keys())
        print(f"list hdf5 items: {keys}")

        for j in range(len(keys)):
            img_ds = hdf[keys[j]]
            shape = img_ds.shape
            nc, nz, ny, nx = shape[0], shape[1], shape[2], shape[3]  # number of channels, z-, y-, x-coordinates
            print(f'Image Dataset info: Shape={img_ds.shape}, Dtype={img_ds.dtype}')
                # info: Shape = (1, 125, 1169, 414), Dtype = float32
            print(f"nc={nc}, nz={nz}, ny={ny}, nx={nx}")
                # nc = 1, nz = 125, ny = 1169, nx = 414

            ## BDV version using Nikita's npy2bdv package:
            fname = file_path_h5.replace(".h5", f"-npy2bdv_test.h5")
            bdv_writer = npy2bdv.BdvWriter(filename=fname, nchannels=nc)

            # filling the new h5 file with the np.ndarray channel by channel
            for i_channel in range(nc):
                bdv_writer.append_view(stack=img_ds[i_channel])
                    # https://nvladimus.github.io/npy2bdv/npy2bdv.html#npy2bdv.npy2bdv.BdvWriter.append_view
                    # def append_view(self, stack, virtual_stack_dim=None, time=0, illumination=0, channel=0, tile=0, angle=0,
                    #                 m_affine=None, name_affine='manually defined', voxel_size_xyz=(1, 1, 1), voxel_units='px',
                    #                 calibration=(1, 1, 1), exposure_time=0, exposure_units='s')

            print(f"Saving file {fname}")
            bdv_writer.close()  # Writing is finalized by calling BdvWriter.close().
            print(f"File saved.")

            ## tif version (failed so far):
            # file_path_tif = file_path_h5.replace(".h5", f"-key_{keys[j]}.tif")  # define output file path
            # print(f"Saving file {file_path_tif}")
            # # skimage.io.imsave(fname=file_path_tif, arr=image)  # save (.tif) file
            # cv2.imwrite(file_path_tif, img_ds)
            # print(f"File saved.")

    return 0


if __name__ == "__main__":

    # This puts the tkinter dialog window (for choosing inputs etc.) on top of other windows.
    window = tk.Tk()
    window.wm_attributes('-topmost', 1)
    window.withdraw()  # this suppresses the tk window

    print("\n- - - - - - - - - -\nstart program.\n")
    main()
    print("\nend program.")
