/*
 * author: Daniel Walther
 * creation date: 7.8.2023 (d.m.yyyy)
 * file purpose: crop .tif files from mesospim, used on the "dataset02" in my Master's thesis project.
 *   dataset02 consistently has 4 channels per specimen.
 */

macroName = "cropTifs-Static-dataset02.ijm";
print(""); print("start of program `"+macroName+"`"); print("");  // start of program, for easy output reading


/* FUNCTIONS */


function getFilesStripped (dir, delimiter)
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


/* MANUAL (=STATIC) VALUE INPUT (CROPPING COORDINATES, ETC.) */


// dataset02 (babb03.something) has 7 specimens, with 4 channels each
// z-crop by duplication
zranges_unique = newArray("2-500", "44-542", "35-533", "54-552", "1-499", "13-511", "96-594");
zranges = newArray(zranges_unique[0], zranges_unique[0], zranges_unique[0], zranges_unique[0], zranges_unique[1], zranges_unique[1], zranges_unique[1], zranges_unique[1], zranges_unique[2], zranges_unique[2], zranges_unique[2], zranges_unique[2], zranges_unique[3], zranges_unique[3], zranges_unique[3], zranges_unique[3], zranges_unique[4], zranges_unique[4], zranges_unique[4], zranges_unique[4], zranges_unique[5], zranges_unique[5], zranges_unique[5], zranges_unique[5], zranges_unique[6], zranges_unique[6], zranges_unique[6], zranges_unique[6]);

// x- and y-crop by making rectangle (just the rectangle tool macro)
// x coordinates
xspan = 1657;  // maximal dx of this dataset (TBD)
xoffsets_unique = newArray(659, 1036, 591, 630, 760, 713, 612);
xoffsets = newArray(xoffsets_unique[0], xoffsets_unique[0], xoffsets_unique[0], xoffsets_unique[0], xoffsets_unique[1], xoffsets_unique[1], xoffsets_unique[1], xoffsets_unique[1], xoffsets_unique[2], xoffsets_unique[2], xoffsets_unique[2], xoffsets_unique[2], xoffsets_unique[3], xoffsets_unique[3], xoffsets_unique[3], xoffsets_unique[3], xoffsets_unique[4], xoffsets_unique[4], xoffsets_unique[4], xoffsets_unique[4], xoffsets_unique[5], xoffsets_unique[5], xoffsets_unique[5], xoffsets_unique[5], xoffsets_unique[6], xoffsets_unique[6], xoffsets_unique[6], xoffsets_unique[6]);

// y coordinates
yspan = 4677;  // maximal dx of this dataset (TBD)
yoffsets_unique = newArray(303, 379, 233, 283, 379, 70, 217);
yoffsets = newArray(yoffsets_unique[0], yoffsets_unique[0], yoffsets_unique[0], yoffsets_unique[0], yoffsets_unique[1], yoffsets_unique[1], yoffsets_unique[1], yoffsets_unique[1], yoffsets_unique[2], yoffsets_unique[2], yoffsets_unique[2], yoffsets_unique[2], yoffsets_unique[3], yoffsets_unique[3], yoffsets_unique[3], yoffsets_unique[3], yoffsets_unique[4], yoffsets_unique[4], yoffsets_unique[4], yoffsets_unique[4], yoffsets_unique[5], yoffsets_unique[5], yoffsets_unique[5], yoffsets_unique[5], yoffsets_unique[6], yoffsets_unique[6], yoffsets_unique[6], yoffsets_unique[6]);


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
suffix = "-cropNorm";
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


/* ITERATIVE IMAGE PROCESSING (BABB03 DATASET) */


// ct3 images
// iterating over all images (specimens and channels on the same iterative level)
for (i = 0; i < filePaths.length; i++) {
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
