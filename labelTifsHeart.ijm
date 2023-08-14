macro_filename = "labelTifsHeart.ijm"
print("-----------------------------------------------------------");
print("start of program `" +macro_filename+ "`"); print("");  // start of program, for easy output reading


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
dirParent = File.getParent(dirIn) + "/";  // works on files or directories
dirParent = dirParent + preSuffix;  // marking all subsequent output folders with the preSuffix '-label', for easier readability of resulting input & output data folder structure.
dirOuts = newArray(
	dirParent + suffixes[0] + "/",
	dirParent + suffixes[0] + suffixes[1] + "/",
	dirParent + suffixes[0] + suffixes[1] + suffixes[2] + "/");
//for (i = 0; i < dirOuts.length; i++) {print(dirOuts[i]);}  // testing
for (i = 0; i < dirOuts.length; i++) {File.makeDirectory(dirOuts[i]);}  // creates the directories, if it does not exist. otherwise it does nothing.

// create output file list (which is to be progressively extended when iterating over input files)
outputs = Array.copy(inputs);  // to be progressively updated during iterations. enables on-the-go (while only iterating over inputs) and progressively saving of intermediate output images.
outputs = appendSuffix(outputs, preSuffix);  // same as with above usage of preSuffix, but used on the output files to be saved.
//for (i = 0; i < outputs.length; i++) {print(outputs[i]);}  // testing

// specify the number of channels (only the fluo channel is processed in this script (fluo channel is assumed to be the highest wavelength one (i.e., largest number in filename) channel))


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