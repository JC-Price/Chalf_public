# CHalf Preprocessing Tools

CHalf is designed to be compatible with most any workflow. When we built it, we originally optimized it for outputs from PEAKS Studio, but we have included some tools for quickly converting other MS data processing software outputs to CHalf compatible input files (protein-peptides.csv and proteins.csv). We have not created tools for converting outputs from every MS data processing software, but we intend to continually update this list of tools as new preprocessing tools are created. If your software output lacks a preprocessing tool, please see our [CHalf v4.2 Formatting Guide](https://github.com/JC-Price/Chalf_public/blob/fc574fafca57c2196174d111e46f9d5ba4452b7b/v4.2/Demos%20and%20Documentation/CHalf%204.2%20Inputs%20Formatting%20Guide.xlsx) or [CHalf v4.3 Formatting Guide](https://github.com/JC-Price/Chalf_public/blob/fc574fafca57c2196174d111e46f9d5ba4452b7b/Demos%20and%20Documentation/formatting_guide.md). As you learn to format your own outputs to be compatible with CHalf, we invite you to submit your own preprocessing tools to us so that everyone can benefit from being able to use CHalf. Your submitted preprocessing tools will be attributed to you in this document and will include a section for users to properly cite your tool if used.

## Table of Contents
- [MaxQuant](https://github.com/JC-Price/Chalf_public/blob/main/CHalf%20Preprocesing%20Tools/README.md#maxquant)
- [Proteome Discoverer (PD)](https://github.com/JC-Price/Chalf_public/blob/main/CHalf%20Preprocesing%20Tools/README.md#proteome-discoverer-pd)
- [Fragpipe](https://github.com/JC-Price/Chalf_public/blob/main/CHalf%20Preprocesing%20Tools/README.md#fragpipe)

## MaxQuant
Author: Chad D. Hyer - Brigham Young University - Department of Chemistry and Biochemistry

[Download](https://github.com/JC-Price/Chalf_public/blob/main/CHalf%20Preprocesing%20Tools/Maxquant_CHalf_Preprocessor.py)

Directions for converting MaxQuant files to the proper CHalf v4.2 output:

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

[Download](https://github.com/JC-Price/Chalf_public/blob/main/CHalf%20Preprocesing%20Tools/Proteome_Discoverer_CHalf_Preprocessor.py)

Directions for converting Proteome Discoverer (PD) files to the proper CHalf v4.2 output:

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

## Fragpipe
Author: Chad D. Hyer - Brigham Young University - Department of Chemistry and Biochemistry

[Download](https://github.com/JC-Price/Chalf_public/tree/fc574fafca57c2196174d111e46f9d5ba4452b7b/CHalf%20Preprocesing%20Tools/frag_to_chalf)

Directions for processing MS data using Fragpipe in preparation for running CHalf.
1. Place FragToCHalf.exe outside of the ```fragpipe``` directory with another directory labeled ```workflows``` in the same directory. Store your desired ```.fp-workflow``` files in this directory for controlling how Fragpipe runs. Fragpipe will be run headless by FragToCHalf.
2. Open ```FragToCHalf.exe```.
3. Select your ```.raw``` or ```.mzML``` files and ensure that your Point values match your desired concentration gradient column names for CHalf.
4. Specify your acquisition method for each file.
5. Specify your condition name, and choose an ouptut directory. It is essential that there are no spaces in any of the paths of any of the files or directories you use. Otherwise Fragpipe will not be able to run your data.
6. Choose your Fragpipe method in the dropdown.
7. Select a custom FASTA if this applies.
8. Press run. Fragpipe will run headless and display its log in the FragToCHalf console. The Fragpipe project will be in your output directory as ```{condition}_FP```.
9. After Fragpipe is finished running, FragToCHalf will automatically detect how to generate a CHalf input by searching for a ```combined_modified_peptides.tsv``` if you are using a DDA method or the ```peptide.tsv``` and ```report_pr_matrix.tsv``` DIANN output for a DIA method. The CHalf input produced will be called ```{condition}.csv``` and can be directly fed into both CHalf v4.2 and v4.3.
10. (ADDITIONAL NOTE) if you do not want to run Fragpipe through FragToCHalf, you can run it independently and click "Run on Existing Project" in FragToCHalf to process the Fragpipe outputs into CHalf inputs. You will be prompted to select the directory of your Fragpipe project, and it will automatically detect if your project is DDA or DIA based on a ```combined_modified_peptides.tsv``` if you are using a DDA method or the ```peptide.tsv``` and ```report_pr_matrix.tsv``` DIANN output for a DIA method. The CHalf output will be included in the Fragpipe project directory and will be the name of the first experiment in the ```fragpipe-files.fp-manifest``` in the directory.
