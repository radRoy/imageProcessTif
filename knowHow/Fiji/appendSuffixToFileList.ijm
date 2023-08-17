print(""); print("start of program"); print("");  // start of program, for easy output reading

/* some useful links:
 *  https://stackoverflow.com/questions/70354753/i-am-trying-to-select-the-last-index-of-a-string-after-splitting-an-image-name-f
 */

function appendSuffix(files, suffix)
{
	// Takes Array of strings and returns a copy where the strings have an appended suffix. Intended to be used to create an Array of filenames to save processed images to.
	saves = Array.copy(files);
	for (i = 0; i < files.length; i++) {saves[i] = saves[i] + suffix;}

	print("appendSuffix(): Output filenames created by suffixing the input filenames.");
	return saves;  // Array of output filenames without their path.
}

dir = getDirectory("");
files = getFileList(dir);
suffix = "-suffix";
saves = appendSuffix(files, suffix);  // returns an Array of suffixed filenames with a given file extension appended
for (i = 0; i < saves.length; i++) {print(saves[i]);}  // testing

print(""); print("exit reached"); exit("exit reached");  // end of program, for easy output reading