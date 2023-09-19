// script for cropping: open all images in a folder with bio-formats importer

macro_filename = "getResolutionsBioFormatsImporter.ijm"
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
	/* Create array of file paths, with extension. Based on a given path (with trailing slash), a given filename list (without extension or trailing dot), and a file extension (with dot).
	Returns a string Array of new file paths. */

	// create output file paths
	newFilePaths = Array.copy(outputs);
	for (i = 0; i < newFilePaths.length; i++)
	{
		newFilePaths[i] = dir + filenames[i] + extension;
	}
	
	return newFilePaths;
}


/* FILE HANDLING */


// get input directory
dirIn = getDir("Choose input directory");

// get input file list (only file names)
delim = ".";
inputs = getFilesStripped(dirIn, delim);  // array of only the file names in the given directory, no path, no extension

// file paths of the input files
filePaths = getFilePaths(dirIn);  // array of the file paths in the given directory, i.e., absolute path, file name, and extension


/* USING BIO-FORMATS IMPORTER ON ALL FILES IN A FOLDER (FOR GETTING THEIR SIZE XYZ) */


for (i = 0; i < filePaths.length; i++)
{	
	// open image with bio-formats importer
	run("Bio-Formats Importer", "open=[" + filePaths[i] + "] color_mode=Default open_files rois_import=[ROI manager] view=[Data Browser] stack_order=XYCZT use_virtual_stack");
	x_size = getWidth();
	y_size = getHeight();
	z_size = nSlices;
	print("xyz size:", x_size+"x", y_size+"y", z_size+"z");
}
//close("*");


print(""); print("end of program `" +macro_filename+ "` reached."); exit("exit reached.");  // end of program, for easy output reading
