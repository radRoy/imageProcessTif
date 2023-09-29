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
            self.get_input_directory()
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

        path = filedialog.askdirectory(title=window_title) + "/"
        #print(f"get folder path returns: {path}")
        #return filedialog.askdirectory(title=window_title) + "/"

        return path

    """ INPUT RELATED GETTER METHODS """

    def get_input_directory(self):
        self.input_directory = filedialog.askdirectory(title="Choose input directory") + "/"

    def get_input_filenames(self, parent_path):
        """
        Reads all file names contained in the given folder path, returns them in a list as strings, with extensions.

        Args:
            parent_path: String absolute folder path (TBD: verify that it's necessary or not: with trailing slash).

        Returns: List of file names with extensions. For example: ['.idea', 'main.py', '__pycache__']
        """
        if parent_path == "":
            parent_path = self.get_folder_path_dialog()  # should be str with trailing slash

        # self.input_filenames = fH.get_file_list(parent_path=self.input_directory)
        self.input_filenames = os.listdir(parent_path)

    def get_input_paths(self):
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
    print("test")
