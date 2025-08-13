# Guide to PDB Tools
PDB Tools is used to extract SASA values from ```.cif``` and ```.pdb``` files while allowing for renaming and renumbering of chains for aiding in downstream analysis and visualization. PDB Tools creates a ```.csv``` file with pLDDT, SASA, and chain information and a ```.cif``` or ```.pdb``` file containing the renamed and renumbered chains with SASA values assigned in the ```occupancy``` attribute. This allows for easy visualization of SASA using tools like ChimeraX using commands like ```color byattribute occupancy palette rainbow``` to visualize SASA values on a structure. 

## Running PDB Tools Headless
PDB Tools can be run in command line by using the flag ```--headless```. If run headless, these are the arguments to consider:
```
options:
  -h, --help            show this help message and exit
  --headless            Run in command-line mode without GUI.
  --file FILE           Path to the input PDB or CIF file (for headless mode).
  --config CONFIG       Path to a JSON file with renumbering and naming configuration (for headless mode).
  --output_dir OUTPUT_DIR
                        Name of the output directory (for headless mode).
  --name NAME           Name of the output file (for headless mode).
  --output_type {pdb,cif}
                        Output file type (for headless mode).
```
An example config file is provided as ```pdb_tools_headless_example.json```

## Creating a PDB Tools Executable from Source Files

PDB Tools is distributed as a compiled executable file to properly manage dependencies, but we recognize that you may want to make edits to it yourself. This can be accomplished by editing ```pdb_tools.py```. After editing, however, it is recommended to recompile an executable for ease of distribution. This can be accomplished using an Anaconda environment and PyInstaller. Follow the steps below to accomplish this:

## Compiling pdb_tools
1. Create conda environment using the command ```conda create --name pdb_tools```.
2. Activate your conda environment using the command ```conda activate pdb_tools```.
3. Install the correct dependencies found in ```pdb_tools_requirements.txt``` plus any you may have added using the command ```pip install -r pdb_tools_requirements.txt```.
4. Install PyInstaller using the command  ```pip install pyinstaller```.
5. Navigate to the directory containing ```frag_to_chalf_UI.py```.
6. Compile the exe using the command ```pyinstaller pdb_tools.py --name "PDB Tools" --onefile --icon "pdb_tools_logo.ico" --add-data "images;images"```
7. ```PDB Tools.exe``` should now be in the ```dist``` folder.pip

Full list of commands:
```
conda create --name pdb_tools
conda activate pdb_tools
pip install -r pdb_tools_requirements.txt
pip install pyinstaller
pyinstaller pdb_tools.py --name "PDB Tools" --onefile --icon "pdb_tools_logo.ico" --add-data "images;images"
```