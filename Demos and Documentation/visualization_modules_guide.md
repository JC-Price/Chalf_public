# Visualization Module & Configuration

The **Visualization** tab is the final stage of the CHalf pipeline. It translates your processed CSV data into publication-ready figures.

---

## 1. GUI Configuration (The Visualization Table)
The core of this module is the interactive table found in the Visualization tab. You do not manually write a `.vis` file; instead, you build your experimental design in this table, and the software compiles it into the necessary configuration for the plotting engines.

### How to Build Your Visualization Config
Use the "Add" button to create a row for each experimental condition you wish to analyze.

| Column | Description |
| :--- | :--- |
| **Condition** | **Must match exactly** the unique condition string from your output folder (e.g., `condition_0`). This tells the software which data source to read. |
| **Group** | Arbitrary label (e.g., `Group 1`). All conditions assigned to the same Group will be plotted together on the same graph in the **Combined Residue Mapper**. |
| **Class** | Defines the dataset's role for comparison: <br>• **Reference**: The baseline state (e.g., Wild Type). <br>• **Experimental**: The variant state. Used by Delta Mapper to calculate $\Delta C_{1/2}$. There **must** be at least one `Reference` per group.|
| **Color** | The specific color used for this condition's curve/points in all plots. Click to select via color picker or enter a hex code (e.g., `#1f77b4`). |

---

## 2. Visualization Tools
The software includes three specific "Mappers," and two additional visualization tools, each with unique algorithmic settings controlled by your workflow file.

### A. Residue Mapper (Single Condition)
*Generates individual stability plots for one condition at a time.*
* **Input Source:** `Combined Sites.csv` (Aggregated residue-level data)

