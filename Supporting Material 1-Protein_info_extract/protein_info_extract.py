'''
This script will take in a cleaned PDB file, and will output a result file with the corresponing PDB ID. If you input the same PDB structure, it will overwrite
'''



from pyrosetta import *
from pyrosetta.toolbox import *
import pyrosetta.rosetta.core.simple_metrics.per_residue_metrics as sm
import pandas as pd
from sys import argv
import operator, os, os.path, shutil
init()


def cal_data(pose, homo=False):

	total = pose.total_residue()
	space = int(total/10)

	if homo is True:
		mono_count = 1
		for i in range(1, total+1):
			if pose.pdb_info().chain(i) == pose.pdb_info().chain(i+1):
				mono_count += 1
			else: 
				break
	if homo is False:
		mono_count = total

	
	print('\n\n*********************** Assigning secondary structures...***********************\n')
	pose.display_secstruct()

	print('\n\n****************************** Calculating Scores ******************************')
	sf = get_score_function()	
	sf(pose)
	
	df = pd.DataFrame(columns=['PDB residue#','rosetta_resi#','chainID','AA','SS','REU','b-factor','SASA'])

	resiList = []
	for i in range(1,mono_count+1):
		resi = i
		resiList.append(resi)

	pdb_resiList = []
	chainID_List = []
	for i in range(1,mono_count+1):
		pdbNo = pose.pdb_info().pose2pdb(i)[:-3]
		Chain = pose.pdb_info().pose2pdb(i)[-2:-1]
		pdb_resiList.append(pdbNo)
		chainID_List.append(Chain)

	seq_List = []
	seq = pose.sequence()[:mono_count]+'\n'
	for i in range(mono_count):
		seq_List.append(seq[i])
	
	ss_List = []
	for i in range(1,mono_count+1):
		ss = pose.secstruct(i)
		ss_List.append(ss)

	score_list = []
	for i in range(1,mono_count+1):
		REU = pose.energies().residue_total_energy(i)
		score_list.append(REU)

	bfactor_list = []
	for i in range(1, mono_count+1):
		atom_No = pose.pdb_info().natoms(i)
		atom_bfactor = []
		for j in range(1,atom_No+1):
			bfactor = pose.pdb_info().bfactor(i,j)
			atom_bfactor.append(bfactor)
		count = 0
		for k in range(len(atom_bfactor)):
			if atom_bfactor[k] == float(0):
				count += 1
		for l in range(count):
			atom_bfactor.remove(0.0)

		ave_bfactor = round(sum(atom_bfactor),3)/len(atom_bfactor)
		bfactor_list.append(ave_bfactor)

	sasa_metric = sm.PerResidueSasaMetric()
	resi_sasa = sasa_metric.calculate(pose)
	resi_sasa = sorted(resi_sasa.items(), key=operator.itemgetter(0), reverse=False)
	relist, salist = zip(*resi_sasa)
	relist = list(relist)[:mono_count]
	salist = list(salist)[:mono_count]
	
	df['PDB residue#'] = pdb_resiList
	df['rosetta_resi#'] = resiList
	df['chainID'] = chainID_List
	df['AA'] = seq_List
	df['SS'] = ss_List
	df['REU'] = score_list
	df['b-factor'] = bfactor_list
	df['SASA'] = salist
	

	return df

def to_csv(df1, output_filename):
	#df_combined = pd.merge(df1)
	df1.to_csv(output_filename, index=False)


# Check folder existance and genarate folders
if os.path.isdir('./Cleaned_structure') == False:
	os.mkdir('./Cleaned_structure')
	print ('\n\n********************** Generating folder: ./Cleaned_structure *********************\n')
if os.path.isdir('./Original_structure') == False:
	os.mkdir('./Original_structure')
	print ('********************** Generating folder: ./Original_structure ********************\n')
if os.path.isdir('./Data_files') == False:
	os.mkdir('./Data_files')
	print ('********************** Generating folder: ./Data_files ****************************\n\n')


# Confirming homo parameter for the rest of the code
homo_param = False
if len(argv) >= 3:
	if 'homo' in argv:
		homo_param = True

# Setting up PDB info, downloading from RCSB.org and sort files 

if any('.csv' in s for s in argv) or any('.xlsx' in s for s in argv):
	ID_file = [t for t in argv if '.csv' in t] or [t for t in argv if '.xlsx' in t]
	ID_file_name = ID_file[0]
	ID_df = pd.read_csv(ID_file_name, header = None, names = ['PDBID'])
	for i in range(len(ID_df)):
		pdbID = ID_df['PDBID'][i]
		pdbID = pdbID.upper()
		pose1 = pose_from_rcsb(pdbID)
		pdbName_C = pdbID + '.clean.pdb'
		pdbName = pdbID + '.pdb'
		pdbFile = './Cleaned_structure/' +pdbID + '.clean.pdb'
		
		# Sorting files
		shutil.move(pdbName_C, 'Cleaned_structure/'+pdbName_C)
		shutil.move(pdbName, 'Original_structure/'+pdbName)
		
		# loading the cleaned structure
		pose = pose_from_pdb(pdbFile)

		# Initiating score calculation
		if bool(homo_param) == True:
			df1 = cal_data(pose, homo = True)
		else:
			df1 = cal_data(pose)	

		# Outputing data files
		to_csv(df1, './Data_files/'+pdbFile[-14:-10]+'_result.csv')

		print('\n\n***************************** Data file generated ******************************')

else:
	pdbID = argv[1]
	pdbID = pdbID.upper()
	pose1 = pose_from_rcsb(pdbID)
	pdbName_C = pdbID + '.clean.pdb'
	pdbName = pdbID + '.pdb'
	pdbFile = './Cleaned_structure/' +pdbID + '.clean.pdb'


	# Sorting files
	shutil.move(pdbName_C, 'Cleaned_structure/'+pdbName_C)
	shutil.move(pdbName, 'Original_structure/'+pdbName)
	# loading the cleaned structure
	pose = pose_from_pdb(pdbFile)

	# Initiating score calculation
	if bool(homo_param) == True:
		df1 = cal_data(pose, homo = True)
	else:
		df1 = cal_data(pose)

	# Outputting data files
	to_csv(df1, './Data_files/'+pdbFile[-14:-10]+'_result.csv')

	print('\n\n***************************** Data file generated ******************************')
