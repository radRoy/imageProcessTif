import os.path

import fileHandling as fH
import h5py
import numpy as np
import readH5


def tif_create_h5(a_tif, h5_path, internal_path):

    with h5py.File(h5_path, "w") as f:
        f.create_dataset(name=internal_path, data=a_tif)  # ...(self, name, shape, dtype, data, kwds)

    print("HDF5 file created:", h5_path)
    return h5_path  # testing (str, not required for function to work)


def tif_append_h5(data_array, h5_path, internal_path):

    appended = True if os.path.isfile(h5_path) else False

    with h5py.File(h5_path, "a") as f:
        f.create_dataset(name=internal_path, data=data_array)

    if appended:
        print("HDF5 file appended to:", h5_path)
    else:
        print("HDF5 file created:", h5_path)
    return h5_path  # testing (str, not required for function to work)


if __name__ == "__main__":

    # Caution: Do not forget to check the 'internal_path=...' argument below when calling the h5 append/create function!
    # set the mode for creating new or appending to HDF5 file(s)
    label_path = "label"
    raw_path = "raw"
    internal_path = raw_path
    mode_append = False
    """
    if True: 2 dialogs will appear:
        1. input directory
        2. output directory
    
    if False: 1 dialog will appear:
        1. input directory
    output directory will be created automatically in this case
    """

    file_paths = []  # the tif input files. to be saved in hdf5 format
    h5_file_paths = []  # the h5 files to be created or appended to.

    # INPUT FILE PATHS
    path = fH.get_folder_path_dialog()  # str: path with slashes and trailing slash
    files = fH.get_file_list(path)  # list: of the filenames (with extension) contained in the given path
    # tif file paths - assume these are formatted correctly (czyx)
    file_paths = [path + file for file in files]

    if mode_append:
        # OUTPUT FILE PATHS, directories, etc.
        path_out = fH.get_folder_path_dialog()  # str with trailing slash (path contains h5 files)
        h5_files = fH.get_file_list(path_out)
        h5_file_paths = [path_out + file for file in h5_files]

    if not mode_append:
        # OUTPUT FILE PATHS, directories, etc.
        path_out = path.strip("/") + "-h5/"  # str: path with appended -h5
        created_path = fH.create_sibling_dir(path_out)  # (str output, not required) create output path if it doesn't exist yet
        # print(path_out == created_path)  # testing (prints True)

        # file paths of the h5 files to be created / appended to
        h5_file_paths = []
        for i, file in enumerate(files):
            filename_h5 = fH.rename_file(file, suffix="-h5", extension="h5")
            h5_file_paths.append(path_out + filename_h5)
            """
            #testing
            print(i, file)
            print(i, filename_h5)
            print(h5_file_paths[i])
            """

    # creating the h5 files
    """internal_path_raw = "raw"
    for i, file_path in enumerate(file_paths):
        a_tif = fH.read_tif_stack(file_path)
        print(type(a_tif), a_tif.shape, file_path)  # testing
        created_file_path_out = tif_create_h5(a_tif, h5_file_paths[i], internal_path_raw)
        break  # testing"""

    # appending to the h5 files
    # Caution: Do not forget to check the internal_path variable above (see append_mode ~)
    for i, file_path in enumerate(file_paths):
        a_tif = fH.read_tif_stack(file_path)
        print(type(a_tif), a_tif.shape, file_path)  # testing
        created_file_path_out = tif_append_h5(data_array=a_tif, h5_path=h5_file_paths[i], internal_path=internal_path)
        # break  # testing

        # testing (verification of shape in created h5 file)
        h5file = readH5.open_h5(created_file_path_out)
        for key in list(h5file.keys()):
            print(f"shape of py-created h5, 'key' {key}: {h5file[key].shape}")

        print("")  # added readability (add a newline between data sets)
