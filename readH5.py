"""
This script is for creating HDF5 files (data sets) for training a 3D U-Net model.
It should take tif as input and create h5 files in the desired format. The plan is to offer different options.

notes, links:
- https://docs.python.org/3/library/pathlib.html#pathlib.Path.expanduser for expanding ~/... to /home/user/...

Author: Daniel Walther
creation date: 2023.07.05
"""


import h5py
import fileHandling as fH


def open_h5(file_path_h5, mode="r"):
    # file_h5: str to an .h5 file including absolute path
    h5 = h5py.File(file_path_h5, mode)
    return h5


def get_resolution_h5(file_path_h5):
    file = h5py.File(name=file_path_h5, mode="r")
    key = list(file.keys())[-1]
    # print(f"this file's shape: {file[key].shape}")  # testing (shape)
    # print(f"this file's shape's type: {type(file[key].shape)}")  # testing (tuple)
    return file[key].shape


def get_resolution_tif(file_path_tif):
    pass


if __name__ == "__main__":

    # 1st folder with h5 images
    path = fH.get_folder_path_dialog()
    files = fH.get_file_list(path)
    file_paths = [path + "/" + file for file in files]

    for file_path in file_paths:
        f = open_h5(file_path)
        print(list(f.keys()))
        for key in f.keys():
            print(f[key])
        # print(get_resolution_h5(file_path))
        # print("")

    file_path = fH.get_file_path_dialog()
    #print(file_path, type(file_path))
    with open_h5(file_path) as f:
        print(list(f.keys()))
    
    exit(0)
