import skimage
import cv2
import os
import matplotlib.pyplot as plt
import fileHandling as fH


def main(file_paths=["M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackSequence/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackSequence.tif", "M:/data/d.walther/Microscopy/babb03/tiff-ct3/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB.tif", "M:/data/d.walther/Microscopy/babb03/tiff-ct3/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24-czyx/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB-czyx.tif"]):

    for file in file_paths:

        if os.path.isfile(file):
            image = skimage.io.imread(file)
            print(f'\ndimension type (~bit depth per pixel): {image.dtype}\npython type: {type(image)}\npython shape (format): {image.shape}\nfile path: {file}')  # testing

        else:
            print("\nFile", file, "does not exist.")

    return 0


if __name__ == "__main__":

    print("")

    #import cv2

    img1 = cv2.imread('black_top_right_triangle.png', 0)
    img2 = cv2.imread('black_bottom_right_triangle.png', 0)

    print(type(img1))
    print(img1)

    img_bwa = cv2.bitwise_and(img1, img2)
    img_bwo = cv2.bitwise_or(img1, img2)
    img_bwx = cv2.bitwise_xor(img1, img2)

    print(type(img_bwa))
    print(img_bwa)
    #plt.imshow(img_bwa)

    #cv2.imshow("Bitwise AND of Image 1 and 2", img_bwa)
    #cv2.imshow("Bitwise OR of Image 1 and 2", img_bwo)
    #cv2.imshow("Bitwise XOR of Image 1 and 2", img_bwx)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
