"""
daniel walther
creation: 23.07.2023 (dd.mm.yyyy)

links:
    https://docs.python.org/3/library/dialog.html#module-tkinter.filedialog
"""


import tkinter as tk
from tkinter import filedialog  # can not be called as tk.filedialog
import numpy
import skimage
import os
import pathlib


def get_file_path_dialog(window_title="Choose file path"):
    """
    Opens a dialog window for choosing a file, with optionally customisable window title, returns file path string.

    Args:
        window_title: title the dialog window displays, instructing the user on what to do

    Returns: str, absolute file path with "/" (slashes) and file extension. For example: C:/Users/Name/file.txt

    """

    """
    # testing
    file_path = get_file_path_dialog()
    print(file_path)
    """

    return filedialog.askopenfilename(title=window_title)


def get_folder_path_dialog(window_title="Choose folder path"):
    """
    Opens a dialog window for choosing a folder, with optionally customisable window title, returns path string.

    Args:
        window_title: title the dialog window displays, instructing the user on what to do

    Returns: str, absolute folder path with "/" (slashes) and trailing "/". For example:  C:/Users/Name/folder/

    """

    """
    # testing
    directory = get_folder_path_dialog()  # str, path with slashes, no trailing "/"
    print("directory with path from dialog:", directory)
    print(type(directory))
    """

    path = filedialog.askdirectory(title=window_title) + "/"
    #print(f"get folder path returns: {path}")
    #return filedialog.askdirectory(title=window_title) + "/"

    return path


def extract_parent_path(file_path: str):
    """
    Extracts the parent directory of an absolute file path, returns path string.

    Args:
        file_path: Absolute path of a file, with the filename and extension.

    Returns: Absolute path of the file's parent directory as a string, with backslashes and a trailing slash. For
    example: C:\\\cdef\\\parent/ (triple backslashes in raw docu. text, to get one backslash in pycharm documentation
    popup helper thingy)

    """

    """
    # testing parent path getter function
    parent = extract_parent_path(get_file_path_dialog())
    print(parent)  # e.g., C:\cdef\parent/
    # testing usability of the output path (mixed back- & slashes)
    print(get_file_list(parent))  # e.g., ['.idea', 'main.py', '__pycache__']
    
    # testing outputs
    file_path, type <class 'str'>
        # with path and extension (slashes)
    pathlib.Path(file_path), type <class 'pathlib.WindowsPath'>
        # (backslashes, same file path in another class type)
    pathlib.Path(file_path).parent.absolute(), type <class 'pathlib.WindowsPath'>
        # (backslashes, no trailing backslash)
    str(pathlib.Path(file_path).parent.absolute()), type <class 'str'>
        # (absolute parent path, no trailing backslash)
    str(pathlib.Path(file_path).parent.absolute()) + '/', type <class 'str'>
        # (absolute parent path, trailing slash, otherwise backslashes)
    """

    return str(pathlib.Path(file_path).parent.absolute()) + '/'


def get_file_list(parent_path=""):
    """
    Reads all file names contained in the given folder path, returns them in a list as strings, with extensions.

    Args:
        parent_path: String absolute folder path (TBD: verify that it's necessary or not: with trailing slash).

    Returns: List of file names with extensions. For example: ['.idea', 'main.py', '__pycache__']

    """
    if parent_path == "":
        parent_path = get_folder_path_dialog()  # should be str with trailing slash

    return os.listdir(parent_path)


def append_suffix(string: str, suffix: str):
    """
    Appends a suffix to a string and returns it.

    Args:
        string: String that needs appending.
        suffix: String that is to be appended.

    Returns: One concatenated string.

    """
    return string + suffix


def create_dir(path: str):
    """
    Creates a given directory.

    Args:
        path: Absolute path string.

    Returns: Created (if new) directory string.

    """

    """
    # testing done by testing create_sibling_dir()
    """

    None if os.path.exists(path) else os.mkdir(path)

    return path


def create_sibling_dir(path: str, suffix: str):
    """
    Creates a sibling directory to the given absolute path by inserting the suffix between it and the trailing slash.

    Args:
        path: str, absolute path with trailing "/"
        suffix: str, suffix to be appended to given path.

    Returns: str, the created (if new) path including trailing "/"

    """

    """
    # testing
    print(create_sibling_dir(path=get_folder_path_dialog(), suffix="test folder"))
    """

    path = path.strip("/") + suffix + "/"
    create_dir(path)

    return path


def rename_file(filename: str, suffix: str, extension=""):
    """
    Appends a suffix to a given filename with extension, returning `filename-suffix.extension`, where `-suffix` is the string given as argument.

    Args:
        filename: str, filename with extension, no path.
        suffix: str, the suffix to be inserted between the given filename and its extension.
        extension: str, desired file extension. if not specified, the extension that came with 'filename' will be reattached.

    Returns: str, filename with the desired suffix inserted between it and the file extension.

    """

    # creating a list of directories to extract certain partial directories and the filename
    """temp = filename.split("/")
    dir_in = temp[-2]
    name_ext = temp[-1]"""

    # create the name of the output directory
    """parent_dir = ""
    for dir_part in temp[:-2]:
        parent_dir += dir_part + "/"
    dir_suffixed = dir_in + "-" + suffix + "/"
    dir_out = parent_dir + dir_suffixed"""

    # creates the dedicated output directory if it doesn't exist
    """os.mkdir(dir_out) if not os.path.exists(dir_out) else None"""

    # create the file_out name, including its full absolute path, added suffix and file extension
    names = filename.split(".")
    extension = names[-1] if extension == "" else extension
    name = ""
    for part in names[:-1]:
        name += part + "."
    name = name.strip(".")
    name_out = name + suffix  # output filename without extension but with suffix describing processing operation
    file_out = name_out + "." + extension
    """file_out = dir_out + name_out_ext"""

    return file_out


