import readH5 as rH
import fileHandling as fH
from PIL import Image


def list_resolutions_h5(file_paths):

    resolutions = []  # initialise list containing all unique zyx (or otherwise) resolutions of the specified file(s)
    for i, file_path in enumerate(file_paths):

        # some snippet from another testing session
        """
        f = rH.open_h5(file_path)
        print(list(f.keys()))
        for key in f.keys():
            print(f[key])
        """

        res = rH.get_resolution_h5(file_path)
        resolutions.append(res) if res not in resolutions else None
        print(f"i={i}: last element of resolutions: {resolutions[-1]}")

    return resolutions


def list_resolutions_tif(file_paths):

    resolutions = []

    for i, file_path in enumerate(file_paths):
        im = Image.open(file_path)
        width, height = im.size


if __name__ == "__main__":

    file_paths = fH.get_file_path_list()
    """
    resolutions_h5 = list_resolutions_h5(file_paths)
    print("h5 resolutions:\n", resolutions_h5)"""
    resolutions_tif = list_resolutions_tif(file_paths)
    print("tif resolutions:\n", resolutions_tif)

    exit(0)
