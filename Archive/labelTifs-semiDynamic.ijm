// get file dir
directory = getDirectory("");
print(directory);

//files = getFileList(directory);
// <loop over dynamically long list of image files> (solved)
// <truncate file extensions> TBD
	// maybe try split(string, ".tiff"); or similar, where the file extension is treated as the delimiter, thus truncating/omimtting it.
// <add some "editX" suffix> <add back file extension> (solved)

indir = "by.085/";
outdir = "by.085labels/";

files = newArray(
	"babb2.1-a5-01-638nm-Int50-crop-xyz-scaled.tiff",
	"babb2.1-a5-02-638nm-Int50-crop-xyz-scaled.tiff",
	"babb2.1-a5-03-638nm-Int50-crop-xyz-scaled.tiff",
	"babb2.1-a5-05-638nm-Int50-crop-xyz-scaled.tiff",
	"babb2.1-a5-06-638nm-Int50-crop-xyz-scaled.tiff");
saves = newArray(
	"babb2.1-a5-01-638nm-Int50-crop-xyz-scaled-otsu.tiff",
	"babb2.1-a5-02-638nm-Int50-crop-xyz-scaled-otsu.tiff",
	"babb2.1-a5-03-638nm-Int50-crop-xyz-scaled-otsu.tiff",
	"babb2.1-a5-05-638nm-Int50-crop-xyz-scaled-otsu.tiff",
	"babb2.1-a5-06-638nm-Int50-crop-xyz-scaled-otsu.tiff");

for (i = 0; i < files.length; i++) {
	// a5-[i]-638
	open(directory + indir + files[i]);
	run("Duplicate...", "duplicate");
	//setMinAndMax(225, 2128);
	//setAutoThreshold("Otsu dark no-reset");
	//run("Threshold...");
	setThreshold(2000, 65535);
	setOption("BlackBackground", true);
	run("Convert to Mask", "method=Otsu background=Dark black");
	saveAs("Tiff", directory + outdir + saves[i]);
	close("*");
}