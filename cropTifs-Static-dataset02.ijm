print("");
print("start of file");
print("");


/* PRELIMINARY INFORMATION */


/*
 * author: Daniel Walther
 * creation date: 7.8.2023 (d.m.yyyy)
 * file purpose: crop .tif files from mesospim, used on the "dataset02" in my Master's thesis project.
 *   dataset02 consistently has 4 channels per specimen.
 */


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


/* PROCEDURES FOR CROPPING */


// get input file list
dirIn = getDir("Choose input directory");
delim = ".";
inputs = getFilesStripped(dirIn, delim);
extension = ".tif";

// get the file list (dynamic array size (number of files, yes))
// btw: directory = getDirectory("M:/data/d.walther/Microscopy/babb03/tiff-ct3/");
directory = getDirectory("Choose directory containing .tif images to be cropped");
print("input directory: " + directory);

dirs = split(directory, "\\");
foldername_in = dirs[dirs.length - 1]
print("input folder name (without path): " + foldername_in);
//exit();

dir_out = "";
suffix = "-crop";
for (i = 0; i < (dirs.length - 1); i++) {
	print("dirs[i]: " + dirs[i]);
	
	dir_out = dir_out + dirs[i] + "/";
	}
dir_out = dir_out + foldername_in + suffix + "/"
print("final dir_out: " + dir_out);
//exit();

File.makeDirectory(dir_out);
//exit();

files = getFileList(directory);
file_save_paths = Array.copy(files);
file_suffix = suffix + ".tif";  // already used above for creating the output directory
//exit();

// This loop will iterate over all n_specimens * n_channels files (in dataset02 case: 7 specimens, 4 channels - 28 images)
for (i = 0; i < files.length; i++) {
	string = split(files[i], ".");
	file_save_paths[i] = string[0] + "." + string[1] + file_suffix;
	print("");  // newline readability helper
	print("file i: " + files[i]);
	print("save i: " + file_save_paths[i]);
	print("dir + save i: " + directory + file_save_paths[i]);
}
exit();


/*
// arrays with the cropping coordinates

// dataset02 (babb03.something) has 7 specimens, with 4 channels each
// z-crop by duplication
// the values in ..._unique array need to be determined manually
	// (open images in Fiji and do the things => note coordinates => calculate biggest spanning~ cropping region, etc.)
zranges_unique = newArray(
	"z0,0-z0,1",
	"z1,0-z1,1",
	"z2,0-z2,1",
	"z3,0-z3,1",
	"z4,0-z4,1",
	"z5,0-z5,1",
	"z6,0-z6,1");

zranges = newArray(
	zranges_unique[0],
	zranges_unique[0],
	zranges_unique[0],
	zranges_unique[0],
	zranges_unique[1],
	zranges_unique[1],
	zranges_unique[1],
	zranges_unique[1],
	zranges_unique[2],
	zranges_unique[2],
	zranges_unique[2],
	zranges_unique[2],
	zranges_unique[3],
	zranges_unique[3],
	zranges_unique[3],
	zranges_unique[3],
	zranges_unique[4],
	zranges_unique[4],
	zranges_unique[4],
	zranges_unique[4],
	zranges_unique[5],
	zranges_unique[5],
	zranges_unique[5],
	zranges_unique[5],
	zranges_unique[6],
	zranges_unique[6],
	zranges_unique[6],
	zranges_unique[6]);

// x- and y-crop by making rectangle (just the rectangle tool macro)
// x range coordinates

// TBDetermined manually
xspan = int;  // maximal dx of this dataset
// the values in ..._unique array need to be determined manually
	// (open images in Fiji and do the things => note coordinates => calculate biggest spanning~ cropping region, etc.)
xoffsets_unique = newArray(
	x0,0,
	x1,0,
	x2,0,
	x3,0,
	x4,0,
	x5,0,
	x6,0);
	// integer values
xoffsets = newArray(
	xoffsets_unique[0],
	xoffsets_unique[0],
	xoffsets_unique[0],
	xoffsets_unique[0],
	xoffsets_unique[1],
	xoffsets_unique[1],
	xoffsets_unique[1],
	xoffsets_unique[1],
	xoffsets_unique[2],
	xoffsets_unique[2],
	xoffsets_unique[2],
	xoffsets_unique[2],
	xoffsets_unique[3],
	xoffsets_unique[3],
	xoffsets_unique[3],
	xoffsets_unique[3],
	xoffsets_unique[4],
	xoffsets_unique[4],
	xoffsets_unique[4],
	xoffsets_unique[4],
	xoffsets_unique[5],
	xoffsets_unique[5],
	xoffsets_unique[5],
	xoffsets_unique[5],
	xoffsets_unique[6],
	xoffsets_unique[6],
	xoffsets_unique[6],
	xoffsets_unique[6]);

// y range coordinates

// TBDetermined manually
yspan = int;  // maximal dx of this dataset
// the values in ..._unique array need to be determined manually
	// (open images in Fiji and do the things => note coordinates => calculate biggest spanning~ cropping region, etc.)
yoffsets_unique = newArray(
	y0,0,
	y1,0,
	y2,0,
	y3,0,
	y4,0,
	y5,0,
	y6,0);
	// integer values
yoffsets = newArray(
	yoffsets_unique[0],
	yoffsets_unique[0],
	yoffsets_unique[0],
	yoffsets_unique[0],
	yoffsets_unique[1],
	yoffsets_unique[1],
	yoffsets_unique[1],
	yoffsets_unique[1],
	yoffsets_unique[2],
	yoffsets_unique[2],
	yoffsets_unique[2],
	yoffsets_unique[2],
	yoffsets_unique[3],
	yoffsets_unique[3],
	yoffsets_unique[3],
	yoffsets_unique[3],
	yoffsets_unique[4],
	yoffsets_unique[4],
	yoffsets_unique[4],
	yoffsets_unique[4],
	yoffsets_unique[5],
	yoffsets_unique[5],
	yoffsets_unique[5],
	yoffsets_unique[5],
	yoffsets_unique[6],
	yoffsets_unique[6],
	yoffsets_unique[6],
	yoffsets_unique[6]);
*/

/* dataset02 */
// ct3 images
// iterating over all images (specimens and channels on the same iterative level)
for (i = 0; i < files.length; i++) {
	open(files[i]);
	
	// z-crop by duplication
	range_string = "duplicate range=" + zranges[i];
	run("Duplicate...", range_string);
	
	// x- and y-crop by drawing a rectangle and running "Crop" macro (crops whole z-stack by default)
	makeRectangle(xoffsets[i], yoffsets[i], xspan, yspan);  // width = dx, height = dy
	run("Crop");
	
	saveAs("Tiff", file_save_paths[i]);
	run("Close All");
	
	
	break;  // testing
}


/* dataset01 (old code for reference) */
// a5-01, 488
open(files[0]);
run("Duplicate...", "duplicate range=6-95");
makeRectangle(339, 432, 2556, 3906);
saveAs("Tiff", directory + "babb2.1-a5-01-488nm-Int50-crop-xyz.tiff");
run("Close All");
