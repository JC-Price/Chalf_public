# CHalf Input Formatting Guide

To ensure CHalf runs correctly, your input files must adhere to a specific structure. This guide covers the formatting for peptide quantification data (`.csv`) and the concentration definition files (`.cc`).

---

## 1. Peptide Quantification Data (.csv)
The primary input for CHalf is a CSV file containing peptide-level intensity data. This data can come from any proteomics software (Fragpipe, MaxQuant, Proteome Discoverer, Skyline, etc.) but must be formatted to match the CHalf standard. See [CHalf Preprocessing Tools](https://github.com/JC-Price/Chalf_public/tree/main/CHalf%20Preprocesing%20Tools) for existing tools for making CHalf-compatible inputs.

### Required Columns
Your CSV **must** contain the following headers (case-sensitive):

| Column Header | Description | Example |
| :--- | :--- | :--- |
| **Protein Accession** | Unique identifier for the protein. | `P02768\|ALBU_HUMAN` |
| **Peptide** | The amino acid sequence. Modifications can be included in parentheses. | `LQKY(+251.99)P` |
| **Start** | The integer position of the first residue in the protein sequence. | `24` |
| **End** | The integer position of the last residue. | `35` |
| **Mutation** | *(Optional)* Required only for Mutation Mode. Specifies the variant. | `E544D` |

### Data Columns (Concentrations)
In addition to the metadata above, your file must contain columns holding the raw intensity values.
* **Headers:** The headers for these columns can be integers (`0`, `1`, `2`) or strings (`Sample_A`, `Sample_B`), but they **must match exactly** the keys defined in your Concentration File (see below).
* **Values:** Raw intensity or area under the curve (AUC).

#### Example Input Table
| Protein Accession | Peptide | Start | End | 0 | 1 | 2 | ... |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| P02768 | LVNEVTEF | 42 | 49 | 95000 | 82000 | 45000 | ... |
| P02768 | VPQVSTPT | 88 | 95 | 10200 | 9800 | 9100 | ... |

### Peptide Label Scheme
In your `Peptide` column, your peptide sequences must use the format `{AA}({mod})` to indicate where the modification is occuring. An example peptide would look like `MASHY(+251.99)LFR`. Your peptide sequence must also be stripped of any additional characters on the ends (e.g., `K.MASHY(+251.99)LFR.A`). This is essential for calculating the correct residue number from the values in the `Start` and `End` columns.

---

## 2. Concentration Definitions (.cc)
The **Concentration Column** file (`.cc`) serves as a dictionary. It maps the column headers in your CSV (e.g., "1") to the actual chemical concentrations used in your experiment (e.g., "0.43 M").

You can create this file using the built-in GUI tool or by manually creating a JSON file.

### Method A: Using the GUI Editor
The CHalf Interface includes a helper tool to generate these files without writing code.

1.  **Open the Editor:** Navigate to the **Workflow** tab and click `Create/Edit` under the `Set concentration columns` section..
2.  **Add Points:**
    * **Column Header:** Enter the exact string used in your CSV header (e.g., `1`).
    * **Concentration:** Enter the numeric value for that sample (e.g., `0.43`).
3.  **Save:** Click "Save" to generate a `.cc` file. This file can now be loaded in the **Workflow** tab for future runs.

### Method B: Manual JSON Creation
The `.cc` file is simply a text file containing a JSON dictionary. You can create this in any text editor (Notepad, VS Code).

**Format Structure:**
```json
{
    "CSV_Column_Header" : Concentration_Value,
    "CSV_Column_Header_2" : Concentration_Value
}
```

These `.cc` files can then be included in the `concentration_columns` directory in the same directory as `CHalf_v4_3.exe`.