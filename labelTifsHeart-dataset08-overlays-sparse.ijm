/*
 * Daniel Walther
 * Creation Date: 08.11.2023 (dd.mm.yyyy)
 * purpose: create label overlays on input images, based on binary masks from intensity thresholding. Change the labelling to sparsely annotated (sparse binary mask label overlay, all other slices should contain a ROI with label "ignore" according to Falk et al paper on unet).
 */


exit("Hang on! Verify that the macro actually does what you want. Then delete this print statement.");


// All slices that should be taken as basis for sparse annotations.

// Below values are for cropped and scaled images from the 'raw-cropNorm-bicubic-scaled0.25-fluo' folder from dataset03, with images from tiff-ct3, babb03.
// The corresponding labels (also relevant for the slice numbers below) are in the 'Y:\Users\DWalther\Microscopy\ dataset08\ raw-cropNorm-bicubic-scaled0.25-fluo-labelBinary-Otsu630-largest' folder.

// specimen id01
slices = newArray(38, 66);  // TBD TBContinued

// specimen id02
//startSlice = 51;
//endSlice = 86;

// specimen id03
//startSlice = 50;
//endSlice = 84;

// specimen id04
//startSlice = 39;
//endSlice = 76;

// specimen id05
//startSlice = 44;
//endSlice = 74;

// specimen id06
//startSlice = 55;
//endSlice = 93;

// specimen id07
//startSlice = 46;
//endSlice = 74;

// 1. comment out all except the wanted specimen id above.
// 2. open and bring to foreground that specimen's binary label .tif image.

// 3. run this macro: iterate through wanted slices create all rois with given label name (e.g. 'heart').
run("ROI Manager...");
organLabel = "heart";  // dataset08, babb03-ct3

// z-size in this batch is 125, normalised cropping (same size for all specimens)
for (i = 0; i < 125; i++) {
	
	Stack.setSlice(i);
	print("slice: " + getSliceNumber());
	run("Create Selection");  // automatically selects all pixels with value 255, just what I need for creating selections of binary organ masks.
	roiManager("Add");  // adds the selection to the ROI manager
	roiManager("Select", i - startSlice);  // selecting the just created ROI by index in the ROI manager.
	roiManager("Rename", organLabel);  // renaming that ROI
	RoiManager.setPosition(i);  // "Sets the position of the selected selections."
}


/* Below is not implemented in macro form, as the actions do not repeat themselves for one image. Above actions do repeat themselves 30 times or so. */


// 4. select the duplicated fluorescence image belonging to the same specimen.
waitForUser("Waiting for User Action", "If you opened the wanted fluorescence image and have it selected, click OK to continue.");
print("continued.");

// 5. transfer the rois from manager to overlay.
// open the input image belonging to the same specimen.
// go to: Image > Overlay > From ROI Manager.
run("From ROI Manager");  // does the same thing.
exit("Continue manually. Open the macro you ran for further instructions.");

// 6. saveAs new image with old name plus suffix.
suffix = "-labelBinaryOverlay-Otsu630-largest-heart";  // used for output folder and output files
suffix = "-labelBinaryOverlay-Otsu630-largest-" + organLabel;  // 'organLabel' from this macro.
suffix = "-labelBinaryOverlay-Otsu" + thresholdMin + "-largest-" + organLabel;  // 'thresholdMin' from another macro, the other labelTifsHeart-dataset08 one.
	// 'largest' stems from the processing step extracting the largest blob from multiple threshold segmentation masks in one fluorescence image.

// 7. close all image windows
close("*");

// 8. reset Roi Manager (ctrl+a => 'Delete') (delete all rois in the list)
roiManager("reset");

// 9. go to step 1 for next image &/ specimen
