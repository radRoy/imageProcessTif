/*
 * author: Daniel Walther
 * creation date: 18.09.2023 (dd.mm.yyyy)
 * file purpose: crop .tif files from mesospim, used on the "dataset05" in my Master's thesis project.
 *   dataset05 has 2 channels per specimen, 488nm autofluorescence and 638nm fluorescence channel.
 *   dataset05 has normalised cropping regions, i.e., all specimens are cropped to the same 3D image size.
 */

macroName = "cropTifs-Static-dataset05-no_tail.ijm";
print(""); print("start of program `"+macroName+"`"); print("");  // start of program, for easy output reading


/* FUNCTIONS */


function getFilesStripped(dir, delimiter)
{
	/* Gets the names of the files contained in dir, excluding file extensions. Returns an array of strings.
	 *  dir :: string of the absolute path that the user wants a file list from
	 *  delimiter :: should be one single character (e.g., `.`). This program does not work as intended if more than 1 character is specified.
	 */
	
	files = getFileList(dir);  // Array of filenames WITH file extensions
	for (i = 0; i < files.length; i++)
	{
		//print("i: " + i);  // testing
		file = split(files[i], delimiter);
		//print("file length: " + toString(file.length));  // testing
	
		nameNoExt = "";
		for (j = (file.length - 2); j >= 0; j--)
		{
			//print("  j: " + j);  // testing
			if (nameNoExt == "") {nameNoExt = file[j] + nameNoExt;}
			else {nameNoExt = file[j] + delimiter + nameNoExt;}
			//print("    nameNoExt: " + nameNoExt);  // testing
		}
		
		files[i] = nameNoExt;
		//print("files[i] :" + files[i]);  // testing
	}

	return files;  // Array of filenames WITHOUT file extensions
}


function appendSuffix(files, suffix)
{
	// Takes Array of strings and returns a copy where the strings have an appended suffix. Intended to be used to create an Array of filenames to save processed images to.
	saves = Array.copy(files);
	for (i = 0; i < files.length; i++) {saves[i] = saves[i] + suffix;}

	print("appendSuffix(): Output filenames created by suffixing the input filenames.");
	return saves;  // Array of output filenames without their path.
}


function duplicateArrayElements(array, n_duplicates)
{
	duplicateArray = newArray(n_duplicates * array.length);
	for (i = 0; i < array.length; i++)
	{
		// zranges = newArray(zranges_unique[0], zranges_unique[0], zranges_unique[0], zranges_unique[0], zranges_unique[1], zranges_unique[1], zranges_unique[1], zranges_unique[1], zranges_unique[2], zranges_unique[2], zranges_unique[2], zranges_unique[2], zranges_unique[3], zranges_unique[3], zranges_unique[3], zranges_unique[3], zranges_unique[4], zranges_unique[4], zranges_unique[4], zranges_unique[4], zranges_unique[5], zranges_unique[5], zranges_unique[5], zranges_unique[5], zranges_unique[6], zranges_unique[6], zranges_unique[6], zranges_unique[6]);
		for (j = 0; j < n_duplicates; j++)
		{
			k = i*n_duplicates + j;
			duplicateArray[k] = array[i];
			// print(array[i], "=", duplicateArray[k]);
		}
	}
	return duplicateArray;
}


/* MANUAL (=STATIC) INPUT VALUES (E.G., CROPPING COORDINATES, ETC.) */
// data (coordinates and stack no.s) are taken from .py-filled excel tables named 'dataset05-...xlsx'


/* // dataset05 (babb02.1 and babb03, both ct3) has 13 specimens, with 2 channels each (488) nm autofluo., 638 nm fluo.);*/
n_channels = 2;

// z-crop by duplication
	// order: babb02.1 id01-06, babb03 id01-07
zranges_unique = newArray("30-79", "31-80", "19-68", "37-86", "20-69", "19-68", "1-50", "6-55", "6-55", "8-57", "1-50", "1-50", "11-60");
	// these ranges are the table ranges (z0_check-z1_check), but added 1 to those coordinates. Fiji takes stack no. here (starting at 1), whereas I calculated the z-coordinates (starting at 0).
zranges = duplicateArrayElements(zranges_unique, n_channels);

// x- and y-crop by making rectangle (just the rectangle tool macro)
// x coordinates
xspan = 467;  // dx_norm of this dataset
xoffsets_unique = newArray(260, 487, 256, 265, 313, 213, 426, 503, 378, 423, 384, 495, 339);
xoffsets = duplicateArrayElements(xoffsets_unique, n_channels);

// y coordinates
yspan = 902;  // dy_norm of this dataset
yoffsets_unique = newArray(167, 116, 106, 217, 204, 45, 1051, 1093, 1055, 1056, 1084, 976, 1071);
yoffsets = duplicateArrayElements(yoffsets_unique, n_channels);


/* FILE HANDLING */


// get input file names
dirIn = getDir("Choose input directory");
delim = ".";
inputs = getFilesStripped(dirIn, delim);

// get input file list (file paths)
filePaths = Array.copy(inputs);
extension = ".tif";
for (i = 0; i < filePaths.length; i++)
{
	filePaths[i] = dirIn + inputs[i] + extension;
}

// create output filenames
suffix = "-cropNorm-no_tail";
outputs = Array.copy(inputs);
outputs = appendSuffix(outputs, suffix);

// create output directory
dirs = split(dirIn, "\\");
foldername_in = dirs[dirs.length - 1]
dirParent = File.getParent(dirIn) + "/";  // works on files or directories
dirOut = dirParent + foldername_in + suffix + "/";
File.makeDirectory(dirOut);  // does nothing if already exists. slash & backslash mixed works, too.

// create output file paths
savePaths = Array.copy(outputs);
for (i = 0; i < savePaths.length; i++)
{
	savePaths[i] = dirOut + outputs[i] + extension;
}


/* ITERATIVE IMAGE PROCESSING (A BABB03 DATASET) */


// babb03-ct3 images
// iterating over all images (specimens and channels on the same iterative level)
for (i = 0; i < filePaths.length; i++) {

	// Opening the .tif file
	print("Opening file, i="+i+". filename = " + inputs[i]);
	open(filePaths[i]);

	// z-crop by duplication
	range_string = "duplicate range=" + zranges[i];
	run("Duplicate...", range_string);
	
	// x- and y-crop by drawing a rectangle and running "Crop" macro (crops whole z-stack by default)
	makeRectangle(xoffsets[i], yoffsets[i], xspan, yspan);  // width = dx, height = dy
	run("Crop");
	
	saveAs("Tiff", savePaths[i]);
	print("File saved as: " + savePaths[i]);
	run("Close All");
}


print(""); print("end of program `"+macroName+"` reached."); exit("exit reached.");  // end of program, for easy output reading


/* ALTERNATIVE CODE SNIPPETS */


// alternative: create output directory, but all dir delimiters are slashes, not mixed with backslashes
/*dirOut = "";
for (i = 0; i < (dirs.length - 1); i++) {
	//print("dirs[i]: " + dirs[i]);  // testing
	dirOut = dirOut + dirs[i] + "/";
	}
dirOut = dirOut + foldername_in + suffix + "/"*/
