# imageProcessTif

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://docs.python.org/3.10/index.html)
[![Format](https://img.shields.io/badge/format-TIFF%20|%20HDF5-green.svg)](#input--output-specifications)
[![Target](https://img.shields.io/badge/target-pytorch--3dunet-orange.svg)](https://github.com/wolny/pytorch-3dunet)
[![ImageJ Macro](https://img.shields.io/badge/-Fiji-blue.svg)](https://imagej.net/scripting/macro)


A specialized data preparation and evaluation toolset for 3D light-sheet microscopy ([mesoSPIM](https://mesospim.org/)) image stacks. This repository bridges raw microscopy outputs (TIFF/HDF5) and [3D U-Net](https://github.com/wolny/pytorch-3dunet) deep learning segmentation pipelines for *Xenopus tropicalis* embryonic organs (heart, eye, kidney) using Python, ImageJ Macro (Fiji), Bash scripts and Git and SLURM.

---

## Table of Contents

1. [Overview & Core Capabilities](#overview--core-capabilities)
2. [Data Processing Pipeline](#data-processing-pipeline)
3. [Script Catalog & Architecture](#script-catalog--architecture)
4. [Input & Output Specifications](#input--output-specifications)
5. [Datasets & Experimental Logs](#datasets--experimental-logs)
6. [Setup & Dependencies](#setup--dependencies)
7. [Important Guidelines & Hazards](#important-guidelines--hazards)
8. [Related Repositories & References](#related-repositories--references)

---

## Overview & Core Capabilities

Light-sheet microscopy recordings often produce massive volumetric datasets (> 1 TB) with dimension orders and bit depths incompatible with deep learning frameworks out of the box. `imageProcessTif` provides modular tools to:

- **Format & Reorder Dimensions:** Convert multi-channel microscopy stacks into standard `(C, Z, Y, X)` arrays while preserving 16-bit (`uint16`) dynamic range.
- **Scale & Crop:** Compute isotropic downsampling factors and normalized 3D bounding boxes across multi-session imaging batches.
- **Fluorescence intensity threshold segmentation:** Automatically segment fluorescent objects based on intensity thresholding (`labelTifs.ijm`)
- **HDF5 Container Generation:** Assemble raw channels (`/raw`) and ground-truth segmentation masks (`/label`) into valid HDF5 datasets for `pytorch-3dunet`.
- **Segmentation Benchmarking:** Evaluate model predictions against ground truth using batch IoU (Jaccard Index) threshold sweeps.

---

## Data Processing Pipeline

The workflow operates in sequential stages:

```
[MesoSPIM Output (.h5/.xml)]
             │
             ▼ (BigStitcher Resave)
       [Raw TIFFs]
             │
             ▼ (scaleTifs-dataset.ijm)
     [Scaled TIFFs]
             │
             ▼ (croppingCoordinateCalculation.py / cropTifs.ijm)
     [Cropped TIFFs]
       ┌─────┴──────────────────────────┐
       │                                │
       ▼ (labelTifs.ijm)                ▼ (concatenateChannels.py)
 [Binary Mask (uint8)]        [Multi-Channel Stack (C,Z,Y,X uint16)]
       │                                │
       └────────────────┬───────────────┘
                        │
                        ▼ (writeH5.py)
              [HDF5 Container File]
              ├── /raw   (C, Z, Y, X)
              └── /label (Z, Y, X)
                        │
                        ▼
          [pytorch-3dunet Training]
                        │
                        ▼ (IoU_batch_processor.py)
              [Evaluation / IoU Scores]
```

> 📖 **Detailed Step-by-Step Guide:** Refer to [`docs/pipeline_guide.md`](docs/pipeline_guide.md) for detailed instructions on BigStitcher export, cropping coordinate calculations, and automated thresholding.

---

## Script Catalog & Architecture

The repository is organized into focused, modular scripts:

### 1. Data Preparation & Formatting
- **`concatenateChannels.py`**: Groups single-channel TIFF files by specimen ID, ensures correct channel ordering, and stacks arrays into `(C, Z, Y, X)` uint16 TIFF images.
- **`writeH5.py`**: Creates HDF5 datasets and writes/appends `/raw` and `/label` datasets for 3D U-Net training.
- **`readH5.py`**: Inspects dataset keys, shapes, bit depths, and internal paths inside generated `.h5` files.
- **`croppingCoordinateCalculation.py`**: Calculates normalized 3D bounding box coordinates from spreadsheet metadata with boundary checks.
- **`convertTif16bitTo8bit.py` / `convertTifList16bitTo8bit.py`**: Bit depth conversion utilities.
- **`tifFormatting.py` / `readTifFormatTest.py`**: Validates TIFF shape, dimension ordering, and data type compliance.

### 2. Evaluation & Analysis
- **`IoU_batch_processor.py`**: Evaluates model prediction outputs against ground truth masks across threshold sweeps (0.1–1.0) and outputs YAML summary reports.
- **`yaml_tester.py`**: Inspects and validates evaluation configuration files.
- **`class_label_balance_randomiser.py` / `blinding/blinding.py`**: Utilities for blinded train/val/test splitting and slice balancing.

### 3. Core Libraries & Support Modules
- **`fileHandling.py` / `file_handling/`**: Shared file system utilities (finding files, extracting tokens, batch path management).
- **`list_internal_dependencies.py`**: Static AST analyzer generating [internal-dependencies.md](internal-dependencies.md).

---

## Input & Output Specifications

`pytorch-3dunet` requires exact dimension orders and dataset names:

| Target Dataset | Internal HDF5 Path | Array Shape | Data Type | Description |
|---|---|---|---|---|
| **Raw Input** | `/raw` | `(C, Z, Y, X)` or `(Z, Y, X)` | `uint16` / `float32` | Multi-channel autofluorescence or single-channel fluorescence |
| **Ground Truth** | `/label` | `(Z, Y, X)` | `uint8` | Binary segmentation mask (0 = background, 255 = target) |

*Note: Python-based stacking (`concatenateChannels.py`) must be used instead of Fiji RGB concatenation to avoid irreversible 16-bit to 8-bit downscaling.*

---

## Datasets & Experimental Logs

Over the course of the project, multiple dataset configurations (`dataset01` through `dataset13`) were developed targeting heart (CT3), eye, and kidney (pronephros) segmentations across various voxel resolutions.

> 📊 **Complete Dataset Registry:** See [`docs/datasets.md`](docs/datasets.md) for full metadata tables, voxel sizes (Z, Y, X in µm), train/val/test splits, and experimental objectives for each dataset version.

---

## Setup & Dependencies

### Python Environment
Managed via [`pyproject.toml`](pyproject.toml) or `uv`:

```bash
# Using uv
uv sync

# Or using pip
pip install -r pyproject.toml
```

**Key Python Libraries:**
- `numpy`, `scipy` — Volumetric array manipulation
- `tifffile` — 16-bit multi-channel TIFF I/O
- `h5py` — HDF5 dataset creation and slicing
- `pandas`, `openpyxl` — Coordinate spreadsheets
- `pyyaml` — Benchmark report serialization

### External Software
- **[Fiji / ImageJ](https://fiji.sc/)**: Used with the [`BigStitcher`](https://imagej.net/plugins/bigstitcher) plugin for HDF5-to-TIFF conversion and [`WaltherFiji`](https://github.com/radRoy/WaltherFiji) macros for manual ROI curation.
- **[pytorch-3dunet](https://github.com/wolny/pytorch-3dunet)**: 3D U-Net neural network engine.

---

## Important Guidelines & Hazards

1. **Dimension Ordering:**  
   Always verify with `readTifFormatTest.py` that multichannel data is `(C, Z, Y, X)` before generating HDF5 containers.
2. **Thresholding Methodology:**  
   Otsu thresholding was determined to provide the best signal-to-noise ratio for binary ground-truth creation on Xenopus autofluorescence/fluorescence channels. This is based on a qualitative comparison with other thresholding methods found in Fiji.
3. **Fiji Multi-Editor Hazard (mainly note to myselfa:**  
   Never edit `.ijm` scripts simultaneously in external editors (e.g. PyCharm/VS Code) and Fiji's built-in editor. Concurrent write conflicts can cause Fiji to freeze and truncate file contents.

> 📘 **Fiji Reference & Thresholding Benchmarks:** See [`docs/fiji_reference.md`](docs/fiji_reference.md) for detailed algorithm comparisons and best practices.

---

## Related Repositories & References

- **[radRoy/WaltherFiji](https://github.com/radRoy/WaltherFiji)** — Dedicated ImageJ / Fiji macro library for organ thresholding and ROI creation.
- **[wolny/pytorch-3dunet](https://github.com/wolny/pytorch-3dunet)** — 3D U-Net framework for volumetric medical and biological image segmentation.
- **[mesoSPIM Initiative](https://mesospim.org/)** — Open-source light-sheet microscopy platform.

### Citation
When using Fiji in downstream analysis:
> Schindelin, J., et al. (2012). *Fiji: an open-source platform for biological-image analysis.* Nature Methods, 9(7), 676–682.

### Acknowledgements
- This code repository stems from my MSc thesis at the University of Zurich. Special thanks to the [Lienkamp Lab](https://lienkamplab.org/) and [Centre for Microscopy and Image Analysis](https://www.zmb.uzh.ch/en.html).
- Code refactoring, documentation, and automation assistance provided by **[Junie](https://www.jetbrains.com/)**, an AI coding assistant by JetBrains.

---
**Author:** Daniel Walther  
**Repository Created:** 19.06.2023
