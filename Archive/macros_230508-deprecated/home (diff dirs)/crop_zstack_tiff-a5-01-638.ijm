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
