macro_filename = "labelTifsHeart.ijm"
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
inputs = getFilesStripped(dirIn, delim);
extension = ".tif";

// define sigma (standard deviation) for the 3D Gaussian Blurring before thresholding
sigma = 1.0;
sigmaString = "x="+sigma+" y="+sigma+" z="+sigma;

// define the lower threshold value
thresholdMin = 570;

// define suffixes for saving of intermediate output images
preSuffix = "-label";
suffixes = newArray(
	"-blur3D" + sigma,
	"-Otsu" + thresholdMin,
	"-largest");

// create output directories (multiple ones for saving intermediate output images of multiple intermediate steps)
dirParent = truncateString(dirIn, 1);
dirParent = dirParent + preSuffix + "/";
/* // previous version. it was revised to get proper output directory without manual correction after running the script
dirOuts = newArray(
	dirParent + suffixes[0] + "/",
	dirParent + suffixes[0] + suffixes[1] + "/",
	dirParent + suffixes[0] + suffixes[1] + suffixes[2] + "/");*/
suffix0 = suffixes[0];
suffix0 = getCreatedDirectory(dirParent, suffix0);
suffix1 = suffixes[0] + suffixes[1];
suffix1 = getCreatedDirectory(dirParent, suffix1);
suffix2 = suffixes[0] + suffixes[1] + suffixes[2];
suffix2 = getCreatedDirectory(dirParent, suffix2);
dirOuts = newArray(suffix0, suffix1, suffix2);

/*
print("dirParent: " + dirParent);  // testing
print("printing dirOuts iteratively, below:");  // testing
for (i = 0; i < dirOuts.length; i++) {print(dirOuts[i]);}  // testing
for (i = 0; i < dirOuts.length; i++) {File.makeDirectory(dirOuts[i]);}  // creates the directories, if it does not exist. otherwise it does nothing.
exit();  // testing
*/

// create output file list (which is to be progressively extended when iterating over input files)
outputs = Array.copy(inputs);  // to be progressively updated during iterations. enables on-the-go (while only iterating over inputs) and progressively saving of intermediate output images.
outputs = appendSuffix(outputs, preSuffix);  // same as with above usage of preSuffix, but used on the output files to be saved.
//for (i = 0; i < outputs.length; i++) {print(outputs[i]);}  // testing

// specify the number of channels (only the fluo channel is processed in this script (fluo channel is assumed to be the highest wavelength one (i.e., largest number in filename) channel))
n_channels = 4;


/* ITERATIVE IMAGE PROCESSING WITH SAVING OF INTERMEDIATE RESULTS */


// loop over input files to apply image processing steps and save output images
for (i = 0; i < inputs.length; i++)
{
	// proceed only with fluo channel files and inform the user
		// in python, if statement would look like this: `if "638" in filename: ...` - no such thing in .ijm language, TTBOMK
	if (! ((i + 1) % n_channels == 0))
	{
		print("i:"+i+", "+inputs[i]+", skipping non-fluo channel image.");
		continue;
	}
	else {print("i:"+i+", "+inputs[i]+", fluo channel, proceeding with image processing.");}

	// open the fluo channel image
	open(dirIn + inputs[i] + extension);
	
	// 3D blur tif, save as tif afterwards (use sigma 1 in case of babb03 heart stains)
	run("Gaussian Blur 3D...", sigmaString);
	outputs[i] = outputs[i] + suffixes[0];
	//print(dirOuts[0] + outputs[i] + extension);  // testing
	saveAs("Tiff", dirOuts[0] + outputs[i] + extension);
		// saveAs (test not-overwriting input - success)
	
	// threshold (at 570 in case of babb03 heart stains)
	setThreshold(thresholdMin, 65535, "raw");
	run("Convert to Mask", "method=Otsu background=Dark black");
	outputs[i] = outputs[i] + suffixes[1];
	//print(dirOuts[0] + outputs[i] + extension);  // testing
	saveAs("Tiff", dirOuts[1] + outputs[i] + extension);  // use dirOuts[1]
		// saveAs (test not-overwriting input - success)
	
	// connected layer stuff from MLJ plug-in
	run("Connected Components Labeling", "connectivity=6 type=[16 bits]");
	// keep largest label from MLJ plug-in
	run("Keep Largest Label");
	outputs[i] = outputs[i] + suffixes[2];
	//print(dirOuts[0] + outputs[i] + extension);  // testing
	saveAs("Tiff", dirOuts[2] + outputs[i] + extension);  // use dirOuts[2]
		// saveAs (test not-overwriting input - success)
	
	// close all image windows
	close("*");
}


print(""); print("end of program `" +macro_filename+ "` reached."); exit("exit reached.");  // end of program, for easy output reading