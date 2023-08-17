import skimage
import os
import fileHandling as fH


def main(file_paths=["M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackSequence/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackSequence.tif", "M:/data/d.walther/Microscopy/babb03/tiff-ct3/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB.tif", "M:/data/d.walther/Microscopy/babb03/tiff-ct3/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24-czyx/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB-czyx.tif"]):

    for file in file_paths:

        if os.path.isfile(file):
            image = skimage.io.imread(file)
            print("shape:", image.shape, ", image filepath", file)

        else:
            print("File", file, "does not exist.")

    return 0


if __name__ == "__main__":

    file_paths = ["M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackSequence/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackSequence.tif",
             "M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB.tif",
             "M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24-czyx/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB-czyx.tif"]  # this line: my reformatted one, should be Czyx (3, z, y, x)

    static = True

    if static:

        main(file_paths)

    else:
        
        # folder 1
        path = fH.get_folder_path_dialog()
        files = fH.get_file_list(path)
        file_paths = [path + file for file in files]
        main(file_paths)

        # folder 2
        path = fH.get_folder_path_dialog()
        files = fH.get_file_list(path)
        file_paths = [path + file for file in files]
        main(file_paths)

    exit(0)
