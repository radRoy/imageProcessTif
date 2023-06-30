print(""); print("start of program"); print("");  // start of program, for easy output reading

/* some useful links:
 *  https://stackoverflow.com/questions/70354753/i-am-trying-to-select-the-last-index-of-a-string-after-splitting-an-image-name-f
 */

/*
 * preliminary remarks:
 * - the `delimiter` variable should contain 1 character only, not 2 or more. This program does not work as intended, otherwise.
 */

dir = getDirectory("");
//print(dir);  // testing

files = getFileList(dir);  // gets the names of the files contained in dir, including file extensions
delimiter = ".";  // should be one single character. This program does not work as intended if more than 1 character is specified.
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
	print("files[i] :" + files[i]);  // testing
}

print(""); print("exit reached"); exit("exit reached");  // end of program, for easy output reading