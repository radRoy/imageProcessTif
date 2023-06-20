open("M:/data/d.walther/Microscopy/babb03/tiff-ct3/TIFF crops/id02-img_Ch638 nm_Angle225.0_Tile2-crop.tif");
selectWindow("id02-img_Ch638 nm_Angle225.0_Tile2-crop.tif");

run("Scale...", "x=.25 y=.25 z=.25 width=293 height=1077 depth=127 interpolation=Bicubic average process create title=[id02-img_Ch638 nm_Angle225.0_Tile2-crop-scaled.25.tif]");
saveAs("Tiff", "M:/data/d.walther/Microscopy/babb03/tiff-ct3/TIFF crops/id02-img_Ch638 nm_Angle225.0_Tile2-crop-scaled.25.tif");

run("Gaussian Blur 3D...", "x=1 y=1 z=1");
saveAs("Tiff", "M:/data/d.walther/Microscopy/babb03/tiff-ct3/TIFF crops/id02-img_Ch638 nm_Angle225.0_Tile2-crop-scaled.25-blured1.tif");

setMinAndMax(229, 1575);
setAutoThreshold("Otsu dark no-reset");
//run("Threshold...");
setThreshold(535, 65535, "raw");
setOption("BlackBackground", true);
run("Convert to Mask", "method=Otsu background=Dark black");
saveAs("Tiff", "M:/data/d.walther/Microscopy/babb03/tiff-ct3/TIFF crops/id02-img_Ch638 nm_Angle225.0_Tile2-crop-scaled.25-blured1-otsu535.tif");

run("Connected Components Labeling", "connectivity=6 type=[16 bits]");
saveAs("Tiff", "M:/data/d.walther/Microscopy/babb03/tiff-ct3/TIFF crops/id02-img_Ch638nm_Angle225.0_Tile2-crop-scaled.25-blured1-otsu535-labels.tif");

run("Keep Largest Label");
saveAs("Tiff", "M:/data/d.walther/Microscopy/babb03/tiff-ct3/TIFF crops/id02-img_Ch638nm_Angle225.0_Tile2-crop-scaled.25-blured1-otsu535-labels-largest.tif");

//<close all>;
