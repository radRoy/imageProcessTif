// Cropping an zyx .tiff image

open("Y:/Users/DWalther/Muscopy/babb02/BABB2.1-a5/babb2.1-a5-01-638nm-Int50.tiff");

run("Duplicate...", "duplicate");  // duplicates whole z-stack
//setTool("rectangle");
//run("Brightness/Contrast...");
resetMinAndMax();
run("Enhance Contrast", "saturated=0.35");  // press "Auto"
makeRectangle(678, 864, 1482, 3276);  // adjust the ROI to be cropped to
run("Crop");  // automatically crops the whole z-stack

// save under ../<foldername>-cropped/<filename>-cropped.tiff
saveAs("Tiff", "Y:/Users/DWalther/Muscopy/babb02/BABB2.1-a5-cropped/babb2.1-a5-01-638nm-Int50-cropped.tiff");
close();  // should close the cropped duplicate
close();  // should close the original image

// done.
