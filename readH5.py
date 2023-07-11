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


def open_h5(file_path_h5):
    # file_h5: str to an .h5 file including absolute path
    h5 = h5py.File(file_path_h5, "r")
    return h5


def get_resolution_h5(file_path_h5):
    file = open_h5(file_path_h5)
    key = list(file.keys())[-1]
    # print(f"this file's shape: {file[key].shape}")  # testing (shape)
    # print(f"this file's shape's type: {type(file[key].shape)}")  # testing (tuple)
    return file[key].shape


def get_resolution_tif(file_path_tif):
    pass


if __name__ == "__main__":

    # 1st folder with h5 images
    
    path = fH.get_directory_dialog()
    files = fH.get_file_list(path)
    file_paths = [path + "/" + file for file in files]

    for file_path in file_paths:
        f = open_h5(file_path)
        # print(list(f.keys()))
        """for key in f.keys():
            print(f[key])"""
        print(get_resolution_h5(file_path))
        # print("")
    
    exit(0)
    # 2nd folder with h5 images
    
    path = fH.get_directory_dialog()
    files = fH.get_file_list(path)
    file_paths = [path + "/" + file for file in files]

    for file_path in file_paths:
        f = open_h5(file_path)
        print(list(f.keys()))

        for key in f.keys():
            print(f[key])

        print("")

    # exit(0)
