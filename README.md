Daniel Walther
repo creation date: 19.06.2023

# imageProcessTiff

My repository containing mainly ImageJ Macros for processing TIFF files for use with 3D U-Net. The files available from start stem from around 09.05.2023, upon which later IJMacros were built.

## important preliminary remarks:

__CAUTION:__ Do ***NOT*** work on one .ijm script in two editors simultaneously! If you do, at some point, Fiji will be 'confused', freeze, and when you force close it with the task manager (or so), Fiji will delete all file contents of the file being changed in the two editors (alternatingly, in my case. I did this, because the VS Code, or most other editors, are way more user-friendly than the Fiji built-in editor).

## useful Fiji / ImageJ (Macro) links in general:

- [Built-in Macro Functions](https://imagej.nih.gov/ij/developer/macro/functions.html)
- [Combining multiple channels/timepoints into a hyperstack in Fiji](https://cbmf.hms.harvard.edu/avada_faq/fiji-hyperstacks/)

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

- babb02 data: 638 nm (fluo), 488 nm
  - dataset01 was created from babb02 (TBD verify)
- babb03 data: 638 nm (fluo), 405 nm, 488 nm, 561 nm
  - dataset02
    - cropped individually, such that every specimen has its own 3D cropping region.
	  - cropped files were created on the 19.06.2023 (dd.mm.yyyy)
	- 4 channels (1 fluo, 3 autofluo) per specimen
	- refer to the folder [ROIs crop xy (dataset02)](https://github.com/radRoy/imageProcessTif/tree/master/ROIs%20crop%20xy%20(dataset02))
  - dataset03
    - normalised cropping, such that all specimens have the same 3D cropping region.
	- refer to the file [babb03-dataset03-cropping-table.xlsx](https://github.com/radRoy/imageProcessTif/blob/master/babb03-dataset03-cropping-table.xlsx) for the cropping coordinates

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