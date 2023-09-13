/*
 * TEMPORARY NOTE FOR THE SCALING INVOLVED IN DATASET01 (FROM BABB2.1)
 * XY-Downscaling factor = 0.085
 * xy-resolution after scaling = 10.0 um
 * z-resolution before & after scaling (unchanged) = 10.0 um
 */


macroName = "scaleTifs-dataset05-babb02.1.ijm";
print("-----------------------------------------------------------");
print("start of program `"+macroName+"`"); print("");  // start of program, for easy output reading


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


function getFilesStripped(dir, delimiter)
{
	/* Gets the names of the files contained in dir, excluding file extensions & excluding files' path. Returns an array of strings.
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


function getFilePaths(directory)
{
	
	/* Takes a path as a string and returns the absolute file paths as an array.
	 * directory (string) : the chosen directory containing some files. has a trailing slash (or backslash).
	 * return filePaths (string Array) : an array of strings of the file paths (with absolute path, filename, and extension).
	 */

	files = getFileList(directory);
	filePaths = Array.copy(files);
	for (i = 0; i < files.length; i++)
	{
		filePaths[i] = directory + files[i];
	}
	
	return filePaths;  // Array of filePaths (strings with absolute path, filename, and extension)
}


function appendSuffix(files, suffix)
{
	// Takes Array of strings and returns a copy where the strings have an appended suffix. Intended to be used to create an Array of filenames to save processed images to.
	saves = Array.copy(files);
	for (i = 0; i < files.length; i++) {saves[i] = saves[i] + suffix;}

	print("appendSuffix(): Output filenames created by suffixing the input filenames.");
	return saves;  // Array of output filenames without their path.
}


function createOutputFilePaths(dir, filenames, extension)
{
	/* Create array of file paths, with extension. Based on a given filename list, a given path, a suffix, and a file extension.
	Returns a string Array of new file paths. */

	// create output file paths
	newFilePaths = Array.copy(outputs);
	for (i = 0; i < newFilePaths.length; i++)
	{
		newFilePaths[i] = dir + filenames[i] + extension;
	}
	
	return newFilePaths;
}


/* STATIC INPUT VALUES (ALSO NEEDED IN FILE HANDLING) */


// specify the scaling factor (unsophisticated & neglecting Nyquist-Shannon sampling theorem)
// dataset05: babb02.1 scaling factors (to arrive at voxel size of 2.53 x 2.53 x 10 (xyz))
xScaling = 0.335968379
yScaling = 0.335968379
zScaling = 1

// specify interpolation scheme. disclaimer: technically, could also be an extrapolation. but the program differs not.
bilinearInterpolString = "Bilinear average process create";  // "<interpolation scheme> <'average' if yes> <'process' if entire stack> <'create' if create new window'>
bicubicInterpolString = "Bicubic average process create";
interpolString = bicubicInterpolString;
// create a interpolation method variable for below automatic naming of the output folder
if (interpolString == bicubicInterpolString) {interpolation = "bicubic";}
else {interpolation = "bilinear";}
// variable 'interpolation' is to be used as a string argument for a macro.


/* FILE HANDLING */


// get input directory
dirIn = getDir("Choose input directory");


// output directory (saving the output files here), has the same folder name as the input directory but with an added suffix
suffix = "-scaled";
scaledByString = "-" + toString(xScaling) + "x-" + toString(yScaling) + "y-" + toString(zScaling) + "z";
suffix = "-" + interpolation + suffix + scaledByString;
dirOut = getCreatedDirectory(dirIn, suffix);

// get input file list (only file names)
delim = ".";
inputs = getFilesStripped(dirIn, delim);  // array of only the file names in the given directory, no path, no extension

// file paths of the input files
filePaths = getFilePaths(dirIn);  // array of the file paths in the given directory, i.e., absolute path, file name, and extension

// output file names
outputs = appendSuffix(inputs, suffix);

// output file paths (saving as these file paths)
extension = ".tif";
outputFilePaths = createOutputFilePaths(dirOut, outputs, extension);


/*
 * file handling done saveAs("Tiff", "M:/data/d.walther/Microscopy/babb03/tiff-ct3/save test manual/blobs-2.tif");
 */


print("directory of input files: " + dirIn);
print("directory of output files: " + dirOut);
// TBD: make a function out of this loop, taking as arguments: Array files, interpolation scheme, Array saves; could also do it with just the in- and output paths
// iteratively scaling all images specified in the Array containing the paths+filenames
for (i = 0; i < filePaths.length; i++)
{
	// open i-th image
	print("opening image "+i+": " + filePaths[i]);
	//print("to be saved image "+i+": " + outputFilePaths[i]);
	open(filePaths[i]);
	
	// get image dimensions
	width = 0; height = 0; channels = 0; slices = 0; frames = 0;
	getDimensions(width, height, channels, slices, frames);  // Returns the dimensions of the current image.
	print("Image dimensions:");
	print(width, height, channels, slices, frames);
	
	// calculate the resolution (=some of the dimensions) after the scaling
		// assumes isotropic scaling
	widthScaled = round(width * xScaling);  // new x-resoluion
	heightScaled = round(height * yScaling);  // new y-resolution
	depthScaled = round(slices * zScaling);  // new z-resolution
	//print(widthScaled, heightScaled, depthScaled);
	
	// concatenating the single argument strings into one big input argument string
	arguments = "x="+xScaling + " y="+yScaling + " z="+zScaling + " width="+widthScaled + " height="+heightScaled + " depth="+depthScaled + " interpolation="+interpolString;
	//print(arguments);
	
	// run the scaling command (no duplication required, will create new image and not overwrite)
	run("Scale...", arguments);
	saveAs("Tiff", outputFilePaths[i]);
	
	// close the scaled and unscaled images
	close("*");

	// give message to the user, informing him of the file having been saved
	print("A file has been saved. filename: " + outputFilePaths[i]);
}


print(""); print("end of program `"+macroName+"`, exit reached"); exit("exit reached");  // end of program, for easy output reading