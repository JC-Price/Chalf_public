# CHalf v4.3

<div align="center" style="width: 100%;">
  <img src="Graphics/v4.3/CHalf Protein Logo.png" align="left" width="180" alt="CHalf Logo">

  <img src="Graphics/v4.3/Brigham_Young_University_medallion.png" align="right" width="180" alt="BYU Logo">

  <br><br>
  <h3 style="font-size: 3.5em;">CHalf v4.3 - JC Price Lab</h3>
</div>

<br clear="all">
<br>

CHalf is a protein stability research tool. CHalf uses peptide intensity information within a denaturation curve to calculate the denaturation midpoint (“CHalf”) of protein/peptide fragments.  The tool was designed for use with mass spectrometry based information and can accept peptide quantification files from any proteomics identification and quantification software with some attention to [formatting](https://github.com/JC-Price/Chalf_public/blob/main/Demos%20and%20Documentation/formatting_guide.md).

As proteins are subjected to a gradient of denaturing solutions (i.e. GdmCl) or temperatures, they unfold in varying amounts, exposing sites that cause precipitation (for thermal denaturation style experiments) or are labeled using tags such as iodine (for chemical denaturation style experiments).
CHalf uses peptide signal intensities at these differing conentration points and produces a sigmoid curve. The midpoint of this sigmoid curve is the CHalf value and represents the relative folding stability of these protein/peptide fragments.

Included with CHalf is a suite of tools that can be used to perform quality control on your folding experiments to calculate the label and fitting efficiency of sample preparation and tools for comparing changes in folding stability at a single residue level and across the protein sequence space in-between conditions.

For information on previous versions, see [here](https://github.com/JC-Price/Chalf_public/blob/main/v4.2/README.md).

## Authors
[Chad D. Hyer](https://www.linkedin.com/in/chadhyer/), [Connor Hadderly](https://www.linkedin.com/in/connorthaderlie), Monica Berg, [Hsien-Jung Lavender Lin](https://www.linkedin.com/in/hsien-jung-lin-254538197), [John C. Price](https://www.linkedin.com/in/john-price-1ba26b35/)

  
## Acknowledgements

Brigham Young University Department of Chemistry and Biochemistry

John C Price Lab Group

Special thanks to Dr. Bradley R. Naylor for development assistance.

We love [Fragpipe](https://fragpipe.nesvilab.org/), so we took some inspiration from their graphical interface as we designed ours. Our tools do very different things, but feel free to check out their work.

DISCLAIMER: Some generative AI was used during development of CHalf's GUI. All CHalf core features were built by hand.

Citations:

Hyer, C. D.; Lin, H.-J. L.; Haderlie, C. T.; Berg, M.; Price, J. C. CHalf: Folding Stability Made Simple. Journal of Proteome Research 2023, 22 (2), 605-614. DOI: 10.1021/acs.jproteome.2c00619.

Lin, H.-J. L.; James, I.; Hyer, C. D.; Haderlie, C. T.; Zackrison, M. J.; Bateman, T. M.; Berg, M.; Park, J.-S.; Daley, S. A.; Zuniga Pina, N. R.; et al. Quantifying In Situ Structural Stabilities of Human Blood Plasma Proteins Using a Novel Iodination Protein Stability Assay. Journal of Proteome Research 2022. DOI: 10.1021/acs.jproteome.2c00323.

## Contact

For inquiries about CHalf or to request additional information, please use our GitHub or direct inquiries to jcprice@chem.byu.edu. We will do our best to respond in a timely fashion, so you can use our software for your needs.

## Table of Contents
- [Installation](https://github.com/JC-Price/Chalf_public/tree/main?tab=readme-ov-file#installation)
- [Features](https://github.com/JC-Price/Chalf_public/tree/main?tab=readme-ov-file#featuress)
- [Instructions](https://github.com/JC-Price/Chalf_public/tree/main?tab=readme-ov-file#instructions)
- [Demo](https://github.com/JC-Price/Chalf_public/tree/main?tab=readme-ov-file#instructions)
- [Support](https://github.com/JC-Price/Chalf_public/tree/main?tab=readme-ov-file#instructions)

## Installation

Version 4.3 - Excecuteable file with integrated tools and GUI. Does not require Python installation.

[Download](https://github.com/JC-Price/Chalf_public/releases/tag/CHalf_v4.3)

Installation: Extract the zipped folder and run ```CHalf_v4_3.exe```. For proper use, please maintain the extracted folder structure. CHalf will rely on assets in ```concentration_columns```, ```core```, ```images```, and ```workflows``` folders for preparing your CHalf runs.

Additional ways of installing and running CHalf:
- [Running CHalf from an IDE and source code](https://github.com/JC-Price/Chalf_public/blob/main/v4.3/ide_build/running_chalf_by_ide.md)
- [Building CHalf from source code as a standalone executable](https://github.com/JC-Price/Chalf_public/blob/main/v4.3/gui_build/building_chalf_gui.md)
- [Running CHalf headless](https://github.com/JC-Price/Chalf_public/blob/main/Demos%20and%20Documentation/headless_chalf_guide.md)

## Features

For all features, see the hyperlinked guides for additional information about how to properly use the module and understand their outputs.

- [CHalf](https://github.com/JC-Price/Chalf_public/blob/main/Demos%20and%20Documentation/chalf_module_guide.md) - Fits chemical/heat denature mass spec data to a sigmoid curve to calculate protein/peptide CHalf values.

        Inputs:
            -Formatted peptide abundance .csv from any proteomics identification and quantification software.
        
        Outputs:
            -{CONDITION}_Combined_OUTPUT.csv - Raw fitted curve information for each condition with CHalf values and other fitting parameters.
            -{CONDITION} Sites.csv - Significant fitted curves with individual-amino-acid-localizable CHalf values.
            -{CONDITION} Combined Sites.csv - Localized CHalf values. This is the primary output of CHalf for downstream analysis.
        
        Graph Outputs: (toggleable, off by default)
            -{ACCESSION@PEPTIDE}.[svg/jpg/png] - Graph of CHalf sigmoid curves for proteins/peptides.

- [Quality Control](https://github.com/JC-Price/Chalf_public/blob/main/Demos%20and%20Documentation/quality_control_module_guide.md) - Identifies condition-specific quality metrics for troubleshooting sample preparation or acquisition issues.

        Inputs:
            -Formatted peptide abundance .csv from any proteomics identification and quantification software.
            -{CONDITION}_Combined_OUTPUT.csv - Raw fitted curve information for each condition with CHalf values and other fitting parameters. Generated by CHalf.
            -{CONDITION} Combined Sites.csv - Localized CHalf values. Generated by CHalf.
        
        Output:
            -{CONDITION} Quality Control.csv - Contains fitting and labeling efficiency metrics from your CHalf run.

- [Visualization Modules](https://github.com/JC-Price/Chalf_public/blob/main/Demos%20and%20Documentation/visualization_modules_guide.md) - Tools for helping you quickly identify changes in CHalf values in-between conditions and generating figures for presentations and publications.

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

This section contains instructions for running CHalf after first opening the program. Included are explanations of how to set up projects, how to use each module, how to start the project once the proper settings have been specified, and how to begin looking at the resulting data.

**Workflow Tab**

![Workflow tab image](https://github.com/JC-Price/Chalf_public/blob/main/Graphics/v4.3/main_page.png)

*Workflow Management:*

Workflows determine how CHalf will approach your data analysis. CHalf will default to the settings that we use for IPSA upon loading up the program. You can access other workflows by dropping ```.workflow``` files into the ```workflows``` directory contained in the same directory as ```CHalf.exe```. These workflows are defined by settings selected throughout the GUI. If you have defined a preset that you wish to use, you can save it as a workflow by pressing ```Save``` which will then prompt you to define the name of the preset. You can overwrite existing ```.workflow``` files to make changes to workflows. You can select other workflows in the dropdown menu, and then press ```Load``` to have the worklow settings apply throughout the GUI and the run. If you wish to see where ```.workflow``` files are saved, you can press ```Open Folder```. For a detailed discussion of all parameters in a workflow, see the [Workflows Tutorial](https://github.com/JC-Price/Chalf_public/blob/main/Demos%20and%20Documentation/workflows_tutorial.md).

*Input Selection:*

CHalf takes inputs of ```.csv``` files with quantified peptide abundances from proteomics analysis softwares. Proper formatting is essential for CHalf to run correctly. For instructions on how you should format your input files see the [Foramtting Guide](https://github.com/JC-Price/Chalf_public/blob/main/Demos%20and%20Documentation/formatting_guide.md). To add input files, press ```Add files```, after which CHalf will prompt you to add your properly formatted input files using the file explorer. Each added file will be added to the table with its associated file path, condition name, and conditions column preset. Files can be removed by highlighting the conditions in the table and pressing ```Remove selected files``` or ```Clear files``` to remove all inputs. Previously defined inputs can be loaded into CHalf using ```.manifest``` files which are generated from the table using ```Save as manifest``` or by CHalf being initialized in a project.

*Condition Definition:*

Condition names and concentration columns control the file structure of the project and are essential to downstream analysis. Condiion names must be unique and can be edited in the table. Highlighted conditions in the table can also be edited using the buttons by ```Set selected condition names```. Concentration column presets determine the format of the input files to be read and are essential to defining your concentration gradient that CHalf will use to fit curves for calculating folding stability. These presets are stored in the ```concentration_columns``` folder in the CHalf directory as ```.cc``` files. They are json-like files that pair input column names to concentration values. To define your own concentration columns presets, you can click ```Create/Edit``` and use the Concentration Column Wizard to define the concentration values in the gradient and their associated column names in your inputs. The ```Column Name``` must exactly match the names of the columns in your input files. For instances where you may have holes in your concentration gradient, CHalf will automatically adjust for missing data, so you do not need to define a new concentration columns preset for these instances. All that is required is that CHalf knows which columns in your inputs are abundance values and their associated denaturant concentrations. You can then use the dropdown and click ```Assign to selected conditions``` to set the correct concentration column preset for each condition. 

**CHalf Tab**

The CHalf tab is used to set the basic settings that will be used to calculate protein folding stability from your inputs. All downstream modules are depedent on outputs from CHalf, so you will rarely opt out of using the CHalf module on this tab. Downstream modules can be run on existing CHalf outputs without having to rerun CHalf if the file structure of the project is maintained after running CHalf and if the original ```.manifest``` file is loaded in the Workflow Tab. The settings in this tab, however, are essential for ensuring that curves are fit properly, for identifying how localization of stability values to individual residues is to be performed, and for classifying curves as significant or insignificant. If no edits need to be made to these parameters, you can skip to the following steps for running CHalf.

*Search Options:*

- Light Search: Depending on your labeling reagent, different amino acid residue types can be labelable. ```Light Search``` filters your inputs to only perform fitting on peptides that contain amino acid residues that can be labeled. This setting dramatically cuts calculation time and helps remove potential artifacts in your data. If you desire to try to fit CHalf curves to unlabelable peptides, you can deactivate this feature.
- Residues to Search: Specifying what amino acids your labeling reagent targets is essential to localizing stability values. Specify your labeling targets using any of the 20 canonical amino acids in this section. For proper localization, it is generally better that you use a more selective labeing agent as, currently, CHalf can only localize stability to peptides that contain a single labeled or labelable species.

*Filter Options:*

- C½ Minimum: This value represents the lower limit of significant C½ values. This should generally be towards the lower limit of your concentration gradient. This setting helps define the window where curve fitting is reasonable and where C½ values should be measureable by your assay. C½ values below this parameter will be marked as insignificant.
- C½ Maximum: This value represents the upper limit of significant C½ values. This should generally be towards the upper limit of your concentration gradient. This setting helps define the window where curve fitting is reasonable and where C½ values should be measureable by your assay. C½ values above this parameter will be marked as insignificant.
- R² Cutoff: This value represents how well a sigmoid curve can be fit to your data with values closer to 1 being more accurate. Values below this parameter will be marked as insignificant. This is generally the best measure of how well your curve was fit for a given peptide, so properly identifying what threshold of R² values yield significant results is essential for identifying significant data and filtering out bad curves and artifacts. Too stringent of R² filters can miss important stuctural insights, but too permissive of R² filters can yield artifacts that do not represent physiologically significant folding stability values.
- Confidence Interval / Range Cutoff: (Optional) Checking this box introduces an additional fitting metric. While fitting, CHalf will attempt to identify the confidence interval of the measured C½ values. It will then calculate what percent of the range of your concentration gradient this confidence interval represents. This parameter labels curves whose confidence interval is greater than this percentage of the range as insignificant. Depending on how many points you have in your curve, this value can be more or less meaningful as sometimes near perfect fits will be assigned infinite confidence intervals due to artifacts in the fitting process. In many instances, CHalf is attempting to fit several parameters off of a limited number of points rather than several hundred points, so this filter can become too stringent and fail to capture physiologically significant stability trends. Unchecking this box will still use the confidence interval value provided for downstream analysis to display the confidence of stability values during visualization while showing significant curves whith large confidence intervals as having no confidence interval for easy identification without unnecesarily removing potentially significant data. Checking this box will remove these "zero-confidence" interval points during visualization.
- Fitting Parameter Optimization Priority: Chalf attempts to optimize curve fitting in multiple steps and takes the most optimized curve from its attempts. This setting identifies which parameter CHalf should optmiize to. If not using the Confidence Interval cutoff, you should generally optimize for R² to ensure best fits of the data. If using the Confidence Interval cutoff, it would be appropriate to optimize towards minimizing confidence intervals.
- Keep Only Significant Curves: This feature filters out insignificant curves in CHalf outputs. Use this feature to reduce file sizes of outputs. Leaving this feature unused, however, enables you to identify areas of improvement in fitting parameters by highlighting which curves are not significant and why they are not significant.

*Fitting Options:*
- Minimum Points for Calculation: This value represents the minimum number of points in a curve for a given peptide before CHalf will attempt to fit a curve. A sigmoid pattern can generally not be measured with anything below 4 points, so it is not recommended to go lower than this value. Higher values will decrease the number of curves that CHalf will attempt to fit, reducing computation time, but potentially missing relevant opportunities to fit significant curves. 
- Outlier Cutoff: CHalf gives an initial attempt at fitting a sigmoid curve to the raw data. From this initial attempt, CHalf can potentially identify a confidence interval surrounding the fit curve. Using an outlier test based on this attempt, CHalf can then remove points that may detract from the curve due to machine noise and enable a cleaner fit on a second attempt. This parameter represents how many standard errors a point must be outside of the curve before it will be considered an outlier. By default, 2 standard errors is a robust parameter for identifying outliers.
- Zero Abundance Rule: CHalf uses min-max normalization before attempting to fit curves. This normalization can be sensitive to holes in your data if you fail to quantify the peptide across all of your samples. Each of these methods of addressing these holes has merit depending on the reason for why a peptide may not have been quantified at a given concentration point, so we leave this decision to you based on the nature of labeling mechanisms in your assays.
    - Remove: Holes are removed and not considered during fitting, reducing the number of points that can be used in fitting. This option assumes that missing data is due to stochastic effects during quantification rather than due to non-existance of the analyte in that sample or the analyte being under the limit of detection. This prevents fitting of curves based on a lack of data.
    - Keep: Normalization factors in these missing points during minimum calculation. This option assumes that missing data is due to non-existance of the analyte in that sample or the analyte being under the limit of detection. If this assumption is true, this approach can help identify real pre- or post-transition baselines that would otherwise be ignored during curve fitting.
    - Impute: Normalization does not factor in missing points during minimum calculation but assigns 0 values to missing points after the measured values have been normalized. This follows a similar approach to "Keep" but is potentially more sensitive to the measured curve shape while still enabling for missing data to be considered as potentially real decreases in abundance that may be missed due to limits of detection.
- Allow Trimming: Allows outlier removal to be considered when determining significance of curves. Unchecking this will only allow the first fitting attempt to be considered in significance determination.

*Graphing Options:*
- Generate Curve Figures: Creates graph figures of the curves that CHalf fits. This is disabled by default due to the large computational cost of generating figures for every fit curve. This option is useful for getting a feel for how well your fitting parameters meet reality when determing significance, but this option also generates a lot of figures that you will probably never look at. Use according to your needs.
- File Type: You can choose to have the figure save as a ```.jpg```, ```.png```, or ```.svg```.
- Filter Options: See the ```Filter Options``` section for more details. These just determine the conditions that must be achieved before a curve has a figure generated for it.


*Experimental Options:*
We experimented with these features along the way as we built ```CHalf v4.3```. Each of them has cases where they might be useful, but each of these cases were either just too niche or conceptually flawed to justify their full incorporation into CHalf (minus Mutation Search). As a result, these features are more prone to cause errors during calculation and may not fit as well into the full CHalf workflow. Properly using them also requires understanding their strengths and weaknesses, so use them at your own risk. For more discussion on how to use these features and on their rationale, see the [Experimental Options Guide](https://github.com/JC-Price/Chalf_public/blob/main/Demos%20and%20Documentation/experimental_options_guide.md).

**Quality Control Tab**

Quality control generates a concise report of how well your assay performed in terms of fitting efficiency (percent of measurements that yielded significant C½ values) and labeling penetrance (what percent of unique sequences that were labelable were quantified in their labeled and unlabeled forms). This is a useful tool for troubleshooting your sample preparation and acquisition methods. All parameters in this tab are discussed in the ```CHalf Tab```. You should generally try to match your Quality Control filters to your CHalf filters. Quality Control can only be run if CHalf has previously been run on the project, and the correct folder structure has been maintained in the project directory. No downstream features are dependent on Quality Control outputs. 

**Visualization Tab**

CHalf's visualization tools are a powerful way of gaining protein- and site-specific insight at a proteomic scale. They are a good place to start when analyzing your proteomic data for identifying the impacts of changes in folding stability due to changes in experimental conditions and can help you save a lot of time and avoid being overwhelmed by your proteomic data. They produce some of the most useful outputs from CHalf that will enable you to do further hypothesis testing if you understand how and when to use each of the visualization tools. This section's goal is to provide you with enough basic instruction to use Groupings to properly make comparisons between conditions and answer questions. For more detailed information about what each visualization tool does see the [Visualization Modules Guide](https://github.com/JC-Price/Chalf_public/blob/main/Demos%20and%20Documentation/visualization_modules_guide.md).

![Visualization tab image](https://github.com/JC-Price/Chalf_public/blob/main/Graphics/v4.3/visualization_tab.png)

Central to using the visualiation tools is understanding how to use groupings. First, you want to import the CHalf conditions that you want to use in the comparisons. You can use the dropdown to individually add conditions or can add all of them at once. You can also individually or completely remove these conditions from the table as well. For each condition added, it will be assigned to a comparison group. Each comparison group can only have one unique instance of each condition added. Trying to add more of the same condition to a group will result in the creation of additional groups. Within each group, there is can also only be one Reference Condition, with every other condition in the group being an Experimental Condition. The visualization tools will use the Reference Condition as the reference point for making comparisons to each Experimental Condition in the set. Visualization tools will be performed groupwise, so if you want to compare one condition across multiple condition groups, you can do so by properly assigning it to each group in the table. Modification of the table can only be done using the buttons in the ```Condition/Group Properties``` section. You can assign selected rows to groups and change group names using ```Set Group```. You can then assign these conditions to Experimental or Reference classes using the ```Set Experimental``` and ```Set Reference``` buttons. Colors of conditions can be controlled using the color assignment wizard accessed by pressing ```Set Color``` after selecting a condition. If no conditions are assigned to groups in the table, group-dependent visualization tools will not be run. Each of the tools can be run on completed CHalf outputs without having to rerun CHalf if the project structure is maintained, and you reload the manifest used in the original project.

**Run Tab**
Once you have chosen the correct settings and comparison methods for your analysis, you are ready to execute CHalf. On the ```Run Tab``` you will start by selecting the output directory. The CHalf project folder structure will be created within this directory when executed, so be sure to create a new directory if you do not want it to overwrite existing files in the assigned directory. You can then press ```Start```, and the run will initialize. The console log will begin to fill with the set parameters and updates on the what steps are currently being performed with ETAs of when each step should complete. There may be some delay between the program starting and the log running, so don't worry if it takes a second. The run can be stopped at any point by pressing ```Stop```. When the run is complete, you will receive a message in the log.

The log automatically exports at the end of each CHalf run, but you can optionally export it to another location or can clear the console. Errors in the CHalf run will be reported in the log, so if something looks wrong with your outputs, be sure to check the log to understand what may have gone wrong.

You can also optionally click ```Export Headless Run``` to export the needed files and commands to be used to run CHalf headless as a command line tool for batch processing. For more information on running CHalf headless, see [Running CHalf headless](https://github.com/JC-Price/Chalf_public/blob/main/Demos%20and%20Documentation/headless_chalf_guide.md).

Now that your CHalf run is done, you can click ```Open``` to start looking at your outputs. Included in the next section is a suggested approach to looking at the results of your CHalf runs.

![Run tab image](https://github.com/JC-Price/Chalf_public/blob/main/Graphics/v4.3/run_tab.png)

**Examining Your CHalf Outputs**

Depending on what modules you chose to use during your CHalf run and what questions you are trying to answer, this approach may or may not apply to you. Assuming you used all of the options included in the default IPSA workflow, this is how we generally begin looking at our data:

1. Examine the ```qc_report.html``` files in each ```Group``` directory generated for each comparison group. This will allow you to see if you had a similar level of coverage and data quality between conditions being compared. You will also be able to see broader trends in differences between the samples in the set.
2. If there appear to be major differences in the quality of data collected between conditions, you can then start looking at ```Quality Control``` files for each condition to identify if differences are due to problems with sample preparation or data acquisition. Play close attention to penetrance to understand label-specific sample preparation differences, raw protein and peptide values for understanding data acqusition issues, and fitting efficiency metrics to gauge both. 
3. If your goal is to understand the impact of a variable on folding stability, look through your ```Delta Mapper``` or ```Combined Residue Mapper``` outputs for each group. As you look through these figures, note larger changes in protein folding stability across the sequence between conditions. These will be great leads to follow in downstream analysis.
4. Use ```Combined Sites``` outputs in your downstream analysis to probe differences in protein folding stability. Be sure to chase the leads you found from looking at the visualization outputs. ```Combined Sites``` files will generally contain all of the information that you will need to make stability comparisons between conditions and will generally have filtered out many of the artifacts and insignificant pieces of data that will slow down your analysis. These files should be easy to work with using bioinformatics tools that you have made to answer your own specific questions.

## Demo

COMING SOON

## Support
As we have developed CHalf, we have put a lot of effort into addressing possible errors that could occur when calcuating CHalf values or preparing other outputs. We have also tried to reduce room for user error. If you are experiencing errors, please refer to the Common Error section below before contacting the JC Price Lab for support. Most errors are a result of improperly selecting inputs or improperly specifying run conditions unique to your samples. Modifying CHalf or using nonstandard inputs runs the risk of raising unanticipated errors, so do so at your own risk. Before using nonstandard inputs or modifying CHalf, please review the demo section within this README.

# Common Errors:
We try to update this list as you or we find them, so please be patient as we continnue to build out this list.

| Error | Keywords | Solution |
| :--- | :--- | :--- |
| Parallelization Error | `Current thread 0x00010dc4` / `The process "46264" not found` | Running CHalf again will usually fix this issue. If the issue persists, consider only using 1 core. |