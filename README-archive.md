Daniel Walther
archived README version creation date: 21.09.2023 (dd.mm.yyyy)

# <u>imageProcessTif</u>

...

## <u>important remarks</u>

...

## <u>conceptual and practical workflow overview</u>

...

### <u>outline of the envisioned automated cropping process</u>

...

### <u>information regarding the input data format required by 3dunet</u>

...

#### <u>input data formatting done with python</u>

...

#### <u>outdated - input data formatting when done with Fiji</u>

**Refer to this repo's `formatTifsHyperstackH5-Recording.ijm` in `FijiRecordings` for a recording on how to format the tifs correctly (TBD: verify).**

**Some detailed information on the *input data formatting* steps that work was previously documented in the [cloud](https://github.com/radRoy/cloud/tree/master)'s README.md repo under [Wrangling with the Input Data Format...](https://github.com/radRoy/cloud/blob/master/README.md#wrangling-with-the-input-data-format-formatting-hdf5-data-sets-for-data-with-multiple-channels-3-autofluorescence-laser-lines-and-the-input-parameters).**  
- Somewhere there, on the date 230710, I found a well-named yaml file **`train_config-RGB24raw,uint16label-230710-1-3in1out-shapeChange.yml` followed by the comment `# successfully trains on the multichannel input data`**. Therefore, 3dunet requires the label input in 16bit per pixel grey format, and the multichannel raw input ... (this appears to be an unfinished note, but it does not matter as the input data formatting problem was solved by writing python scripts (refer to README.md and my python scripts)).

When investigating the format of tif images from dataset02 (where the valid multi-channel input format was determined), I ran my file `imageProcessTif/readTifFormatTest.py` on some images:
- processed (with my **Fiji macros**), non-formatted tif image: `shape: (109, 1102, 371) , image filepath M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo/id01-Ch405nm-crop-scaled0.25.tif`
- after 1st formatting step (concatenating raw input channels with **Fiji built-ins** (reduces 16bit to 8bit per pixel! no fiji work-around found in web)): `shape: (327, 1102, 371) , image filepath M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackSequence/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackSequence.tif`
- after 2nd formatting step (converting the sequence to RGB with **Fiji built-ins**): `shape: (109, 1102, 371, 3) , image filepath M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB.tif`
- after 3rd & final formatting step (changing the image data format to CZYX with **python scripts**): `shape: (3, 109, 1102, 371) , image filepath M:/data/d.walther/Microscopy/babb03/tiff-ct3/dataset02/-crop-bicubic-scaled0.25-autofluo-hyperstackRGB24-czyx/id01-Ch405,488,561nm-crop-scaled0.25-hyperstackRGB-czyx.tif`

## <u>datasets overview</u>

...

## <u>links & information about Fiji / ImageJ (Macro)</u>

...

### <u>copied from the BIO321 course - Joana Delgado Martin's fiji hands-on hand-out</u>

...

### <u>comparison of Fiji's built-in thresholding algorithms</u>

...

#### <u>thresholding algorithm; transformations, quality</u>

...









-------------------------------------- above is ordered and clean ----------------------------

## <u>3D U-Net training data set formatting / creation (HDF5 files)</u>

TBD: Archive this information for documenting how the relevant dataset was created.

TBD: Then, reference this archived text file under the relevant dataset in the **datasets overview** section.

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
