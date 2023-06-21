print(""); print("start of program"); print("");  // start of program, for easy output reading

/* some useful links:
 *  https://stackoverflow.com/questions/70354753/i-am-trying-to-select-the-last-index-of-a-string-after-splitting-an-image-name-f
 */

function addSuffixToFileList(files, suffix, fileExtension)
{
	// Takes Array of filenames (including absolute path) and returns a copy where the filenames have an added suffix. Intended to be used to create an Array of filenames to save processed images to.
	saves = Array.copy(files);
	
	for (i = 0; i < files.length; i++)
	{
		string = split(files[i], ".");  // splits input string where any given character occurs and not where the word occurs.
		saves[i] = string[0] + suffix + fileExtension;  // assumes the only "." in the filename is the one preceding the file extension.
	}

	return saves;  // Array of output filenames without their path.
}

dir = getDirectory("");
saveDir = getDirectory("");
//print(directory);

files = getFileList(dir);
suffix = "-suffix";
fileExtension = ".tif";
saves = addSuffixToFileList(files, suffix, fileExtension);  // returns an Array of suffixed filenames with a given file extension appended
for (i = 0; i < saves.length; i++)
{
	print(saves[i]);
}

print(""); print("exit reached"); exit("exit reached");  // end of program, for easy output reading