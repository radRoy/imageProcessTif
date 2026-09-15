# Practical & Conceptual Pipeline Guide

This guide describes the end-to-end data processing workflow for preparing large light-sheet microscopy (mesoSPIM) recordings for 3D U-Net segmentation.

---

## High-Level Processing Flow

```
[Microscope HDF5 / XML]
        │
        ▼ (BigStitcher Resave)
   [TIFF Images]
        │
        ▼ (scaleTifs-dataset.ijm)
 [Scaled TIFF Images]
        │
        ▼ (croppingCoordinateCalculation.py / cropTifs.ijm)
 [Cropped TIFF Images]
   ┌────┴──────────────────────────┐
   │                               │
   ▼ (labelTifs.ijm)               ▼ (concatenateChannels.py)
[Binary Mask Labels]       [Multichannel Autofluo (C,Z,Y,X)]
   │                               │
   └───────────────┬───────────────┘
                   │
                   ▼ (writeH5.py)
         [HDF5 Container File]
         ├── /raw   (C, Z, Y, X - uint16)
         └── /label (Z, Y, X - uint8)
                   │
                   ▼
     [pytorch-3dunet Training & Evaluation]
                   │
                   ▼ (IoU_batch_processor.py)
         [Jaccard Index / Evaluation]
```

---

## Step-by-Step Workflow

### 1. H5 to TIFF Conversion (BigStitcher)
- **Tool:** Fiji plugin `Plugins > BigStitcher > BigStitcher`.
- **Input:** Microscope `.h5` file accompanied by `.xml` metadata.
- **Procedure:**
  1. Open XML dataset in BigStitcher (`MultiView` mode).
  2. Select target tile/channel images to export.
  3. Right-click and choose `Resave > Resave as TIFF`.
  4. Naming convention should preserve sample ID and laser channel (e.g., `id01_Ch405.tif`).

### 2. Resolution Scaling
- **Script:** `scaleTifs-dataset(...).ijm`
- **Objective:** Downscale raw high-resolution stacks (e.g. from 0.85 × 0.85 × 2.0 µm³ to isotropic 5.784 µm³ or target resolution) to manage GPU VRAM and fit patches during training.
- **Key Consideration:** Match spatial resolution across different microscope recording batches before pooling into a single training dataset.

### 3. Cropping & ROI Calculation
- **Scripts:** `croppingCoordinateCalculation.py`, `cropTifs-Static-dataset(...).ijm`
- **Uniform vs. Individual Cropping:**
  - **Normalized Cropping:** Standardizes bounding box dimensions across all specimens in a dataset.
  - **Isometric Uncropped:** Newer datasets (e.g., `dataset10`, `dataset11`) scale isometrically without tight bounding box cropping, relying on `pytorch-3dunet`'s patch extraction sampler.
- **Coordinate Calculation:**
  - `croppingCoordinateCalculation.py` reads specimen bounding boxes from an Excel spreadsheet, computes normalized bounding boxes with boundary safety margins, and outputs updated coordinates.

#### Envisioned Automated Cropping Process
1. Downscale raw images using fast interpolation.
2. Segment foreground from background via automated thresholding.
3. Compute 3D extents (min/max in X, Y, Z).
4. Identify organ centers of mass / peak intensity via 3D Gaussian filtering.
5. Export coordinate bounds to CSV/XLSX using `pandas`.
6. Scale bounding coordinates back to full-resolution images with boundary buffers.

### 4. Binary Organ Labeling (Ground Truth)
- **Tools:** Fiji / ImageJ macros in [`WaltherFiji`](https://github.com/radRoy/WaltherFiji)
- **Method:**
  - Apply Otsu automated intensity thresholding on the specific fluorescence channel (e.g., 638 nm for CT3 heart stain).
  - Convert binary threshold masks to ROI overlays (`binary_to_overlay.ijm`).
  - Perform manual brush curation where necessary to isolate organ boundaries from nonspecific background staining.
  - Export final masks as 8-bit binary TIFF stacks (`uint8`, values 0 and 255).

### 5. Channel Concatenation & Dimension Ordering
- **Script:** `concatenateChannels.py`
- **Critical Requirement:** `pytorch-3dunet` requires multi-channel inputs structured in **`(C, Z, Y, X)`** format.
- **Python Processing Advantages:**
  - Preserves full **16-bit (`uint16`)** dynamic range (Fiji RGB concatenation forces 8-bit reduction).
  - Groups single-channel TIFF files by specimen ID and stacks them into shape `(C, Z, Y, X)` deterministically.

### 6. HDF5 File Assembly
- **Script:** `writeH5.py`
- **Structure:**
  - `/raw`: Multi-channel raw autofluorescence or fluorescence image stack (`uint16`, shape `(C, Z, Y, X)` or `(Z, Y, X)`).
  - `/label`: Ground truth binary segmentation mask (`uint8`, shape `(Z, Y, X)`).
- **Execution:** Run `writeH5.py` to create the HDF5 containers with `/raw` datasets, then append `/label` datasets.

### 7. Evaluation & IoU Benchmark
- **Script:** `IoU_batch_processor.py`
- **Metric:** Jaccard Index (Intersection over Union, IoU) computed across predicted probability volumes against ground truth binary masks.
- **Features:** Batch processing across prediction directories, threshold sweeps (0.1–1.0), and YAML score summary exports.
