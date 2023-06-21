/* useful links:
 *  c#, nevermind, then. leaving the link here, though:
 *  	https://stackoverflow.com/questions/4048185/read-a-tiff-files-dimension-and-resolution-without-loading-it-first
 *  javascript, but on github, maybe add to plug-ins (inludes consideration of the Nyquist-Shannon sampling theorem & looks like it accounts for sampling artefacts before downscaling(=downsampling)):
 *  	https://imagej.net/tutorials/downsample
 */

//open("M:\data\d.walther\Microscopy\babb03\tiff-ct3\TIFF 638 downscaled by 4\id01-img_Ch638nm-crop-downscaled,4-xyz.tif");
open("M:/data/d.walther/Microscopy/babb03/tiff-ct3/TIFF 638 downscaled by 4/id01-img_Ch638nm-crop-downscaled,4-xyz.tif");

width = 0; height = 0; channels = 0; slices = 0; frames = 0;
// getDimensions() requires: an opened image (tif works), variables to fill (like on preceding line)
getDimensions(width, height, channels, slices, frames);  // getDimensions(width, height, channels, slices, frames): Returns the dimensions of the current image. (DW: in unknown format...)
	// refer to online documentation of all functions: https://imagej.nih.gov/ij/developer/macro/functions.html

print(width, height, channels, slices, frames);
exit("exit reached");