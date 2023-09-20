Daniel Walther
repo creation date: 19.06.2023 (dd.mm.yyyy)

# <u>imageProcessTiff</u>

My repository containing ImageJ Macros and python scripts for processing TIFF (tif) and HDF5 (h5, hdf5) files for use with 3D U-Net (3dunet). The files available from start stem from around 09.05.2023, upon which later IJMacros (ijm) were built. In general, the ijm files are for the image processing regardless of 3dunet input data format (referred below) and the python scripts are for the input data formatting steps after the binary label images have been created. Most parts of the whole image processing workflow have been automated by script files (that includes macros).

The [input data format](https://github.com/wolny/pytorch-3dunet#input-data-format) for multi-channel image data required by [3D U-Net](https://github.com/wolny/pytorch-3dunet) is (C, Z, Y, X) with proper handling of internal paths in the h5 datasets given to 3D U-Net. The HDF5 or TIFF outputs from the [mesoSPIM](https://mesospim.org/) are in a different format. This requires some image processing beyond creation of training labels. **An overview over all image processing steps involved in relation to this repository is given in order here** (things are generally done iteratively for all files in a specified input folder) (refer to the section below this list for the process on finding (/reconstructing from my READMEs etc.) input data formatting steps):

- **convert** the h5 microscopy output image data to **tif** format (no script for this yet)
  - Note: The microscope recordings can be very large (> 1 TB). You may require a more powerful computer than your local workstation.
- **scale** the tif images down to the desired size
  - Note: Ideally, the scaling factor is determined by an informed choice based on computing resource constraints and U-Net model results.
  - If data from multiple imaging sessions are to be combined into one dataset for unet training, the spatial resolution (voxel size - correspondance between volume of sample and recorded pixel size in 3D, i.e., in respective dimensions) from the two image recordings have to be considered. Most likely, training data with a single spatial resolution is desired. The spatial resolution of tif images (or probably h5 images just as well) can be determined with Fiji, by opening an image and looking at its info (File > Show Info, or something like), i.e., the `Voxel size: x * y * z pixels per micron^3`. I recommend using the `Bio-Formats Importer` to open a tif image of interest as a virtual stack and then `Show Info (Ctrl + I)`, as this will always show the voxel size in xyz-pixels-per-micron^3, no matter how many consecutive scaling steps between the opened and the original unscaled tif iamge. (In contrast - this is not recommended to prevent confusion and save reduce image loading time - tif is scaled with Fiji and this tif file is just dragged into Fiji, then `Show Info` will show the voxel size in xyz-pixels-per-pixel^3, referring to the pixel size of the original unscaled image.)
- **crop** the tif images so that all cropped images have the same size (U-Net can handle different sizes, at least during training, but there will be some complications if different specimens' images are cropped individually). This step could be exchanged in order with scaling, but this would be more space and time intensive. If data from multiple different imaging sessions are to be combined into one dataset, then the images must have the same spatial resolution (voxel size) before cropping (or the scaling must be completed before cropping, in any case, e.g., when a model able to handle different voxel sizes equivalently on a semantic levels is to be trained).
  - a script for calculating cropping coordinates `croppingcoordinateCalculation.py` exists and is robust against all edge cases/ boundary conditions including rounding issues.
  - a script for checking the cropped images' sizes `getResolutionsBioFormatsImporter` exists and is efficient in working with large image data (i.e., does not need to load the whole image stack to get the info. it wants).
- **label** (create binary annotations of) the fluorescently labelled organs / tissues using the appropriate laser channels (channel handling included in labelling ijm script).
- **format** the autofluorescence channels to the above mentioned input data format (this may involve multiple steps / scripts).
  - 1. order of x, y, z information in tif files (array handling) (TBD verify list order)
  - 2. single to multi channel (TBD verify list order)
- (**verify**) the format of the newly created, re-formatted tif images (dedicated script for this is available)
- **convert** the tif images to hdf5
  - 1. create h5 files with either the auto- or the fluorescence images (separate folders, does not matter which is chosen) (be mindful of setting the parameters correctly of the corresponding python script)
  - 2. append the remaining images to the h5 files (again, be mindful of setting the parameters correctly of the corresponding python script)
- (**verify**) the format of the newly created hdf5 files which should be ready for training a U-Net model (uncertain whether a script (readH5.py) contains code for this, already)
- (**transfer**) the files to the Science Cluster drives (no script for this yet)

**Refer to this repo's `formatTifsHyperstackH5-Recording.ijm` in `FijiRecordings` for a recording on how to format the tifs correctly (TBD: verify).**

**Some detailed information on the *input data formatting* steps that work was previously documented in the [cloud](https://github.com/radRoy/cloud/tree/master)'s README.md repo under [Wrangling with the Input Data Format...](https://github.com/radRoy/cloud/blob/master/README.md#wrangling-with-the-input-data-format-formatting-hdf5-data-sets-for-data-with-multiple-channels-3-autofluorescence-laser-lines-and-the-input-parameters).**  
- Somewhere there, on the date 230710, I found a well-named yaml file **`train_config-RGB24raw,uint16label-230710-1-3in1out-shapeChange.yml` followed by the comment `# successfully trains on the multichannel input data`**. Therefore, 3dunet requires the label input in 16bit per pixel grey format, and the multichannel raw input

When investigating the format of tif images from dataset02 (where the valid multi-channel input format was determined), I ran my file `imageProcessTif/readTifFormatTest.py` on some images:
- processed (with my **Fiji macros**), non-formatted tif image: `shape: (109, 1102, 371) , image filepath M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo/id01-Ch405nm-crop-scaled0.25.tif`
- after 1st formatting step (concatenating raw input channels with **Fiji built-ins** (reduces 16bit to 8bit per pixel! no fiji work-around found in web)): `shape: (327, 1102, 371) , image filepath M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackSequence/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackSequence.tif`
- after 2nd formatting step (converting the sequence to RGB with **Fiji built-ins**): `shape: (109, 1102, 371, 3) , image filepath M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB.tif`
- after 3rd & final formatting step (changing the image data format to CZYX with **python scripts**): `shape: (3, 109, 1102, 371) , image filepath M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24-czyx/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB-czyx.tif`

## <u>important remarks:</u>

__CAUTION:__ Do ***NOT*** work on one .ijm script in two editors simultaneously (e.g., VS Code and Fiji's built-in editor)! If you do, at some point, Fiji will be 'confused', freeze, and when you force close it with the task manager (or so), Fiji will delete all file contents of the file being changed in the two editors (alternatingly, in my case. I did this, because the VS Code, or most other editors, are more user-friendly than the Fiji built-in editor, in my opinion (imo)).

## <u>useful Fiji / ImageJ (Macro) links in general:</u>

- [Built-in Macro Functions](https://imagej.nih.gov/ij/developer/macro/functions.html)
- [Combining multiple channels/timepoints into a hyperstack in Fiji](https://cbmf.hms.harvard.edu/avada_faq/fiji-hyperstacks/)

"Fiji" and "Imagej" are used interchangeably as the difference between them would not matter to me, if there was one.

### <u>copied from the BIO321 course - Joana Delgado Martin's fiji hands-on hand-out:</u>

21. Literature and further information:  
- The ImageJ online documentation
	- https://imagej.net/learn/
	- https://imagej.nih.gov/ij/docs/
	- can also be accessed via Help>Documentation...
- Help from the community
	- https://forum.image.sc/
- Very useful guides and tutorials
	- https://imagej.net/learn/user-guides
	- https://imagej.net/Presentations
- Github
	- https://github.com/fiji

Any publication that uses Fiji should cite the original Fiji paper:  

Schindelin J, Arganda-Carreras I, Frise E, Kaynig V, Longair M, Pietzsch T, Preibisch S, Rueden C, Saalfeld S, Schmid B, Tinevez JY, White DJ, Hartenstein V, Eliceiri K, Tomancak P and Cardona A (2012). Fiji: an open-source platform for biological-image analysis. Nat Methods Jun 28;9()7);676-82

## <u>my .ijm scripts (= macros)</u>

In all my scripts, in-line documentation is available.

- `cropTifs-Static.ijm` is a static cropping script. no automatic edge or signal detection is done. x-, y- and z-coordinates for cropping have to be given (i.e., changed) manually in the script.
- `scaleTifs.ijm` is a dynamic script for scaling any set of TIF stacks images in a given folder in x-, y- and z-dimensions. Only the scaling factor is static - specify it in the script somewhere.
- `labelTifsHeart.ijm` is a dynamic script for segmenting the biggest fluorescence signal of a group of TIF stack images. The selection of fluorescence vs. non-fluorescence images is still static, as my string comparison / comprehension skills in .ijm (IJM) are still rudimentary. The value for the threshold segmentation needs to be manually determined in a given image group and statically changed in the script.

### <u>overview over the datasets created</u>

- **dataset01** (babb03-ct3-488)
  - babb02.1 data: 638 nm (fluo), 488 nm

- **dataset02** (babb03-ct3-405,488,561)
  - voxel size x, y, z [micron^3 / voxel] = 10, 10, 10
    - babb02.1 voxel size: 0.85, 0.85, 10
    - scaling factor used: .085, .085, 1 (applied to resolution [pixel / micron])
  - babb03 data: 638 nm (fluo), 405 nm, 488 nm, 561 nm
  - the dataset used from <= 2023.07.06 until >= 2023.07.18 (just before my holidays (21.07.2023 - 06.08.2023))
  - cropped individually, such that every specimen has its own 3D cropping region.
    - cropped files were created on the 19.06.2023 (dd.mm.yyyy)
  - 4 channels (1 fluo, 3 autofluo) per specimen
  - refer to the folder [ROIs crop xy (dataset02)](https://github.com/radRoy/imageProcessTif/tree/master/ROIs%20crop%20xy%20(dataset02))
  - kinds of image processing performed to get the dataset (& scripts used & relevant folder names in the microscopy image directories)
    - cropping regions determined manually & individually Fiji (see some `ROI` folder); `cropTifs-Static-dataset02.ijm` used for doing the actual cropping; folder: `M:\data\d.walther\Microscopy\babb03\tiff-ct3\dataset02\raw-cropInd`
    - scaling;
    - raw: **QU:no notes found - TBD: reconstruct based on what works with dataset03 (same original recordings)**
    - label: **QU:no notes found - TBD: reconstruct based on what works with dataset03 (same original recordings)**

- **dataset03** (babb03-ct3-405,488,561-normCrop)
  - voxel size x, y, z [micron^3 / voxel] = 4, 4, 4
    - babb03 voxel size: 1, 1, 1
    - scaling factor used: 0.25 (applied to resolution [pixel / micron])
  - channels 405,488,561 nm were autofluorescence, channel 638 nm was fluorescence, in all stainings (babb03 microscope session).
  - the dataset in creation starting 2023.08.07 (Monday just after holidays) until 2023.08.21.
  - the dataset used from 2023.08.21 until 2023.09.07.
  - normalised cropping, such that all specimens have the same 3D cropping region.
  - refer to the file [babb03-dataset03-cropping-table.xlsx](https://github.com/radRoy/imageProcessTif/blob/master/babb03-dataset03-cropping-table.xlsx) for the cropping coordinates
  - kinds of image processing performed to get the dataset (& scripts used & relevant folder names in the microscopy image directories)
    - cropping; `cropTifs-Static-dataset03.ijm`;
    - scaling; `scaleTifs.ijm`;
    - labelling; `labelTifsHeart-dataset03.ijm`;
    - concatenating autofluorescence channels by specimen (from single to multi channel); `concatenateChannels.py`; no reformatting was necessary, just read in tifs in python, concatenate the arrays of one specimen, save (with python, the bit depth stays 16 bit per pixel, per channel, not like with Fiji where a forced conversion to 8 bit takes place).
      - np.array shape: (C, Z, Y, X), 16 bit per channel & pixel - np.array dtype `uint16`
    - (nothing done to label images);
      - np.array shape: (Z, Y, X), 8 bit - np.array dtype `uint8`
    - writing the images to H5 format; `writeH5.py`; write autofluo concatenats first, then append labels;
  - train, val, test division: 3-2-2: specimen...
    - id 01,02,03 in the train,
    - id 04,05 in the val,
    - id 06,07 in the test set (although the test set was not used in the end).
- **dataset04**
  - identical to dataset03, except for the train,val,test division: 5-1-1: specimen...
    - id 01,02,03,04,05 in the train,
    - id 06 in the val,
    - id 07 in the test set.
  - The purpose of dataset04 is to try to achieve better validation evaluation scores (therefore, I think, better validation prediction images (which is the ultimate goal)) with 3dunet by increasing the number of train images.

- **dataset05**
  - The purpose of this dataset is to get better validation performance metrics by increasing train sample size by pooling together ct3 (aka tnnt2) images from babb02.1 and babb03 microscope sessions.
  - Goal: Heart segmentations (CT3 stainings (Troponin))
  - babb02.1 and babb03 have the heart stain in the 638 and autofluorescence in the 488 nm laser channel (babb03 also has two other autofluo. channels, but these are not used for training in this dataset).
  - voxel size x, y, z [micron^3 / pixel] = 2.53, 2.53, 10
    - resolution [pixel / micron] = 1 / (10 * 2.53 * 2.53) = 0.015622803
    - resolution of dataset03: 1 / (64 = 4 * 4 * 4) = 0.015625
    - minimal dataset05.0 resolution is, xyz: 1, 1, 10, but the resolution would then be 0.1 px/micron, which is much more data than datset03. Dataset03 was just right in fitting the whole images into one A100 with one big patch (with a small buffer zone in each image, unfortunatley).
      - voxel size of babb03, xyz: 1, 1, 1
      - voxel size of babb02.1, xyz: .85, .85, 10
  - voxel size (xyz, micron) of scaled babb02.1 images: 2.5298, 2.5298, 10
  - voxel size (xyz, micron) of scaled babb03 images: 2.5297, 2.5297, 10
    - difference in voxel size is 0.0001 micron = 0.1 nm, which is orders of magnitude smaller than the simple body size difference between specimens and therefore negligible.
  - in creation since 12.09.2023
  - scaling done with: `scaleTifs-dataset05-babb02.1.ijm` for the babb02.1 `scaleTifs-dataset05-babb03.ijm` for the babb03 ct3 (aka tnnt2, heart stain) images.
- **dataset05.0**
  - Identical to the other dataset05s, except for the **label** creation threshold value - the purpose of this dataset is to set a different value for the intensity threshold labelling to investigate the effect of different labels on the model training performance metrics.
  - label threshold value: TBD
- **dataset05.1**
  - Identical to the other dataset05s, except for the **label** creation threshold value - the purpose of this dataset is to set a different value for the intensity threshold labelling to investigate the effect of different labels on the model training performance metrics.
  - label threshold value: TBD
- **dataset05.2**
  - Identical to the other dataset05s, except for the **label** creation threshold value - the purpose of this dataset is to set a different value for the intensity threshold labelling to investigate the effect of different labels on the model training performance metrics.
  - label threshold value: TBD

## <u>outline of the envisioned automated cropping process</u>

__useful links:__  
- high-level Segmentation tutorial (imagej.net): <https://imagej.net/imaging/segmentation#flexible-workflow>
- Creating 3D masks from segmented z-stack, or [Selecting connected pixels in a binary mask in 3D](https://forum.image.sc/t/selecting-connected-pixels-in-a-binary-mask-in-3d/4142/2).

__envisioned process:__  
- downscale images to pre-determined maximal image size (low-quality interpolation should suffice)
- distinguish background from signal (thresholding, pixel brightness distribution cluster analysis, etc.)
- determine 6 coordinates: min & max locations of signal in each x, y, and z dimensions
- determine 3 more coordinates: centre coordinate of the brightest region in the fluorescence image of each specimen (representing the centre coordinates of interests, i.e., where the labelled organ of interest is located in an image) in x, y, and z dimensions. Gaussian Blurring will be helpful in achieving this.
- export image-wise coordinates into a csv table or similar (e.g., to .xlsx with pythons pandas package - refer to `croppingCoordinateCalculation.py` for some implemented code for table handling in python).
- extrapolate back up to original image size, include a boundary, e.g., by extrapolating to the outer pixel locations instead of the middle ones ~
- perform cropping on original images

## <u>comparison of Fiji's built-in thresholding algorithms</u>

Fiji thresholding algorithms ranking by segmentation(label) quality (i.e., whole signal included, noise excluded) (view in Source, not Preview, mode):

### <u>thresholding algorithm; transformations, quality</u>

default  
= Huang  
  
< Li  
= MaxEntropy  
  
<< Intermodes               gauss < gauss 3D (same sigmas)  
= IsoData                   2D < 3D regarding noise exclusion, 2D > 3D regarding signal inclusion  
= IJ_IsoData  
  
< **Otsu**                      slightly but noticeably better inclusion & exclusion of signal & noise  
(<) Percentile  
= RenyiEntropy  
= Shanbhag  
= Triangle  
= Yen  

Conclusion: Since 'Otsu' thresholding was used before and Thomas Naert reported it to work the best, I will use the Fiji built-in Otsu thresholding algorithm.

## <u>(TEMP: outdated. python scripts done in the meantime. TBD: keep still relevant information, add it to above input data formatting section.) 3D U-Net training data set formatting / creation (HDF5 files)</u>

Refer to (above listed) link about [Combining multiple channels/timepoints into a hyperstack in Fiji](https://cbmf.hms.harvard.edu/avada_faq/fiji-hyperstacks/). Following this procedure specimen-wise:

Creating the label input data set:  
- copy the label image as many times as there are autofluorescence channels in that imaging batch (e.g., 3 channels - 405, 488, 561). This mimicks 3 channels to the 3D U-Net, because (when using binary loss functions) per raw input channel, U-Net requires 1 corresponding label data set. Since there is only 1, the same, intended correct (organ) segmentation for all 3 (autofluorescence) channels, the label has to be copied for creating the HDF5 data set used for training U-Net.
- start with the procedure written on above linked website - choose the n (e.g., 3) label copies, mimicking n channgels, as images to import.
- follow the link above for further steps (creating a tif hyperstack).
- when saving the tif (hyper)stack~ to HDF5, call the "label_internal_path" `/label`. Consider the formatting  specified in pytorch-3dunet's README (C, Z, Y, X).

Creating the raw input data set:  
- No step required, here. (No copying or similar required. There are already n (e.g., 3) (autofluorescence) channels available for the raw input data.)
- start with the procedure written on above linked website - choose the n (e.g., 3) raw (autofluorescence) input channels as images to import.
- follow the link above for further steps (creating a tif hyperstack).
- when saving the tif (hyper)stack~ to HDF5, call the "raw_internal_path" `/raw`. Consider the formatting  specified in pytorch-3dunet's README (C, Z, Y, X).
