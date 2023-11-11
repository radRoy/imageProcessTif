/*
 * Daniel Walther
 * Creation Date: 08.11.2023 (dd.mm.yyyy)
 * purpose: Create label overlays on input images, based on binary masks from intensity thresholding.
 *   addition: Creation of 3D segmentation model by training 2Dunet with 2D images: split up z-stacks into 2D .tif images with one slice per image with slices without organ of interest being annotated with an "ignore" ROI overlay.
 * 
 * links:
 *   https://static-content.springer.com/esm/art%3A10.1038%2Fs41592-018-0261-2/MediaObjects/41592_2018_261_MOESM1_ESM.pdf section SN 2.2.1 - 3D paragraph.
 */

/* STATIC INPUT VARIABLES */
// first and last slices that contain label (binary mask of organ of interest) pixels
	// Below values are for cropped and scaled images from the 'raw-cropNorm-bicubic-scaled0.25-fluo' folder from dataset03, with images from tiff-ct3, babb03.
	// The corresponding labels (also relevant for the slice numbers below) are in the 'Y:\Users\DWalther\Microscopy\ dataset08\ raw-cropNorm-bicubic-scaled0.25-fluo-labelBinary-Otsu630-largest' folder.
startSliceList = newArray(30,51,50,39,44,55,46);  // ordered list of above startSlice values of specimens id01 to 07
endSliceList = newArray(67,86,84,76,74,93,74);  // ordered list of above endSlice values of specimens id01 to 07
organLabel = "heart";  // dataset08, babb03-ct3

/* PROCESSING */
run("ROI Manager...");  // initialise the ROI manager (open that window)



for (i = 1; i <= nSlices; i++) {
	Stack.setSlice(i);
	// if(...){ <annotate slice> } else{ <ignore slice> }
	if (i >= startSlice && i <= endSlice) {run("Create Selection");}  // automatically selects all pixels with value 255, just what I need for creating selections of binary organ masks.
		else {run("Select All");}
	roiManager("Add");  // adds the selection to the ROI manager
	roiManager("Select", i - startSlice);  // selecting the just created ROI by index in the ROI manager.
	// if(...){ <annotate slice> } else{ <ignore slice> }
	if (i >= startSlice && i <= endSlice) {roiManager("Rename", organLabel + "#" + toString(i_specimen));}  // renaming that ROI
		// Why the #1? Refer to above linked unet paper by Falk et al section SN 2.2.1
		else {roiManager("rename", "ignore");}
	RoiManager.setPosition(i);  // "Sets the position of the selected selections." Necessary because renaming a ROI somehow removes its slice information.
}

// TBDopen the raw input image to be overlayed.

run("From ROI Manager");  // transfer ROIs to Overlay of current image.
exit("Continue manually. Open the macro you ran for further instructions.");

// 6. saveAs new image with old name plus suffix.
suffix = "-labelBinaryOverlay-Otsu" + thresholdMin + "-largest-" + organLabel;  // 'thresholdMin' from another macro, the other labelTifsHeart-dataset08 one.
	// 'largest' stems from the processing step extracting the largest blob from multiple threshold segmentation masks in one fluorescence image.

close("*");  // 7. close all image windows
roiManager("reset");  // 8. reset Roi Manager (ctrl+a => 'Delete') (delete all rois in the list)
// 9. go to step 1 for next image &/ specimen