/* Tiff to HDF5 for Pytorch 3D UNet autofluorescence segmentation (proof of concept phase) */
	// Author: Daniel Walther
	// Date of Completion: TBD

/* code TBD
 *  BUILD ON: ~otsuThreshold.ijm for filename and path handling
*/

/* Loop over the stainings of a clearing batch */
	/* loop over the samples of a staining */
		// save the raw data & the labels into one HDF5 file
		
		selectWindow(filename);
		// save to HDF5 (new)
		
		selectWindow(filename + thresholdSuffix + ".tif");
		// save to HDF5 (append)