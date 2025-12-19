# CHalf Module

The **CHalf module** is the core computational engine of the software. It processes raw peptide intensity data, fits it to a sigmoid denaturation curve, and calculates the **$C_{1/2}$ value**—the concentration at which half of the protein population is unfolded to expose the specific peptide to labeling.

## 1. CHalf Tab Settings
The **CHalf** tab in the user interface controls the mathematical algorithms used for curve fitting and data filtering. These settings directly correspond to the parameters in your workflow configuration file.

### A. Search Settings
These options filter the input data before analysis begins, typically to isolate specific types of labeled peptides based on the labeling chemistry used in your experiment.

| Setting | Workflow Key | Description |
| :--- | :--- | :--- |
| **Light Search** | `chalf.search.light` | *(Default: True)* When enabled, the software only analyzes peptides containing specific amino acids relevant to the labeling chemistry. |
| **Residues** | `chalf.search.residues` | *(Default: chmy)* Defines the amino acids to search for when Light Search is enabled.<br>• **C**: Cysteine<br>• **H**: Histidine<br>• **M**: Methionine<br>• **Y**: Tyrosine |

### B. Filter Settings
These settings determine which curves are considered "valid" and retained in the final output.

* **Min / Max** (`chalf.filter.min` / `.max`)
    * *(Default: 0.0 - 3.48)* Defines the valid range for calculated $C_{1/2}$ values. Curves with midpoints extrapolated outside this range are discarded.
* **R² Cutoff** (`chalf.filter.rsq`)
    * *(Default: 0.8)* The coefficient of determination. Fits with an $R^2$ value below this threshold are rejected.
* **Confidence Interval (CI) Filter** (`chalf.filter.ci_filter`)
    * *(Default: False)* An optional filter that removes curves where the 95% confidence interval of the $C_{1/2}$ estimate is too wide, indicating high uncertainty. Confidence interval is not always a good measure of curve fit. Oftentimes, it will filter out significant transitions with near-perfect fits, but you may optionally use this as a filtering method.
* **Optimize** (`chalf.filter.optimize`)
    * *(Default: rsq)* Determines which metric the fitting algorithm prioritizes for filtering when performing multiple fits. The best fit will be chosen based on this parameter.

### C. Fitting Options
Controls the mechanics of the sigmoid curve fitting algorithm.

* **Minimum Points** (`chalf.fitting.min_pts`)
    * *(Default: 4)* The minimum number of non-zero data points required to attempt a fit. If a peptide has fewer than 4 data points, it is skipped.
* **Allow Trimming** (`chalf.fitting.outlier_trimming`)
    * *(Default: True)* Enables an iterative "Outlier Removal" process.
        * *Process:* The software fits the curve, identifies points with Standardized Residuals > Cutoff, removes them, and refits. This generates the "Trimmed" dataset in the output.
* **Outlier Cutoff** (`chalf.fitting.outlier_cutoff`)
    * *(Default: 2)* The z-score threshold for defining an outlier.
* **Zero Criteria** (`chalf.fitting.zero_criteria`)
    * *(Default: remove)* Determines handling of zero-intensity values:
        * **Remove:** Treat zeros as missing data (useful if zeros are a result of stochastic sampling issues during acquisition).
        * **Keep:** Treat zeros as actual 0.0 intensity. These points will dictate the minimum value used during min-max normalization (useful if zeros represent real absence of an analyte).
        * **Impute:** Treat zeros as actual 0.0 intensity, but only after min-max normalization. Normalization will be applied to non-zero points and then zero-value points will be filled back in as zeros, post-normalization (useful if zeros represent "below detection limit").

### D. Graphing Options
* **Graph** (`chalf.graphing.graph`)
    * *(Default: False)* If enabled, generates individual image files (JPG/PNG/SVG) for every fitted peptide.
    * *Warning: This can generate thousands of files and significantly slow down processing.*

---

## 2. CHalf Outputs
The module generates three primary CSV files for each condition processed, representing data at increasing levels of aggregation.

### A. Raw Output: `_Combined_OUTPUT.csv`
This is the most granular file, containing **every peptide** analyzed. It includes raw data, normalization stats, and two sets of fitting parameters: the initial "Fit" (all points) and the "Trimmed" fit (outliers removed).

