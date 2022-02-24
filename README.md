
# CHalf v4.2
![alt text](https://github.com/JC-Price/Folding-Chalf/blob/master/CHalf%20Versions/v4.2/CHalf%20v4.2%20README%20Logo.png)

CHalf is a protein stability research tool. CHalf uses Mass Spectrometry data run through the “PEAKS” software to calculate the chemical denaturation midpoint (“CHalf”) of protein/peptide fragments.

As proteins are subjected to varying concentrations of denaturing solutions (i.e. GdmCl), they unfold in varying ammounts, exposing sites that can be labeled using tags such as iodine.
CHalf measures what ammount of protein is denatured at these differing conentration points and produces a sigmoidal curve. The midpoint of this sigmoidal curve is the CHalf value and represents the relative folding stability of these protein/peptide fragments.

Included with CHalf is a suite of tools that can be used to calculate the label and fitting efficiency of sample preparation, to compare single residue protein stability across conditions, and to compare regional stability across residues within a protein in one or multiple conditions.

## Authors
Chad D. Hyer, Connor Hadderly, Monica Berg, Hsien-Jung Lavender Lin

  
## Acknowledgements

Brigham Young University Department of Chemistry and Biochemistry

John C Price Lab Group

Folding Assay and CHalf Release Paper: doi

Citation:

## Table of Contents
- [Installation](https://github.com/JC-Price/Folding-Chalf/blob/master/CHalf%20Versions/v4.2/README.md#installation)
- [Features](https://github.com/JC-Price/Folding-Chalf/blob/master/CHalf%20Versions/v4.2/README.md#features)
- [Instructions](https://github.com/JC-Price/Folding-Chalf/blob/master/CHalf%20Versions/v4.2/README.md#instructions)
- [Demo](https://github.com/JC-Price/Folding-Chalf/blob/master/CHalf%20Versions/v4.2/README.md#demo)
- [Support](https://github.com/JC-Price/Folding-Chalf/blob/master/CHalf%20Versions/v4.2/README.md#support)

## Installation

Version 4.2 - Excecuteable file with integrated tools and GUI. Does not require Python installation.

Download: fakeurl.com

Installation: Extract the zipped folder and run CHalf_v4.2.exe.

Version 3.3 - Standalone program (no integrated tools or GUI). Only to be used by more advanced users. Requires Python installation with Numpy, Pandas, OS, Scipy, and Matplotlib.

Download: fakeurl.com

Installation: Run using python terminal or edit masterfile line in a Python IDE and run.
```bash
  python CHalf_v3.3.py 'masterfile.csv'
```

## Features

- CHalf - Fits chemical/heat denature mass spec data to a sigmod curve to calculate protein/peptide CHalf values.

        Inputs:
            -proteins.csv (from PEAKS)
            -protein-peptides.csv (from PEAKS)
            -Masterfile.csv (only must be prepared if using v3.3 or lower, v4.2 onwards prepares this for you)
        
        Outputs:
            -[CONDITION]_Rep[n]_OUTPUT.csv - CHalf values and curve data for each Rep in a condition
            -[CONDITION]_Combined_OUTPUT.csv - Combination of rep data for each condition. Contains trimmed CHalf values and curve data. (toggleable)
            -[CONDITION]_Giant_OUTPUT.csv - Combination of all Combined_OUTPUT.csv's for a given run. (toggleable)
        
        Graph Outputs: (toggleable, off by default)
            -[CONDITION]_Rep[n]==Index==[k]==Graph[.svg/.jpg/.png] - Graph of CHalf sigmoidal curves for proteins/peptides in Rep data
            -[CONDITION]_Combined==Index==[k]==Graph[.svg/.jpg/.png] - Graph of CHalf sigmoidal curves for proteins/peptides in Combined data
- Label Finder (Label Efficiency) - Calculates what percent of peptides/proteins in your sample were successfully tagged.

        Input: [CONDITION]_Rep[n]_OUTPUT.csv (from CHalf)

        Outputs: 
            -[CONDITION] Label Efficiency.csv : Summary table of label efficiency counts for a given rep.
            -[CONDITION] Tags.csv : List of tagged peptides.
- Fitting Efficiency - Calculates what percent of peptides/proteins in your sample were fittable by a sigmoidal curve.
        
        Input: [CONDITION]_Combined_OUTPUT.csv (from CHalf)

        Outputs:
            -[CONDITION] Fitting Efficiency.csv : Summary table of fitting efficiency counts for combined data.
            -[CONDITION] Label Sites.csv : Table of peptides that meet all fitting conditions (minus >1 reporter)
                         and have a label. This table also shows the label site and type of each peptide (i.e. 'Y423.0').
                         This table is used by Combined Site.
            -[CONDITION] Combined Label Sites.csv : Similar to Label Sites. Combined Label Sites differs in that it 
                         combines the CHalf curves of peptides that have the same modification at the same residue 
                         and refits them to calculate a new combined CHalf value, r^2 value, and confidence interval.
                         This table used by Residue Mapper and Combined Residue Mapper.
            -[CONDITION] Fitted Peptides.csv : Table of lists of peptides that meet the various conditions for the fitting
                         counts. Used for reference.
            -[CONDITION] Removed Sites.csv : Table of peptides that failed the second fitting between label sites and combined label sites.

- Combined Site - Compares CHalf values across conditions for shared peptides.

        Inputs: [CONDITION] Label Sites.csv (from Fitting Efficiency)

        Ouputs:
            - [MODIFICATION][_LABELSITE][_ACCESSION][.svg/.jpg/.png] : Boxplots of CHalf values for a given residue across multiple conditions.
            - [PROJECT] Shared_OUTPUT.csv : Statistical data from boxplots for reference.
- Residue Mapper - Shows regional protein stability by comparing CHalf values across label sites in a given protein.

        Input: [CONDITION] Combined Label Sites.csv (from Fitting Efficiency)

        Outputs:
            -[ACCESSION][.svg/.jpg/.png] - Graphs of CHalf values [y-axis] vs. label site [x-axis] for a given protein.
            -[ACCESSION].csv - Statistical values for graphs. For reference.
- Combined Residue Mapper - Compares Residue Mapper ouputs across conditions. Note: CRM performed in CHalf v4.2 if you opt to do Combined Site or if you perform it manually using the Other Tools Menu.

        Inputs: [CONDITION] Combined Label Sites.csv (from Fitting Efficiency)

        Outputs:
            -[[NAME]] CRM Summary.csv - Combination of all CRM Stats.csv files into a single summary table.
            -[ACCESSION] Combined Residue Map [.svg/.jpg/.png] - Graphs of CHalf values [y-axis] vs. label site [x-axis] for a given protein across conditions.
            -[ACCESSION] CRM Stats.csv - Statistical values for graphs. For reference.
## Instructions

CHalf_v4.2:
- Run CHalf_v4.2.exe and a GUI will open
- Select an output directory by pressing Set Dir (unless you have a default directroy set in CHalf Defaults.csv)
- Input Project Name and press Create Project or press Open Project to select an existing project.
- Press Add Condition to add conditions to your project. This opens the Condition Creator.
- Condition Creator

        1. Input Condition Name
        2. Specify the number of replicates
        3. Specify the type of denature used (CD (default) - Chemical Denature, HD - Heat Denature)
        4. Specify the number of Concentration/Temperature points used in the experiment
        5. Switch to the Concentrations/Temperatures Tab and specify the values used in your experiment. By default, we use [0, 0.43, 0.87, 1.3, 1.74, 2.17, 2.61, 3.04, 3.48, 3.59]. If you use other concetrations/temperatures, it is imperative that you change these values to get correct outputs.
        6. Switching back to the Condition Tab, you may modify the Calculation Options. These options should largely be left alone, you may change them, but the defaults provide the most useful results:
            - Individual Rep Analysis (True) : Produces a [CONDTION]_Rep[n]_OUTPUT.csv file for each replicate in your run.
            - Rep Graphs (False) : Produces graph outputs for each protein/peptide in your replicates that meet the specified conditions (see Graph Filters). (It is recommended to leave graphing off as graphing the values takes more time than running the actual calculations. Most graphs aren't really necessary, and we have found that the other tools included with CHalf are more useful for making inferences about protein stability.)
            - Combined Analysis (True) : Combines data from replicates to calculate CHalf values for a whole condition. Without this, Remove Outlier Analysis will not occur and Fitting Efficiency cannot be calculated.
            - Remove Outlier Analysis (True) : Calculates trimmed CHalf values and trimmed curve values. Without this, Fitting Efficiency cannot be calculated.
            - Graph Combined (False) : Produces graph outputs for each protein/peptide in your combined data that meet the specified conditions (see Graph Filters).
            - Giant Output (False) : Creates a large table with data from each of your conditions. This can be useful for comparing protein/peptide presence across conditions if your experiment uses fractionation, but, otherwise, this option can largely be ignored.
            - Minimum Points for Calculation (4) : Sets the minimum number of non-null points CHalf will accept to fit a protein/peptide to a sigmoidal curve. It is not recommended to go any lower than 4 if you want useful data.
            - Outier StdErr Cutoff (StdErr x #) (2) : Sets the cutoff interval for points to be used in calculating sigmoidal curves. Points whose values are greater than the standard error times the number listed will be treated as outliers and will be excluded from the fitting calculation.
            - Graph Filters: (default values are the most useful)
                CI Mx% of Range (0.3): Graphs if 2 * [CONFIDENCE INTERVAL] <= [NUMBER] * [CONC/TEMP RANGE]
                R^2 Cutoff (0.99): Graphs if R^2 value for sigmoidal curve >= [NUMBER]
                CHalf Range Cutoff (0.5): Graphs if [FIRST CONC/TEMP] - [TEMP/CONC RANGE] * [NUMBER] <= [CHalf] <= [LAST CONC/TEMP] + [CONC/TEMP RANGE] * [NUMBER]
        7. Select Other Features (for a detailed description of what the other features do, consult the Features section)
        8. (If using Combined Site or Residue Mapper) Specify the ymin (0) and ymax (3.6) for graphic outputs. These should be similar in value to your minimum and maximum concentrations/temperatures. You may alternatively elect to have a dynamic y axis that fits the axis according to your data. Note: Combined Site uses the range listed for the last condition prepared, so it is best to use the same range across conditions.
        9. Press Create and a folder will be opened containing your Rep folders.
        10. Add your proteins.csv and protein-peptides.csv files to each Rep folder in the condition.
        11. Double check that your specifications for the condition are correct.
        12. Press Process. A popup will appear if the condition has been created successfuly.
        13. Press Return
- Press Refresh to confirm that your condition has been added to the project.
- Add all conditions you would like to run. You may select a condition in the list to edit its masterfile or delete it. WARNING: Deleting a condition deletes the folder and all of the files inside it. Editing a masterfile is not difficult, but please refer to the section on masterfile editing in v3.3 to edit the masterfile properly.
- After adding all the conditions, you can specify what type of graphics outputs you would like (.svg/.jpg/.png) by pressing Graphics Options on the Menubar.
- Press Start and a popup will appear indicating that CHalf has been initialized. Press OK and CHalf will start. A progress bar should be visible in the console, and CHalf will run until a popup says that the run is complete or an error apepears. For errors, check the common error section.
- Once CHalf is complete, you may view the outputs by pressing Open Folder.

CHalf_v3.3:
- Create a Masterfile using 'CHalf_v3.3 Masterfile Template.csv.'
        
        MASTERFILE EDITING:
        1. Specify Run Description and Condition (eash row is a seperate condition unless you specify multiple replicates for a condition)
        2. Input the replicate number for each replicate (if there is only one replicate in a condition, just list it as 1; for multiple replicates, be sure to have the same run description and condition for each replicate.)
        3. Input the path for your Protein-Peptides Infile for each condition and its replicates. (this is the path of your PEAKS protein-peptides.csv file)
        4. Input the path for your Protein Infile for each condition and its replicates. (this is the path of your PEAKS proteins.csv file)
        5. Specify CD or HD (chemical vs heat denature)
        6. Under Conc/Temp Start, list your first concentration/temperatures
        7. In the columns following Conc/Temp Start, fill in your other conc/temp values horizontally (i.e. Conc/Temp Start: Conc1, [COLUMN K]: Conc2, [COLUMN L]: Conc3, ..., [LAST NEEDED COLUMN]: Conc[END])
        8. Specify Calculation Options:
            - Individual Rep Analysis (Yes) : Produces a [CONDTION]_Rep[n]_OUTPUT.csv file for each replicate in your run.
            - Rep Graphs (No) : Produces graph outputs for each protein/peptide in your replicates that meet the specified conditions (see Graph Filters). (It is recommended to leave graphing off as graphing the values takes more time than running the actual calculations. Most graphs aren't really necessary, and we have found that the other tools included with CHalf are more useful for making inferences about protein stability.)
            - Combined Analysis (Yes) : Combines data from replicates to calculate CHalf values for a whole condition. Without this, Remove Outlier Analysis will not occur and Fitting Efficiency cannot be calculated.
            - Remove Outlier Analysis (Yes) : Calculates trimmed CHalf values and trimmed curve values. Without this, Fitting Efficiency cannot be calculated.
            - Graph Combined (No) : Produces graph outputs for each protein/peptide in your combined data that meet the specified conditions (see Graph Filters).
            - Giant Output (No) : Creates a large table with data from each of your conditions. This can be useful for comparing protein/peptide presence across conditions if your experiment uses fractionation, but, otherwise, this option can largely be ignored.
            - Minimum Points for Calculation (4) : Sets the minimum number of non-null points CHalf will accept to fit a protein/peptide to a sigmoidal curve. It is not recommended to go any lower than 4 if you want useful data.
            - Outier StdErr Cutoff (StdErr x #) (2) : Sets the cutoff interval for points to be used in calculating sigmoidal curves. Points whose values are greater than the standard error times the number listed will be treated as outliers and will be excluded from the fitting calculation.
            - Graph Filters: (default values are the most useful)
                CI Mx% of Range (0.3): Graphs if 2 * [CONFIDENCE INTERVAL] <= [NUMBER] * [CONC/TEMP RANGE]
                R^2 Cutoff (0.99): Graphs if R^2 value for sigmoidal curve >= [NUMBER]
                CHalf Range Cutoff (0.5): Graphs if [FIRST CONC/TEMP] - [TEMP/CONC RANGE] * [NUMBER] <= [CHalf] <= [LAST CONC/TEMP] + [CONC/TEMP RANGE] * [NUMBER]
            - Other Features: (see Features section for detailed explanation) (all Yes by defualt)
                Label Efficiency
                Fitting Efficiency
                Combined Site
                Residue Mapper
                Dynamic Y-axis (No): Makes the y-axis of figures in Combined Site and Residue Mapper adjust dynamically to CHalf values
                Min (0): Minimum value on y-axis for Combined Site and Residue Mapper (Should be close to your lowest concentration/temperature) (will be ignored if Dynamic is Yes)
                Max (3.6): Maximum value on y-axis for Combined Site and Residue Mapper (Should be close to your highest concentration/temperature) (will be ignored if Dynamic is Yes)
            - CHalf Version: Leave as v3.3 if you are using v3.3.
- (For running in Python IDE) In CHalf_v3.3, Replace 'DIRECTORY' in os.chdir('DIRECTORY') on Line 34 with the path of the directory that contains your master file (i.e C:/Users/user/Desktop/CHalf_v3.3)
- (For running in Python IDE) Replace "MASTERFILE.csv" on line 41 with the name of your masterfile (i.e Folding Assay Masterfile.csv)
- (For running in Python IDE) Specify graphics file_type on line 59 (.jpg/.svg/.png) (.jpg by defualt)
- Run CHalf_v3.3.py
- If you would like to run CHalf in command line instead of in a Python IDE, run the following command (replacing 'MASTERFILE.csv' with the path of your masterfile):
```bash
    python CHalf_v3.3.py 'MASTERFILE.csv'
```
- The run will be complete when it prints 'CHalf Run Complete.'

Label Finder (Label Efficiency):

- Select Label Finder (Label Efficiency) under Other Tools on the Menubar.
- Specify Project Name
- Select Input File ([CONDITION]_Rep[n]_OUTPUT.csv or [CONDITION]_Combined_OUTPUT.csv from CHalf)
- Select Output Directory
- Drag and drop desired labels from Label Dictionary to Labels to Find (labels can be added to or removed from the dictionary by editing 'Label Finder Dictionary.csv'; press open under Label Dictionary to open the file for editing; there should be a list by default in labels to find; these defaults can be changed in 'Label Finder Dictionary.csv')
- Press Process and a popup will indicate that Label Finder has been initiated. Press OK to continue.
- A popup will appear indicating that the run is complete or an error occured. If an error occurs, consult the error section of the documentation for fixes to common problems.

Fitting Efficiency:
- Select Fitting Efficiency under Other Tools on the Menubar.
- Specify Output Name
- Select Input File ([CONDITION]_Combined_OUTPUT.csv from CHalf)
- Select Output Directory
- Specify Options
    
        OPTIONS:
        - CHalf Range :
            Low (0) - Lowest CHalf value that will be counted as properly fit (Should be close to your lowest concentration/teperature value)
            High (3.48) - Highest CHalf value that will be counted as properly fit (Should be close to your highest concentration/teperature value)
        - R Squared (0.6) : Only CHalf sigmoidal curves with values above this will be counted as properly fit.
        - Confidence Interval :
            Low (0) - Lowest CHalf Confidence Interval that will be counted as properly fit (realistically you should not change this value)
            High (0.35) - Highest CHalf Confidence Interval that will be counted as properly fit (lower value = stricter fitting criteria)
- Press Process. A popup will appear indicating that the run has initiated. Press OK to continue.
- A popup will appear indicating that the run is complete or an error occured. If an error occurs, consult the error section of the documentation for fixes to common problems.

Combined Site:
- Select Combined Site under Other Tools on the Menubar.
- Specify Output Name
- Select Output Directory
- Press Add to select input files ([CONDITION] Label Sites.csv from Fitting Efficiency). Note: You must have more than one input.
- Once you are done adding inputs, you can remove input files from the run by selecting them in the list and clicking Remove.
- Specify Options
    
        OPTIONS:
        - File Type : File type of output graphics (.svg/.jpg/.png)
        - Low Bound : Low bound of y-axis on graphics (should be close to lowest concentration/temperature value in your experiment)
        - High Bound : High bound of y-axis on graphics (should be close to highest concentration/temperature value in your experiment)
        - Dynamic Y-Axis : Allows the y-axis to change based on CHalf values in your data set (if checked, low and high will be ignored)

- Press Process. A popup will appear indicating that the run has initiated. Press OK to continue.
- A popup will appear indicating that the run is complete or an error occured. If an error occurs, consult the error section of the documentation for fixes to common problems.

Residue Mapper:
- Select Residue Mapper under Other Tools on the Menubar.
- Specify Output Name
- Select Input File ([CONDITION] Combined Label Sites.csv from Fitting Efficiency)
- Select Output Directory
- Specify Options

        OPTIONS:
        - File Type : File type of output graphics (.svg/.jpg/.png)
        - Low Bound : Low bound of y-axis on graphics (should be close to lowest concentration/temperature value in your experiment)
        - High Bound : High bound of y-axis on graphics (should be close to highest concentration/temperature value in your experiment)
        - Dynamic Y-Axis : Allows the y-axis to change based on CHalf values in your data set (if checked, low and high will be ignored)

- Press Process. A popup will appear indicating that the run has initiated. Press OK to continue.
- A popup will appear indicating that the run is complete or an error occured. If an error occurs, consult the error section of the documentation for fixes to common problems.

Combined Residue Mapper:
- Select Combined Residue Mapper under Other Tools on the Menubar.
- Specify Output Name
- Select Output Directory
- Press Add to select input files ([CONDITION] Combined Label Sites.csv from Fitting Efficiency). Note: You must have more than one input.
- Once you are done adding inputs, you can remove input files from the run by selecting them in the list and clicking Remove.
- Specify Options
    
        OPTIONS:
        - File Type : File type of output graphics (.svg/.jpg/.png)
        - Low Bound : Low bound of y-axis on graphics (should be close to lowest concentration/temperature value in your experiment)
        - High Bound : High bound of y-axis on graphics (should be close to highest concentration/temperature value in your experiment)
        - Dynamic Y-Axis : Allows the y-axis to change based on CHalf values in your data set (if checked, low and high will be ignored)

- Press Process. A popup will appear indicating that the run has initiated. Press OK to continue.
- A popup will appear indicating that the run is complete or an error occured. If an error occurs, consult the error section of the documentation for fixes to common problems.
## Demo

CHalf v4.2:

- Input Format:
- Basic Operatation:
- Masterfile Editing:
- Editing CHalf Defaults.csv
- Other CHalf Tools:
	- Label Finder
	- Fitting Efficiency
	- Combined Site
	- Residue Mapper
	- Combined Residue Mapper

CHalf v3.3:

- Creating a Masterfile:
- Running Using Python IDE:
- Running Using Command Line:
- Using CHalf Tools:

Outputs Explained In Depth:

- CHalf:
- Label Finder (Label Efficiency):
- Fitting Efficiency:
- Combined Site:
- Residue Mapper:
- Combined Residue Mapper:


For Working With Non-PEAKS Outputs:

- CHalf:
- Other CHalf Tools:
## Support
As we have developed CHalf, we have put a lot of effort into addressing possible errors that could occur when calcuating CHalf values or preparing other outputs. We have also tried to reduce room for user error. If you are experiencing errors, please refer to the Common Error section bellow before contacting the JC Price Lab for support. Most errors are a result of improperly selecting inputs or improperly specifying run conditions unique to your samples. Modifying CHalf or using nonstandard inputs runs the risk of raising unanticipated errors, so do so at your own risk. Before using nonstandard inputs or modifying CHalf, please review the demo section within this README.

Common Errors:

- Common Input Error Likely: Number of points in [Condition] does not match between condition files and the masterfile. Check that your number of concentration/temperature columns in your proteins.csv and protein-peptides.csv files are the same as in your masterfile. You may also check the printed error statement.
    
    Solution: Most of the time, this error is simply an issue of forgetting to specify the correct number or concentrations in a condition. If you have too many concentrations listed, the printed error statement should be as follows: TypeError: '<' not supported between instances of 'str' and 'float' with the error being raised in getMinMax_Absolute(numList). Check the masterfile of the condition listed and compare it to its input files. Fix the columns in either the masterfile or the input files, and press start to run again. If a TypeError printed error statement is different than the one listed above, you are encountering a different type of error.

- Label Finder Dictionary.csv not found. Please add to [PATH].

    Solution: The dictionary file used by Label Finder is not in the CHalf directory or it is not named properly. In the case that the file is missing, download from here: 'fakeurl.com'.

- CHalf Defaults.csv not found. Please add to folder.

    Solution: The settings file used by CHalf is not in the CHalf directory or it is not named properly. In the case that the file is missing, download from here: 'fakeurl.com'.

- No input file or output directory selected.

    Solution: Anytime you see this error, the issue is simply that you need to specify input files and output directories. There are buttons on each part of the GUI that coincide with the error.

- Error Occured / Error in Run Check Print Statement

    Solution: Check the print statement. Fixing these largely depend on the kind of error that appears. The most common source of errors are improper formatting of input files or masterfiles. Check that your inputs are formatted properly. If you have any questions regarding formatting, first refer to the Input Format video under Demo in the documentation.

- Unable to delete condition. Check print statement and check if condition files/folders are open.
    
    Solution: Likelihood is that you have deleted the folder already or you have a file open in the folder for that condition. Close any condition associated files, press refresh, and try again.

- Combined Site: Not enough inputs selected. Please select at least two.

    Solution: Combined Site requires multiple Label Sites files to run.

- Combined Site: [CONDITION] Shared_OUTPUT.csv is empty

    Solution: The issue is likely that there were no shared label sites between the conditions. This can be the result of using data from different species. To check this, compare your input Label Sites files. If this is true, there will not be any matches in the Label@Accession column between conditions. You can also check the print statement with the run. A error message should be returned with a statement included "No shared sites found."

- Residue Mapper: No outputs

    Solution: The issue is likely that your Label Sites.csv file is empty. This is most likely an issue of having no labeled peptides passing the fitting conditions in Fitting Efficiency. First check your Label Sites.csv file, then check your Fitted Peptides.csv file under the Conf Int in Range column. If the column is empty, no peptides could be fit properly. This can be an issue of your criteria being too strict or experimental error. If there are peptides in the Conf Int in Range column, check if any of them contain labels in the CHalf format (i.e. Y(+125.90)); this does not include TMT tags of the form (+229.16). If there are no tags present, nothing was labeled and fit properly. If there are tags present, but they are not in the CHalf format of AA(+MASS), they will not be transferred over properly to Label Sites.csv files. In this case, you must edit your tags in your proteins.csv and protein-peptides.csv files to fit the CHalf format and run CHalf again.

- Combined Residue Mapper: No outputs

    Solution: The issue is likely that your Label Sites.csv files are empty or have no shared proteins. If a Label Sites.csv is empty, this is most likely an issue of having no labeled peptides passing the fitting conditions in Fitting Efficiency. First check your Label Sites.csv file, then check your Fitted Peptides.csv file under the Conf Int in Range column. If the column is empty, no peptides could be fit properly. This can be an issue of your criteria being too strict or experimental error. If there are peptides in the Conf Int in Range column, check if any of them contain labels in the CHalf format (i.e. Y(+125.90)); this does not include TMT tags of the form (+229.16). If there are no tags present, nothing was labeled and fit properly. If there are tags present, but they are not in the CHalf format of AA(+MASS), they will not be transferred over properly to Label Sites.csv files. In this case, you must edit your tags in your proteins.csv and protein-peptides.csv files to fit the CHalf format and run CHalf again.

