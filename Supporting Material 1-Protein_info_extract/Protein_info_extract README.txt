This README contains the instruction to run the script protein_info_extract.py

1.	Description:
Rosetta is a protein modeling/designing software developed by the Baker Lab of the University of Washington. PyRosetta is a Rosetta version that is compatible with Python which allows users to access Rosetta functions easier. Under normal circumstances, PyRosetta intakes cleaned protein PDB files (without non-protein molecules). If a protein small-molecule ligand is not parameterized in the PyRosetta database, it will automatically discard it. protein_info_extract.py is a Python script that uses the functions in PyRosetta to:
	Download PDB files from https://www.rcsb.org/ based on the input 4-letter PDBIDs. The downloaded PDB files will be cleaned and will be input for extracting the parameters.
	Assign secondary structures to the input crystal structures.
	Calculate the solvent accessible surface area (SASA) of each amino acid residue.
	Calculate the total residue energy (Rosetta energy unit, REU) of each residue based on Rosetta score functions.
	Extract the b-factor of each residue based on the input crystal structures
All parameters will be recorded into a .csv file. This script will automatically separate the downloaded PDB files, the cleaned PDB files and the result data files into three separate directories. 

2.	Installations and set up:
2.1	Installations of BASH, PyRosetta and Python:
PyRosetta can only be run via a BASH system. If a Linux computer is not available, BASH can also be installed on Windows 10. The instructions to install BASH, PyRosetta and Python can be found on https://www.pyrosetta.org/downloads/windows-10 
2.2	Setting up the Path to PyRosetta program:
This setup is to let BASH and Python know where PyRosetta is, so it does not have to run the program in the same directory as PyRosetta. 
        To do this:
2.2.1	Start a BASH terminal.
2.2.2	Type cd and hit enter.
2.2.3	Type vi .bashrc and hit enter.
2.2.4	Hit shift+G to reach the bottom of the file. 
2.2.5	Hit i to start editting.
2.2.6	To the bottom of the file type export PYTHONPATH=$PYTHONPATH:/path/to/the/directory/of/PyRosetta/
Example:
export PYTHONPATH=$PYTHONPATH:/mnt/c/Users/me/Desktop/Pyrosetta4
2.2.7	Hit Esc and type :wq to save and exit out of the file.
2.2.8	Type souce .bashrc
2.3	Install Pandas:
Pandas is a Python package for manipulating Excel files. To do this, execute ipython and type pip install Pandas

3.	instruction to run the script:
3.1	Start a BASH terminal.
3.2	Change directory to where the protein_info_extract.py script is located by typing 
cd /path/to/the/script/
3.3	Execute ipython
3.4	Run the script with input arguments
3.4.1	If only one structure is required to be calculated, then just pass the 4-letter PDBID as the argument.
Example: in the terminal type run protein_info_extract.py 4M7T
3.4.2	By default, this script will calculate the parameters of all protein chains available in the input PDB file. However, to save time a "homo" argument can be passed to only calculate one protein chain (chain A) of the input PDB file. This assumes all protein chains are homo-multimer (all subunits are the same).
            Example: run protein_info_extract.py 4M7T homo
3.4.3	Multiple PDBIDs can be stored in one .csv file. If this .csv file is passed as one of the arguments, this script will process the parameters of each PDBID indicated in the file automatically (run time varies based on the amount of the PDBIDs in the file). The .csv file should be in the following format:
	A
1	PDBID
2	4R33
3	1TV8
4	2A5H
Example: In the terminal type run protein_info_extract.py Input_PDB_ID.csv
run protein_info_extract.py Input_PDB_ID.csv homo

			