def read_tif_stack(tif_stack_filepath: str):
    """
    reads in and returns a tif stack.

    Args:
        tif_stack_filepath: str, absolute tif stack file path.

    Returns: `numpy.ndarray` containing that tif image.

    """
    return skimage.io.imread(tif_stack_filepath)


def export_file(image: numpy.ndarray, filename: str):
    """
    Exports a numpy.ndarray (e.g., a tif z stack) to .tif format.

    Args:
        image: `numpy.ndarray` (e.g., a formatted RGB24 TIFF z stack, or something else entirely)
        filename: `str` - Aboslute path and filename with extension.

    Returns: nothing (pass).
    """

    skimage.io.imsave(filename, image)  # , photometric='minisblack'

    print("export_file(): saved shape :", image.shape)
    print(f"export_file(): saved bitdepth (numpy type): {image.dtype}")
    print("export_file(): File created: {}".format(filename))

    pass


def get_file_path_list(parent_path=""):
    """
    Returns list of file paths in a given, or interactively chosen if none provided, directory, including extensions.

    Args:
        parent_path: `str`, absolute folder paths with trailing slash.

    Returns: `list`, file paths of the files contained in the given directory, with absolute path (slashes) and extension.
    """

    parent_path = get_folder_path_dialog(window_title="Choose the folder you want the file path list from") if parent_path == "" else parent_path
    files = get_file_list(parent_path)

    #return [path + "/" + file for file in files]  # old, TBD: adapt usages such that they give the right input regarding trailing slash.
    return [parent_path + file for file in files]


def iterate_function_args_over_iterable(iterable, sub_function, *args):
    """
    iterates over a given iterable (e.g., list of strings), calls a given function with given set of input arguments
    *args every iteration.

    Args:
        iterable: An iterable, e.g., list of strings, whose elements are passed as the first arguments to sub_function.
        sub_function: A function, must have the first argument be compatible with the elements in the given iterable.
        *args: The list (or whatever object) of input arguments passed to sub_function every iteration.

    Returns: Nothing, currently.

    """

    output_list = []
    for i, element in enumerate(iterable):
        #print(f"i={i}, ")
        output_list.append(sub_function(element, *args))

    return output_list


def exclude_extension_from_filename(filename_with_extension: str, delim="."):
    """
    Strips the extension from a filename string and returns the filename and its extension as a tuple.

    Args:
        filename_with_extension: str = The filename string with extension, delimited by 'delim'.
        delim: str = The delimiter used between the filename and its extension (default is '.').

    Returns: (filename, extension) - a tuple containing the extracted 'filename' and 'extension' string variables.

    """

    filename = ""
    parts = filename_with_extension.split(delim)
    for part in parts[:-1]:
        filename += part + delim
    filename = filename[:-1]
    extension = parts[-1]

    return filename, extension


def get_string_list_filtered_by_wanted_ending(l: list, s: str):
    """
    Filters out all list elements that do not end with the specified file ending. Returns the filtered list, i.e., with the unwanted list elements excluded.

    Args:
        l: list - The string list intended to contain file paths.
        s: string - The desired ending string of the strings in list 'l', e.g., '.tif'.

    Returns: list 'l_out' - A copy of the input list but filtered to contain only strings that end with 's'.

    """
    l_out = []
    for i, x in enumerate(l):
        # Debugging
        # print(f" i {i}, {x}")
        if x.endswith(s):
            l_out.append(x)
    return l_out


def get_string_list_filtered_by_wanted_substring(l: list, s: str):
    """
    Filters out all list elements that do not contain the specified string. Returns the filtered list, i.e., with the unwanted list elements excluded.

    Args:
        l: list - The string list intended to contain file paths.
        s: string - The desired sub string of the strings in list 'l', e.g., 'file_tree'.

    Returns: list 'l_out' - A copy of the input list but filtered to contain only strings that contain 's'.

    """
    l_out = []
    for x in l:
        if s in x:
            l_out.append(x)
    return l_out


def get_string_list_filtered_by_unwanted_substring(l: list, s: str):
    """
    Filters out all list elements that do not contain the specified string. Returns the filtered list, i.e., with the unwanted list elements excluded.

    Args:
        l: list - The string list intended to contain file paths.
        s: string - The unwanted sub string of the strings in list 'l', e.g., ','.

    Returns: list 'l_out' - A copy of the input list but filtered to contain only strings that do not contain 's'.

    """
    l_out = []
    for x in l:
        if s not in x:
            l_out.append(x)
    return l_out


if __name__ == "__main__":

    # insert test blocks archived in the functions above for testing

    exit(0)