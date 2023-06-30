// label (label input data) TIF to HDF5 conversion (new file, in this case)

run("Image Sequence...", "open=[M:/data/d.walther/Microscopy/babb03/tiff-ct3/-bicubic-scaled0.25-label-blur3D1-Otsu570-largest/id01-img_Ch638nm-crop-scaled0.25-label-blur3D1-Otsu570-largest - Copy.tif] number=3 file=id01 sort");

run("Stack to Hyperstack...", "order=xyzct channels=3 slices=109 frames=1 display=Composite");
// assume this hyperstack output folder exists
saveAs("Tiff", "M:/data/d.walther/Microscopy/babb03/tiff-ct3/-bicubic-scaled0.25-label-blur3D1-Otsu570-largest-hyperstack/id01-img_Ch638nm-crop-scaled0.25-label-blur3D1-Otsu570-largest-hyperstackComposite.tif");

run("Save to HDF5 File (new or replace)...", "save=M:/data/d.walther/Microscopy/babb03/tiff-ct3/-crop-bicubic-scaled0.25-set6-val.h5");  // /label/channel{c}, where {c} = %d (channel01,02,03)
close();


// autofluo (raw input data) TIF to HDF5 conversion (append to existing, in this case)

run("Image Sequence...", "open=M:/data/d.walther/Microscopy/babb03/tiff-ct3/-bicubic-scaled0.25-autofluo/id01-img_Ch405nm-crop-scaled0.25.tif number=3 file=id01 sort");

run("Stack to Hyperstack...", "order=xyzct channels=3 slices=109 frames=1 display=Composite");
// assume this hyperstack output folder exists
saveAs("Tiff", "M:/data/d.walther/Microscopy/babb03/tiff-ct3/-bicubic-scaled0.25-autofluo-hyperstack/id01-img_Ch405,488,561nm-crop-scaled0.25-hyperstackComposite.tif");

run("Save to HDF5 File (append)...", "save=M:/data/d.walther/Microscopy/babb03/tiff-ct3/-crop-bicubic-scaled0.25-set6-val.h5");  // /raw/channel{c}, where {c} = %d (channel01,02,03)
close();