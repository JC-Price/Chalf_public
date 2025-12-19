# Experimental Options

The **Experimental Options** in CHalf allow users to apply advanced signal processing and alternative fitting strategies to their data. These settings are designed for datasets with high noise levels or complex, non-ideal folding behaviors.

> **⚠️ Note:** These features modify the raw data or the standard fitting logic. Use them with caution and always verify the results against the standard output to ensure biological relevance.

## 1. Savitzky-Golay Smoothing (`sg`)
This option applies a digital filter to the raw intensity data *before* any curve fitting occurs. It is used to reduce random noise in the mass spectrometry signal without distorting the overall shape of the denaturation curve.

### How it Works
The software uses the **Savitzky-Golay filter** (from `scipy.signal`), which fits successive sub-sets of adjacent data points with a low-degree polynomial by the method of linear least squares.
* **Effect:** It smooths out high-frequency "jitter" or spikes in intensity.
* **Benefit:** Can improve $R^2$ values for peptides with low signal-to-noise ratios.

### Settings
| Setting | Workflow Key | Description |
| :--- | :--- | :--- |
| **Smooth** | `chalf.experimental.sg.smooth` | *(Default: False)* Set to `True` to enable the filter. |
| **Window** | `chalf.experimental.sg.window` | *(Default: 5)* The size of the filter window (number of data points). A larger window creates a smoother curve but may flatten sharp transitions. |
| **Order** | `chalf.experimental.sg.order` | *(Default: 2)* The order of the polynomial used to fit the samples. |

---

## 2. Window Fit (`wf`)
The Window Fit algorithm is a "rescue" strategy for curves that fail standard quality control checks, particularly those that exhibit **non-monotonic behavior** (e.g., intensity goes up and down randomly).

### How it Works
Standard CHalf analysis attempts to fit the entire concentration range (e.g., 0M to 3.59M) to a single sigmoid curve. If this fit is poor (low Spearman correlation or does not meet other fitting criteria), the **Window Fit** option activates:
1.  **Segmentation:** It breaks the full curve into smaller, overlapping segments ("windows") of `N` points.
2.  **Local Fitting:** It attempts to fit a sigmoid curve to each individual window.
3.  **Selection:** It identifies if any valid transition exists within these smaller windows that was obscured by noise or secondary kinetic effects elsewhere in the gradient.

### Use Case
This is particularly useful for:
* **Multiphasic Transitions:** Proteins that unfold in multiple distinct steps.
* **Artifacts:** Data where one end of the curve is perfect but the other end has erratic noise that ruins the global fit.

### Settings
| Setting | Workflow Key | Description |
| :--- | :--- | :--- |
| **Window Fit** | `chalf.experimental.wf.window_fit` | *(Default: False)* Set to `True` to enable this logic. |
| **Window Size** | `chalf.experimental.wf.window` | *(Default: 6)* The number of consecutive concentration points to include in each sub-segment. |

---

## 3. Mutation Scanning (Advanced Input)
While not a flag in the `chalf.experimental` section, the software supports an experimental **Mutation Mode** via specific input formatting.

### How it Works
When provided with an input file containing an additional `Mutation` column:
1.  **Tracking:** The software tracks the stability ($C_{1/2}$) of the specific mutant peptide separately from the wild-type.
2.  **Comparison:** In downstream Visualization modules (Residue Mapper), enabling `mutation_search` allows the software to automatically calculate and plot the $\Delta C_{1/2}$ (Stability Change) induced by the mutation.

* **Input Requirement:** Your CSV must contain a `Mutation` column (e.g., containing "E544D").
* **Visualization Key:** `visualization.rm.other.mutation_search=True`