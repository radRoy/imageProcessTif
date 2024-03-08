Daniel Walther
repo creation date: 19.06.2023 (dd.mm.yyyy)

# <u>imageProcessTif</u>

Some `.ijm` files have been moved to the new repo [`radRoy/WaltherFiji`][radRoy/WaltherFiji] (as of 11.11.2023) which is locally embedded into Fiji's scripting directory making my macros in that repo appear in the `Plugins` tab of Fiji.

My repository containing ImageJ Macros and python scripts for processing TIFF (tif) and HDF5 (h5, hdf5) files for use with 3D U-Net (3dunet). The files available from start stem from around 09.05.2023, upon which later IJMacros (ijm) were built. In general, the ijm files are for the image processing regardless of 3dunet input data format (referred below) and the python scripts are for the input data formatting steps after the binary label images have been created. Most parts of the whole image processing workflow have been automated by script files (that includes macros).

The [input data format](https://github.com/wolny/pytorch-3dunet#input-data-format) for multi-channel image data required by [3D U-Net](https://github.com/wolny/pytorch-3dunet) is (C, Z, Y, X) with proper handling of internal paths in the h5 datasets given to 3D U-Net. The HDF5 or TIFF outputs from the [mesoSPIM](https://mesospim.org/) are in a different format. This requires some image processing beyond creation of training labels.

## <u>important remarks</u>

__CAUTION:__ Do ***NOT*** work on one .ijm script in two editors simultaneously (e.g., VS Code and Fiji's built-in editor)! If you do, first it will work fine and both ask you to auto-update, but at some point, Fiji will be 'confused', freeze, and when you force close it with the task manager (or so), Fiji will delete all file contents of the file being changed in the two editors (alternatingly, in my case. I did this, because the VS Code, or most other editors, are more user-friendly than the Fiji built-in editor, in my opinion (imo)).

## <u>conceptual and practical workflow overview</u>

Things are generally done iteratively for all files in a specified input folder. For information on the correct 3dunet input data format, refer to section [Information regarding the input data format required by 3dunet](#Information-regarding-the-input-data-format-required-by-3dunet) below. This list is **concept-focussed**. For a shorter application-focussed list of available scripts, refer to section [my scripts and macros](#my-scripts-and-macros) below.

- **convert** (`TBD: auto conversion`) the h5 microscopy output image data to **tif** format (no script for this yet).
  - Note: The microscope recordings can be very large (> 1 TB). You may require a more powerful computer than your local workstation.
  - This is done with `Fiji > Plugins > BigStitcher > BigStitcher` which then requires an `.xml` file belonging to the `.h5` file containing the images to be converted to `.tif`. For HDF5 (h5) files of size around 500GB, the opening of the file can take half an hour or so, so be patient. Some warning messages might appear, but the images will still open, just be patient. When they are opened, make sure to select `MultiView` at the top of the `Stitching...(TBD)` window and uncheck boxes like `Group Tiles` at the bottom of that window.
    - To convert the .h5 file or parts thereof, select the images you want to convert to .tif, right click on them and choose `Resave > Resave as TIFF`. If only one file is selected, it will be named something like `img.tif`. If multiple files are selected with the same Tile (=sample =specimen ID) number and different channel numbers, the files will be named something like `img_Ch405.tif`, but the tile will not appear as all images are of the same tile. To get the channel and tile number in the .tif filenames, select multiple channels of multiple tiles (just select all images after a microscope session and do the h5 to tif process once on the unicorn, takes about 12 hours for a 500GB h5 file to convert to tif with BigStitcher (=Big Data Viewer underneath the hood)) and resave them as tiff, the filenames will be something like `img_Ch405 nm_Tile0.tif`. From there on, it is unambiguous which newly created .tif file belongs to which sample ID and laser/illumination channel.
- **scale** (`scaleTifs-dataset(...).ijm`) the tif images down to the desired size
  - Note: Ideally, the scaling factor is determined by an informed choice based on computing resource constraints and U-Net model results.
  - If data from multiple imaging sessions are to be combined into one dataset for unet training, the spatial resolution (voxel size - correspondance between volume of sample and recorded pixel size in 3D, i.e., in respective dimensions) from the two image recordings have to be considered. Most likely, training data with a single spatial resolution is desired. The spatial resolution of tif images (or probably h5 images just as well) can be determined with Fiji, by opening an image and looking at its info (File > Show Info, or something like), i.e., the `Voxel size: x * y * z pixels per micron^3`. I recommend using the `Bio-Formats Importer` to open a tif image of interest as a virtual stack and then `Show Info (Ctrl + I)`, as this will always show the voxel size in xyz-pixels-per-micron^3, no matter how many consecutive scaling steps between the opened and the original unscaled tif iamge. (In contrast - this is not recommended to prevent confusion and save reduce image loading time - tif is scaled with Fiji and this tif file is just dragged into Fiji, then `Show Info` will show the voxel size in xyz-pixels-per-pixel^3, referring to the pixel size of the original unscaled image.)
- **crop** (`TBD: auto edge detection`, `croppingCoordinateCalculation.py`, `cropTifs-Static-dataset(...).ijm`) the tif images so that all cropped images have the same size (U-Net can handle different sizes, at least during training, but there will be some complications if different specimens' images are cropped individually). This step could be exchanged in order with scaling, but this would be more space and time intensive. If data from multiple different imaging sessions are to be combined into one dataset, then the images must have the same spatial resolution (voxel size) before cropping (or the scaling must be completed before cropping, in any case, e.g., when a model able to handle different voxel sizes equivalently on a semantic levels is to be trained).
  - Currently, no script for determining the specimen cropping regions/coordinates and coordinates of interest (where its labelled organ is) exists. This has to be done manually for now. I suggest using a computer that has short image loading times for opening the whole .tif images in Fiji (e.g., a device connected to the research group's fast network infrastructure).
    - For now, copy a non-filled `.xlsx` file from previous datasets and fill those cells again. You can re-format the file, just do not change the column headers (relevant for later scripting).
  - a script for calculating cropping coordinates `croppingCoordinateCalculation.py` exists and is robust against all edge cases/ boundary conditions including rounding issues. Currently, this script reads data from an `.xlsx` file and fills that file with additional information (coordinates).
  - a script for checking the cropped images' sizes `getResolutionsBioFormatsImporter` exists and is efficient in working with large image data (i.e., does not need to load the whole image stack to get the info. it wants).
  - For the actual cropping process, a script `cropTifs-Static-dataset05-no_tail.ijm` or similar exists. For now, adapt the newest version of this script to the calculated, normalised cropping coordinates (i.e., change the static array definitions by manually copying cells' values from the `.xlsx` file filled by an earlier script).
- **label** (`labelTifsHeart-dataset(...).ijm`) (create binary annotations of) the fluorescently labelled organs / tissues using the appropriate laser channels (channel handling included in labelling ijm script).
- **format** (`concatenateChannels.py`) the autofluorescence channels to the above mentioned input data format (this may involve multiple steps / scripts).
  - 1. order of x, y, z information in the single channel tif files (array handling, `np.roll` or a similar function)
  - 2. single to multi channel
- (**verify**) the format of the newly created, re-formatted tif images. You can do this by reading the output of the formatting python script.
- **convert** (`writeH5.py`) the tif images to hdf5
  - 1. create h5 files with either the auto- or the fluorescence images (separate folders, does not matter which is chosen, although I recommend to first choose the autofluorescence images because the autofluorescence folder names are more informative, at least at the time of writing) (be mindful of setting the parameters correctly of the corresponding python script)
  - 2. append the remaining images to the h5 files (again, be mindful of setting the parameters correctly of the corresponding python script)
- (**verify**) (`readH5.py`, maybe) the format of the newly created hdf5 files which should be ready for training a U-Net model (uncertain whether a script contains code for this, already)
- (**transfer**) (`TBD: auto transfer`) the files to the Science Cluster drives. Currently, this is done manually with the [globus](https://www.globus.org/) file transfer service.

### <u>outline of the envisioned automated cropping process</u>

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

### <u>information regarding the input data format required by 3dunet</u>

#### <u>input data formatting done with python</u>

As this was not at all straight forward at an earlier point in time, this section stays here in case it needs to be looked up again.

program structure as implemented in `concatenateChannels.py:
- group single channel files by specimen
- ensure the correct & consistent sorting of channels accross specimens (check the filenames in the chosen input directory beforehand)
- **ensure the correct dimension format** (when done with python, the default appears to be ZYX, which already is 3dunet's required format)
- concatenate the single channel images into one image per specimen (here, the channel order within specimens matters as it is not reversible afterwards)
- export the concatenated tif images

Afterwards, conversion to hdf5 format with `writeH5.py` is the only step remaining for having datasets valid & ready for 3dunet training.

The above mentioned **dimension format** causes a lot of work if done with Fiji. The reasons are that Fiji's default dimension orders are handled differently depending on plug-in and concatenating multiple images into one is complicated, might change dimension order and reduces the 16 bit per pixel & channel to 8 bit without alternative.

#### <u>outdated - input data formatting when done with Fiji</u>

*This section is of no active use anymore and was removed from the main README and moved to an archived version of it (`README-archive.md`). Refer to that file if you are interested.*

## <u>datasets overview</u>

- **dataset01** (babb03-ct3-488)
  - babb02.1 data: 638 nm (fluo), 488 nm

- **dataset02** (babb03-ct3-405,488,561)
  - Recommendation: I would refrain from using this dataset in the future. Rather, remake this dataset with the kept individually cropped single channel images by using newer (python) scripts that work reliably and not as confusing as the same workflow done with Fiji.
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
    - scaling: `scaleTifs.ijm`, if I recall correctly. This script might have been changed for creation of dataset03 since then, but the things done are essentially the same.
    - raw:
      - concatenated to RGB24 with Fiji, thereby automatically converting the uInt16 pixel (per channel) values to uInt8 values.
      - formatted with python to CZYX (from something like YXZC from Fiji RGB24-concatenating beforehand).
    - label:
      - converted from uInt8 to uInt16 with Fiji
    - both raw & label images were written to h5 format with the python script `writeH5.py`.
  - Refer to `README-archive.md`, section 'dataset02 creation (outdated) ...' for additional details about the input formatting problem during the creation of dataset02.

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
  - identical to dataset03, except for the train,val,test division: 5-1-1 (true for all datasets / models part of dataset04): Which specimen is in train/val/test set differs between dataset04 sub-versions.
  - The purpose of dataset04 is to try to achieve better validation evaluation scores (therefore, I think, better validation prediction images (which is the ultimate goal)) with 3dunet by increasing the number of train images.
  - **dataset04.a**
    - = 3D model 10.a; val=id06, test=id07, train=id01,02,03,04,05
    - (rem.: input images, etc. taken from dataset03, read above point...)
  - **dataset04.b**
    - = 3D model 10.b; val=id05, test=id01, train=id02,03,04,06,07
  - **dataset04.c**
    - = 3D model 10.c; val=id04, test=id02, train=id01,03,05,06,07

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
- **dataset05.0,1,2,...** (TEMP)
  - TEMP: This dataset was not created. I am keeping the note here because I am still planning to do something like this, but with a little more sophisticated labelling techniques.
  - Identical to the other dataset05s, except for the **label** creation threshold value - the purpose of this dataset is to set a different value for the intensity threshold labelling to investigate the effect of different labels on the model training performance metrics.
  - label threshold value: TBD
  - normCrop: no_tail crop (refer to .roi files stored somewhere sensible (this repo, probably))

- **dataset06**: VRAM study about channels, bitdepth, and patch shape
  - The purpose of this dataset is to refine the VRAM usage prediction formula by also considering number of channels and each channels bit depth. I also vary patch shape to experimentally confirm that there is no interaction between these VRAM usage predictors (TBD: note outcome regarding interaction)
  - babb03 data set
  - ct3 (heart stain, aka tnnt2)
  - crop: normCrop (all images cropped to the same size), whole body crop fr crop (TBD verify?)
  - train/val/test: 5(id01-05) / 1(id06) / 1(id07)
  - data taken from dataset03 (bicubic scaled by 0.25 in xyz)
    - () raw input: autofluorescence, ranging from triple to single channel (405, 488, 561 nm).
    - () label input: manual otsu threshold based on 638 nm channel
- **dataset06.x** (.0 - .5):
  - multi channel to single channel autofluorescence raw inputs: 405,488,651; 405,488; 405;
  - once in 16 bit (numpy uint16) and once in 8 bit (numpy uint8)

- **dataset07**: Fluo single channel raw input test based on dataset03 processed images.
  - The purpose of this dataset is to verify that to verify that I understand 3dunet and use it properly (control study for carrying on with autofluorescence segmentation goal). I hope to achieve this by using fluorescence images as the raw input to be trained to segment. This should work as it is the conventional approach in image segmentation 
  - created on 231007
  - in use since 231007
  - babb03 data set
  - ct3 (heart stain, aka tnnt2)
  - crop: normCrop (all images cropped to the same size), whole body crop
  - train/val/test: 5(id01-05) / 1(id06) / 1(id07)
  - data taken from dataset03 (labels and fluo bicubic scaled by 0.25 in xyz)
    - () raw input: fluo channel 638 nm
    - () label input: manual otsu threshold based on 638 nm channel
  - no processing steps performed, just used `writeH5.py` to convert the `.tif` images to `.h5` files.

- **dataset08**: (babb03) Tif images for training with the Fiji 2D-UNet Plugin.
  - preprocessed images were taken from **dataset03**.
    - scaling: bicubic scaling by 0.25 in all dimensions z, y and x.
    - cropping: normalised cropping including the whole body.
  - babb03
  - heart stain, CT3
  - This unet plugin requires the tif images to be opened in Fiji.
  - Tif images are required.
  - Each training and validation image must have an Overlay of the segmentation label saved into it. Refer to this [video tutorial on generating training data by Thomas Naert](https://lienkamplab.org/wp-content/uploads/2021/10/2_Annotation.mp4) from the [lienkamplab.org page for deep learning resources](https://lienkamplab.org/deep-learning-models/).
    - Therefore, I need to take my 3D binary masks (tif stacks) from a previous dataset (TBD: which one? note here.) and make Image > Overlay from them for each training and validation image (& per channel if multichannel training data).
  - **dataset08.0**: positive fluorescence control heart segmentation dataset
    - I separated the single slices of every specime's z-stack into separate tif images (one slice per tif image), on the group drive. I wrote an `.ijm` script for that.
    - I did not use all the slices for training a unet model. Refer to my [`README-protocol.md`][README protocol] entry for the  [day 231113][231113 monday] for potentially more information.
    - train / val: specimen id01-id05 train, id06-id07 val.
    - slices 3, 13, 23, ..., 123 were used for each specimen.
  - **dataset08.1**: autofluorescence single channel heart segmentation dataset
  - TBD: add description all further dataset08 sub-datasets (up to 08.07 or so were made).

- **dataset09**: (babb03-ct3) Eye labels, tif images for training with the fixed 3D U-Net using pytorch-3dunet.
  - in creation since: 240105 or so, earliest fiji macro created on 240107.
  - purpose/goal of this dataset: Proof of concept - prove the 3d autofluorescence segmentation is possible with the eyes of Xenopus tropicalis embryos at NF stage 42-44. Sample size n = 7 (train + val + test).
  - kind of data: multichannel autofluorescence data (405, 488, 561 nm), labels from autofluorescence, 1 output channel.
  - dense annotations of the eyes used for training.
  - software used for label creation:
    - Fiji, ImageJ Macro (= Fiji Macro = macro)
    - Fiji: creating binary masks manually with Otsu Auto Threshold in the slice with the cross section of the eye and no heart (because the heart is brighter than the eye, heart stain).
    - ImageJ Macro: `[WaltherFiji]/Labelling/label_tifs_eyes-dataset09-binary_to_overlay.ijm` used for converting the binary masks to ROI overlays, with labels "nothing" and "eye".
    - Fiji: Manually alter overlays/ROIs such that only the eyes are included in the ROIs. Use drawing tools like polygon or similar.
    - (TBD Wait for Wolny's response email: Is multi-class semantic segmenation possible in this way with pytorch-3dunet? - Probably skip this step and convert ROIs back to binary masks:)
      - (TBD Fiji Macro: Add inverted label "background" in all the slices where there is an "eye" label. based on [Cicek et al 2016 3D U-Net](https://doi.org/10.48550/arXiv.1606.06650) paper)
    - Fiji Macro: Convert ROI overlays back to binary masks, all with 255 intensity value (uint8), the default in Fiji. This can be used later on for multi-class semantic segmentation with appropriate changes (label processing, e.g.). Depends on how to do this, not clear in pytorch-3dunet documentation & accompanying paper ([Wolny et al 2020 PlantSeg](https://doi.org/10.7554/eLife.57613)).
    - Fiji: correct the voxel size information of the .tif images.
  - **dataset09.0**: binary semantic segmentation of eyes
    - TBD Decide approach: python HDF5 creation: custom scripts in [imageProcessTif] or Nikita's scripts in [npy2bdv]. Can I keep the metadata with npy2bdv?
  - **dataset09.1**: multi-class semantic segmentation of eyes
    - Fiji: Multi-class labelling for pytorch-3dunet: Choose a unique intensity value for each object (eye) to be segmented, based on combination of [Wolny et al 2020 PlantSeg](https://doi.org/10.7554/eLife.57613) and pytorch-3dunet sample data.
    - TBD Decide approach: python HDF5 creation: custom scripts in [imageProcessTif] or Nikita's scripts in [npy2bdv]. Can I keep the metadata with npy2bdv?

- **dataset10**: babb03-ct3-scaled-uncropped-isometric ~(5.784 um)^3 voxel size, **eye labels**
  - This dataset is isometric
  - This dataset is **not cropped**, only scaled (downscaled). *Since pytorch-3dunet only uses patches containing a desired (default 60 %) minimal amount of the label ~volume, cropping is not important as long as I take the smallest of the input images for patch & stride shape calculations since the patch shape and number of images are the only significant predictors of VRAM usage during training.*  
  => original voxel sizes (pixel lengths) of babb03, ct3 (probably the same in all babb03 stains) (z,y,x) in um: 2, 0.85, 0.85  
  => scaled voxel sizes (pixel lengths) of dataset09 (z,y,x) in um: 5.784, 5.784, 5.784
  - label creation: same process & approach as for dataset09 (Fiji manual + macro)
  - software used for label creation (should not contradict process from dataset09):
    - Fiji: threshold of fluo images, Otsu auto threshold at a cross section of an eye without heart on that slice, so that whole eye outline (where connected) is segmented. This resulted in intensity thresholds ranging from 343 to 378 (16 bit images).
    - Fiji macro: [WaltherFiji]`/Labelling/label_tifs_eyes-dataset10-binary_to_overlay.ijm`
    - Fiji: brush tool allows editing ROIs from Overlays. [ImageJ Doc: Tools](https://imagej.net/ij/docs/tools.html), see "Selection Brush" for usage details.
    - Fiji: brush tool fine adjustments: brightness & contrast settings:
      - id01-07: min, max = 291, 556
  - **dataset10.a** sparse eye fluo 2dunet
    - Caution! This dataset is useless for 2dunet training because its slices labeled with "unlabeled" should be called "ignore" for 2dunet to know such a slice contains no class at all.
    - class balance (see [imageProcessTif]/blinding/... for the R scripts) (see `Group/.../dataset10.a/...-sliced/` for images, and `...-slice-balanced/` for the balanced selection thereof):
      - id01: 18: 10 unlabeled, 8 eye: selected "unlabeled" slices (ignoring index of "eye" slices):
        - 1  2  3  4  6  7  9 10
      - id02: 19: 13 unlabeled, 6 eye: selected "unlabeled" slices (ignoring index of "eye" slices):
        - 1  3  4  6 12 13
      - id03: 19: 11 unlabeled, 8 eye: selected "unlabeled" slices (ignoring index of "eye" slices):
        - 3  5  6  7  8  9 10 11
      - id04: 21: 15 unlabeled, 6 eye: selected "unlabeled" slices (ignoring index of "eye" slices):
        - 7 10 11 12 14 15
      - id05: 18: 11 unlabeled, 7 eye: selected "unlabeled" slices (ignoring index of "eye" slices):
        - 2 4 5 6 7 8 9
      - id06: 18: 12 unlabeled, 6 eye: selected "unlabeled" slices (ignoring index of "eye" slices):
        - 2  3  4  5  7 11
      - id07: 23: 20 unlabeled, 3 eye (damaged sample, only 1 eye, rest is fine): selected "unlabeled" slices (ignoring index of "eye" slices):
        - 5 18 20
    - train-val division of embryo IDs:
      - R output: 3 4 2 7 6 1 5
      - id02,03,04,06,07 in the train set
      - id01,05 in the val set
      - id01-07: min, max = 291, 556, with context dependent adaptation to see a large fraction of the 16bit range in brightness.
  - **dataset10.b** dense eye 3 channel autofluo 3dunet
    - r blinding ([imageProcessTif]...): sample output: 2 3 5 7 6 4 1
    - **dataset10.b.0**, previously known as just `dataset10.b`
      - val=id04, test=id01, train=id02,03,05,06,07
    - **dataset10.b.1**
      - val=id07, test=id06, train=id02,03,05,01,04
    - **dataset10.b.2**
      - val=id03, test=id05, train=id01,02,04,06,07
    - **dataset10.b.3** - bonus: id07 only has 1 eye (organ of interest). This model's segmentation serves as a preliminary test for how 3dunet handles different, ~pseudo-mutant~ (damaged sample), samples without being trained for them (again, just an eye missing, everything else intact and not morphed significantly).
      - val=id02, test=id07, train=id01,03,04,05,06,
      
  - **dataset10.c** dense eye fluo 3dunet
    - train-val-test division: same as dataset10.b for comparability:
      - id 2,3,5,6,7 train
      - id 4 val
      - id 1 test
  - **dataset10.c.1** dense eye fluo 3dunet
    - only difference to dataset10.c: train-val-test assignment
    - train-val-test division & val loss experiment: Same blinding assignment as in dataset10.b and 10.c. But train-val-test is 3-2-2 in this dataset, instead of 5-1-1 as in the other two, to see whether val loss avg curves are different when there are more than 1 images in val set
      - id 2,3,5 train
      - id 6,7 val
      - id 4,1 test
    - Question to answer with this dataset: Does the validation loss avg curve in the tensorboard training statistics vary more than the usual range ~ 0.01 with n_val_images > 1, or is it something else causing the curve to stay practically constant? Usually when using deep learning, the validation loss decreases similarly in shape and magnitude as the training loss does.  
    => Refert to the [MSc]/README-protocol.md of 240125 for more information (answer) about this question.

- **dataset11**: babb03 a5 scaled uncropped isometric ~(5.784(? - TBDecided) um)^3
  - This dataset is isometric
  - This dataset is **not cropped**, only scaled (downscaled).  
  => original voxel sizes (pixel lengths) of babb03, a5 (probably the same in all babb03 stains) (z,y,x) in um: 2.0, 0.85, 0.85  
  => all the scalings made for these a5 recordings:  
    - *scaled by (z,y,x): ~(0.345760547, 0.146948232, 0.146948232); resulting voxel size in um (z,y,x): ~(5.784, 5.784, 5.784)*
    - scaled by (z,y,x): ~(0.4, 0.17, 0.17); resulting voxel size in um (z,y,x): (5, 5, 5)
    - scaled by (z,y,x): ~(0.444444444, 0.188888889, 0.188888889); resulting voxel size in um (z,y,x): ~(4.500, 4.500, 4.500)
    - scaled by (z,y,x): ~(0.5, 0.2125, 0.2125); resulting voxel size in um (z,y,x): (4, 4, 4)  
  - This dataset was scaled to voxel size (zyx): ~ 5.784, 5.784, 5.784 - scaled by ~(0.345760547, 0.146948232, 0.146948232) in (z,y,x)
  - Blinding (train/val/test) for this dataset done in python because RStudio deletes my blinding script on different devices for some reason.
    - Script used: [imageProcessTif]`\blinding\blinding.py`
    - random sequence with seed `random.seed(240220)`: 7, 5, 2, 1, 4, 6, 3
  - **dataset11.a** is for boundary type model
    - **dataset11.a.0**
      - test 7; val 5; train 2,1,4,6,3
    - **dataset11.a.1**
      - test 2; val 1; train 4,6,3,7,5
    - **dataset11.a.2**
      - test 4; val 6; train 3,7,5,2,1
  - **dataset11.b** is for nuclei type model
    - The 11.b.x datasets have the same train/val/test assignment like the 11.a.x datasets
    - **dataset11.b.0** see 11.a.x for info
    - **dataset11.b.1** see 11.a.x for info
    - **dataset11.b.2** see 11.a.x for info
  - **dataset11.c**
    - kidney (pronephros) labels were filled with my 2d binary mask fill macro. Some holes still exist in some slices, but the big majority of 2D holes was filled.
    - this model still produced bad results. last checkpoint is always better than the best checkpoint, measure in IoU (see the Group drive dataset folders for results (.yml files currently))
  - **dataset11.d**: babb03 ct3 eye autofluo dataset isometric 5.784 um3, just for getting eye labels for the multi-organ eye,kidney dataset11.e
    - This dataset is isometric
    - This dataset is **not cropped**, only scaled (downscaled).  
    => original voxel sizes (pixel lengths) of babb03, col2a1 (z,y,x) in um: 2.0, 0.85, 0.85
    - These eye labels were made with previous nuclei type eye models using the 3 autofluo channels (same channels throughout babb03 imaging batch)
    - TBD: This dataset can be used for model validation since this was not only a different stain but also a different imaging batch (although the same sample preparation batch).
  - **dataset11.e**: babb03 ct3 eye and kidney multi-organ dataset isometric 5.784 um3
    - wait for dataset11.d to finish predictions

- **dataset12**: babb03 col2a1 scaled uncropped isometric ~(5.784(? - TBDecided) um)^3
  - This dataset is isometric
  - This dataset is **not cropped**, only scaled (downscaled).  
  => original voxel sizes (pixel lengths) of babb03, col2a1 (z,y,x) in um: 2.0, 0.85, 0.85  
  => TBD: all the scalings To Be made for these a5 recordings (?):  
    - *scaled by (z,y,x): ~(0.345760547, 0.146948232, 0.146948232); resulting voxel size in um (z,y,x): ~(5.784, 5.784, 5.784)*
    - scaled by (z,y,x): ~(0.4, 0.17, 0.17); resulting voxel size in um (z,y,x): (5, 5, 5)
    - scaled by (z,y,x): ~(0.444444444, 0.188888889, 0.188888889); resulting voxel size in um (z,y,x): ~(4.500, 4.500, 4.500)
    - scaled by (z,y,x): ~(0.5, 0.2125, 0.2125); resulting voxel size in um (z,y,x): (4, 4, 4)  
  - This dataset was scaled to voxel size (zyx): ~ 5.784, 5.784, 5.784 - scaled by ~(0.345760547, 0.146948232, 0.146948232) in (z,y,x)
  - Labels were attempted in Imaris  
  => Imaris was abandoned for making annotations
  - Currently, no labels exist for this dataset

## <u>links & information about Fiji / ImageJ (Macro)</u>

- [Built-in Macro Functions](https://imagej.nih.gov/ij/developer/macro/functions.html)
- [Combining multiple channels/timepoints into a hyperstack in Fiji](https://cbmf.hms.harvard.edu/avada_faq/fiji-hyperstacks/)

"Fiji" and "Imagej" are used interchangeably as the difference between them would not matter to me, if there was one.

### <u>copied from the BIO321 microscopy block course (fall 2022) - Joana Delgado Martin's fiji hands-on hand-out</u>

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

  [imageProcessTif]

Any publication that uses Fiji should cite the original Fiji paper:  

Schindelin J, Arganda-Carreras I, Frise E, Kaynig V, Longair M, Pietzsch T, Preibisch S, Rueden C, Saalfeld S, Schmid B, Tinevez JY, White DJ, Hartenstein V, Eliceiri K, Tomancak P and Cardona A (2012). Fiji: an open-source platform for biological-image analysis. Nat Methods Jun 28;9()7);676-82

### <u>comparison of Fiji's built-in thresholding algorithms</u>

Subjective Fiji thresholding algorithms ranking by segmentation(label) quality (i.e., whole signal included, noise excluded) (view in Source, not Preview, mode):

#### <u>thresholding algorithm; transformations, quality</u>

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

[radRoy/WaltherFiji]: https://github.com/radRoy/WaltherFiji
[WaltherFiji]: https://github.com/radRoy/WaltherFiji
[radRoy/imageProcessTif]: https://github.com/radRoy/imageProcessTif
[imageProcessTif]: https://github.com/radRoy/imageProcessTif
[npy2bdv]: https://github.com/nvladimus/npy2bdv

[README protocol]: https://github.com/radRoy/msc/blob/master/README-protocol.md
[231113 monday]: https://github.com/radRoy/msc/blob/master/README-protocol.md#231113-monday