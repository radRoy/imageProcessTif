function getFilesNoExt (dir, delimiter)
{
	/* Gets the names of the files contained in dir, excluding file extensions. Returns an array of strings.
	 * delimiter :: should be one single character. This program does not work as intended if more than 1 character is specified.
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


// testing

dir = getDirectory("Choose a directory with files containing multiple dots (/ delimiter occurrences) in their filenames");
//print(dir);  // testing
delimiter = ".";
strippedList = getFilesNoExt(dir, delimiter);

for (i = 0; i < strippedList.length; i++)
{
	print(strippedList[i]);
}
