/* Threshold segmentation of a 3-dimensional (3D) fluorescence microscopy recording */
	// Author: Daniel Walther
	// Date of Completion: 26.4.2023

//open("Y:/Users/DWalther/Muscopy/Copies/BABB2/BABB2.1-a5/babb2-a5-01-638nm-Int50.tiff");
//selectWindow("babb2-a5-01-638nm-Int50.tiff");
pathAbsHome_Prefix = "C:/Users/Dancer/BenchtopImages/BABB2/BABB2.1";  // for working at home
pathAbsLab_Prefix = "Y:/Users/DWalther/Muscopy/Copies/BABB2/BABB2.1";  // for working at the office / lab
clearingExp = "babb2.1-";

size_stains = 2;
stains = newArray(size_stains);  // array containing character strings (the names (abbrev.s) of the immunostaining epitopes)
	stains[0] = "a5";
	stains[1] = "tnnt2";
pathAbsLab_Array = newArray(size_stains);

size_samples = 6;  // sample size of one staining
filenames = newArray(size_samples);

/* Loop over all stainings of a clearing batch */
for (j = 0; j < size_stains; j++) {  // iterating over the immunostainings (epitope) done (in the babb2.1 clearing, 2 stains were made)
	stain = stains[j];
		// not useful for now (25.4.23), first testing the pytorch 3D UNet with the a5 staining (because much stronger signal there)
		// VERBOSE: using this requires adjusting the threshold values, at least, if not also the threshold algorithm, most probably including some additional steps like Gaussian Blur for ~signal amplification, etc. (at worst, requires re taking the images).
	pathAbsLab_Array[j] = pathAbsLab_Prefix + "-" + stain + "/";
	pathAbsLab = pathAbsLab_Array[j];

	/* loop over all samples of the given immunostaining (e.g., BABB2.1-a5-638) 3D recordings for threshold segmentation incl. saving binary output & freeing used memory. */
	/* Threshold segmentation of one 3D fluorescence mesoSPIM / whole mount recording */
	for (i = 0; i < size_samples; i++) {
		filenames[i] = clearingExp + stain + "-0" + (i+1) + "-638nm-Int50.tiff";  // ugly quickfix TBD: better...
			// stains[x] to be adapted/generalised later on.
			// VERBOSE: //filenames[i] = clearingExp + stains[0] + String.format("%.02d", i) + "-638nm-Int50.tiff";  // does not work... String.format is the problem
		filename = filenames[i];
		
		open(pathAbsLab + filename);
		
		// First duplicate it to not overwrite the actual image with your labels (ctrl + shift + D)
		run("Duplicate...", "duplicate");  // duplicates the full stack
		// Open the threshold tool at Image>Adjust>Threshold (ctrl + shift + T), not the 'threshold Default on GPU' or so.
		setAutoThreshold("Otsu dark");
		//run("Threshold...");
		// Set threshold (First look at threshold in the duplicate and compare it with the non-threshold-overlain original image)
		setThreshold(2000, 65535);  // threshold for BABB2-a5-01-638
		// Click on "Apply" in the "Threshold" tool window // Make sure to uncheck the "Calculate threshold for each image" option before running
		setOption("BlackBackground", true);
		run("Convert to Mask", "method=Otsu background=Dark black");
		break; // prevent loop from iterating over all samples of the current stain. (for testing)
		// creates a binary image of pixels above (1) and below (0) the threshold
		
		// => Save the binary image (only 0 and 255 values)
		thresholdSuffix = "-denseOtsu";
		saveAs("Tiff", pathAbsLab + filename + thresholdSuffix);
		
		// REFER TO ANOTHER FILE: save the raw data & the labels into one HDF5 file
			// VERBOSE: the way in which the binary label images may be used in Deep Learning might differ a lot.
			// VERBOSE: so the HDF5 file creation scripts should also be separate
		
		// close the files
		close("*");  // close all image windows
	}

	break; // prevent loop from iterating over all samples of the current clearing batch. (for testing)
}

// -------------------- EOF(code part) --------------------
/* TBD: .ijm syntax
 * lists for looping over filenames / folders
 * (nice to have) navigate through file structures, so filenames do not matter that much
 */
/* TBD: pytorch-3d-unet
 *  In the HDF5 file format given to UNet, is it possible to have only 1 label stack, instead of 2 as with the confocal boundary wolny sample data (labels & labels with ignore)?
 */


//// archive


/* home path, attempt at scriptable HDF5 conversion
selectWindow("babb2-a5-01-638nm-Int50.tiff");
open("C:/Users/Dancer/BenchtopImages/BABB2/BABB2.1-a5/babb2-a5-01-638nm-Int50.tiff");
selectWindow("babb2-a5-01-638nm-Int50.tiff");
run("Duplicate...", "duplicate");

setAutoThreshold("Otsu dark");
//run("Threshold...");
setThreshold(2000, 65535, "raw");
setOption("BlackBackground", true);
run("Convert to Mask", "method=Otsu background=Dark black");

saveAs("Tiff", "C:/Users/Dancer/BenchtopImages/BABB2/BABB2.1-a5/otsuThreshold-binary-babb2-a5-01-638nm-Int50-1.tif");

run("HDF5 (new or replace)...", "save=C:/Users/Dancer/BenchtopImages/BABB2/BABB2.1-a5/labelDenseOtsu-babb2.1-a5-01-638nm-Int50.h5");

run("Save to HDF5 File (append)...", "save=C:/Users/Dancer/BenchtopImages/BABB2/BABB2.1-a5/labelDenseOtsu-babb2.1-a5-01-638nm-Int50.h5");
*/


/* creating labels with gaussian blurring
// Analyze Particles (?) - creating ROIs for each label
// 3D UNet takes image labels where the lables are some non-zero value (1-255), and the wrong pixels have value 0.
// Therefore, I guess the 3D UNet might work with binary images, but will not detect different parts that way. So, for instance, the brain and kidney cells could probably not be differentiated with binary image labels, but probably they both could nonetheless be recognized as the correct signal (i.e., segmented).
*/


/* 
// REFER TO ANOTHER FILE: save the raw data & the labels into one HDF5 file
			// VERBOSE: the way in which the binary label images may be used in Deep Learning might differ a lot.
			// VERBOSE: so the HDF5 file creation scripts should also be separate
			
			//selectWindow(filename);
			// save to HDF5 (new)
			//selectWindow(filename + thresholdSuffix + ".tif");
			// save to HDF5 (append)
 */