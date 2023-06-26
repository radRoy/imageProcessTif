
run("Image Sequence...", "open=[M:/data/d.walther/Microscopy/babb03/tiff-ct3/-bicubic-scaled0.25-label-blur3D1-Otsu570-largest/id01-img_Ch638nm-crop-scaled0.25-label-blur3D1-Otsu570-largest - Copy (2).tif] number=3 file=id01 sort");

run("Stack to Hyperstack...", "order=xyzct channels=3 slices=109 frames=1 display=Color");
saveAs("Tiff", "M:/data/d.walther/Microscopy/babb03/tiff-ct3/-bicubic-scaled0.25-label-blur3D1-Otsu570-largest/id01-img_Ch638nm-crop-scaled0.25-label-blur3D1-Otsu570-largest-hyperstack.tif");
run("Save to HDF5 File (new or replace)...");
run("Save to HDF5 File (new or replace)...", "save=M:/data/d.walther/Microscopy/babb03/tiff-ct3/-bicubic-scaled0.25-h5-set6-val.h5");
run("Load HDF5 File...");
run("Load HDF5 File...", "open=M:/data/d.walther/Microscopy/babb03/tiff-ct3/-crop-bicubic-scaled0.25-set6-val.h5");
selectWindow("M:\data\d.walther\Microscopy\babb03\tiff-ct3\-crop-bicubic-scaled0.25-set6-val.h5: /raw/channel0");
close();
selectWindow("id01-img_Ch638nm-crop-scaled0.25-label-blur3D1-Otsu570-largest-hyperstack.tif");
close();


