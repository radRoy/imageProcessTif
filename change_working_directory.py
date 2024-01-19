import os  # https://docs.python.org/3.10/library/os.html#os.chdir
from pathlib import Path  # https://docs.python.org/3/library/pathlib.html


def change_wd_to_git_parent():
    """ Set wd dynamically (i.e., with symlink to parent folders of this file. My git repos should be organised the same way in relation to each other) """

    print(f"This script's path: {__file__}")
    wd = Path(__file__).parent.absolute().parent.absolute()
    os.chdir(wd)
    print(f"Setting working dir (parent dir of my git repos): {Path(__file__).parent.absolute().parent.absolute()}")

    return wd
