# imageProcessTif

Python & ImageJ Macro scripts for processing `.tif` and `.h5` image files for 3D U-Net training.

**Status:** Currently being cleaned up
**Author:** Daniel Walther
**Created:** 19.06.2023

## Features

- **File conversion:** `.tif` <=> `.h5`
- **Segmentation:** IoU calculation, intensity thresholding
- **Preprocessing:** scaling, cropping, channel concatenation
- **Format:** CZYX for [pytorch-3dunet](https://github.com/wolny/pytorch-3dunet)

## Workflow

1. Convert h5 → tif (BigStitcher)
2. Scale images (`scaleTifs-dataset(...).ijm`)
3. Crop uniformly (`croppingCoordinateCalculation.py`, `cropTifs-Static-dataset(...).ijm`)
4. Label organs (`labelTifsHeart-dataset(...).ijm`)
5. Format channels (`concatenateChannels.py`)
6. Convert to h5 (`writeH5.py`)

## Key Scripts

- `IoU_batch_processor.py` - Jaccard-Index analysis
- `concatenateChannels.py` - Multi-channel formatting
- `writeH5.py` / `readH5.py` - H5 conversion
- `cropTifs-Static-dataset(...).ijm` - Image cropping
- `scaleTifs-dataset(...).ijm` - Image scaling

## Missing

1. Code organization/polish
2. Dependency documentation
3. Usage guides
4. Test datasets
5. SOLID principles adherence

## Related Repos

- [WaltherFiji](https://github.com/radRoy/WaltherFiji) - ImageJ macros (submodule)
- [pytorch-3dunet](https://github.com/wolny/pytorch-3dunet) - 3D U-Net implementation

## Important Notes

- No `main` function - self-contained workflow components
- Use Otsu thresholding for segmentation
- Never edit `.ijm` files in multiple editors simultaneously (Fiji may delete contents)
- Input format: (C, Z, Y, X) for 3dunet

## Citation

When using Fiji:
> Schindelin J, et al. (2012). Fiji: an open-source platform for biological-image analysis. *Nat Methods* 9(7):676-82
