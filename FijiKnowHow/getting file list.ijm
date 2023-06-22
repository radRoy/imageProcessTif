print(""); print("start of program"); print("");  // start of program, for easy output reading

/* some useful links:
 *  https://stackoverflow.com/questions/70354753/i-am-trying-to-select-the-last-index-of-a-string-after-splitting-an-image-name-f
 */

dir = getDirectory("");
//print(dir);

files = getFileList(dir);  // gets the names of the files contained in dir, including file extensions

print(""); print("exit reached"); exit("exit reached");  // end of program, for easy output reading

/*
 * for getting file names without file extensions: File.name, File.nameWithoutExtension
 * (see different .ijm for this)
 */