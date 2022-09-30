# CHalf Preprocessing Tools

CHalf is designed to be compatible with most any workflow. When we built it, we optimized it for outputs from PEAKS Studio, but we have included some tools for quickly converting other MS data processing software outputs to CHalf compatible input files (protein-peptides.csv and proteins.csv). We have not created tools for converting outputs from every MS data processing software, but we intend to continually update this list of tools as new preprocessing tools are created. If your software output lacks a preprocessing tool please see our [CHalf Formatting Guide](https://github.com/JC-Price/Chalf_public/blob/main/Demos/CHalf%20Inputs%20Formatting%20Guide.xlsx). As you learn to format your own outputs to be compatible with CHalf, we invite you to submit your own preprocessing tools to us so that everyone can benefit from being able to use CHalf. Your submitted preprocessing tools will be attributed to you in this document and will include a section for users to properly cite your tool if used.

## Table of Contents
- [MaxQuant](https://github.com/JC-Price/Chalf_public/edit/main/CHalf%20Preprocesing%20Tools/README.md#MaxQuant)
- [Proteome Discoverer (PD)](https://github.com/JC-Price/Chalf_public/edit/main/CHalf%20Preprocesing%20Tools/README.md#proteome-discoverer-pd)

## MaxQuant
Author: Chad D. Hyer - Brigham Young University - Department of Chemistry and Biochemistry

Citation: doi

[Download](https://github.com/JC-Price/Chalf_public/blob/main/CHalf%20Preprocesing%20Tools/Maxquant_CHalf_Preprocessor.py)

Directions for converting MaxQuant files to the proper CHalf output:

1. Open 'Maxquant_CHalf_Preprocessor.py' using an IDE capable of editing Python files
2. Set 'evidence_txt_path' to the path for your evidence.txt file from MaxQuant
3. Set 'peptides_txt_path' to the path for your peptides.txt file from MaxQuant
4. Find the abundance columns in your evidence.txt file. Add their names as strings 
   to the list 'abundance_columns'
5. Set 'output_directory' to your desired output directory
6. Set 'output_name' to your desired output name
7. For every PTM searched for in your MaxQuant run, calculate the mass shift. Using
   these PTM names and mass shifts, edit 'reporters_dictionary'. It will take the format
   reporters_dictionary = {
       (PTM name 1) : (mass shift 1),
       (PTM name 2) : (mass shift 2),
       ...
       (PTM name n) : (mass shift n)
       }
   As an example of a key set: {'Oxidation (M)' : '+15.99'}
   
   ***It is essential that every single PTM is accounted for, or there will be errors.***
8. Run 'Maxquant_CHalf_Preprocessor.py'
9. Take the protein-peptides.csv and proteins.csv files outputed for use with CHalf





## Proteome Discoverer (PD)
Author: Chad D. Hyer - Brigham Young University - Department of Chemistry and Biochemistry

Citation: doi

[Download](https://github.com/JC-Price/Chalf_public/blob/main/CHalf%20Preprocesing%20Tools/Proteome_Discoverer_CHalf_Preprocessor.py)

Directions for converting Proteome Discoverer (PD) files to the proper CHalf output:

1. Open 'Proteome_Discoverer_CHalf_Preprocessor.py' using an IDE capable of editing Python files
2. Set 'peptide_txt_path' to the path for your PeptideGroups.txt file from PD
3. Set 'proteins_txt_path' to the path for your Proteins.txt file from PD
4. Find the abundance columns in your PeptideGroups.txt file. Add their names as strings 
   to the list 'abundance_columns'
5. Set 'output_directory' to your desired output directory
6. Set 'output_name' to your desired output name
7. For every PTM searched for in your PD run, calculate the mass shift. Using
   these PTM names and mass shifts, edit 'reporters_dictionary'. It will take the format
   reporters_dictionary = {
       (PTM name 1) : (mass shift 1),
       (PTM name 2) : (mass shift 2),
       ...
       (PTM name n) : (mass shift n)
       }
   As an example of a key set: {'Oxidation' : '+15.99'}
   
   ***It is essential that every single PTM is accounted for, or there will be errors.***
8. Run 'Proteome_Discoverer_CHalf_Preprocessor.py'
9. Take the protein-peptides.csv and proteins.csv files outputed for use with CHalf