**Key Columns:**
| Column Name | Description |
| :--- | :--- |
| `Accession@Peptide` | Unique ID combining protein ID and peptide sequence. |
| `Accession` | Protein ID associated with the peptide sequence. |
| `Peptide` | Peptide sequence of the fit analyte. |
| `Site Type` | Describes the label status of the peptide (Single Labeled/Unlabeled, Multi Labeled/Unlabled, Not labelable). Single vs multi refers to the number of labelable amino acids in a given peptide and how many are chemically labeled. This status is essential to localizing stability to a specific residue. Currently, deconvolution of multi sites to identify localized stability is not supported, so single sites are used to calculate stability. |
| `Residue Number` | The residue number associated with the fitted curve. |
| `Label Site` | The specific residue being tracked (e.g., `M24`). |
| `Label Type` | The identity of the label at the site (e.g., `M(+15.99)` for methionine oxidation or `M` for unlabeled methionine). |
| `CHalf` | The calculated denaturation midpoint (selected from the best fit according your fitting parameters). |
| `r_squared` | Goodness of fit (selected from the best fit according your fitting parameters). |
| `ratioTOrange` | Ratio of the calculated confidence interval to the range of the denaturation gradient. |
| `CHalf_ConfidenceInterval` | Raw confidence interval calculated for the transition point. |
| `Slope` | The direction of the transition curve (e.g., `Positive` or `Negative`). |
| `Curve_b` | The steepness of the transition point in the curve. |
| `Baseline` | The starting abundance of the analyte prior to denaturation. |
| `Post-Transition` | The ending abundance of the analyte after denaturation. |
| `Trimmed` | Whether or not the best measured curve used outlier trimming. |
| `Significant` | `True`/`False`. Indicates if the curve passed all filter criteria ($R^2$, Range, etc.). |
| `Window` | Which range of points in the concentration gradient was used to fit the curve. Only relevant if using experimental window fitting settings. |
| `0.0`, `0.43`... | The normalized intensity values at each concentration point. |
| `Start` | Residue number of the first amino acid in the peptide. |
| `End` | Residue number of the last amino acid in the peptide. |
| `#pts` | Number of measurements across the curve. |
| `Mean` | Average abundance of the peptide. |
| `RSD` | Relative Standard Deviation of the abundance of the peptide. |
| `Range` | Range of peptide abundances. |
| `Relative Range` | Peptide abundance range divided by the average abundance. |
| `% Change` | Percent change from min to max abundance. |
| `End-Start` | Difference between the abundance of the last measured point and first measured point. |
| `fit_#nonZero` | Number of non-zero points used to fit the curve. |
| `Spearman` | Spearman coefficient of the abundances against the concentration values. |
| `P-value` | P-value for the spearman coefficient. |
| `fit_{value}` | Value derived from the *initial* fit (before outlier removal). See "Understanding the Fit Parameters" below. |
| `trim_{value}}` | Value derived from the *trimmed* fit (after outlier removal). See "Understanding the Fit Parameters" below. |

### B. Cleaned Output: `Sites.csv`
This file filters the master list to focus on specific, singlely labeled or unlabeled sites. If a single peptide contains a label (e.g., Oxidation on Met-24), it appears here.
* **Purpose:** Provides a clean list of valid, fitted curves for individual labeled residues.
* **Difference from Combined Output:** Contains a subset of columns focused on the final result rather than intermediate fitting stats.

### C. Localized Stability: `Combined Sites.csv`
This is the highest level of aggregation. If multiple unique peptides map to the same specific residue (e.g., `Peptide A` covers M24 and `Peptide B` also covers M24), calculations are performed to deconvolute the impacts of the individual peptides on the labelable site. This allows for a localized, site-specific measure of stability.
* **Count:** Indicates how many unique peptides contributed to this measurement.
* **Usage:** Best for downstream biological interpretation, providing a consensus stability value for each residue.

### Understanding the Fit Parameters (A, B, b)
Columns like `Curve_A`, `Curve_B`, and `Curve_b` correspond to the sigmoid equation parameters:

$$y = A + \frac{B - A}{1 + e^{-b \cdot (x - C_{1/2})}}$$

* **A (Baseline):** The intensity of the folded state (bottom of curve).
* **B (Post-Transition):** The intensity of the unfolded state (top of curve).
* **b (Slope):** The steepness of the folding transition.
* **CHalf:** The midpoint ($x$) where $y$ is halfway between $A$ and $B$.