/* INTERACTIVE MACRO SNIPPET */


//<open image>
setTool("rectangle");
waitForUser("Select the cropping region Do the thing. Click OK when done.");
run("Crop");
saveAs("Tiff", "C:/Users/popsicle_cell/Documents/imageProcessTif-crop/interactive_crop_test.tif");
close("*");