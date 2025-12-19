# Workflow Configuration Guide

This guide details every variable found in a `.workflow` configuration file. It explains the function of each setting, the expected data format, and the **experimental rationale** for modifying these values.

---

## 1. CHalf Settings
*Global settings for the core fitting algorithm.*

| Variable | Data Type & Options | Default | Description & Rationale |
| :--- | :--- | :--- | :--- |
| **`chalf`** | **Boolean**<br>`True` / `False` | `True` | **Master Switch:** Set to `True` to run the CHalf fitting module. Set to `False` if you only want to re-run visualizations on already processed data.  |
| **`cores`** | **Integer** | `-1` | **CPU Allocation:** Determines the number of processor cores to use. `-1` uses all available cores. Decrease this number if you need to use the computer for other tasks while processing.  |

### Search Settings
*Controls how the software identifies relevant peptides before analysis.*

| Variable | Data Type & Options | Default | Description & Rationale |
| :--- | :--- | :--- | :--- |
| **`chalf.search.light`** | **Boolean**<br>`True` / `False` | `True` | **Light Search Filter:** If `True`, the software ignores peptides that do not contain the specific residues listed below. <br>**Rationale:** Set to `False` to analyze *every* peptide detected (e.g., for global abundance checks).  |
| **`chalf.search.residues`** | **String**<br>e.g., `chmy`, `k`, `de` | `chmy` | **Target Residues:** Defines the amino acids to search for when Light Search is enabled (C=Cys, H=His, M=Met, Y=Tyr).<br>**Rationale:** Change this string to match your labeling chemistry. |

### Filter Settings
*Criteria for accepting or rejecting a fitted curve.*

| Variable | Data Type & Options | Default | Description & Rationale |
| :--- | :--- | :--- | :--- |
| **`chalf.filter.min`**<br>**`chalf.filter.max`** | **Float** | `0.0`<br>`3.48` | **Valid $C_{1/2}$ Range:** The range of denaturant concentrations where a calculated midpoint is considered valid.<br>**Rationale:** **Crucial Setting.** Update to match your experimental gradient (e.g., set max to `8.0` for Urea). Curves extrapolated outside this range are unreliable.  |
| **`chalf.filter.rsq`** | **Float**<br>Range: 0.0 - 1.0 | `0.8` | **$R^2$ Cutoff:** The minimum goodness-of-fit required.<br>**Rationale:** Lower (e.g., `0.7`) for noisy datasets; raise (e.g., `0.9`) for strict quantification.  |
| **`chalf.filter.ci_filter`** | **Boolean**<br>`True` / `False` | `False` | **Confidence Interval Filter:** Rejects curves with wide confidence intervals.<br>**Rationale:** Enable for high statistical rigor. Keep disabled generally, as perfect fits with fewer points often have wide CIs but are valid.  |
| **`chalf.filter.ci_value`** | **Float** | `0.35` | **CI Threshold:** If `ci_filter` is True, curves with a confidence interval width divided by the concentration range greater than this value are rejected.  |
| **`chalf.filter.optimize`** | **String**<br>Option: `rsq` / `ci` | `rsq` | **Optimization Metric:** Determines which metric the fitting algorithm prioritizes for filtering.<br>**Rationale:** If using the CI filter, switch to `ci` to optimize fitting for CI minimization.  |
| **`chalf.filter.sig_only`** | **Boolean**<br>`True` / `False` | `False` | **Significance Only:** If `True`, results will only show significant curves.<br>**Rationale:** Usually kept `False` to allow the user to go back and look at insignficant data.  |

### Fitting Options
*Mechanics of the curve-fitting algorithm.*

| Variable | Data Type & Options | Default | Description & Rationale |
| :--- | :--- | :--- | :--- |
| **`chalf.fitting.min_pts`** | **Integer** | `4` | **Minimum Points:** Minimum non-zero data points required to attempt a fit.<br>**Rationale:** Lowering to `3` recovers data but increases false positives. Raising to `5+` ensures quality but reduces coverage.  |
| **`chalf.fitting.outlier_trimming`** | **Boolean**<br>`True` / `False` | `True` | **Outlier Removal:** Iteratively removes points that deviate significantly from the curve.<br>**Rationale:** Keep `True` for most MS data. Disable for sparse data where every point counts.  |
| **`chalf.fitting.outlier_cutoff`** | **Float** | `2` | **Z-Score Cutoff:** How far a point must be from the curve to be considered an outlier.<br>**Rationale:** Decrease (e.g., `1.5`) to trim aggressively; increase (e.g., `3`) to be more permissive.  |
| **`chalf.fitting.zero_criteria`** | **String**<br>`remove`, `keep`, `impute` | `remove` | **Handling Zeros:**<br>• `remove`: Treat zeros as missing (stochastic dropout).<br>• `keep`: Treat zeros as real 0.0 intensity.<br>• `impute`: Fill zeros as 0.0 *after* normalization.<br>**Rationale:** Use `remove` if you believe that the zeros are due to missing measurements due to stochastic sampling issues. Use `keep` if you believe the zeros represent real absence of an analyte. Use `impute` if zeros represent abundances below the detection limit.  |

