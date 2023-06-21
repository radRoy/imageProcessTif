print(""); print("start of program"); print("");  // start of program, for easy output reading

/* some useful links:
 *  https://stackoverflow.com/questions/70354753/i-am-trying-to-select-the-last-index-of-a-string-after-splitting-an-image-name-f
 */

dir = getDirectory("");
//print(directory);
files = getFileList(dir);
saves = Array.copy(files);

for (i = 0; i < files.length; i++) {
	print(files[i]);
	
	string = split(files[i], ".");  // splits input string where any given character occurs and not where the word occurs.
	/*for (j = 0; j < string.length; j++) {
		print("string[" + j + "] = " + string[j]);
	}*/

	saves[i] = string[0] + "." + string[1] + "-crop-xyz.tiff";
	print("files[i] = " + files[i]);
	print("saves[i] = " + saves[i]);
	print("dir + saves[i] = " + dir + saves[i]);
}

print(""); print("exit reached"); exit("exit reached");  // end of program, for easy output reading