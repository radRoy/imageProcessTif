Daniel Walther
repo creation date: 19.06.2023

# imageProcessTiff

My repository containing mainly ImageJ Macros for processing TIFF files for use with 3D U-Net. The files available from start stem from around 09.05.2023, upon which later IJMacros were built.

## outline of the cropping process

- downscale images to pre-determined maximal image size (low-quality interpolation should suffice)
- distinguish background from signal (thresholding, pixel brightness distribution cluster analysis, etc.)
- determine 6 coordinates: min & max locations of signal in each x, y, and z dimensions
- export image-wise coordinates into a csv table or similar
- extrapolate back up to original image size, include a boundary, e.g., by extrapolating to the outer pixel locations instead of the middle ones ~
- perform cropping on original images