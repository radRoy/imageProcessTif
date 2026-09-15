# Datasets Registry & Overview

This document catalogs the datasets (`dataset01` through `dataset13`) used and produced during light-sheet microscopy (mesoSPIM) image processing and 3D U-Net segmentation experiments for *Xenopus tropicalis* embryonic organs (heart, eye, kidney).

---

## Voxel Dimension & Metadata Summary

> **Important Note on Voxel Sizes:**  
> MesoSPIM `babb03` recording raw voxel sizes (Z, Y, X) are **2.0, 0.85, 0.85 µm**. Previous conversions via BigDataViewer suffered from metadata discrepancy. Ensure voxel sizes are verified for combined cross-session datasets.

| Dataset | Sample / Batch | Staining / Target | Laser Channels (nm) | Raw Voxel Size (Z,Y,X µm) | Processed Voxel Size (Z,Y,X µm) | Cropping Strategy | Train/Val/Test Split |
|---|---|---|---|---|---|---|---|
| **dataset01** | babb02.1 / babb03 | Heart (CT3) | 638 (fluo), 488 | 10.0, 0.85, 0.85 | Varies | Individual | - |
| **dataset02** | babb03-ct3 | Heart (CT3) | 638 (fluo), 405, 488, 561 | 2.0, 0.85, 0.85 | 10.0, 10.0, 10.0 | Individual per specimen | - |
| **dataset03** | babb03-ct3 | Heart (CT3) | 638 (fluo), 405, 488, 561 | 2.0, 0.85, 0.85 | 8.0, 3.4, 3.4 | Normalized 3D crop | 3 / 2 / 2 (id01-03 / 04-05 / 06-07) |
| **dataset04** | babb03-ct3 | Heart (CT3) | 638 (fluo), 405, 488, 561 | 2.0, 0.85, 0.85 | 8.0, 3.4, 3.4 | Normalized 3D crop | 5 / 1 / 1 (sub-versions a, b, c) |
| **dataset05** | babb02.1 + babb03 | Heart (CT3) | 638 (fluo), 488 | 10.0, 0.85, 0.85 / 2.0, 0.85, 0.85 | ~10.0, 2.53, 2.53 | Normalized (no tail / whole) | Pooled sample |
| **dataset06** | babb03-ct3 | Heart (VRAM study) | 405, 488, 561 (varies) | 2.0, 0.85, 0.85 | 8.0, 3.4, 3.4 | Normalized whole body | 5 / 1 / 1 |
| **dataset07** | babb03-ct3 | Heart (Control) | 638 (fluo only) | 2.0, 0.85, 0.85 | 8.0, 3.4, 3.4 | Normalized whole body | 5 / 1 / 1 |
| **dataset08** | babb03-ct3 | Heart (2D U-Net) | 638 (fluo), autofluo | 2.0, 0.85, 0.85 | 8.0, 3.4, 3.4 | 2D slices with overlay | 5 / 2 (id01-05 / 06-07) |
| **dataset09** | babb03-ct3 | Eye (Proof of Concept) | 405, 488, 561 | 2.0, 0.85, 0.85 | Scaled | Manual eye ROI | 5 / 1 / 1 (n=7) |
| **dataset10** | babb03-ct3 | Eye (Isometric) | 405, 488, 561 (or 638) | 2.0, 0.85, 0.85 | 5.784, 5.784, 5.784 (isometric) | Uncropped (full volume) | 5 / 1 / 1 (sub-versions a, b, c) |
| **dataset11** | babb03-a5 | Kidney (Pronephros) & Eye | Autofluo + Stain | 2.0, 0.85, 0.85 | 5.784, 5.784, 5.784 (isometric) | Uncropped | Randomized blinded split |
| **dataset12** | babb03-col2a1 | Cartilage (Col2a1) | Autofluo + Stain | 2.0, 0.85, 0.85 | 5.784, 5.784, 5.784 (isometric) | Uncropped | In progress |
| **dataset13** | babb03-ct3 & a5 | Eye + Kidney (Multi-organ) | 488 nm / Multi-channel | 2.0, 0.85, 0.85 | 5.784, 5.784, 5.784 (isometric) | Uncropped | Multi-organ prediction |

---

## Detailed Dataset Descriptions

### dataset01 (`babb03-ct3-488`)
- **Stains & Channels:** 638 nm (fluorescence - CT3 heart), 488 nm (autofluorescence).
- **Origin:** Early pilot data combining babb02.1 and babb03.

### dataset02 (`babb03-ct3-405,488,561`)
- **Status:** Deprecated (kept for historical reference).
- **Voxel Size:** 10 × 10 × 10 µm³ (scaled by 0.085, 0.085, 1).
- **Channels:** 4 channels (638 nm fluo, 405/488/561 nm autofluorescence).
- **Cropping:** Individual 3D cropping regions per specimen (see `ROIs crop xy (dataset02)`).
- **Processing Issues:** Concatenation via Fiji RGB24 forced 16-bit to 8-bit reduction and distorted dimension order. Replaced by Python-based pipeline in subsequent datasets.

