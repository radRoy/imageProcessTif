# Fiji & ImageJ Reference Notes

This document collects practical guidelines, macro development precautions, thresholding benchmarks, and reference resources for working with Fiji / ImageJ in this pipeline.

---

## Fiji Macro scripting: multi-editor hazard

**DO NOT edit the same `.ijm` script simultaneously in multiple editors** (e.g., VS Code / PyCharm and Fiji's built-in script editor). 

- **Symptom / Failure Mode:** When auto-updating activates across both editors, Fiji's editor can freeze during concurrent write operations.
- **Consequence:** Force-closing Fiji via Task Manager (Windows) can truncate or completely wipe the file contents of the active script (that is, .ijm macro).
- **Safe Practice:** Pick one editor for active scripting. If running in Fiji, load or drag the file only after saving in your external editor.

---

## Thresholding Algorithm Ranking

Based on manual testing on *Xenopus* embryo microscopy channels (comparing whole signal inclusion vs. background noise suppression):

```
Default
= Huang
< Li
= MaxEntropy
<< Intermodes               (gauss < gauss 3D with equal sigmas)
= IsoData                   (2D < 3D for noise exclusion; 2D > 3D for signal inclusion)
= IJ_IsoData
< Otsu                      (Best balance of signal inclusion and noise exclusion)
(<) Percentile
= RenyiEntropy
= Shanbhag
= Triangle
= Yen
```

**Conclusion:** **Otsu thresholding** consistently provided the highest fidelity binary segmentation masks for 3D ground truth label creation.

---

## Macro & Plugin Resources

- **Git Submodule / Macro Repository:** [`radRoy/WaltherFiji`](https://github.com/radRoy/WaltherFiji) (placed in Fiji's `scripts` or `plugins` directory).
- [ImageJ Built-in Macro Functions Documentation](https://imagej.nih.gov/ij/developer/macro/functions.html)
- [Combining Channels into Hyperstacks in Fiji](https://cbmf.hms.harvard.edu/avada_faq/fiji-hyperstacks/)
- [ImageJ Flexible Segmentation Workflow](https://imagej.net/imaging/segmentation#flexible-workflow)
- [Selecting Connected Pixels in a Binary Mask in 3D](https://forum.image.sc/t/selecting-connected-pixels-in-a-binary-mask-in-3d/4142/2)

---

## Citations

When using Fiji in publication workflows, please cite:

> Schindelin, J., Arganda-Carreras, I., Frise, E., Kaynig, V., Longair, M., Pietzsch, T., Preibisch, S., Rueden, C., Saalfeld, S., Schmid, B., Tinevez, J. Y., White, D. J., Hartenstein, V., Eliceiri, K., Tomancak, P., & Cardona, A. (2012). **Fiji: an open-source platform for biological-image analysis.** *Nature Methods*, 9(7), 676–682. https://doi.org/10.1038/nmeth.2019
