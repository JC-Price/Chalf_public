# Fitting Efficiency Headers and File Components Explained

Fitting Efficiency Output

![Fitting Efficiency Output](https://github.com/JC-Price/Chalf_public/blob/main/Graphics/FE%20Explained.png)

Label Sites Output Headers
- Version: Version of CHalf used to produce the file
- Accession: Uniprot protein accession of the associated peptide
- Peptide: Peptide sequence
- Start: Starting amino acid residue number
- End: Ending amino acid residue number
- Peptide Length: Length of the peptide sequence
- trim_CHalf: C½ value of the peptide
- trim_r_squared: R^2 value of the fitting curve
- trim_ratioTOrange: Confidence interval of the C½ value / range of the denaturant curve
- trim_CHalf_ConfidenceInterval: Confidence interval of the C½ value
- trim_slope: Slope of the fitting curve
- trim_b: Steepness of the fitting curve
- Label Site: Amino acid residue identity and position of the label on the peptide
- Label Type: Label species on the labeled residue
- Residue Number: Residue number for the labeled site
- Label@Accession: Identifier for the peptide containing label site, label type, and accession ID
- Denaturant Points: Normalized abuncances used to fit the curve

Combined Label Sites Output Headers
- Version: Version of CHalf used to produce the file
- Accession: Uniprot protein accession of the associated peptide
- Peptide: Peptide sequences of source peptides
- Label@Accession: Identifier for the peptide containing label site, label type, and accession ID
- Label Site: Amino acid residue identity and position of the label on the peptide
- Label Type: Label species on the labeled residue
- Residue Number: Residue number for the labeled site
- Count: Number of peptides used to calculate the combined site
- trim_CHalf: C½ value of the peptide
- trim_r_squared: R^2 value of the fitting curve
- trim_ratioTOrange: Confidence interval of the C½ value / range of the denaturant curve
- trim_CHalf_ConfidenceInterval: Confidence interval of the C½ value
- trim_slope: Slope of the fitting curve
- trim_b: Steepness of the fitting curve


Fitted Peptides Output Headers
- Version: Version of CHalf used to produce the file (also includes source index from combined output for peptides under "C1/2 in range")
- C1/2 in range (MIN:MAX): peptides whose C½ value is within the specified fitting range for C½ value
- index_1: source index from combined output for peptides under "r^2 > (MIN)"
- r^2 > (MIN): peptides within the correct C½ range and with an r^2 value greater than the specified threshold
- index_2: source index from combined output for peptides under "Conf Int in range (MIN:MAX)"
- Conf Int in range (MIN:MAX): peptides within the correct C½ range, r^2 value, and with a confidence interval within the specified threshold
- index_3: source index from combined output for peptides under "has >1 reporter"
- has >1 reporter: peptides within the correct C½ range, r^2 value, confidence interval, and have more than one peptide within the given protein

Removed Sites Output Headers
- Version: Version of CHalf used to produce the file
- Accession: Uniprot protein accession of the associated peptide
- Peptide: Peptide sequences of source peptides
- Label@Accession: Identifier for the peptide containing label site, label type, and accession ID
- Label Site: Amino acid residue identity and position of the label on the peptide
- Label Type: Label species on the labeled residue
- Residue Number: Residue number for the labeled site
- Count: Number of peptides used to calculate the combined site
- trim_CHalf: C½ value of the peptide
- trim_r_squared: R^2 value of the fitting curve
- trim_ratioTOrange: Confidence interval of the C½ value / range of the denaturant curve
- trim_CHalf_ConfidenceInterval: Confidence interval of the C½ value
- trim_slope: Slope of the fitting curve
- trim_b: Steepness of the fitting curve