### dataset03 (`babb03-ct3-405,488,561-normCrop`)
- **Voxel Size:** 8.0 × 3.4 × 3.4 µm³ (scaling factor: 0.25 on babb03 raw 2.0, 0.85, 0.85 µm).
- **Channels:** 405, 488, 561 nm (autofluorescence) + 638 nm (fluorescence heart label).
- **Cropping:** Normalized uniform 3D cropping box across all specimens (`babb03-dataset03-cropping-table.xlsx`).
- **Data Split (3-2-2):**
  - Train: `id01`, `id02`, `id03`
  - Validation: `id04`, `id05`
  - Test: `id06`, `id07`
- **Output Format:**
  - Raw: `(C, Z, Y, X)` uint16 array (autofluorescence concatenated via `concatenateChannels.py`).
  - Label: `(Z, Y, X)` uint8 binary mask.
  - HDF5 container generated with `writeH5.py`.

### dataset04 (`dataset04.a`, `dataset04.b`, `dataset04.c`)
- **Purpose:** Evaluate sample size sensitivity by adopting a **5-1-1** train/val/test split using dataset03 preprocessed images.
- **Variants:**
  - **dataset04.a** (Model 10.a): Val = `id06`, Test = `id07`, Train = `id01, id02, id03, id04, id05`
  - **dataset04.b** (Model 10.b): Val = `id05`, Test = `id01`, Train = `id02, id03, id04, id06, id07`
  - **dataset04.c** (Model 10.c): Val = `id04`, Test = `id02`, Train = `id01, id03, id05, id06, id07`

### dataset05 (`babb02.1 + babb03 ct3 pool`)
- **Purpose:** Pool CT3 heart recordings across multiple mesoSPIM sessions (`babb02.1` and `babb03`) to increase total training set size.
- **Resolution Matching:**
  - Raw babb03: 2.0, 0.85, 0.85 µm
  - Raw babb02.1: 10.0, 0.85, 0.85 µm
  - Scaled voxel size: **10.0 × 2.53 × 2.53 µm³** (voxel size delta < 0.1 nm between sessions).
- **Scripts:** `scaleTifs-dataset05-babb02.1.ijm`, `scaleTifs-dataset05-babb03.ijm`, `cropTifs-Static-dataset05-no_tail.ijm`.

### dataset06 (VRAM & Channel Sensitivity Study)
- **Purpose:** Empirical study of GPU VRAM consumption against patch shape, channel count (1 to 3), and bit depth (uint8 vs uint16).
- **Sub-datasets (`dataset06.0` – `dataset06.5`):**
  - Triple channel (405, 488, 561 nm), dual channel (405, 488 nm), and single channel (405 nm).
  - Bit depth comparisons: 16-bit uint16 vs 8-bit uint8.

### dataset07 (Fluorescence Control Baseline)
- **Purpose:** Positive control using fluorescence (638 nm) as raw input to validate 3D U-Net baseline segmentation quality before evaluating autofluorescence.
- **Split:** 5 / 1 / 1 (`id01-05` train, `id06` val, `id07` test).

### dataset08 (2D U-Net Benchmark)
- **Purpose:** Benchmark against Fiji 2D-UNet plugin using single-slice 2D overlays.
- **Sub-datasets:**
  - `dataset08.0`: Positive fluorescence control (slices 3, 13, 23, ..., 123).
  - `dataset08.1`: Autofluorescence single channel.

### dataset09 (Eye Segmentation - Proof of Concept)
- **Purpose:** Multichannel autofluorescence segmentation of *Xenopus* embryo eyes (NF stage 42–44, n=7).
- **Sub-datasets:**
  - `dataset09.0`: Binary semantic segmentation.
  - `dataset09.1`: Multi-class semantic segmentation.

### dataset10 (Isometric Eye Dataset, ~5.784 µm³)
- **Key Feature:** **Uncropped isometric downsampling** to (5.784 µm)³. Patch-based sampling in `pytorch-3dunet` bypasses the need for tight pre-cropping.
- **Variants:**
  - `dataset10.a`: Sparse 2D U-Net slices (with class balancing).
  - `dataset10.b` (`dataset10.b.0` – `dataset10.b.3`): Dense 3-channel autofluorescence 3D U-Net (includes pseudo-mutant test `dataset10.b.3` with single eye).
  - `dataset10.c` / `dataset10.c.1`: Dense fluorescence control and validation loss stability experiments (3-2-2 split).

### dataset11 (Isometric Kidney & Eye, `babb03-a5`)
- **Key Feature:** Isometric scaling to (5.784 µm)³ on `a5` antibody series.
- **Sub-datasets:**
  - `dataset11.a.0` – `dataset11.a.2`: Boundary model.
  - `dataset11.b.0` – `dataset11.b.2`: Nuclei model.
  - `dataset11.c`: Kidney pronephros segmentation with 2D hole filling.
  - `dataset11.d`: Eye autofluorescence annotations for cross-organ experiments.
  - `dataset11.e`: Multi-organ (eye + kidney) dataset.

### dataset12 (`babb03-col2a1`)
- **Target:** Cartilage segmentation (*Col2a1* stain). Isometric ~5.784 µm³ voxel grid.

### dataset13 (Multi-Organ Compound Evaluation)
- **Target:** Joint eye and kidney model predictions across single-channel (488 nm) and multi-channel autofluorescence inputs.
