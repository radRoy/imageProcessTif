print(""); print("start of program"); print("");  // start of program, for easy output reading


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


/* PROCEDURES FOR HEART LABEL CREATION */


// get input file list
dirIn = getDir("Choose input directory");
delim = ".";
inputs = getFilesStripped(dirIn, delim);
extension = ".tif";

// get output file list
dirOut = getDir("Choose output directory");
outputs = Array.copy(inputs);  // to be progressively updated during iterations. enables on-the-go (while only iterating over inputs) and progressively saving of intermediate output images.

// loop over input files to apply image processing steps and save output images
for (i = 0; i < inputs.length; i++)
{
	print("Testing input filename: "+ dirIn + inputs[i] + extension);  // testing

	// proceed only with fluo channel files and inform the user
		// in python, if statement would look like this: `if "638" in filename: ...` - no such thing in .ijm language, TTBOMK
	if (! ((i + 1) % 4 == 0)) {
		print("i:"+i+", "+inputs[i]+", skipping non-fluo channel image."); continue;}
	else {print("i:"+i+", "+inputs[i]+", fluo channel, proceeding with image processing.");}

	// open the fluo channel image
	open(dirIn + inputs[i] + extension);
	
	// blur 3D with sigma 1.0
	// saveAs (test not-overwriting input)
	
	// threshold at 570 (in case of babb03 heart stains)
	// saveAs (test not-overwriting input)
	
	// connected layer stuff from MLJ plug-in
	// keep largest label from MLJ plug-in
	// saveAs (test not-overwriting input)
	
	// close all image windows
	close("*");
}


print(""); print("end of program reached."); exit("exit reached.");  // end of program, for easy output reading