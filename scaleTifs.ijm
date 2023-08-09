/*
 * XY-Downscaling factor = 0.085
 * xy-resolution after scaling = 10.0 um
 * z-resolution before & after scaling (unchanged) = 10.0 um
 */

run("Record...");
macroName = "scaleTifs.ijm";
print(""); print("start of program `"+macroName+"`"); print("");  // start of program, for easy output reading


/* FUNCTIONS */


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
dir = getDirectory("choose dir");
delimiter = ".";
files = getFilesStripped(dir, delimiter);
for (i = 0; i < files.length; i++)
{
	print(files[i]);
}
exit();


function appendSuffix(files, suffix)
{
	// Takes Array of strings and returns a copy where the strings have an appended suffix. Intended to be used to create an Array of filenames to save processed images to.
	saves = Array.copy(files);
	for (i = 0; i < files.length; i++) {saves[i] = saves[i] + suffix;}

	print("appendSuffix(): Output filenames created by suffixing the input filenames.");
	return saves;  // Array of output filenames without their path.
}


/* STATIC INPUT VALUES */


// specify the scaling factor (unsophisticated & neglecting Nyquist-Shannon sampling theorem)
scaling = 0.25;
isotropicScaling = true;
if (isotropicScaling)
{
	xScaling = scaling;
	yScaling = scaling;
	zScaling = scaling;
}
//else: ...not implemented yet - above is easier with an if() condition

// specify interpolation scheme. disclaimer: technically, could also be an extrapolation. but the program differs not.
bilinearInterpolString = "Bilinear average process create";  // "<interpolation scheme> <'average' if yes> <'process' if entire stack> <'create' if create new window'>
bicubicInterpolString = "Bicubic average process create";
interpolString = bicubicInterpolString;
// create a interpolation method variable for below automatic naming of the output folder
if (bicubicInterpolString == bicubicInterpolString) {interpolation = "bicubic";}
else {interpolation = "bilinear";}


/* FILE HANDLING */


// get file paths (input & output) (dialogue)
dir = getDirectory("Choose a folder containing input image(s)");  // choosing folder with input files
dirOut = getDirectory("Choose the parent folder of your output folder (the output folder will be created automatically)");  // choosing folder to save output files to

// create the string of the output directory's name, containing the scaling factor & interpolation scheme
dirOut = dirOut + interpolation + " scaled by " + scaling + "/";

// create the output directory
File.makeDirectory(dirOut);  // creates the directory, if it does not exist. otherwise it does nothing.

// get file list in given path (can specify filetype, or just keep different image data in different folders)
files = getFileList(dir);
suffix = "-scaled" + toString(scaling);
fileExtension = ".tif";
saves = addSuffixToFileList(files, suffix, fileExtension);


/*
 * file handling done saveAs("Tiff", "M:/data/d.walther/Microscopy/babb03/tiff-ct3/save test manual/blobs-2.tif");
 */


print("directory of input files: " + dir);
print("directory of output files: " + dirOut);
// TBD: make a function out of this loop, taking as arguments: Array files, interpolation scheme, Array saves; could also do it with just the in- and output paths
// iteratively scaling all images specified in the Array containing the paths+filenames
for (i = 0; i < files.length; i++)
{
	// open i-th image
	print(dir);
	print(files[i]);
	open(dir + files[i]);
	
	// get image dimensions
	width = 0; height = 0; channels = 0; slices = 0; frames = 0;
	getDimensions(width, height, channels, slices, frames);  // Returns the dimensions of the current image.
	//print(width, height, channels, slices, frames);
	
	// calculate the resolution (=some of the dimensions) after the scaling
		// assumes isotropic scaling
	widthScaled = round(width * scaling);  // new x-resoluion
	heightScaled = round(height * scaling);  // new y-resolution
	depthScaled = round(slices * scaling);  // new z-resolution
	//print(widthScaled, heightScaled, depthScaled);
	
	// concatenating the single argument strings into one big input argument string
	arguments = "x="+xScaling + " y="+yScaling + " z="+zScaling + " width="+widthScaled + " height="+heightScaled + " depth="+depthScaled + " interpolation="+interpolString;
	//print(arguments);
	
	// run the scaling command (no duplication required, will create new image and not overwrite)
	run("Scale...", arguments);
	saveAs("Tiff", dirOut + saves[i]);
	
	// close the scaled and unscaled images
	close("*");

	// give message to the user, informing him of the file having been saved
	print("A file has been saved. filename: " + saves[i]);
}


print(""); print("end of program `"+macroName+"`, exit reached"); exit("exit reached");  // end of program, for easy output reading