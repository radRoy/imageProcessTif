import skimage
import 
import os
import imageProcessTif.fileHandling as fH


def main(file_paths=["M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackSequence/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackSequence.tif", "M:/data/d.walther/Microscopy/babb03/tiff-ct3/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB.tif", "M:/data/d.walther/Microscopy/babb03/tiff-ct3/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24-czyx/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB-czyx.tif"]):

    for file in file_paths:

        if os.path.isfile(file):
            image = skimage.io.imread(file)
            print(f'\ndimension type (~bit depth per pixel): {image.dtype}\npython type: {type(image)}\npython shape (format): {image.shape}\nfile path: {file}')  # testing

        else:
            print("\nFile", file, "does not exist.")

    return 0