**Residue Mapper Output**
![Example residue mapper figure](https://github.com/JC-Price/Chalf_public/blob/main/Graphics/v4.3/residue_mapper_example.jpg)

**Settings:**
* **Min / Max:** (`visualization.rm.min` / `.max`)
    * *(Default: 0.0 - 3.48)* Sets the vertical range of the plot. *Recommendation:* Set slightly wider than your denaturant gradient to avoid clipping data.
* **Trendline:** (`visualization.rm.trendline`)
    * *(Default: True)* Overlays a rolling average line on the raw data points. Essential for distinguishing structural domains from noise.
    * **Window Size:** (`visualization.rm.trendlines.window`)
        * *(Default: 3)* The number of residues averaged for each point on the line.
    * **Minimum Points:** (`visualization.rm.trendlines.min`)
        * *(Default: 5)* The minimum number of quantified residues required  to draw the trendline.
* **Reference Stats:** (`visualization.rm.other.reference_stats`)
    * *(Default: True)* If enabled, generates `_stats.csv` files containing the numbers associated with each figure.
* **Trendline Stats:** (`visualization.rm.other.crm_trendline_stats`)
    * *(Default: False)* Adds the numbers behind the trendline to the `_stats.csv` file.
* **Mutation Search:** (`visualization.rm.other.mutation_search`)
    * *(Default: False)* If enabled, highlights specific point mutations defined in the input CSV. To use this function, your CHalf search must have used the mutation setting in [CHalf Experimental Options](https://github.com/JC-Price/Chalf_public/blob/main/Demos%20and%20Documentation/experimental_options_guide.md).

### B. Combined Residue Mapper (Multi-Condition)
*Overlays multiple conditions (sharing the same "Group") onto a single plot.*
* **Input Source:** `Combined Sites.csv` (Aggregated residue-level data)

**Combined Residue Mapper Output**
![Example combined residue mapper figure](https://github.com/JC-Price/Chalf_public/blob/main/Graphics/v4.3/combined_residue_mapper_example.jpg)

**Settings:**
* **Min / Max:** (`visualization.crm.min` / `.max`)
    * *(Default: 0.0 - 3.48)* Vertical axis range.
* **Shared Only:** (`visualization.crm.other.shared_only`)
    * *(Default: True)* **Critical Filter:** If enabled, the plot **only** displays residues that were successfully quantified in **every** condition within the group. This ensures a strict 1-to-1 comparison.
* **Labeled and Unlabeled Curves:** (`visualization.crm.other.all_curves`)
    * *(Default: True)* Plots both significant labeled and unlabeled curves.
* **Reference Stats:** (`visualization.crm.other.reference_stats`)
    * *(Default: True)* If enabled, generates `_stats.csv` files containing the numbers associated with each figure.
* **Trendline Stats:** (`visualization.crm.other.crm_trendline_stats`)
    * *(Default: False)* Adds the numbers behind the trendline to the `_stats.csv` file.
* **Mutation Search:** (`visualization.rm.other.mutation_search`)
    * *(Default: False)* If enabled, highlights specific point mutations defined in the input CSV. To use this function, your CHalf search must have used the mutation setting in [CHalf Experimental Options](https://github.com/JC-Price/Chalf_public/blob/main/Demos%20and%20Documentation/experimental_options_guide.md).

### C. Delta Mapper (Stability Change)
*Plots the difference ($\Delta C_{1/2}$) between "Experimental" and "Reference" classes.*
* **Equation:** $\Delta C_{1/2} = C_{1/2} (Experimental) - C_{1/2} (Reference)$

**Delta Mapper Output**
![Example delta mapper figure](https://github.com/JC-Price/Chalf_public/blob/main/Graphics/v4.3/delta_mapper_example.jpg)

**Delta Mapper Distribution Figure**
![Example delta mapper distribution figure](https://github.com/JC-Price/Chalf_public/blob/main/Graphics/v4.3/delta_mapper_dist_example.jpg)

**Settings:**
* **Min / Max:** (`visualization.dm.min` / `.max`)
    * *(Default: -3.48 to +3.48)* Centered at 0 (no change).
    * **Positive (+):** Stabilized (Experimental is more stable).
    * **Negative (-):** Destabilized (Experimental is less stable).
* **Significance Filter:** (`visualization.dm.sig_filter`)
    * *(Default: False)* If enabled, the tool filters out non-significant changes based on the P-value column in the input data.
    * **Significance Cutoff:** (`visualization.dm.sig_value`)
        * *(Default: 0.05)* Points with $p > 0.05$ are hidden.
* **KDE Density Plot:**
    * Generates a side-panel histogram (Kernel Density Estimate) showing the global distribution of stability changes.
    * **Min Points:** (`visualization.dm.kde.min_pts`)
        * *(Default: 3)* The minimum number of shared data points required to generate this distribution.

### D. Quality Control Report
The Quality Control (QC) Report is a standalone HTML dashboard (`report.html`) that summarizes the statistical quality of your entire run. It provides interactive figures that allow you to assess fitting efficiency and reproducibility without opening multiple CSV files.

**Settings:**
These parameters control the generation of the report.

| Setting | Workflow Variable | Description |
| :--- | :--- | :--- |
| **Generate Report** | `visualization.qc.report` | *(Default: True)* If enabled, generates the `report.html` file in your output directory. |
| **Auto-Open** | `visualization.qc.open` | *(Default: False)* If enabled, automatically launches the report in your default web browser after processing. |

### E. Combined Site Visualization
The **Combined Site** module is a dedicated visualization tool for plotting stability data from the `Sites.csv` files. It is distinct from the Residue Mapper and offers specific settings for comparing site-level stability.

**Combined Site Output**
![Example combined site figure](https://github.com/JC-Price/Chalf_public/blob/main/Graphics/v4.3/combined_site_example.jpg)

**Settings**
These settings control the file output and axis scaling for the Combined Site plots.

| Setting | Workflow Variable | Description |
| :--- | :--- | :--- |
| **Enable Module** | `visualization.cs` | *(Default: True)* Master switch to generate Combined Site plots. |
| **File Type** | `visualization.cs.file_type` | *(Default: jpg)* Format of the output images (jpg, svg, png). |
| **Y-Axis Min** | `visualization.cs.min` | *(Default: 0.0)* Lower limit of the stability axis. |
| **Y-Axis Max** | `visualization.cs.max` | *(Default: 3.48)* Upper limit of the stability axis. |

---

## 3. Annotation Files (.ann) Technical Guide (Advanced Options)
The Annotation File is a powerful feature for injecting custom markers (domain boundaries, active sites, titles) onto your plots.

**Technical Format:**
The `.ann` file is a JSON-like text file that you can generate using any text editing software. CHalf reads this file and looks for specific variable names.

### A. The `custom_annotation` Dictionary (Required)
You must define a dictionary named `custom_annotation`.
* **Key:** Protein Accession ID (Exact match to accession in column, e.g., `P02768|ALBU_HUMAN`).
* **Value:** A **List** of annotation dictionaries.

**Supported Annotation Types:**
1.  **Vertical Line (`vline`):** Marks a specific residue index.
    * `{'type': 'vline', 'value': 103}`
2.  **Horizontal Line (`hline`):** Marks a specific $C_{1/2}$ value.
    * `{'type': 'hline', 'value': 2.5}`
3.  **Title Override (`title`):** Replaces the default Accession ID title.
    * `{'type': 'title', 'value': 'Serum Albumin'}`

### B. The `subset` List (Optional)
You may optionally define a list named `subset`.
* `subset = ['P02768|ALBU_HUMAN', 'P02766|TTHY_HUMAN']`
* **Function:** If this variable exists, the visualization module will **ignore all other proteins** in your dataset and only generate figures for the accessions listed here. This is ideal for quickly regenerating figures for a few targets of interest without processing the entire dataset.

### Example File Content
```python
# example.ann

# Optional: Limit run to these two proteins
subset = ['P02768|ALBU_HUMAN', 'P02766|TTHY_HUMAN']

# Required: Define markers
custom_annotation = {
    'P02768|ALBU_HUMAN' : [  
        # Set a custom title
        {'type' : 'title', 'value' : 'Albumin Domains'},
        
        # Mark Domain Boundaries
        {'type' : 'vline', 'value' : 103},
        {'type' : 'vline', 'value' : 298},
        
        # Mark a stability threshold
        {'type' : 'hline', 'value' : 2.3}
    ],
    
    'P02766|TTHY_HUMAN' : [
        {'type' : 'title', 'value' : 'Transthyretin'}
    ]
}