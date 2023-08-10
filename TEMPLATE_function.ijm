/* TEMPLATE FUNCTION REGARDING COMMENT CONVENTIONS */


function fun(x)
{
	/* <function description>
	 * <input arguments> (<type>) : <argument description>
	 * return <variable> (<type>) : <return variable description>
	 */

	y = x**2;
	z = y + x;
	
	return z;  // Array of filePaths (strings with absolute path, filename, and extension)
}


/* EXAMPLE */


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