### Graphing Options
*Controls the generation of individual peptide plots during the CHalf run.*

| Variable | Data Type & Options | Default | Description & Rationale |
| :--- | :--- | :--- | :--- |
| **`chalf.graphing.graph`** | **Boolean**<br>`True` / `False` | `False` | **Generate Graphs:** Creates an image file for *every* peptide fit.<br>**Rationale:** **Warning:** Slows processing. Only enable for debugging or small datasets.  |
| **`chalf.graphing.file_type`** | **String**<br>`jpg`, `png`, `svg` | `jpg` | **File Format:** The format of the output images.  |
| **`chalf.graphing.min` etc.** | *Same as Filter* | *N/A* | *Overrides the global filter settings specifically for the output graphs.*  |

### Experimental Options
*Advanced signal processing for difficult data.*

| Variable | Data Type & Options | Default | Description & Rationale |
| :--- | :--- | :--- | :--- |
| **`chalf.experimental.sg.smooth`** | **Boolean**<br>`True` / `False` | `False` | **Savitzky-Golay Smoothing:** Digital filter to reduce noise before fitting.<br>**Rationale:** Enable if raw data is very "jittery" or has low signal-to-noise.  |
| **`chalf.experimental.sg.window`** | **Integer**<br>Odd Numbers (3, 5, 7...) | `5` | **Window Size:** Number of points to smooth over.<br>**Rationale:** Larger windows smooth more but may flatten sharp transitions.  |
| **`chalf.experimental.sg.order`** | **Integer** | `2` | **Polynomial Order:** Order of the polynomial used for smoothing.  |
| **`chalf.experimental.wf.window_fit`** | **Boolean**<br>`True` / `False` | `False` | **Window Fit:** "Rescue" strategy looking for transitions in sub-segments.<br>**Rationale:** Enable for **multiphasic proteins** or if data has artifacts at extreme gradient ends.  |
| **`chalf.experimental.wf.window`** | **Integer** | `6` | **Window Fit Size:** Number of consecutive points to include in each sub-segment.  |
| **`chalf.experimental.ms.mutations`** | **Boolean**<br>`True` / `False` | `False` | **Mutation Mode:** Tracks mutant peptides separately.<br>**Rationale:** Enable ONLY if input CSV has a "Mutation" column.  |

---

## 2. Quality Control (QC) Settings
*Independent filters for the "Funnel Report" in the QC module.*

| Variable | Data Type & Options | Default | Description & Rationale |
| :--- | :--- | :--- | :--- |
| **`qc`** | **Boolean**<br>`True` / `False` | `True` | **Enable QC:** Runs the QC statistics module.  |
| **`qc.search.residues`** | **String** | `chmy` | **QC Targets:** Residues tracked in the stats report. Should match `chalf.search.residues`.  |
| **`qc.filter.min`** / **`.max`** | **Float** | `0.0`<br>`3.48` | **QC Range:** Defines "success" for the report.<br>**Rationale:** Widen these to see how many curves fail just slightly outside your range.  |
| **`qc.filter.rsq`** | **Float** | `0.8` | **QC $R^2$:** Defines "high quality" for the report.  |
| **`qc.filter.ci_filter`** | **Boolean**<br>`True` / `False` | `False` | **QC CI Filter:** If enabled, peptides with wide confidence intervals are marked as failed in the report.  |
| **`qc.filter.ci_value`** | **Float**<br> | `0.35` | **QC CI Filter Value:** If `CI Filter` is enabled, this is the value that will be used to define what represents wide confidence intervals. It is calculated via `confidence_interval` / `concentration_range`.  |
| **`qc.filter.optimize`** | **String**<br>Option: `rsq` / `ci` | `rsq` | **Optimization Metric:** Determines which metric the fitting algorithm prioritizes for filtering.<br>**Rationale:** If using the CI filter, switch to `ci` to optimize fitting for CI minimization.  |

---

