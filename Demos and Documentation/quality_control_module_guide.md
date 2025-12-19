# Quality Control Module

The **Quality Control (QC)** module provides a statistical breakdown of your experiment's success rate. It tracks the attrition of data as it passes through the various filtering steps (fitting, range checks, $R^2$ cutoffs), allowing you to evaluate the quality of your sample preparation and mass spectrometry acquisition.

## 1. QC Settings
The Quality Control module uses its own independent set of filters, allowing you to run "stricter" or "looser" checks than your main analysis if desired. These settings are found in the **Quality Control** tab or the `[qc]` section of your workflow file.

| Setting | Workflow Key | Description |
| :--- | :--- | :--- |
| **Perform Quality Control** | `qc` | *(Default: True)* Master switch to enable this module. |
| **Residues** | `qc.search.residues` | *(Default: chmy)* Defines which amino acids are considered "labelable" targets. Only peptides containing these residues are tracked in the detailed breakdown. |
| **Min / Max** | `qc.filter.min` / `.max` | *(Default: 0.0 - 3.48)* The valid $C_{1/2}$ range. Curves outside this range are considered "failed" in the QC report. |
| **R² Cutoff** | `qc.filter.rsq` | *(Default: 0.8)* The minimum goodness-of-fit required to count a peptide as "high quality." |
| **CI Filter** | `qc.filter.ci_filter` | *(Default: False)* If enabled, peptides with wide confidence intervals (high uncertainty) are marked as failed. |

---

## 2. QC Outputs
The module generates a CSV file named `Quality Control.csv` for each condition. This file serves as a "Funnel Report," showing how many peptides survive each step of the analysis pipeline.

### Row Definitions
The rows in the CSV represent sequential filtering steps. Data must pass the previous step to be counted in the next.

1.  **Raw:** The total number of peptide entries found in your input CSV.
2.  **Labelable:** The subset of raw peptides that contain at least one of the target residues (C, H, M, or Y). This represents the theoretical maximum number of useful data points.
3.  **Can be fit:** Peptides that had enough non-zero data points (default: 4+) to attempt a curve fit.
    * *Drop-off here indicates:* Poor signal intensity or too many missing values.
4.  **C½ in range:** Peptides where the fitted curve had a midpoint ($C_{1/2}$) falling within your specified Min/Max limits.
    * *Drop-off here indicates:* Curves that were essentially flat lines or had midpoints extrapolated far beyond the concentration gradient.
5.  **R² in range:** Peptides that passed the range check **AND** met the $R^2$ quality threshold.
    * *Drop-off here indicates:* Noisy data that fits the sigmoid model poorly.
6.  **Confidence Interval (Optional):** Peptides passing all above checks **AND** having a narrow confidence interval.
7.  **Has >1 reporter:** Peptides passing all above checks **AND** are part of protein with multiple significant $C_{1/2}$ measurements.
8.  **Unique Sequences:** Unique peptide sequence coverage. Aggregates unique sequences from their labeled and unlabeled forms.
9.  **Sequence Count:** Number of unique sequences that match a condition.
10.  **Labeled Penetrance:** Number of unique sequences that have a labeled form.
11.  **Unlabeled Penetrance:** Number of unique sequences that have an unlabeled form.
12.  **Combined Sites:** Number of localized stability values measured.

### Column Definitions
* **peptide:** The absolute count of peptides at this step.
* **protein:** The number of unique proteins represented by these peptides.
* **peptide % / protein %:** The retention rate (percentage) relative to the "Labelable" starting pool.
* **Residue Columns (C, H, M, Y):** Breakdowns showing how many peptides containing specific residues survived.
* **Modification Columns (e.g., `M(+15.99)`):** Detailed counts for specific modifications found in your data (e.g., Oxidation). This is highly useful for checking labeling efficiency—for example, you can see if your oxidized methionine peptides fit better or worse than unmodified ones.

### Example Analysis
If you see a sharp drop between **Can be fit** and **C½ in range**, it often means your concentration gradient didn't capture the unfolding transition (the protein was either too stable or too unstable for the denaturant range used).