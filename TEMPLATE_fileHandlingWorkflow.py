"""
Daniel Walther
creation date (dd.mm.yyyy): 28.09.2023

purpose: create the filehandling workflow manually implemented over and over again in my python scripts.
"""


import fileHandling as fH


if __name__ == "__main__":

    """ INPUT FILE PATHS HANDLING """

    # TBD: file extension handling: filter out all unwanted file extensions (=> make changes in filHandling.py)

    input_path = fH.get_folder_path_dialog("Choose input folder")
    file_paths = fH.get_file_path_list(input_path)

    """ OUTPUT FILE PATHS HANDLING """

    # TBD: file extension handling: filter out all unwanted file extensions (=> make changes in filHandling.py)

    # get list of input file names (TBD verify again, whether with(out) extension).
    inputs = fH.get_file_list(input_path)

    # create list of output file names - choose suffix, etc.

    # ask user whether he wants to choose an output directory

        # if yes: ask user to choose the output directory

        # else: handle the output directory automatically

    """ FILE OPERATIONS """

    # <insert file operations here>
