"""
This file is for concatenating multiple (autofluorescence) channels in tif format, so that the multiple individual
(single channel) tif files from one specimen form a single RGB-like tif file containing Channel, X, Y, and Z information
instead of just X, Y, and Z, like the single channel images.

Author: Daniel Walther
creation date: 2023.08.18
"""


import tkinter as tk
import fileHandling as fH
import numpy as np


def extract_specimen_ids_from_single_channel_paths(single_channel_paths: list):

    specimen_ids = []
    filenames = []

    for i, single_channel_path in enumerate(single_channel_paths):
        # print('\n', i, single_channel_path)
        file = single_channel_path.split('/')[-1]  # assumes that single_channel_path is a file path
        # print(file)

        specimen_id = file.split('-')[0]  # assumes the filename starts with 'id' (i.e., contains 'id<xy>' in the first '-' delimited segment).
        # print(specimen_id)
        specimen_ids.append(specimen_id)
        filenames.append(file.split('-')[2:])  # leaving out the 'id01' and 'img_Ch405 nm_Angle...Tile...' parts, keeping my suffixes from previous processing steps.

    return specimen_ids, filenames


def get_file_paths_grouped_by_specimen_id(single_channel_paths: list, a_specimen_ids_unique: np.ndarray):

    grouped_specimen_file_paths = []

    for i, specimen_id in enumerate(a_specimen_ids_unique):
        grouped_specimen_file_paths.append([])
        for file_path in single_channel_paths:
            if specimen_id in file_path:
                grouped_specimen_file_paths[i].append(file_path)

    return grouped_specimen_file_paths


if __name__ == '__main__':

    # INFO: when commenting: files, file paths, etc. are always with extension except when stated otherwise
    # TBD: Add new code the code below in such a way, that the processed auto- & fluorescence tifs need to be opened just once for them to be formatted, concatenated, and converted to the 3dunet ready hdf5 files. This will probably involve calling writeH5.py, etc.

    # This is supposed to put the tkinter dialog window (for choosing inputs etc.) on top of other windows (I think it works but is buggy).
    window = tk.Tk()
    window.wm_attributes('-topmost', 1)
    window.withdraw()  # this suppresses the tk window

    ''' INPUT STUFF '''

    # get the file path list of the processed autofluorescence single channel tif images
    input_path = fH.get_folder_path_dialog(window_title='Choose single channel raw input (autofluo.) folder')
    single_channel_paths = fH.get_file_path_list(input_path)

    ids, filename_parts = extract_specimen_ids_from_single_channel_paths(single_channel_paths)
    a_ids_unique = np.unique(ids)  # list of strings of unique specimen IDs (e.g., 'id01')
    #print(ids[0])
    #print(filename_parts[0])

    # creates a list of n_specimens lists, each to be filled with a specimen's corresponding file path.
    file_paths_grouped_by_specimen = get_file_paths_grouped_by_specimen_id(single_channel_paths, a_ids_unique)
    #print(np.array(grouped_specimen_file_paths).shape)  # 7 (n_specimens), 3 (n_single_channels_per_specimen)
    #fH.iterate_function_args_over_iterable(np.array(grouped_specimen_file_paths), print)
    file_paths_grouped_by_specimen = fH.iterate_function_args_over_iterable(file_paths_grouped_by_specimen, sorted)  # sorts in ascending order, within specimens
    file_paths_grouped_by_specimen = sorted(file_paths_grouped_by_specimen)  # sorts in ascending order (by specimen id)
    print("\nSorted raw input file paths:")
    fH.iterate_function_args_over_iterable(np.array(file_paths_grouped_by_specimen), print)

    ''' OUTPUT STUFF '''

    # 'multichannel' and 'concatenated' are used interchangeably in variable names

    # create output file paths (create dirs, and get list - ezpz fH.some_function(input_paths) or so)
    single_channel_filenames = fH.get_file_list(input_path)
    #print([filename for filename in single_channel_filenames])

    ''' STATIC VARIABLE DEFINITION '''
    suffix_multi_channel = '-multiChannel(CZYX)'
    channel_string = 'Ch405,488,561nm'
    suffix_multi_channel += '-' + channel_string
    ''' STATIC VARIABLE DEFINITION END '''

    output_path = fH.create_sibling_dir(path=input_path, suffix=suffix_multi_channel)
    print(f'\nOutput path:\n{output_path}')

    # create output file names
    # (replace the 'id' and 'ch405 nm_angle...' parts by the unique id and append the multichannel part)
    output_multi_channel_filenames = []
    for i, id in enumerate(a_ids_unique):
        preceding_part = id
        succeeding_part = ''
        for sub_part in filename_parts[i]:
            succeeding_part += '-' + sub_part
        output_multi_channel_filenames.append(preceding_part + succeeding_part)
        #print(output_multi_channel_filenames[i])  # testing, e.g., 'id01-Ch405,488,561nm-cropNorm-bicubic-scaled0.25.tif'

    # append filename suffix to the filenames
    output_multi_channel_filenames = fH.iterate_function_args_over_iterable(output_multi_channel_filenames, fH.rename_file, *[suffix_multi_channel])  # inserts a suffix between filenames and their extensions
    print('\nOutput file names:')
    fH.iterate_function_args_over_iterable(output_multi_channel_filenames, print)  # testing

    # fuse output path and output file names together to form the (absolute) output file paths
    output_concatenated_file_paths = [output_path + filename for filename in output_multi_channel_filenames]
    #print(f'\nOutput file paths:')
    #fH.iterate_function_args_over_iterable(output_concatenated_file_paths, print)  # testing
    #exit(0)

    ''' CONCATENATION (SINGLE TO MULTI CHANNEL IMAGES) TAKES PLACE BELOW '''

    # concatenate each specimen's single channel tifs
    print('\nStarting the processing steps')
    for i, specimen_paths in enumerate(file_paths_grouped_by_specimen):
        concatenated = []
        for j, channel_path in enumerate(specimen_paths):
            # open single channel image
            single_channel = fH.read_tif_stack(channel_path)
            print(f'{a_ids_unique[i]}, i{i}j{j}; single channel shape: {single_channel.shape}, channel path: {channel_path}')  # check format (should be (Z,Y,X), i.e., (smallest, largest, middle) shape output)
                # single channel shape: (125, 1169, 414)
                # <same shape for all images (tested between dataset03 specimens)>
                # (check format: The Fiji-processed tif is already in the correct format (Z,Y,X))
            # (above print line:) also check: ch405 before ch488 before ch561 & id01 before id02 etc. (check whether sorted works (sanity double-check, don't know how it shouldn't work, used sorted() above).

            # append single channel to a list for later concatenation into one multichannel array
            #concatenated.append([single_channel])
                # single channel shape: (125, 1169, 414)
                # single channel shape: (125, 1169, 414)
                # concatenated shape: (3, 1, 125, 1169, 414)
            concatenated.append(single_channel)
                # single channel shape: (125, 1169, 414)
                # single channel shape: (125, 1169, 414)
                # single channel shape: (125, 1169, 414)
                # concatenated shape: (3, 125, 1169, 414)

        # do the np.array conversion thing
        concatenated = np.array(concatenated)
        print(f'concatenated (multichannel) shape (should be sth. like (3, 100, 1000, 400): {concatenated.shape}')

        # export the concatenated ndarray to an actual tif file
        fH.export_file(concatenated, output_concatenated_file_paths[i])

    exit(0)
