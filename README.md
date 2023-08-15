Daniel Walther
repo creation date: 19.06.2023 (dd.mm.yyyy)

# imageProcessTiff

My repository containing ImageJ Macros and python scripts for processing TIFF (tif) and HDF5 (h5, hdf5) files for use with 3D U-Net (3dunet). The files available from start stem from around 09.05.2023, upon which later IJMacros (ijm) were built. In general, the ijm files are for the image processing regardless of 3dunet input data format (referred below) and the python scripts are for the input data formatting steps after the binary label images have been created. Most parts of the whole image processing workflow have been automated by script files (that includes macros).

The [input data format](https://github.com/wolny/pytorch-3dunet#input-data-format) for multi-channel image data required by [3D U-Net](https://github.com/wolny/pytorch-3dunet) is (C, Z, Y, X) with proper handling of internal paths in the h5 datasets given to 3D U-Net. The HDF5 or TIFF outputs from the [mesoSPIM](https://mesospim.org/) are in a different format. This requires some image processing beyond creation of training labels. An overview over all image processing steps involved in relation to this repository is given in order here (things are generally done iteratively for all files in a specified input folder):

- convert the h5 microscopy output image data to **tif** format (no script for this yet)
  - Note: The microscope recordings can be very large (> 1 TB). You may require a more powerful computer than your local workstation.
- **scale** the tif images down to the desired size
  - Note: Ideally, the scaling factor is determined by an informed choice based on computing resource constraints and U-Net model results.
- **crop** the tif images so that all cropped images have the same size (U-Net can handle different sizes, but there will be some complications if different specimens' images are cropped individually). This step could be exchanged in order with scaling, but this would be more space and time intensive.
- **label** (create binary annotations of) the fluorescently labelled organs / tissues using the appropriate laser channels (channel handling included in labelling ijm script).
- **format** the autofluorescence channels to the above mentioned input data format (this may involve multiple steps / scripts).
  - 1. order of x, y, z information in tif files (array handling) (TBD verify list order)
  - 2. single to multi channel (TBD verify list order)
- (**verify**) the format of the newly created, re-formatted tif images (dedicated script for this is available)
- **convert** the tif images to hdf5
  - 1. create h5 files with either the auto- or the fluorescence images (separate folders, does not matter which is chosen) (be mindful of setting the parameters correctly of the corresponding python script)
  - 2. append the remaining images to the h5 files (again, be mindful of setting the parameters correctly of the corresponding python script)
- (**verify**) the format of the newly created hdf5 files which should be ready for training a U-Net model (uncertain whether a script (redH5.py) contains code for this, already)
- (**transfer**) the files to the Science Cluster drives (no script for this yet)

## important remarks:

__CAUTION:__ Do ***NOT*** work on one .ijm script in two editors simultaneously (e.g., VS Code and Fiji's built-in editor)! If you do, at some point, Fiji will be 'confused', freeze, and when you force close it with the task manager (or so), Fiji will delete all file contents of the file being changed in the two editors (alternatingly, in my case. I did this, because the VS Code, or most other editors, are way more user-friendly than the Fiji built-in editor, in my opinion (imo)).

## useful Fiji / ImageJ (Macro) links in general:

- [Built-in Macro Functions](https://imagej.nih.gov/ij/developer/macro/functions.html)
- [Combining multiple channels/timepoints into a hyperstack in Fiji](https://cbmf.hms.harvard.edu/avada_faq/fiji-hyperstacks/)

"Fiji" and "Imagej" are used interchangeably as the difference between them would not matter to me, if there was one.

### copied from the BIO321 course - Joana Delgado Martin's fiji hands-on hand-out:

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

## my .ijm scripts (= macros)

In all my scripts, in-line documentation is available.

- `cropTifs-Static.ijm` is a static cropping script. no automatic edge or signal detection is done. x-, y- and z-coordinates for cropping have to be given (i.e., changed) manually in the script.
- `scaleTifs.ijm` is a dynamic script for scaling any set of TIF stacks images in a given folder in x-, y- and z-dimensions. Only the scaling factor is static - specify it in the script somewhere.
- `labelTifsHeart.ijm` is a dynamic script for segmenting the biggest fluorescence signal of a group of TIF stack images. The selection of fluorescence vs. non-fluorescence images is still static, as my string comparison / comprehension skills in .ijm (IJM) are still rudimentary. The value for the threshold segmentation needs to be manually determined in a given image group and statically changed in the script.

### overview over the datasets created

- dataset01 (babb03-ct3-488) babb03? rather babb02, no? and a5, no? QU:
  - babb02 data: 638 nm (fluo), 488 nm QU: TBD verify
- dataset02 (babb03-ct3-405,488,561)
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
- dataset03 (babb03-ct3-405,488,561-body_crop)
  - (temp: the **current** dataset)
  - the dataset in creation starting 2023.08.07 (Monday just after holidays) until ...TBDetermined.
  - the dataset used from ...TBDetermined until ...TBDetermined.
  - the next to-be dataset, where the cropping region only includes the tadpoles' bodies and not the tail - for getting more cube-like images for easier patch shape handling
  - normalised cropping, such that all specimens have the same 3D cropping region.
  - refer to the file [babb03-dataset03-cropping-table.xlsx](https://github.com/radRoy/imageProcessTif/blob/master/babb03-dataset03-cropping-table.xlsx) for the cropping coordinates
  - kinds of image processing performed to get the dataset (& scripts used & relevant folder names in the microscopy image directories)
    - cropping; `cropTifs-Static-dataset03.ijm`; 

- 
  - dataset01
- babb03 data: 638 nm (fluo), 405 nm, 488 nm, 561 nm
  - dataset02
  - dataset03

## outline of the envisioned automated cropping process

__useful links:__  
- high-level Segmentation tutorial (imagej.net): <https://imagej.net/imaging/segmentation#flexible-workflow>
- Creating 3D masks from segmented z-stack, or [Selecting connected pixels in a binary mask in 3D](https://forum.image.sc/t/selecting-connected-pixels-in-a-binary-mask-in-3d/4142/2).

__envisioned process:__  
- downscale images to pre-determined maximal image size (low-quality interpolation should suffice)
- distinguish background from signal (thresholding, pixel brightness distribution cluster analysis, etc.)
- determine 6 coordinates: min & max locations of signal in each x, y, and z dimensions
- export image-wise coordinates into a csv table or similar
- extrapolate back up to original image size, include a boundary, e.g., by extrapolating to the outer pixel locations instead of the middle ones ~
- perform cropping on original images

## comparison of Fiji's built-in thresholding algorithms

Fiji thresholding algorithms ranking by segmentation(label) quality (i.e., whole signal included, noise excluded) (view in Source, not Preview, mode):

thresholding algorithm		transformations, quality
----------------------------------------------------
default  
= Huang  
  
< Li  
= MaxEntropy  
  
<< Intermodes               gauss < gauss 3D (same sigmas)  
= IsoData                   2D < 3D regarding noise exclusion, 2D > 3D regarding signal inclusion  
= IJ_IsoData  
  
< Otsu                      slightly but noticeably better inclusion & exclusion of signal & noise  
(<) Percentile  
= RenyiEntropy  
= Shanbhag  
= Triangle  
= Yen  

## 3D U-Net training data set formatting / creation (HDF5 files)

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