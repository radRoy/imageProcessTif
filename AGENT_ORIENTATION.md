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
* **Status:** Contains standalone utility scripts, macros, and analysis tables that need cleanup, separation of reusable core modules from legacy/archive scripts, and packaging.

---

## 3. Guiding Principles for Agents
To preserve token context and maintain code quality, adhere strictly to the following rules:
* **Minimal Context & Iterative Steps:** Tackle one module or one refactoring task per turn. Do not perform sweeping multi-repo changes in a single step.
* **Modular Packaging:** Move reusable library logic into standard Python packages (e.g., `src/mesospim/...` or dedicated package folders) with `pyproject.toml` managed via `uv`.
* **HPC & SLURM Ready:** Ensure scripts designed for cluster execution have clear CLI entry points (via `argparse` or `click`) and decoupled configuration (e.g., YAML/TOML).
* **Source of Truth:** Rely on the actual code and file structure over conversational memory.

---

## 4. Phased Roadmap

### Phase 1: Clean & Sanitize Current Repositories (Current Focus)
- [ ] Audit and catalog core reusable logic vs. ad-hoc/legacy scripts in `imageProcessTif`.
- [ ] Refactor loose functions into structured modules (I/O, metrics, transforms).
- [ ] Establish basic unit tests and type annotations for core functions.
- [ ] Repeat sanitization for the other 3 component repositories.

### Phase 2: Monorepo Setup with `uv`
- [ ] Initialize `mesospim_segmentation` workspace layout with `uv`.
- [ ] Define workspace members / sub-packages with explicit dependencies.
- [ ] Configure linting (`ruff`) and test runner (`pytest`).

### Phase 3: Cluster (SLURM) & Evaluation Integration
- [ ] Standardize SLURM job submission scripts and environment definitions.
- [ ] Integrate end-to-end testing from preprocessing to training and model evaluation.

---

## 5. Next Immediate Task for Agent
When starting the next session, instruct the agent to:
1. Inspect the core I/O and processing scripts in this repository (`fileHandling.py`, `IoU_batch_processor.py`, `tifFormatting.py`, etc.).
2. Propose a clean module structure to separate reusable library code from one-off batch scripts.