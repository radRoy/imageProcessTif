"""
This file is for formatting hdf5 files the right way, so that 3D U-Net can handle the multi-channel images.
Fiji's default is to save RGB images in the order zyxC, but U-Net takes multi-channel input as Czyx.

Author: Daniel Walther
creation date: 2023.07.04
"""


import numpy as np
import os.path
import fileHandling as fH


def reformat_tif_stack(tif_stack):
    """
    Reformats a given tif stack: moves the 4th dimension to the first index, e.g., zyxC to Czyx. (TBD: QU: Why "e.g." and not "i.e."? Which data format is assumed of the input tif_stack files?)

    Args:
        tif_stack: absolute file path, with extension. TBD: what data format of the file is assumed? zyxc, zyx, ...?

    Returns: numpy.ndarray, formatted as described above

    """

    # reading tiff z stack into a numpy.ndarray
    image = fH.read_tif_stack(tif_stack)

    # reformatting tiff z stack with np.rollaxis() from Fiji's RGB zyxC order to the 3D U-Net desired Czyx order
    image = np.rollaxis(image, 3, 0)  # 'rolling' the array with regard to its shape (shifting array's shape).
    # print(image.shape)  # testing
    
    print("reformat_tif_stack: image formatted")
    return image


def main(file_path, output_file_path):
    """
    TBD: Write description

    Args:
        file_path: TBD, most importantly: Is some manual reformatting, e.g., RBG stuff in fiji, assumed?
        output_file_path: TBD

    Returns: TBD

    """

    # if <'file' exists>
    if os.path.isfile(file_path):
        print("\nFile", file_path, "exists and is a file.")

        image_formatted = reformat_tif_stack(file_path)
        fH.export_ndarray_to_file_path(image_formatted, output_file_path)
        return 0

    # else
    print("\nFile", file_path, "does not exist or is not a file. exit.")
    return 1


if __name__ == "__main__":

    # Example tif file with its data dimensions / order as such: [z, y, x, c], where zyx are image dimensions (pixel
    # locations), and c is channel (laser lines saved as RGB)
    """
    tif_from_fiji = "M:/data/d.walther/Microscopy/babb03/tiff-ct3/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24/" \
                    "id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB.tif"
    """

    path = fH.get_folder_path_dialog()  # str: path with slashes and trailing slash
    files = fH.get_file_list(path)  # list: of the filenames (with extension) contained in the given path

    # tif file paths - assume these are formatted correctly (czyx)
        # QU: The assumption that the file paths (?) are formatted correctly seems out of place. What did I mean, earlier?
    file_paths = [path + file for file in files]

    # output file paths, directories, etc.
    suffix = "-czyx"
    extension = "tif"
    path_out = path.strip("/") + suffix + "/"  # str: path with appended suffix
    created_path = fH.create_sibling_dir(path_out)  # (str output, not required) create output path if it doesn't exist yet
    # print(path_out == created_path)  # testing (prints True)
    output_file_paths = []
    for i, file in enumerate(files):
        output_file_path = fH.rename_file(file, suffix=suffix, extension=extension)
        output_file_paths.append(path_out + output_file_path)

    for i, file_path in enumerate(file_paths):
        main(file_path, output_file_paths[i])

    # test of error messages
    """folder_path = "M:/data/d.walther/Microscopy/babb03/tiff-ct3/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24/"
    main(folder_path, "ASDF")"""
