#import tkinter as tk
from tkinter import filedialog
import skimage
import os
import pathlib


def get_filepath_dialog():
    file_path = filedialog.askopenfilename()
    return file_path


def get_directory_dialog():
    """

    Returns: str, absolute path with "/" and trailing "/"

    """
    return filedialog.askdirectory() + "/"


def extract_parent_dir(file_path):
    parent_dir = pathlib.Path(file_path)
    parent_dir = parent_dir.parent.absolute()
    return parent_dir


def get_file_list(parent_dir=""):
    if parent_dir == "":
        parent_dir = get_directory_dialog()  # should be str with trailing slash
    file_list = os.listdir(parent_dir)
    return file_list


def create_dir(path, suffix=""):
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



def rename_file(filename, suffix, extension=""):

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


def read_tif_stack(tif_stack_filepath):
    """
    reads in and returns a tif stack.

    Args:
        tif_stack_filepath: str, absolute tif stack file path

    Returns: numpy.ndarray containing that tif image

    """
    return skimage.io.imread(tif_stack_filepath)


def export_file(image, filename):
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


def get_file_path_list():
    path = get_directory_dialog()
    files = get_file_list(path)
    return [path + "/" + file for file in files]


if __name__ == "__main__":

    # tkinter notes
    """
    # tell python / tkinter explicitly to initialise the window creation process (and hide the init window)
    root = tk.Tk()
    root.withdraw()"""

    # file reading dialog notes
    """file_path = filedialog.askopenfilename()
    parent_dir = filedialog.askdirectory()
    print(file_path)

    parent_dir = pathlib.Path(file_path)
    parent_dir = parent_dir.parent.absolute()
    print(parent_dir)

    file_list = os.listdir(parent_dir)
    for file in file_list:
        print("," + file + ".")"""

    """
    file_path = get_filepath_dialog()  # str, path with slashes
    print("file path from dialog:", file_path)
    print(type(file_path))

    directory = get_directory_dialog()  # str, path with slashes, no trailing "/"
    print("directory with path from dialog:", directory)
    print(type(directory))
    """

    """parent_dir = extract_parent_dir(get_filepath_dialog())  # pathlib.WindowsPath, path with backslashes, no trailing "\"
    print("extracted parent directory from file path:", parent_dir)
    print(type(parent_dir))

    parent_dir_str = str(parent_dir)
    print(parent_dir_str)
    print(type(parent_dir_str))"""

    parent_dir = get_directory_dialog()
    file_list = get_file_list(parent_dir)
    print("file list in the given directory (regardless of filetype) " + parent_dir + ":")
    for file in file_list:
        print("  " + file)
        print(type(file))
