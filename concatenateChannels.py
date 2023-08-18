"""
This file is for concatenating multiple (autofluorescence) channels in tif format, so that the multiple individual
(single channel) tif files from one specimen form a single RGB-like tif file containing Channel, X, Y, and Z information
instead of just X, Y, and Z, like the single channel images.

Author: Daniel Walther
creation date: 2023.08.18
"""


import fileHandling as fH


if __name__ == '__main__':

    #file_paths = fH.get_file_path_list( path=fH.get_folder_path_dialog( window_title="Choose folder with single channel images to concatenate"))
    input_file_paths = fH.get_file_path_list()

    output = fH.iterate_function_args_over_iterable(input_file_paths, fH.append_suffix, *['suffix'])
    print(f'\noutputs:\n{output}')

    exit(0)
