/*
 * daniel walther
 * creation date: 07.11.2023 (dd.mm.yyyy)
 * purpose: create labels for dataset08 which is to be used by the Fiji 2D-UNet Plugin. This plugin requires different forms of labels than Wolny's pytorch-3dunet.
 * 
 * MorphoLibJ Pluging required: https://imagej.net/plugins/morpholibj for installation guide (manage update sites: 'IJBP-plugins')
 */


// define sigma (standard deviation) for the 3D Gaussian Blurring before thresholding
sigma = 1.0;
sigmaString = "x="+sigma+" y="+sigma+" z="+sigma;

// define the lower threshold value
thresholdMin = 570;


// specimen id01

sigma = 1.0;
sigmaString = "x="+sigma+" y="+sigma+" z="+sigma;
run("Gaussian Blur 3D...", sigmaString);

thresholdMin = 570;
setThreshold(thresholdMin, 65535, "raw");
run("Convert to Mask", "method=Otsu background=Dark black");

// connected layer stuff from MLJ plug-in
run("Connected Components Labeling", "connectivity=6 type=[16 bits]");
// keep largest label from MLJ plug-in
run("Keep Largest Label");
