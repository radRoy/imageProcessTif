/* useful later:
exit("exit reached");
*/

// get the file list (dynamic array size (number of files, yes))
// btw: directory = getDirectory("Y:/Users/DWalther/Microscopy/babb02.1tnnt2/");
directory = getDirectory("");
print(directory);
files = getFileList(directory);
saves = Array.copy(files);
suffix = "-crop.tif";

for (i = 0; i < files.length; i++) {
	string = split(files[i], ".");
	saves[i] = string[0] + "." + string[1] + suffix;
	print("file i: " + files[i]);
	print("save i: " + saves[i]);
	print("dir + save i: " + directory + saves[i]);
}


// example arrays with the cropping coordinates, this was for 2 channel data (every range is given twice, once for each channel)
zrange = newArray("5-95", "5-95", "5-95", "5-95", "8-98", "8-98", "5-95", "5-95", "4-94", "4-94", "1-91", "1-91");
xoffsets = newArray(990, 990, 1710, 1710, 690, 690, 966, 966, 642, 642, 756, 756);


// unfinished iterative version
/*
for (i = 0; i < 10; i++) {
	open(files[i]);
	run("Duplicate...", "duplicate range=" + zrange[i]);
}
*/


// finished manual version

// a5-01, 488
open(files[0]);
run("Duplicate...", "duplicate range=6-95");
makeRectangle(339, 432, 2556, 3906);
saveAs("Tiff", directory + "babb2.1-a5-01-488nm-Int50-crop-xyz.tiff");
run("Close All");
// a5-01, 638
open(files[1]);
run("Duplicate...", "duplicate range=6-95");
makeRectangle(339, 432, 2556, 3906);
run("Crop");
saveAs("Tiff", "babb2.1-a5-01-638nm-Int50-crop-xyz.tiff");
close();
close();

// a5-02, 488
open(files[2]);
run("Duplicate...", "duplicate range=7-96");
makeRectangle(240, 216, 2556, 3906);   // biggest height(dy)
saveAs("Tiff", "babb2.1-a5-02-488nm-Int50-crop-xyz.tiff");
close();
close();
// a5-02, 638
open(files[3]);
run("Duplicate...", "duplicate range=7-96");
makeRectangle(240, 216, 2556, 3906);   // biggest height(dy)
saveAs("Tiff", "babb2.1-a5-02-638nm-Int50-crop-xyz.tiff");
close();
close();

// a5-03, 488
open(files[4]);
run("Duplicate...", "duplicate range=10-99");
makeRectangle(404, 684, 2556, 3906);
saveAs("Tiff", "babb2.1-a5-03-488nm-Int50-crop-xyz.tiff");
close();
close();
// a5-03, 638
open(files[5]);
run("Duplicate...", "duplicate range=10-99");
makeRectangle(404, 684, 2556, 3906);
saveAs("Tiff", "babb2.1-a5-03-638nm-Int50-crop-xyz.tiff");
close();
close();

// a5-05, 488
open(files[6]);
run("Duplicate...", "duplicate range=1-90");
makeRectangle(399, 390, 2556, 3906);   // biggest width(dx)
saveAs("Tiff", "babb2.1-a5-05-488nm-Int50-crop-xyz.tiff");
close();
close();
// a5-05, 638
open(files[7]);
run("Duplicate...", "duplicate range=1-90");
makeRectangle(399, 390, 2556, 3906);   // biggest width(dx)
saveAs("Tiff", "babb2.1-a5-05-638nm-Int50-crop-xyz.tiff");
close();
close();

// a5-06, 488
open(files[8]);
run("Duplicate...", "duplicate range=3-92");
makeRectangle(282, 447, 2556, 3906);
saveAs("Tiff", "babb2.1-a5-06-488nm-Int50-crop-xyz.tiff");
close();
close();
// a5-06, 638
open(files[9]);
run("Duplicate...", "duplicate range=3-92");
makeRectangle(282, 447, 2556, 3906);
saveAs("Tiff", "babb2.1-a5-06-638nm-Int50-crop-xyz.tiff");
close();
close();