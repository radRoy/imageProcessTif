/*
 * daniel walther
 * creation date: 07.11.2023 (dd.mm.yyyy)
 * purpose: create labels for dataset08 which is to be used by the Fiji 2D-UNet Plugin. This plugin requires different forms of labels than Wolny's pytorch-3dunet.
 * 
 * MorphoLibJ Pluging required: https://imagej.net/plugins/morpholibj for installation guide (manage update sites: 'IJBP-plugins')
 */


macro_filename = "labelTifsHeart-dataset08-binaryMasks-noBlur.ijm"
print("-----------------------------------------------------------");
print("start of program `" +macro_filename+ "`"); print("");  // start of program, for easy output reading


/* FUNCTIONS */


function truncateString(s, n)
{
	/* truncates a given string s by n characters (if n is 1, the last character is removed). assumes input arguments are valid & does no checking. */
	s = substring(s, 0, lengthOf(s) - n);
	return s;
}


function getCreatedDirectory(dirIn, suffix)
{
	/* Creates a directory with the same name as the given directory but with a suffix appended to it, and returns the path of it.
	 * dirIn (string) : The input directory containing input files to be processed. has a trailing slash (or backslash).
	 * suffix (string) : The suffix to be appended to the given folder name
	 * return dirOut (string) : The output (or just the created) directory as a string.
	 */

	// create string of the directory to be created
	dirOut = replace(dirIn, "\\", "/");
	dirOut = truncateString(dirOut, 1);  // truncate the folder path by the trailing slash
	dirOut = dirOut + suffix + "/";  // extend the input folder by the suffix

	// create the directory
	File.makeDirectory(dirOut);
	
	// return the string of the created directory
	return dirOut;
}


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


/* PROCEDURES FOR HEART LABEL CREATION */


// get input file list
dirIn = getDir("Choose input directory (contains all images, i.e., all channels)");
delim = ".";
inputs = getFilesStripped(dirIn, delim);  // filenames without paths, without extensions
extension = ".tif";

// define the lower threshold value
thresholdMin = 630;  // dataset08 (no blurring)

// define suffixes for saving of intermediate output images
suffix = "-labelBinary-Otsu" + thresholdMin + "-largest";

// create output directory
dirOut = getCreatedDirectory(dirIn, suffix);  // with trailing slash

/*
print("dirParent: " + dirParent);  // testing
print("printing dirOuts iteratively, below:");  // testing
for (i = 0; i < dirOuts.length; i++) {print(dirOuts[i]);}  // testing
exit();  // testing
*/

// create output file list (which is to be progressively extended when iterating over input files)
outputs = Array.copy(inputs);  // to be progressively updated during iterations. enables on-the-go (while only iterating over inputs) and progressively saving of intermediate output images.
outputs = appendSuffix(outputs, suffix);  // same as with above usage of suffix, but used on the output files to be saved.


/* ITERATIVE IMAGE PROCESSING WITH SAVING OF INTERMEDIATE RESULTS */


// loop over input files to apply image processing steps and save output images
for (i = 0; i < inputs.length; i++)
{
	// assume that only fluorescence images are contained in the chose input folder.
	// open the fluo channel image
	open(dirIn + inputs[i] + extension);
	
	// thresholding
	setThreshold(thresholdMin, 65535, "raw");
	run("Convert to Mask", "method=Otsu background=Dark black");
	
	// connected layer stuff from MLJ plug-in
	run("Connected Components Labeling", "connectivity=6 type=[16 bits]");
	// keep largest label from MLJ plug-in
	run("Keep Largest Label");
	filePath_out = dirOut + outputs[i] + extension;
	print("filePath out:" + filePath_out);  // testing
	
	saveAs("Tiff", filePath_out);
	
	// close all image windows
	close("*");
}


print(""); print("end of program `" +macro_filename+ "` reached."); exit("exit reached.");  // end of program, for easy output reading
