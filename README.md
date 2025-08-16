# CHalf v4.3
![alt text](https://github.com/JC-Price/Chalf_public/blob/main/v4.2/Graphics/CHalf%20v4.2.2%20README%20Logo.png)

CHalf is a protein stability research tool. CHalf uses peptide intensity information within a denaturation curve to calculate the denaturation midpoint (“CHalf”) of protein/peptide fragments.  The tool was designed for use with mass spectrometry based information and can accept peptide quantification files from any proteomics identification and quantification software with some attention to [formatting](https://github.com/JC-Price/Chalf_public/blob/fc574fafca57c2196174d111e46f9d5ba4452b7b/Demos%20and%20Documentation/formatting_guide.md).

As proteins are subjected to a gradient of denaturing solutions (i.e. GdmCl) or temperatures, they unfold in varying amounts, exposing sites that cause precipitation (for thermal denaturation style experiments) or are labeled using tags such as iodine (for chemical denaturation style experiments).
CHalf uses peptide signal intensities at these differing conentration points and produces a sigmoid curve. The midpoint of this sigmoid curve is the CHalf value and represents the relative folding stability of these protein/peptide fragments.

Included with CHalf is a suite of tools that can be used to perform quality control on your folding experiments to calculate the label and fitting efficiency of sample preparation and tools for comparing changes in folding stability at a single residue level and across the protein sequence space in-between conditions.

For information on previous versions, see [here](https://github.com/JC-Price/Chalf_public/blob/main/v4.2/README.md).

## Authors
[Chad D. Hyer](https://www.linkedin.com/in/chad-hyer-833702162/), [Connor Hadderly](https://www.linkedin.com/in/connorthaderlie), Monica Berg, [Hsien-Jung Lavender Lin](https://www.linkedin.com/in/hsien-jung-lin-254538197), [John C. Price](https://www.linkedin.com/in/john-price-1ba26b35/)

  
## Acknowledgements

Brigham Young University Department of Chemistry and Biochemistry

John C Price Lab Group

Special thanks to Dr. Bradley R. Naylor for development assistance.

We love [Fragpipe](), so we took some inspiration from their graphical interface as we designed ours. Our tools do very different things, but feel free to check out their work.

DISCLAIMER: Some generative AI was used during development of CHalf's GUI. All CHalf core features were built by hand.

Citations:

Hyer, C. D.; Lin, H.-J. L.; Haderlie, C. T.; Berg, M.; Price, J. C. CHalf: Folding Stability Made Simple. Journal of Proteome Research 2023, 22 (2), 605-614. DOI: 10.1021/acs.jproteome.2c00619.

Lin, H.-J. L.; James, I.; Hyer, C. D.; Haderlie, C. T.; Zackrison, M. J.; Bateman, T. M.; Berg, M.; Park, J.-S.; Daley, S. A.; Zuniga Pina, N. R.; et al. Quantifying In Situ Structural Stabilities of Human Blood Plasma Proteins Using a Novel Iodination Protein Stability Assay. Journal of Proteome Research 2022. DOI: 10.1021/acs.jproteome.2c00323.

## Contact

For inquiries about CHalf or to request additional information, please use our GitHub or direct inquiries to jcprice@chem.byu.edu. We will do our best to respond in a timely fashion so you can use our software for your needs.

## Table of Contents
- [Installation](https://github.com/JC-Price/Chalf_public/blob/main/v4.2,README.md#installation)
- [Features](https://github.com/JC-Price/Chalf_public/blob/main/v4.2,README.md#features)
- [Instructions](https://github.com/JC-Price/Chalf_public/blob/main/v4.2,README.md#instructions)
- [Demo](https://github.com/JC-Price/Chalf_public/blob/main/v4.2,README.md#demo)
- [Support](https://github.com/JC-Price/Chalf_public/blob/main/v4.2,README.md#support)

## Installation

Version 4.3 - Excecuteable file with integrated tools and GUI. Does not require Python installation.

[Download](https://github.com/JC-Price/Chalf_public/releases/tag/CHalf_v4.3)

Installation: Extract the zipped folder and run ```CHalf_v4_3.exe```. For proper use, please maintain the extracted folder structure. CHalf will rely on assets in ```concentration_columns```, ```core```, ```images```, and ```workflows``` folders for preparing your CHalf runs.

Additional ways of installing and running CHalf:
- [Running CHalf from an IDE and source code]()
- [Building CHalf from source code as a standalone executable]()
- [Running CHalf headless]()

## Features

For all features, see the hyperlinked guides for additional information about how to properly use the module and understand their outputs.

- [CHalf]() - Fits chemical/heat denature mass spec data to a sigmoid curve to calculate protein/peptide CHalf values.

        Inputs:
            -Formatted peptide abundance .csv from any proteomics identification and quantification software.
        
        Outputs:
            -{CONDITION}_Combined_OUTPUT.csv - Raw fitted curve information for each condition with CHalf values and other fitting parameters.
            -{CONDITION} Sites.csv - Significant fitted curves with individual-amino-acid-localizable CHalf values.
            -{CONDITION} Combined Sites.csv - Localized CHalf values. This is the primary output of CHalf for downstream analysis.
        
        Graph Outputs: (toggleable, off by default)
            -{ACCESSION@PEPTIDE}.[svg/jpg/png] - Graph of CHalf sigmoid curves for proteins/peptides.

- [Quality Control]() - Identifies condition-specific quality metrics for troubleshooting sample preparation or acquisition issues.

        Inputs:
            -Formatted peptide abundance .csv from any proteomics identification and quantification software.
            -{CONDITION}_Combined_OUTPUT.csv - Raw fitted curve information for each condition with CHalf values and other fitting parameters. Generated by CHalf.
            -{CONDITION} Combined Sites.csv - Localized CHalf values. Generated by CHalf.
        
        Output:
            -{CONDITION} Quality Control.csv - Contains fitting and labeling efficiency metrics from your CHalf run.

- [Visualization Modules]() - Tools for helping you quickly identify changes in CHalf values in-between conditions and generating figures for presentations and publications.

    - Quality Control Report - Compares Residue Mapper ouputs across conditions. Note: CRM performed in CHalf v4.2.2 if you opt to do Combined Site or if you perform it manually using the Other Tools Menu.

            Inputs:
                -{CONDITION} Combined Sites.csv (from CHalf) (one per condition)
                -visualization_config.vis (from CHalf GUI) (contains figure parameters)

            Output: qc_report.html - Interactive figure for comparing overall distributions of CHalf values between conditions and identifying the number of significant measurements calculated across conditions.

    - Residue Mapper - Shows regional protein stability by comparing CHalf values across label sites in a given protein.

            Input: {CONDITION} Combined Sites.csv (from CHalf)

            Outputs:
                -{ACCESSION}.[svg/jpg/png] - Graphs of CHalf values [y-axis] vs. residue number [x-axis] for a given protein.
                -{ACCESSION}_stats.csv - Statistical values for graphs. For reference.
    
    - Combined Residue Mapper - Compares Residue Mapper-like outputs across conditions.

            Inputs:
                -{CONDITION} Combined Sites.csv (from CHalf) (one per condition)
                -visualization_config.vis (from CHalf GUI) (contains figure parameters)

            Outputs:
                -{ACCESSION}.[svg/jpg/png] - Graphs of CHalf values [y-axis] vs. residue number [x-axis] for a given protein across conditions.
                -{ACCESSION}_stats.csv - Statistical values for graphs. For reference.
    
    - Delta Mapper - Compares CHalf values across conditions across the protein sequence to identify significant changes in protein folding stability in-between conditions

            Inputs:
                -{CONDITION} Combined Sites.csv (from CHalf) (one per condition)
                -visualization_config.vis (from CHalf GUI) (contains figure parameters)

            Outputs:
                -{ACCESSION}_condition_comparison.[svg/jpg/png] - Graphs of delta CHalf values (Experimental - Reference) [y-axis] vs. residue number [x-axis] for a given protein across conditions.
                -{ACCESSION} ({REFERENCE_CONDITION} vs {EXPERIMENTAL_CONDITION}) Distribution Comparison.[svg/jpg/png] - KDE and boxplots comparisons between distributions of shared CHalf values for a given protein. Performs a kruskal-wallace test to determine the level of significance of differences between distributions.
                -{ACCCESSION}_condition_comparison_stats.csv - Statistical values for graphs. For reference.
    
    - Combined Site - Generates boxplots for Label@Accession groups across different conditions. Useful for comparing the distributions of peptide CHalf values that contribute to a localized amino-acid-specific CHalf value.

            Inputs:
                -{CONDITION} Sites.csv (from CHalf) (one per condition)
                -visualization_config.vis (from CHalf GUI) (contains figure parameters)

            Ouputs:
                - {LABEL@ACCESSION} Boxplot.[svg/jpg/png] - Boxplots of CHalf values for a given residue across multiple conditions.
                - CombinedSites_Summary.csv - Statistical data from boxplots for reference.

## Instructions

COMING SOON

## Demo

COMING SOON

## Support
As we have developed CHalf, we have put a lot of effort into addressing possible errors that could occur when calcuating CHalf values or preparing other outputs. We have also tried to reduce room for user error. If you are experiencing errors, please refer to the Common Error section bellow before contacting the JC Price Lab for support. Most errors are a result of improperly selecting inputs or improperly specifying run conditions unique to your samples. Modifying CHalf or using nonstandard inputs runs the risk of raising unanticipated errors, so do so at your own risk. Before using nonstandard inputs or modifying CHalf, please review the demo section within this README.

Common Errors:

COMING SOON