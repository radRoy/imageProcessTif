directory = getDirectory("");
//print(directory);
files = getFileList(directory);
saves = Array.copy(files);
for (i = 0; i < files.length; i++) {
	string = split(files[i], ".");
	saves[i] = string[0] + "." + string[1] + "-crop-xyz.tiff";
	//print(files[i]);
	//print(saves[i]);
	//print(directory + saves[i]);
}

zrange = newArray("5-95", "5-95", "5-95", "5-95", "8-98", "8-98", "5-95", "5-95", "4-94", "4-94", "1-91", "1-91");
for (i = 0; i < zrange.length; i++) {
	print("duplicate range=" + zrange[i]);
}
