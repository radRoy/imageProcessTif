# Agent Orientation & Project Roadmap

## 1. Project Overview & Vision
The overarching goal is to consolidate and refactor 4 related bioimage processing repositories into a unified, clean, package-based monorepo named **`mesospim_segmentation`**, managed with **`uv`**.

### End-to-End Pipeline Scope
1. **Microscopy & Preprocessing:** Light-sheet (mesoSPIM) raw data ingestion, cropping, channel concatenation, format conversions (TIF / HDF5 / BigStitcher), metadata handling, and PyImageJ integrations.
2. **Segmentation & Training:** 3D U-Net / deep learning segmentation training workflows dispatched via **SLURM** on an HPC cluster.
3. **Model Evaluation & Metrics:** Intersection over Union (IoU), threshold sweeps, segmentation quality assessment, and validation pipelines.

---

## 2. Current State (This Repository: `imageProcessTif`)
* **Role:** Preprocessing, format conversion, cropping, ROI handling, HDF5/TIF I/O, and IoU metric calculations.
* **Status:** Audit completed (`CODEBASE_AUDIT.md`). Moving to modular package structure under `src/mesospim/`.

---

## 3. Guiding Principles for Agents
To preserve token context and maintain code quality, adhere strictly to the following rules:
* **Minimal Context & Iterative Steps:** Tackle one task/module per prompt. Do not perform sweeping multi-repo changes in a single step.
* **Modular Packaging:** Move reusable library logic into standard Python packages (e.g., `src/mesospim/...`) with `pyproject.toml` managed via `uv`.
* **HPC & SLURM Ready:** Ensure scripts designed for cluster execution have clear CLI entry points (via `argparse` or `click`), headless capability, and decoupled configuration (YAML/TOML).
* **Headless First:** Computational and I/O functions must never depend on GUI/Tkinter dialogs; GUI prompts are strictly optional wrappers.
* **Source of Truth:** Rely on the actual code and file structure over conversational memory.
* **Ignored Folders in Refactorings:** Ignore folders `Archive`, `.venv`, `.idea`, `.git`, `pycache` (and `__pycache__`) in refactorings.

---

## 4. Phased Roadmap & Implementation Plan

### Phase 1: Clean & Modularize `imageProcessTif` (Current Focus)
- [x] **Task 1.0:** Audit and catalog core reusable logic vs. ad-hoc/legacy scripts (see `CODEBASE_AUDIT.md`).
- [ ] **Task 1.1:** Setup package layout (`src/mesospim/`) and implement headless path & filesystem utilities (`src/mesospim/io/paths.py`).
- [ ] **Task 1.2:** Implement standard TIF I/O and bit-depth conversion modules (`src/mesospim/io/tiff.py`, `src/mesospim/transforms/conversions.py`).
- [ ] **Task 1.3:** Implement HDF5 I/O module with context managers for 3D U-Net dataset creation (`src/mesospim/io/hdf5.py`).
- [ ] **Task 1.4:** Implement core spatial & channel transforms (`src/mesospim/transforms/formatting.py`, `src/mesospim/transforms/masks.py`).
- [ ] **Task 1.5:** Implement specimen cropping coordinate normalization logic (`src/mesospim/transforms/cropping.py`).
- [ ] **Task 1.6:** Implement IoU evaluation metrics and YAML reporting (`src/mesospim/metrics/iou.py`, `src/mesospim/metrics/reporting.py`).
- [ ] **Task 1.7:** Build CLI entrypoints for headless / SLURM execution (`src/mesospim/cli/`).
- [ ] **Task 1.8:** Establish unit test suite (`pytest`) and type annotations (`mypy`/`ruff`) across all modules.

### Phase 2: Monorepo Setup with `uv`
- [ ] **Task 2.1:** Initialize `mesospim_segmentation` workspace layout with `uv`.
- [ ] **Task 2.2:** Define workspace members / sub-packages with explicit dependencies.
- [ ] **Task 2.3:** Configure linting (`ruff`) and test runner (`pytest`).
- [ ] **Task 2.4:** Migrate sanitization to the remaining 3 component repositories.

### Phase 3: Cluster (SLURM) & Evaluation Integration
- [ ] **Task 3.1:** Standardize SLURM job submission scripts and environment definitions.
- [ ] **Task 3.2:** Integrate end-to-end testing from preprocessing to training and model evaluation.

---

## 5. Next Immediate Task for Agent
**Task 1.1:** Setup the `src/mesospim/` package layout and implement `src/mesospim/io/paths.py` (pure `pathlib`-based file listing, filtering, sibling directory creation, and naming utilities without Tkinter dependencies).