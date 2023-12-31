"""
Daniel Walther
creation date (dd.mm.yyyy): 30.12.2023
purpose: read .h5 file and export to .tif format. Intended use case: Take predict3dunet output .h5 images and convert to .tif format for being able to open them with Fiji.
"""


import skimage
import h5py
from imageProcessTif import fileHandling as fH


def main():

    path = fH.get_folder_path_dialog(window_title="Choose folder with .h5 file(s)")
    file_path_list = fH.get_file_path_list(parent_path=path)

    for i in range(len(file_path_list)):
        file_path_h5 = file_path_list[i]  # define input file path
        if not file_path_h5.endswith(".h5"):
            print(f"File {file_path_h5} does not end with '.h5'. Skipping file.")
            continue

        print(f"Opening file {file_path_h5}")
        image = h5py.File(name=file_path_h5, mode="r")  # read .h5 image to np.ndarray

        file_path_tif = file_path_h5.replace(".h5", ".tif")  # define output file path
        print(f"Saving file {file_path_tif}")
        print(image)
        skimage.io.imsave(fname=file_path_tif, arr=image)  # save (.tif) file
        print(f"File saved.")

    return 0


if __name__ == "__main__":
    print("\n- - - - - - - - - -\nstart program.\n")
    main()
    print("\nend program.")
