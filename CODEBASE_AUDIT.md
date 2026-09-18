# Codebase Audit & Modularization Plan: `imageProcessTif`

## 1. Overview & Objectives
This audit catalogs the Python scripts, utilities, and workflows in the `imageProcessTif` repository. The goal is to separate reusable library code from ad-hoc scripts, eliminate Tkinter GUI coupling from computational functions, and establish a clean module architecture ready for the `mesospim_segmentation` package and HPC/SLURM execution.

---

## 2. Component Catalog & Audit

| Script / Component | Primary Responsibility | Classification | Coupling & Technical Debt |
| :--- | :--- | :--- | :--- |
| `fileHandling.py` / `files.py` | Path manipulation, batch listing, filtering, TIF read/write (`skimage.io`). | **Reusable Core Utility** (16+ internal dependents) | Coupled with `tkinter` dialogs; uses manual string path concatenation instead of `pathlib.Path`. |
| `IoU_batch_processor.py` | Calculates 3D Intersection over Union (IoU) across segmentations and thresholds, records highscores, writes YAML. | **Reusable Metric & CLI Tool** | GUI dialogs directly embedded; mathematical IoU calculation mixed with filename parsing and file I/O. |
| `union_of_two_binary_mask_stacks.py` | Computes element-wise binary union (`label_a \| label_b`) across specimens. | **Reusable Transform** | Duplicate copy-paste of functions from `IoU_batch_processor.py`. |
| `tifFormatting.py` | Dimension permutations (e.g., `zyxC` -> `Czyx` for 3D U-Net). | **Reusable Transform** | Uses `np.rollaxis`; batch execution mixes Tkinter prompts with file iteration. |
| `concatenateChannels.py` | Groups single-channel TIF stacks by specimen ID (`id01-...`) and stacks into multi-channel `(C, Z, Y, X)` arrays. | **Reusable Pipeline** | Hardcoded naming conventions and GUI dialogs inside script body. |
| `convertTif16bitTo8bit.py` / `convertTifList16bitTo8bit.py` | Bit-depth downscaling (`uint16` -> `uint8`). | **Reusable Transform & Batch Tool** | Separated into two files (single array vs. directory loop); relies on Tkinter dialogs. |
| `croppingCoordinateCalculation.py` | Calculates specimen-normalized ROI cropping bounds from Excel tables with edge-case handling (undershoot/overshoot). | **Reusable Transform / Domain Logic** | Directly reads/writes Excel files without separated pure mathematical functions. |
| `readH5.py` / `writeH5.py` | HDF5 dataset creation and appending (`/raw`, `/label`) for 3D U-Net pipelines. | **Reusable I/O Module** | Logic mixed between Tkinter folder prompts and file operations; lacks context-manager abstraction. |
| `h5_predict3dunet_to_Segmentation.py` | Converts `.h5` model predictions into BigDataViewer (BDV) format via `npy2bdv`. | **Reusable I/O / Export Module** | GUI coupling and ad-hoc script structure. |
| `class_label_balance_randomiser.py` | Balances slice counts per class across specimens for 2D training. | **Ad-hoc / Unfinished Utility** | Incomplete experimental code. |
| `yaml_tester.py` / `test_yaml_*.yml` | Serializes IoU results to YAML. | **Ad-hoc Validation** | Consolidate into evaluation metric reporting. |
| `Archive/`, `knowHow/`, `FijiRecordings/` | Historical macros, Excel scaling tables, documentation notes. | **Legacy / Reference Data** | Retain as reference or move to `docs/` and `data/` reference folders. |

---

## 3. Key Findings & Technical Debt

1. **Tight Coupling with Tkinter GUI Dialogs:**
   Most scripts initialize `tk.Tk()` and spawn dialog windows (`filedialog.askdirectory()`). This breaks headless execution, SLURM batch job submission on HPC clusters, and automated unit testing.
2. **Duplication of Metric & Validation Logic:**
   Functions like `intersection_over_union()`, `assert_iou_input_images_shapes_equal()`, and `get_label_image()` are duplicated across `IoU_batch_processor.py` and `union_of_two_binary_mask_stacks.py`.
3. **Hardcoded Metadata & Suffix Parsing:**
   File name conventions (`id01-...`, `-Ch405,488,561nm-...`, `threshold_[0.1,1.0]`) are parsed using ad-hoc `split('-')` and string slicing rather than structured regex or configuration schemas.
4. **Scattered I/O and Array Transformations:**
   Array reading/writing is spread across `skimage.io`, `h5py`, `npy2bdv`, and custom numpy slicing across multiple standalone scripts.

---

## 4. Target Module Architecture (`src/mesospim/`)

```text
src/
└── mesospim/
    ├── __init__.py
    ├── io/                           # All file and format handling (pure Python + libraries)
    │   ├── __init__.py
    │   ├── paths.py                 # Pure pathlib-based file listing, filtering, sibling dir creation, naming utilities
    │   ├── tiff.py                  # read_tif_stack, write_tif_stack, bitdepth conversion (uint16 -> uint8)
    │   ├── hdf5.py                  # H5 reader/writer (raw/label datasets, dataset inspection, BDV export)
    │   └── dialogs.py               # Optional Tkinter dialog wrappers (only invoked in interactive mode)
    │
    ├── transforms/                   # Pure array manipulations & image geometry
    │   ├── __init__.py
    │   ├── formatting.py            # Dimension rolling (zyxC <-> Czyx), channel stacking & concatenation
    │   ├── cropping.py              # Specimen bounding-box normalization & coordinate calculation
    │   ├── conversions.py           # uint16 to uint8 scaling, type casting, validation
    │   └── masks.py                 # Binary mask union, multi-label combinations
    │
    ├── metrics/                      # Model validation and segmentation evaluation
    │   ├── __init__.py
    │   ├── iou.py                   # Intersection over Union, threshold sweeps, binary shape validators
    │   └── reporting.py             # YAML/JSON summary reporting and highscore logging
    │
    └── cli/                          # Headless CLI entry points for local & SLURM execution (argparse/click)
        ├── __init__.py
        ├── evaluate_iou.py          # Decoupled CLI for IoU batch evaluation
        ├── convert_tif_to_h5.py     # Batch converter from TIF channel stacks to 3D U-Net HDF5 files
        ├── concatenate_channels.py  # CLI for specimen channel grouping & concatenation
        └── convert_bitdepth.py      # CLI for uint16 -> uint8 conversions
```