## 3. Visualization Settings
*Configuration for figure generation. These do not affect the math, only the plots.*

### QC Report
| Variable | Data Type & Options | Default | Description & Rationale |
| :--- | :--- | :--- | :--- |
| **`visualization.qc.report`** | **Boolean**<br>`True` / `False` | `True` | **HTML Report:** Generates `report.html` dashboard.  |
| **`visualization.qc.open`** | **Boolean**<br>`True` / `False` | `False` | **Auto-Open:** Opens the browser automatically after processing.  |

### Residue Mapper (Single Condition)
*Plots stability across the sequence for one condition.*

| Variable | Data Type & Options | Default | Description & Rationale |
| :--- | :--- | :--- | :--- |
| **`visualization.rm`** | **Boolean**<br>`True` / `False` | `False` | **Enable:** Set to `True` to generate these plots.  |
| **`visualization.rm.file_type`** | **String**<br>`jpg`, `png`, `svg` | `jpg` | **File Format:** Output format for images.  |
| **`visualization.rm.min`** / **`.max`** | **Float** | `0.0`<br>`3.48` | **Y-Axis Limits:** Vertical range of the plot.<br>**Rationale:** Set slightly wider than your gradient range to avoid cutting off data points.  |
| **`visualization.rm.trendlines.trendline`** | **Boolean**<br>`True` / `False` | `True` | **Rolling Average:** Draws a line through data points.<br>**Rationale:** Essential for visualizing domains.  |
| **`visualization.rm.trendlines.window`** | **Integer** | `3` | **Smoothing Window:** Number of residues to average.<br>**Rationale:** Increase (e.g., 5 or 7) for large proteins to see broad domains.  |
| **`visualization.rm.trendlines.min`** | **Integer** | `5` | **Required Number of Points:** Number of residues required before a trendline will be generated.<br>**Rationale:** Smaller numbers allow for more trendlines to be generated but at the risk of generating uninformative trendlines.  |
| **`visualization.rm.other.all_curves`** | **Boolean**<br>`True` / `False` | `True` | **Plot All:** Plots both labeled and unlabeled data if available.  |
| **`visualization.rm.other.reference_stats`** | **Boolean**<br>`True` / `False` | `True` | **Stats Export:** Generates a CSV file containing the data used to build the figure.  |
| **`visualization.rm.other.rm_trendline_stats`** | **Boolean**<br>`True` / `False` | `False` | **Trendline Stats Export:** Adds the data used to build the trendline in the figure to the stats CSV.  |
| **`visualization.rm.other.mutation_search`** | **Boolean**<br>`True` / `False` | `False` | **Mutation Search:** Highlights specific point mutations. Requires mutation mode enabled in experimental settings.  |
| **`visualization.rm.other.advanced`** | **String**<br>`<path>` |  | **Advanced Figure Options:** See [Advanced Visualization Options](https://github.com/JC-Price/Chalf_public/blob/main/Demos%20and%20Documentation/visualization_modules_guide.md#3-annotation-files-ann-technical-guide-advanced-options).   |


### Combined Residue Mapper (Multi-Condition)
*Overlays multiple conditions (e.g., WT vs Mutant) on one plot.*

| Variable | Data Type & Options | Default | Description & Rationale |
| :--- | :--- | :--- | :--- |
| **`visualization.crm`** | **Boolean**<br>`True` / `False` | `True` | **Enable:** Set to `True` for comparison plots.  |
| **`visualization.crm.file_type`** | **String**<br>`jpg`, `png`, `svg` | `jpg` | **File Format:** Output format for images.  |
| **`visualization.crm.min`** / **`.max`** | **Float** | `0.0`<br>`3.48` | **Y-Axis Limits:** Vertical range of the plot.  |
| **`visualization.crm.trendlines.trendline`** | **Boolean**<br>`True` / `False` | `True` | **Rolling Average:** Draws a line through data points.<br>**Rationale:** Essential for visualizing domains.  |
| **`visualization.crm.trendlines.window`** | **Integer** | `3` | **Smoothing Window:** Number of residues to average.<br>**Rationale:** Increase (e.g., 5 or 7) for large proteins to see broad domains.  |
| **`visualization.crm.trendlines.min`** | **Integer** | `5` | **Required Number of Points:** Number of residues required before a trendline will be generated.<br>**Rationale:** Smaller numbers allow for more trendlines to be generated but at the risk of generating uninformative trendlines.  |
| **`visualization.crm.other.all_curves`** | **Boolean**<br>`True` / `False` | `True` | **Plot All:** Plots both labeled and unlabeled data if available.  |
| **`visualization.crm.other.reference_stats`** | **Boolean**<br>`True` / `False` | `True` | **Stats Export:** Generates a CSV file containing the data used to build the figure.  |
| **`visualization.crm.other.crm_trendline_stats`** | **Boolean**<br>`True` / `False` | `False` | **Trendline Stats Export:** Adds the data used to build the trendline in the figure to the stats CSV.  |
| **`visualization.crm.other.mutation_search`** | **Boolean**<br>`True` / `False` | `False` | **Mutation Search:** Highlights specific point mutations. Requires mutation mode enabled in experimental settings.  |
| **`visualization.crm.other.advanced`** | **String**<br>`<path>` |  | **Advanced Figure Options:** See [Advanced Visualization Options](https://github.com/JC-Price/Chalf_public/blob/main/Demos%20and%20Documentation/visualization_modules_guide.md#3-annotation-files-ann-technical-guide-advanced-options).   |

### Delta Mapper Options
*Plots the stability difference ($\Delta C_{1/2}$) between conditions.*

| Variable | Data Type & Options | Default | Description & Rationale |
| :--- | :--- | :--- | :--- |
| **`visualization.dm`** | **Boolean**<br>`True` / `False` | `True` | **Enable:** Set to `True` for Delta plots.  |
| **`visualization.dm.min`** / **`.max`** | **Float** | `-3.48`<br>`3.48` | **Y-Axis Limits:** The range of stability change.<br>**Rationale:** Should be symmetrical around 0.  |
| **`visualization.dm.trendlines.trendline`** | **Boolean**<br>`True` / `False` | `True` | **Rolling Average:** Draws a line through data points.<br>**Rationale:** Essential for visualizing domains.  |
| **`visualization.dm.trendlines.window`** | **Integer** | `3` | **Smoothing Window:** Number of residues to average.<br>**Rationale:** Increase (e.g., 5 or 7) for large proteins to see broad domains.  |
| **`visualization.dm.trendlines.min`** | **Integer** | `5` | **Required Number of Points:** Number of residues required before a trendline will be generated.<br>**Rationale:** Smaller numbers allow for more trendlines to be generated but at the risk of generating uninformative trendlines.  |
| **`visualization.dm.kde.min_pts`** | **Integer** | `3` | **KDE Min Points:** Minimum data points required to draw the side-panel distribution histogram.  |
| **`visualization.dm.sig_filter`** | **Boolean**<br>`True` / `False` | `False` | **Significance Filter:** Does not generate figures for proteins that do not have statistically significant differences.<br>**Rationale:** `True` produces "clean" figures showing only real hits. `False` visualizes global trends, even if noisy.  |
| **`visualization.dm.sig_value`** | **Float** | `0.05` | **P-Value Cutoff:** Threshold for significance (usually 0.05).  |
| **`visualization.dm.other.all_curves`** | **Boolean**<br>`True` / `False` | `True` | **Plot All:** Plots both labeled and unlabeled data if available.  |
| **`visualization.dm.other.reference_stats`** | **Boolean**<br>`True` / `False` | `True` | **Stats Export:** Generates a CSV file containing the data used to build the figure.  |
| **`visualization.dm.other.dm_trendline_stats`** | **Boolean**<br>`True` / `False` | `False` | **Trendline Stats Export:** Adds the data used to build the trendline in the figure to the stats CSV.  |
| **`visualization.dm.other.mutation_search`** | **Boolean**<br>`True` / `False` | `False` | **Mutation Search:** Highlights specific point mutations. Requires mutation mode enabled in experimental settings.  |
| **`visualization.dm.other.advanced`** | **String**<br>`<path>` |  | **Advanced Figure Options:** See [Advanced Visualization Options](https://github.com/JC-Price/Chalf_public/blob/main/Demos%20and%20Documentation/visualization_modules_guide.md#3-annotation-files-ann-technical-guide-advanced-options).   |

### Combined Site Visualization
*Dedicated plots for site-specific stability.*

| Variable | Data Type & Options | Default | Description & Rationale |
| :--- | :--- | :--- | :--- |
| **`visualization.cs`** | **Boolean**<br>`True` / `False` | `False` | **Enable:** Set to `True` to generate Combined Site plots.  |
| **`visualization.cs.file_type`** | **String**<br>`jpg`, `png`, `svg` | `jpg` | **File Format:** Output format for site plots.  |
| **`visualization.cs.min`** / **`.max`** | **Float** | `0.0`<br>`3.48` | **Y-Axis Limits:** Lower and upper limits of the stability axis.  |