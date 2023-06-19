directory = getDirectory("Y:/Users/DWalther/Microscopy/babb02.1a5/raw usable/");
files = getFileList(directory);  // length = 10 in this case

// a5-01, 488
open("C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-01-488nm-Int50.tiff");
run("Duplicate...", "duplicate range=6-95");
makeRectangle(339, 432, 2556, 3906);
saveAs("Tiff", "C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-01-488nm-Int50-cropped.tiff");
close();  
close();  

// a5-01, 638
open("C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-01-638nm-Int50.tiff");
run("Duplicate...", "duplicate range=6-95");
makeRectangle(339, 432, 2556, 3906);
run("Crop");   

saveAs("Tiff", "C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-01-638nm-Int50-cropped.tiff");

close();  
close();  


// a5-02, 488

open("C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-03-488nm-Int50.tiff");
open("C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-05-488nm-Int50.tiff");
open("C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-06-488nm-Int50.tiff");




run("Crop");   

saveAs("Tiff", "C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-02-488nm-Int50-cropped.tiff");
saveAs("Tiff", "C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-03-488nm-Int50-cropped.tiff");
saveAs("Tiff", "C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-05-488nm-Int50-cropped.tiff");
saveAs("Tiff", "C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-06-488nm-Int50-cropped.tiff");

close();  
close();  

// 638

open("C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-02-638nm-Int50.tiff");
open("C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-03-638nm-Int50.tiff");
open("C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-05-638nm-Int50.tiff");
open("C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-06-638nm-Int50.tiff");

run("Duplicate...", "duplicate range=7-96");
makeRectangle(240, 216, 2556, 3906);   // biggest height(dy)
run("Duplicate...", "duplicate range=10-99");
makeRectangle(404, 684, 2556, 3906);
run("Duplicate...", "duplicate range=1-90");
makeRectangle(399, 390, 2556, 3906);   // biggest width(dx)
run("Duplicate...", "duplicate range=3-92");
makeRectangle(282, 447, 2556, 3906);

run("Crop");  


saveAs("Tiff", "C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-02-638nm-Int50-cropped.tiff");
saveAs("Tiff", "C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-03-638nm-Int50-cropped.tiff");
saveAs("Tiff", "C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-05-638nm-Int50-cropped.tiff");
saveAs("Tiff", "C:/Users/Dancer/Documents/BenchtopImages/BABB2/BABB2.1-a5/babb2.1-a5-06-638nm-Int50-cropped.tiff");

close();  
close();  