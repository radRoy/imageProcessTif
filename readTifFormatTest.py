import skimage
import os
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

    file_paths = [
        "M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackSequence/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackSequence.tif",
        "M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB.tif",
        "M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24-czyx/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB-czyx.tif"]  # this line: my reformatted one, should be Czyx (3, z, y, x), where y > x > z
        # see output comment section at the end for output of these file_paths

    file_paths = [
        'M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo/id01-Ch405nm-crop-scaled0.25.tif'
    ]
        # see output comment section at the end for output of these file_paths

    file_paths_dataset03_autofluo = [
        'M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset03/raw-cropNorm-bicubic-scaled0.25-autofluo/id01-img_Ch405 nm_Angle180.0_Tile1-cropNorm-bicubic-scaled0.25.tif',
        'M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset03/raw-cropNorm-bicubic-scaled0.25-autofluo-multiChannel(CZYX)-Ch405,488,561nm/id01-cropNorm-bicubic-scaled0.25-multiChannel(CZYX)-Ch405,488,561nm.tif'
    ]
    '''
    dimension type (~bit depth per pixel): uint16
    python type: <class 'numpy.ndarray'>
    python shape (format): (125, 1169, 414)
    file path: M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset03/raw-cropNorm-bicubic-scaled0.25-autofluo/id01-img_Ch405 nm_Angle180.0_Tile1-cropNorm-bicubic-scaled0.25.tif
    
    dimension type (~bit depth per pixel): uint16
    python type: <class 'numpy.ndarray'>
    python shape (format): (3, 125, 1169, 414)
    file path: M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset03/raw-cropNorm-bicubic-scaled0.25-autofluo-multiChannel(CZYX)-Ch405,488,561nm/id01-cropNorm-bicubic-scaled0.25-multiChannel(CZYX)-Ch405,488,561nm.tif
    '''

    file_paths_dataset03_fluo = [
        'M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset03/raw-cropNorm-bicubic-scaled0.25-fluo/id01-img_Ch638 nm_Angle180.0_Tile1-cropNorm-bicubic-scaled0.25.tif',
        'M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset03/raw-cropNorm-bicubic-scaled0.25-label-blur3D1-Otsu570-largest/id01-img_Ch638 nm_Angle180.0_Tile1-cropNorm-bicubic-scaled0.25-label-blur3D1-Otsu570-largest.tif'
    ]
    '''
    dimension type (~bit depth per pixel): uint16
    python type: <class 'numpy.ndarray'>
    python shape (format): (125, 1169, 414)
    file path: M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset03/raw-cropNorm-bicubic-scaled0.25-fluo/id01-img_Ch638 nm_Angle180.0_Tile1-cropNorm-bicubic-scaled0.25.tif
    
    dimension type (~bit depth per pixel): uint8
    python type: <class 'numpy.ndarray'>
    python shape (format): (125, 1169, 414)
    file path: M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset03/raw-cropNorm-bicubic-scaled0.25-label-blur3D1-Otsu570-largest/id01-img_Ch638 nm_Angle180.0_Tile1-cropNorm-bicubic-scaled0.25-label-blur3D1-Otsu570-largest.tif
    '''

    static = True

    #file_paths = file_paths_dataset03_autofluo
    file_paths = file_paths_dataset03_fluo
    if static:

        main(file_paths)

    else:
        
        # folder 1
        path = fH.get_folder_path_dialog()
        files = fH.get_file_list(path)
        file_paths = [path + file for file in files]
        main(file_paths)

        # folder 2
        '''path = fH.get_folder_path_dialog()
        files = fH.get_file_list(path)
        file_paths = [path + file for file in files]
        main(file_paths)'''
    
    exit(0)

# some outputs:
'''
C:/Users/Dancer/Documents/imageProcessTif/venv/Scripts/python.exe C:/Users/Dancer/Documents/imageProcessTif/readTifFormatTest.py 
shape: (327, 1102, 371) , image filepath M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackSequence/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackSequence.tif
shape: (109, 1102, 371, 3) , image filepath M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB.tif
shape: (3, 109, 1102, 371) , image filepath M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24-czyx/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB-czyx.tif

Process finished with exit code 0
'''
'''
C:/Users/Dancer/Documents/imageProcessTif/venv/Scripts/python.exe C:/Users/Dancer/Documents/imageProcessTif/readTifFormatTest.py 
shape: (109, 1102, 371) , image filepath M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo/id01-Ch405nm-crop-scaled0.25.tif

Process finished with exit code 0
'''