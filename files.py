"""
Daniel  Walther
creation date (dd.mm.yyyy): 29.09.2023

links:
    https://www.youtube.com/watch?v=pTB30aXS77U
    https://docs.python.org/3/tutorial/classes.html
"""
import os
import tkinter as tk
from tkinter import filedialog  # can not be called as tk.filedialog

import fileHandling as fH  # TEMP: remove when code is transferred


class Filestream(object):
    def __init__(self, input_extension: str, input_directory="", output_extension="", output_directory="", suffix="-suffix"):

        # This puts the tkinter dialog window (for choosing inputs etc.) on top of other windows.
        window = tk.Tk()
        window.wm_attributes('-topmost', 1)
        window.withdraw()  # this suppresses the tk window

        # input related variables
        self.input_extension = input_extension
        self.input_directory = input_directory
        self.input_filenames = []
        self.input_paths = []

        if input_directory == "":
            self.input_directory = self.get_folder_path_dialog(window_title="Choose input directory")
        self.get_input_filenames()
        self.get_input_paths()

        # output related variables
        self.output_extension = input_extension if output_extension == "" else output_extension
        self.output_directory = output_directory
        self.output_filenames = []
        self.output_paths = []

        self.suffix = suffix

        if self.output_directory == "":
            self.get_output_directory()
        self.get_output_filenames()
        self.get_output_paths()

    def __str__(self):
        print(f"\nclass Filestream instance variables:")
        for i, key in enumerate(self.__dict__.keys()):
            var = self.__dict__[key]
            print(f" {key} {type(var)}: {var}")
        return ""  # else printing this method prints 'None' for some reason

    """ GENERAL HELPER METHODS """

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
        # print(f"get folder path returns: {path}")
        # return filedialog.askdirectory(title=window_title) + "/"

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
            tif_stack_filepath: str, absolute tif stack file path

        Returns: `numpy.ndarray` containing that tif image

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

        print("saved shape :", image.shape)
        print("export_file(): File created: {}".format(filename))

        pass

    def get_file_path_list(parent_path=""):
        """
        Returns list of file paths in a given, or interactively chosen if none provided, directory, including extensions.

        Args:
            parent_path: `str`, absolute folder paths with trailing slash.

        Returns: `list`, file paths of the files contained in the given directory, with absolute path (slashes) and extension.
        """

        parent_path = get_folder_path_dialog(
            window_title="Choose the folder you want the file path list from") if parent_path == "" else parent_path
        files = get_file_list(parent_path)

        # return [path + "/" + file for file in files]  # old, TBD: adapt usages such that they give the right input regarding trailing slash.
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
            # print(f"i={i}, ")
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

    @staticmethod
    def get_folder_path_dialog(window_title="Choose folder path"):
        """
        Opens a dialog window for choosing a folder, with optionally customisable window title, returns path string.

        Args:
            window_title: title the dialog window displays, instructing the user on what to do.

        Returns: str, absolute folder path with "/" (slashes) and trailing "/". For example:  C:/Users/Name/folder/

        """

        """
        # testing
        directory = get_folder_path_dialog()  # str, path with slashes, no trailing "/"
        print("directory with path from dialog:", directory)
        print(type(directory))
        """

        return filedialog.askdirectory(title=window_title) + "/"

    @staticmethod
    def get_file_list(parent_path: str):
        """
        Reads all file names contained in the given folder path, returns them in a list as strings, with extensions.

        Args:
            parent_path: String absolute folder path.

        Returns: List of file names with extensions. For example: ['.idea', 'main.py', '__pycache__']

        """
        return os.listdir(parent_path)

    @staticmethod
    def filter_list_for_extension(l: list, extension: str):
        """
        Filters a given list for a given file extension, removing all elements not ending in this extension.

        Args:
            l: list: A list of strings. Intended to contain filenames.
            extension: str: A string. Intended to be a file extension (ending), e.g., '.tif'.

        Returns: A filtered list only containing the elements ending with the given extension.

        """
        for x in l:
            if x.endswith(extension):
                l.remove(x)
        return l

    """ INPUT RELATED GETTER METHODS """

    def get_input_filenames(self, filter=True):
        """
        Reads all file names contained in the given folder path, returns them in a list as strings, with extensions.

        Args:
            filter:

        Returns: List of file names with extensions. For example: ['.idea', 'main.py', '__pycache__']
        """
        if filter:
            self.input_filenames = self.filter_list_for_extension(l=os.listdir(self.input_directory), extension=self.input_extension)
        else:
            self.input_filenames = self.get_file_list(self.input_directory)

    def get_input_paths(self):
        """
        Returns list of file paths in a given, or interactively chosen if none provided, directory, including extensions.

        Returns: `list`, file paths of the files contained in the given directory, with absolute path (slashes) and extension.
        """
        filenames = fH.get_file_list(self.input_directory)

        #return [path + "/" + file for file in files]  # old, TBD: adapt usages such that they give the right input regarding trailing slash.
        return [parent_path + file for file in filenames]
        self.input_paths = fH.get_file_path_list(parent_path=self.input_directory)

    """ OUTPUT RELATED GETTER METHODS """

    def get_output_directory(self, choose=True):
        if choose:
            self.output_directory = filedialog.askdirectory(title="Choose output directory") + "/"
        else:
            self.output_directory = fH.create_sibling_dir(path=self.input_directory, suffix=self.suffix)

    def get_output_filenames(self):
        self.output_filenames = fH.get_file_list(parent_path=self.output_directory)

    def get_output_paths(self):
        # TBD revise this method to create a list of output file paths
        self.output_paths = fH.get_file_path_list(parent_path=self.output_directory)


if __name__ == "__main__":
    fs = Filestream(input_extension=".tif")
    print(fs.__str__())

    """
    # I imagine my Filestream classes to be used somewhat like this:
    fs = Filestream()
    input = fs.input(input_extension=".tif")
    output = fs.output()
    main(input, output)
    """
