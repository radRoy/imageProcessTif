"""
daniel walther
creation: 23.07.2023 (dd.mm.yyyy)
"""


from tkinter import filedialog
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

    return filedialog.askdirectory(title=window_title) + "/"


# mark


def extract_parent_path(file_path: str):
    """
    extracts the parent directory's absolute path of an absolute file path

    Args:
        file_path: absolute path of a file, with the filename and extension

    Returns: absolute path of the file's parent directory with trailing slash

    """
    parent_path = pathlib.Path(file_path)  # probably replacing backslashes with slashes (not commented when coded)
    parent_path = parent_path.parent.absolute()  # extract a file's parent path
    return parent_path


def get_file_list(parent_path=""):
    """
    TBD

    Args:
        parent_path: should be str with trailing slash (TBD: revise description)

    Returns: TBD: list of only filenames? (i.e., with path? with extension?)

    """
    if parent_path == "":
        parent_path = get_folder_path_dialog()  # should be str with trailing slash
    file_list = os.listdir(parent_path)
    return file_list


def create_dir(path: str, suffix=""):
    """
    creates a given directory specified by path (absolute path) and the suffix to be appended to it.

    Args:
        path: str, absolute path with trailing "/"
        suffix: str, suffix to be appended to given path. can be nothing.

    Returns: str, the created (if new) path including trailing "/"

    """
    path = path.strip("/") + suffix + "/"
    os.mkdir(path) if not os.path.exists(path) else None
    return path


def rename_file(filename: str, suffix: str, extension=""):

    """
    Appends a suffix to a given filename with extension, returning `filename-suffix.extension`

    Args:
        filename: str, filename with extension, no path
        suffix: str, filename with added suffix and extension, no path
        extension: str, desired file extension. if not specified, the extension appended to 'file' will be reattached.

    Returns: str, filename with the desired suffix appended to it, preceding file extension.

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
        tif_stack_filepath: str, absolute tif stack file path

    Returns: numpy.ndarray containing that tif image

    """
    return skimage.io.imread(tif_stack_filepath)


def export_file(image, filename: str):
    """
    Exports a numpy.ndarray (e.g., a tif z stack) to .tif format.
    Args:
        image: numpy.ndarray (e.g., a formatted RGB24 TIFF z stack)
        filename: filename preceded by the absolute path where it is to be saved

    Returns: nothing (0)
    """

    skimage.io.imsave(filename, image)  # , photometric='minisblack'

    print("saved shape :", image.shape)
    print("export_file(): File created: {}".format(filename))
    return 0


def get_file_path_list(path=""):
    """
    returns list of file paths in a given, or chosen if none provided, directory, including extensions.
    """

    path = get_folder_path_dialog() if path == "" else path
    files = get_file_list(path)
    
    return [path + "/" + file for file in files]


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

    for i, element in enumerate(iterable):
        print(f"i={i}, ")
        sub_function(element, *args)

    pass


if __name__ == "__main__":

    # hier stehengeblieben
    """
    testing and beautifying (proper documentation etc.) of functions done until: "# mark" above.
    completed functions:
        get_file_path_dialog()
        get_folder_path_dialog()
    """
    # bis hier

    """
    parent_dir = pathlib.Path(file_path)
    parent_dir = parent_dir.parent.absolute()
    print(parent_dir)

    file_list = os.listdir(parent_dir)
    for file in file_list:
        print("," + file + ".")
    """

    """
    file_path = get_filepath_dialog()  # str, path with slashes
    print("file path from dialog:", file_path)
    print(type(file_path))

    """

    """parent_dir = extract_parent_dir(get_filepath_dialog())
        # pathlib.WindowsPath, path with backslashes, no trailing "\"
    print("extracted parent directory from file path:", parent_dir)
    print(type(parent_dir))

    parent_dir_str = str(parent_dir)
    print(parent_dir_str)
    print(type(parent_dir_str))"""

    """
    parent_dir = get_directory_dialog()
    file_list = get_file_list(parent_dir)
    print("file list in the given directory (regardless of filetype) " + parent_dir + ":")
    for file in file_list:
        print("  " + file)
        print(type(file))
    """