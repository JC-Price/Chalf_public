# CHalf Outputs Explained

- CHalf - Fits chemical/heat denature mass spec data to a sigmoid curve to calculate protein/peptide C½ values.

        Table Outputs:
            -[CONDITION]_Rep[n]_OUTPUT.csv - C½ values and curve data for each Rep in a condition
            -[CONDITION]_Combined_OUTPUT.csv - Combination of rep data for each condition. Contains trimmed C½ values and curve data. (toggleable)
            -[CONDITION]_Giant_OUTPUT.csv - Combination of all Combined_OUTPUT.csv's for a given run. (toggleable)

        Graph Outputs: (toggleable, off by default)
            -[CONDITION]_Rep[n]==Index==[k]==Graph[.svg/.jpg/.png] - Graph of C½ sigmoidal curves for proteins/peptides in Rep data
            -[CONDITION]_Combined==Index==[k]==Graph[.svg/.jpg/.png] - Graph of C½ sigmoidal curves for proteins/peptides in Combined data

  Headers and Graph Components Explained: [Link](https://github.com/JC-Price/Chalf_public/blob/main/Demos/CHalf%20Outputs%20Headers.md)
- Label Finder (Label Efficiency) - Calculates what percent of peptides/proteins in your sample were successfully tagged.

        Outputs: 
            -[CONDITION] Label Efficiency.csv : Summary table of label efficiency counts for a given rep.
            -[CONDITION] Tags.csv : List of tagged peptides.
  Headers and File Components Explained: [Link](https://github.com/JC-Price/Chalf_public/blob/main/Demos/Label%20Finder%20Explanations.md)
- Fitting Efficiency - Calculates what percent of peptides/proteins in your sample were fittable by a sigmoidal curve.

        Outputs:
            -[CONDITION] Fitting Efficiency.csv : Summary table of fitting efficiency counts for combined data.
            -[CONDITION] Label Sites.csv : Table of peptides that meet all fitting conditions (minus >1 reporter)
                         and have a label. This table also shows the label site and type of each peptide (i.e. 'Y423.0').
                         This table is used by Combined Site.
            -[CONDITION] Combined Label Sites.csv : Similar to Label Sites. Combined Label Sites differs in that it 
                         combines the C½ curves of peptides that have the same modification at the same residue 
                         and refits them to calculate a new combined C½ value, r^2 value, and confidence interval.
                         This table used by Residue Mapper and Combined Residue Mapper.
            -[CONDITION] Fitted Peptides.csv : Table of lists of peptides that meet the various conditions for the fitting
                         counts. Used for reference.
            -[CONDITION] Removed Sites.csv : Table of peptides that failed the second fitting between label sites and combined label sites.
  Headers and File Components Explained: [Link](https://github.com/JC-Price/Chalf_public/blob/main/Demos/Fitting%20Efficiency%20Explanations.md)

- Combined Site - Compares C½ values across conditions for shared peptides.

        Ouputs:
            - [MODIFICATION][_LABELSITE][_ACCESSION][.svg/.jpg/.png] : Boxplots of C½ values for a given residue across multiple conditions.
            - [PROJECT] Shared_OUTPUT.csv : Statistical data from boxplots for reference.
  Headers and File Components Explained: [Link](https://github.com/JC-Price/Chalf_public/blob/main/Demos/Combined%20Site%20Explanations.md)
  
- Residue Mapper - Shows regional protein stability by comparing C½ values across label sites in a given protein.

        Outputs:
            -[ACCESSION][.svg/.jpg/.png] - Graphs of C½ values [y-axis] vs. label site [x-axis] for a given protein.
            -[ACCESSION].csv - Statistical values for graphs. For reference.
  Headers and File Components Explained: [Link](https://github.com/JC-Price/Chalf_public/blob/main/Demos/Residue%20Mapper%20Explanations.md)
            
- Combined Residue Mapper - Compares Residue Mapper ouputs across conditions. Note: CRM performed in CHalf v4.2.1 if you opt to do Combined Site or if you perform it manually using the Other Tools Menu.

        Outputs:
            -[[NAME]] RCS Summary.csv - Combination of all CRM Stats.csv files into a single summary table.
            -[ACCESSION] Combined Residue Map [.svg/.jpg/.png] - Graphs of C½ values [y-axis] vs. label site [x-axis] for a given protein across conditions.
            -[ACCESSION] CRM Stats.csv - Statistical values for graphs. For reference.
  Headers and File Components Explained: [Link](https://github.com/JC-Price/Chalf_public/blob/main/Demos/Combined%20Residue%20Mapper%20Explained.md)
