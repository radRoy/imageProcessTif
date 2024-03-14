import os.path
import tkinter as tk
import datetime

import h5py

import fileHandling as fH
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


def main(str_internal_path: str, bool_mode_append: bool):

    # This puts the tkinter dialog window (for choosing inputs etc.) on top of other windows.
    window = tk.Tk()
    window.wm_attributes('-topmost', 1)
    window.withdraw()  # this suppresses the tk window

    """ INPUT FILE PATHS """

    # the tif input files. to be saved in hdf5 format

    path = fH.get_folder_path_dialog(window_title="Choose input folder containing '.tif' files to be converted into '.h5' files")  # str: path with slashes and trailing slash
    files = fH.get_file_list(path)  # list: of the filenames (with extension) contained in the given path
    # tif file paths - assume these are formatted correctly (czyx)
    file_paths = [path + file for file in files]

    # the h5 files to be created or appended to (below two """ SECTIONS """)

    """ INPUT FILE PATHS - H5 APPEND CASE """

    if bool_mode_append:
        # OUTPUT FILE PATHS, directories, etc.
        path_out_append = fH.get_folder_path_dialog("Choose the output folder containing already existing '.h5' files to write (append) into")  # str with trailing slash (path contains h5 files)
        h5_files = fH.get_file_list(path_out_append)
        h5_file_paths = [path_out_append + file for file in h5_files]

    """ INPUT FILE PATHS - H5 NEW CASE """

    if not bool_mode_append:
        # OUTPUT FILE PATHS, directories, etc.
        suffix = "-h5"  # suffix should be given without trailing slash
        path_out_new = fH.create_sibling_dir(path=path, suffix=suffix)  # (str output, not required) create output path if it doesn't exist yet
        # print(path_out == created_path)  # testing (prints True)

        # file paths of the h5 files to be created / appended to
        h5_file_paths = []
        for i, file in enumerate(files):
            filename_h5 = fH.rename_file(file, suffix="-h5", extension="h5")
            h5_file_paths.append(path_out_new + filename_h5)
            """
            #testing
            print(i, file)
            print(i, filename_h5)
            print(h5_file_paths[i])
            """

        #print(f'\nh5 create mode: h5 file paths:')
        #fH.iterate_function_args_over_iterable(h5_file_paths, print)
        #exit(0)

    """ ENSURING THAT INPUT AND OUTPUT FILE PATHS ARE BOTH SORTED ASCENDINGLY & OF EQUAL LENGTH """

    # sorting the file path lists to ensure correct specimen correspondence between raw and label input internal paths
    #print(f'\npre-sorted file paths:')
    #fileHandling.iterate_function_args_over_iterable(file_paths, print)
    #print(f'\npre-sorted h5 (output) file paths:')
    #fileHandling.iterate_function_args_over_iterable(h5_file_paths, print)
    ##file_paths = sorted(file_paths, reverse=True)  # double-checking that sorted() actually does something & what is expected.
    ##h5_file_paths = sorted(h5_file_paths, reverse=True)  # double-checking that sorted() actually does something & what is expected.
    file_paths = sorted(file_paths)  # sorts ascendingly
    h5_file_paths = sorted(h5_file_paths)  # sorts ascendingly
    #print(f'\nascendingly sorted file paths:')
    #fileHandling.iterate_function_args_over_iterable(file_paths, print)
    #print(f'\nascendingly sorted h5 (output) file paths:')
    #fileHandling.iterate_function_args_over_iterable(h5_file_paths, print)
    #exit(0)

    if bool_mode_append:
        print(f'\n h5 append mode: tif (input) file paths:')
        fH.iterate_function_args_over_iterable(print, file_paths)
        print(f'\n h5 append mode: h5 (output) file paths:')
        fH.iterate_function_args_over_iterable(print, h5_file_paths)
    else:
        print(f'\n h5 create mode: tif (input) file paths:')
        fH.iterate_function_args_over_iterable(print, file_paths)
        print(f'\n h5 create mode: h5 (output) file paths:')
        fH.iterate_function_args_over_iterable(print, h5_file_paths)

    # ensure only the right file type is in the file path lists
    file_paths = fH.get_string_list_filtered_by_wanted_ending(l=file_paths, s=".tif")
    h5_file_paths = fH.get_string_list_filtered_by_wanted_ending(l=h5_file_paths, s=".h5")

    # The two file path (input and output) lists must contain the same number of elements.
    # h5_file_paths = h5_file_paths.append(h5_file_paths[0])  # testing assert statement below
    assert len(file_paths) == len(h5_file_paths), f"writeH5.py: Input and output file path lists should contain the same number of file paths (but they do not). Length input list 'file_paths': {len(file_paths)}, length output list 'h5_file_paths': {len(h5_file_paths)}."

    # The two file path (input and output) lists must be different.
    assert file_paths != h5_file_paths, "writeH5.py: Input and output file path lists should be different (but they are not)."

    """ H5 CREATION / APPENDING, ITERATIVELY """

    # creating the h5 files (deprecated, handled below with function 'tif_append_h5()')
    """internal_path_raw = "raw"
    for i, file_path in enumerate(file_paths):
        a_tif = fH.read_tif_stack(file_path)
        print(type(a_tif), a_tif.shape, file_path)  # testing
        created_file_path_out = tif_create_h5(a_tif, h5_file_paths[i], internal_path_raw)
        break  # testing"""

    # appending to the h5 files (creating new or appending to existing ones works the same in ~'append' file saving mode)
    # Caution: Do not forget to check the internal_path variable above (see append_mode ~)
    if bool_mode_append:
        print(f'\nH5 files are going to be appended to.')
    else:
        print(f'\nNew H5 files are going to be created.')
    for i, file_path in enumerate(file_paths):

        # open the tif file
        print(f"\ni: {i}, Opening a tif file: {file_path}")
        a_tif = fH.read_tif_stack(file_path)
        print(f'A tif file has been opened and will be written to an H5 file. Properties of this tif file:')
        print(f' python type: {type(a_tif)}\n python shape (format): {a_tif.shape}\n file path: {file_path}\n dimension type (~bit depth per pixel): {a_tif.dtype}')  # testing
        created_file_path_out = tif_append_h5(data_array=a_tif, h5_path=h5_file_paths[i], internal_path=str_internal_path)
        # break  # testing

        # testing (verification of shape in created h5 file)
        h5file = readH5.open_h5(created_file_path_out)
        for key in list(h5file.keys()):
            print(f"Shape of python-saved H5 file / internal H5 path: 'key' {key}: {h5file[key].shape}")


if __name__ == "__main__":

    print(f"\nProgram start: {datetime.datetime.now()}")

    """ STATIC PARAMETERS """
    # Caution: Do not forget to check the 'internal_path=...' argument below when calling the h5 append/create function!
    # set the mode for creating new or appending to HDF5 file(s)
    # Instructions:
    #   set 'internal_path' either to 'label_path' or 'raw_path'
    #   set 'mode_append' either to 'True' (if h5 files exist already) or 'False' (if new h5 files should be created)
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
    """ STATIC PARAMETERS END """

    main(internal_path, mode_append)

    print(f"\nProgram finish: {datetime.datetime.now()}\n----\t----\t----\t----")
