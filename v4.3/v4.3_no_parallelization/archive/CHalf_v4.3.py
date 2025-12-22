from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
import os, sys, shutil, re, traceback
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import t
from tqdm import tqdm
import warnings, webbrowser, itertools
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
tqdm.pandas()
CHalf_folder = os.getcwd() #For storing location of auxilary files
if 'CHalf v4.2 Logo.png' in os.listdir(CHalf_folder):
	mainLogo = os.path.realpath('CHalf v4.2 Logo.png')
if 'CRM v4.2 Logo.png' in os.listdir(CHalf_folder):
	crmLogo = os.path.realpath('CRM v4.2 Logo.png')
if 'CS v4.2 Logo.png' in os.listdir(CHalf_folder):
	csLogo = os.path.realpath('CS v4.2 Logo.png')
if 'FE v4.2 Logo.png' in os.listdir(CHalf_folder):
	feLogo = os.path.realpath('FE v4.2 Logo.png')
if 'LF Logo Full.png' in os.listdir(CHalf_folder):
	lfLogo = os.path.realpath('LF Logo Full.png')
if 'PM v4.2 Logo.png' in os.listdir(CHalf_folder):
	pmLogo = os.path.realpath('PM v4.2 Logo.png')
if 'CHalf Protein Logo.png' in os.listdir(CHalf_folder):
	icon = os.path.realpath('CHalf Protein Logo.png')
if 'LF Logo Blue.png' in os.listdir(CHalf_folder):
	icon2 = os.path.realpath('LF Logo Blue.png')

''' LABEL FINDER DICTIONARY LOCATION '''
try:
	labelfinderpath = os.path.realpath('Label Finder Dictionary.csv')
	print(labelfinderpath)
except:
	None

''' CHALF DEFAULTS CHECK ''' #Setting up default values you will see when you open CHalf, these can be edited in "CHalf Defaults.csv"
try:
	defaultsDF = pd.read_csv('CHalf Defaults.csv')
	CHgraphs = defaultsDF.iloc[0]['Default']
	reps = defaultsDF.iloc[1]['Default']
	CDHD = defaultsDF.iloc[2]['Default']
	conctemp = defaultsDF.iloc[3]['Default']
	if defaultsDF.iloc[4]['Default'].upper() == 'FALSE':
		ira = False
	else:
		ira = True
	if defaultsDF.iloc[5]['Default'].upper() == 'TRUE':
		repg = True
	else:
		repg = False
	if defaultsDF.iloc[6]['Default'].upper() == 'FALSE':
		comban = False
	else:
		comban = True
	if defaultsDF.iloc[7]['Default'].upper() == 'FALSE':
		roa = False
	else:
		roa = True
	if defaultsDF.iloc[8]['Default'].upper() == 'TRUE':
		combg = True
	else:
		combg = False
	if defaultsDF.iloc[9]['Default'].upper() == 'TRUE':
		giantout = True
	else:
		giantout = False
	minpts = defaultsDF.iloc[10]['Default']
	outstdcut = defaultsDF.iloc[11]['Default']
	cirange = defaultsDF.iloc[12]['Default']
	r2cut = defaultsDF.iloc[13]['Default']
	chrangecut = defaultsDF.iloc[14]['Default']
	if defaultsDF.iloc[15]['Default'].upper() == 'FALSE':
		lebool = False
	else:
		lebool = True
	if defaultsDF.iloc[16]['Default'].upper() == 'FALSE':
		febool = False
	else:
		febool = True
	if defaultsDF.iloc[17]['Default'].upper() == 'FALSE':
		csbool = False
	else:
		csbool = True
	if defaultsDF.iloc[18]['Default'].upper() == 'FALSE':
		rmbool = False
	else:
		rmbool = True
	if defaultsDF.iloc[19]['Default'].upper() == 'TRUE':
		chdynamic = True
	else:
		chdynamic = False
	chymix = defaultsDF.iloc[20]['Default']
	chymax = defaultsDF.iloc[21]['Default']
	conctemplst = defaultsDF[defaultsDF['Default Conc/Temp'].notnull()]['Default Conc/Temp'].tolist()
	lelst = []
	for item in defaultsDF[defaultsDF['Label Efficiency Default Labels'].notnull()]['Label Efficiency Default Labels'].tolist():
		lelst.append(item)
	FElow = defaultsDF.iloc[0]['FE Value']
	FEhigh = defaultsDF.iloc[1]['FE Value']
	FE_r = defaultsDF.iloc[2]['FE Value']
	FEcilow = defaultsDF.iloc[3]['FE Value']
	FEcihigh = defaultsDF.iloc[4]['FE Value']
	CSfile = defaultsDF.iloc[0]['CS Value']
	CSlow = defaultsDF.iloc[1]['CS Value']
	CShigh = defaultsDF.iloc[2]['CS Value']
	if defaultsDF.iloc[3]['CS Value'].upper() == 'TRUE':
		CSdynamic = True
	else:
		CSdynamic = False
	RMfile = defaultsDF.iloc[0]['RM Value']
	RMlow = defaultsDF.iloc[1]['RM Value']
	RMhigh = defaultsDF.iloc[2]['RM Value']
	if defaultsDF.iloc[3]['RM Value'].upper() == 'TRUE':
		RMdynamic = True
	else:
		RMdynamic = False
	CRMfile = defaultsDF.iloc[0]['CRM Value']
	CRMlow = defaultsDF.iloc[1]['CRM Value']
	CRMhigh = defaultsDF.iloc[2]['CRM Value']
	if defaultsDF.iloc[3]['CRM Value'].upper() == 'TRUE':
		CRMdynamic = True
	else:
		CRMdynamic = False
	try:
		os.chdir(defaultsDF.iloc[22]['Default'])
		directory_set = True
	except:
		directory_set = False
except:
	print('CHalf Defaults.csv not found. Native Defaults will be used instead')
	traceback.print_exc()
	CHgraphs = '.svg'
	reps = 1
	CDHD = 'CD'
	conctemp = 10
	ira = True
	repg = False
	comban = True
	roa = True
	combg = False
	giantout = False
	minpts = 4
	outstdcut = 2
	cirange = 0.3
	r2cut = 0.99
	chrangecut = 0.5
	lebool = True
	febool = True
	csbool = True
	rmbool = True
	chdynamic = False
	chymix = 0
	chymax = 3.6
	conctemplst = [0,0.43,0.87,1.3,1.74,2.17,2.61,3.04,3.48,3.59]
	lelst = [re.escape('Y(+125.90)'), re.escape('Y(+251.79)'), re.escape('H(+125.90)'), re.escape('H(+251.79)'), re.escape('C(+47.98)'), re.escape('C(+31.99)'), re.escape('C(+15.99)'), re.escape('M(+15.99)'), re.escape('M(+31.99)'), re.escape('W(+125.90)')]
	FElow = 0
	FEhigh = 3.48
	FE_r = 0.6
	FEcilow = 0
	FEcihigh = 0.35
	CSfile = '.svg'
	CSlow = 0
	CShigh = 3.6
	CSdynamic = False
	RMfile = '.svg'
	RMlow = 0
	RMhigh = 3.6
	RMdynamic = False
	CRMfile = '.svg'
	CRMlow = 0
	CRMhigh = 3.6
	CRMdynamic = False
	directory_set = False

CHdefaultslst = [CHgraphs,reps,CDHD,conctemp,ira,repg,comban,roa,combg,giantout,minpts,outstdcut,cirange,r2cut,chrangecut,lebool,febool,csbool,rmbool,chdynamic,chymix,chymax,conctemplst,lelst]
FEdefaultslst = [FElow,FEhigh,FE_r,FEcilow,FEcihigh]
CSdefaultslst = [CSfile,CSlow,CShigh,CSdynamic]
RMdefaultslst = [RMfile,RMlow,RMhigh,RMdynamic]
CRMdefaultslst = [CRMfile,CRMlow,CRMhigh,CRMdynamic]
#print(CHdefaultslst)
''' CHALF TOOLS '''
#Functions for running other counts
def trim_ends(df): #trims ends of peptides and removes TMT tags
	for i in range(len(df)):
		string = df.at[i,'Peptide']
		if string[1] == '.':
			string = string[2:]
		if string[-2] == '.':
			string = string[:-2]
		df.at[i,'Peptide'] = string
	df['Peptide'] = df['Peptide'].str.replace("\\(\\+229.16\\)","")
	return df

def getIndexes(dfObj, value): #A borrowed function that finds the position in a data frame of a given string
	listOfPos = []
	result = dfObj.isin([value])
	seriesObj = result.any()
	columnNames = list(seriesObj[seriesObj == True].index)
	for col in columnNames:
		rows = list(result[col][result[col] == True].index)
		for row in rows:
			listOfPos.append(row)
	return listOfPos

def peptideTOproteinDF(df): #Finds proteins in peptide data frame and returns data frames of each protein as a list
	proteinlst = []
	for i in range(len(df)):
		proteinlst.append(getIndexes(df,df.iloc[i]["Accession"])) #Makes a list of lists of each mention of an accession
	templst = []
	for i in proteinlst: #Removes duplicate lists from the protein list
		if i not in templst:
			templst.append(i)
	proteinlst = templst.copy()
	proteinDF_lst = []
	for i in range(len(proteinlst)):
		proteinDF = pd.DataFrame(columns=df.columns.values.tolist())
		proteinDF = proteinDF.append(df.loc[proteinlst[i]]).reset_index(drop=True)
		proteinDF_lst.append(proteinDF)
	return proteinDF_lst

def check_float(potential_float): #for testing if possible to convert to float since data is in string form
		try:
				float(potential_float) #Try to convert argument into a float
				return True
		except ValueError:
				return False

def make_label_site_function(row): #calculates label site
	try:
		peptide = row['Peptide']
		modded = peptide
		start = row['Start']
		delimiters = ['(',')']
		for delimiter in delimiters:
			modded = ' '.join(modded.split(delimiter))
		modded = modded.split()
		mods = [modded[i] for i in range(len(modded)) if i % 2 == 1]
		unmodified = ''.join([modded[i][:-1] + modded[i][-1].lower() for i in range(len(modded)-1) if i % 2 == 0])
		sites = [i + start for i, a in enumerate(unmodified) if a.islower()]
		residues = [modded[i][-1] for i in range(len(modded)) if i % 2 == 0][:-1]
		ID = ''.join([f'{residues[i]}({mods[i]})@{sites[i]}_' for i in range(len(residues))])[:-1]
		ID = row['Accession'] + '|' + ID
		if len(sites) == 1 and len(residues) == 1 and len(mods) == 1:
			sites = sites[0]
			residues = residues[0]
			mods = mods[0]
		else:
			row['Label Site'] = 'N/A'
			return row
		row['Label Site'] = f'{residues}{sites}'
		row['Residue Number'] = sites
		row['Label Type'] = f'{residues}({mods})'
	except ValueError:
		row['Label Site'] = 'N/A'
	return row

def getDataFrame(file): #Returns dataframe of file
	""" Returns pandas DataFrame of file.  Can use either .csv, .xls, or .xlsx files. """
	if ".csv" in file:
		df = pd.read_csv(file)
	elif ".xls" in file:
		df = pd.read_excel(file)
	else:
		print("*** ERROR: Incorrect file name: \"" + file + "\". Must include ending ('.csv' or '.xls' or '.xlsx') ***")
		return
	return df

def combineBool(array,logic): #takes a boolean array and logical operator to return the combined logic statement for the array i.e. combineBool([True,True,False],'and') => False, combineBool([True,True,False],'or') => True
	if type(array) ==type(np.array([])):
		total = len(array)
		actual = array.sum()
		if logic == 'and':
			if actual == total:
				return True
			else:
				return False
		elif logic == 'or':
			if actual > 0:
				return True
			else:
				return False
		else:
			raise ValueError("Logic argument only accepts 'and' or 'or'")
	else:
		raise TypeError('Only accepts numpy array composed of boolean values')

def AtoOR(row,dictionary):
	try:
		row['Out Reporter']=dictionary[row['Accession@Peptide'].split('@')[0]]
	except AttributeError:
		None
	return row

def describe_apply(row,conditionDict):
	for condition in list(conditionDict):
		tempDF = conditionDict[condition][conditionDict[condition]['Label@Accession'] == row['Label@Accession']]['trim_CHalf']
		row[condition] = tempDF.tolist()
		row['max'+condition] = tempDF.describe()['max']
		row['Q3'+condition] = tempDF.describe()['75%']
		row['median'+condition] = tempDF.describe()['50%']
		row['Q1'+condition] = tempDF.describe()['25%']
		row['min'+condition] = tempDF.describe()['min']
		row['std'+condition] = tempDF.describe()['std']
		row['mean'+condition] = tempDF.describe()['mean']
		row['count'+condition] = tempDF.describe()['count']
	return row

def CS_graph_apply(row,conditionDict,min,max,dynamic,file_type,RCS_output_dir):

	RCS_data = []
	RCS_names = list(conditionDict)
	for condition in RCS_names:
		RCS_data.append(row[condition])
	if not dynamic:
		RCS_fig, RCS_ax = plt.subplots()
		RCS_ax.boxplot(RCS_data, labels = RCS_names)
		RCS_ax.set_xlabel('Condition')
		RCS_ax.set_ylabel('C1/2 Value')
		RCS_ax.set_title(row['Label@Accession'])
		RCS_ax.set_ylim([min,max])
		plt.xticks(rotation=90)
		plt.savefig(RCS_output_dir + '/' + row['Label@Accession'].replace('|','-') + file_type, format=file_type[1:],bbox_inches='tight')
		plt.clf()
		plt.close(fig='all')
		del RCS_fig, RCS_ax
	else: #if y axis values are allowed to stay dynamic
		RCS_fig, RCS_ax = plt.subplots()
		RCS_ax.boxplot(RCS_data, labels = RCS_names)
		RCS_ax.set_xlabel('Condition')
		RCS_ax.set_ylabel('C1/2 Value')
		RCS_ax.set_title(row['Label@Accession'])
		plt.xticks(rotation=90)
		plt.savefig(RCS_output_dir + '/' + row['Label@Accession'].replace('|','-') + file_type, format=file_type[1:],bbox_inches='tight')
		plt.clf()
		plt.close(fig='all')
		del RCS_fig, RCS_ax

''' FITTING EFFICIENCY '''
def FittingEfficiency(file,name,version="",CHalflow=0,CHalfhigh=3.48,rsquared=0.6,confintlow=0,confinthigh=0.35): #accepts 'Combined_OUTPUT.csv' file path and name for fitting efficiency table and returns fitting efficiency data frame, RCS_transfer data frame, and peptides that meet conditions list
	fittingDF = pd.read_csv(file)
	fittingDF = trim_ends(fittingDF) #trims ends for combined site transfer
	print('Calculating Fitting Efficiency for ' + name)

	''' PEPTIDES '''
	print('Current: Calculating peptide and protein counts')
	#Total Peptides
	raw_peptide = len(fittingDF)
	#Make a copy of the fittingDF to avoid problems with it later
	peptideDF = fittingDF.copy()
	#Remove peptides with 'cnc' trim_CHalf because they will not be needed for later calculations
	peptideDF = peptideDF[peptideDF['trim_CHalf'] != 'cnc'].reset_index(drop=True)
	peptideDF['trim_CHalf'] = peptideDF['trim_CHalf'].astype(float) #modifying type to allow for calculations later

	#Count of peptides with chalf value
	can_be_fit_peptide = len(peptideDF) #can_be_fit_protein = len(peptideTOproteinDF(peptideDF))

	#C1/2 in range (>=0 and <=3.48)
	chalf_inrange_bool = np.logical_and(np.array(peptideDF['trim_CHalf'] >= CHalflow), np.array(peptideDF['trim_CHalf'] <= CHalfhigh))
	chalf_inrange = chalf_inrange_bool.sum()
	chalf_inrange_peptide_lst = peptideDF[chalf_inrange_bool]['Accession@Peptide'].tolist() #chalf_inrange_protein = len(peptideTOproteinDF(peptideDF[chalf_inrange_bool]))
	chalf_inrange_peptide_lst_index = peptideDF[chalf_inrange_bool].index.tolist()
	#r^2 > 0.6 and C1/2 in range
	rsquared_peptide_bool = np.logical_and(chalf_inrange_bool, np.array(peptideDF['trim_r_squared'].astype(float) > rsquared))
	rsquared_peptide = rsquared_peptide_bool.sum()
	rsquared_lst = peptideDF[rsquared_peptide_bool]['Accession@Peptide'].tolist() #rsquared_protein = len(peptideTOproteinDF(peptideDF[rsquared_peptide_bool]))
	rsquared_lst_index = peptideDF[rsquared_peptide_bool].index.tolist()

	#Conf int in range (>=0 <=0.35) and r^2 > 0.6 and C1/2 in range
	inrange_peptide_bool = np.logical_and(rsquared_peptide_bool, np.logical_and(np.array(peptideDF['trim_ratioTOrange'].astype(float) >= confintlow), np.array(peptideDF['trim_ratioTOrange'].astype(float) <= confinthigh)))
	inrange_peptide = inrange_peptide_bool.sum()
	inrange_lst = peptideDF[inrange_peptide_bool]['Accession@Peptide'].tolist() #inrange_protein = len(peptideTOproteinDF(peptideDF[inrange_peptide_bool]))
	inrange_lst_index = peptideDF[inrange_peptide_bool].index.tolist()

	#RCS_transfer
	RCS_transfer = pd.DataFrame(columns=["Accession","Peptide", "Start", "End",'Peptide Length','trim_CHalf','trim_r_squared','trim_ratioTOrange','trim_CHalf_ConfidenceInterval','trim_slope','trim_b','Label Site','Label Type','Residue Number','Label@Accession']) #for transferring the needed information for combined site processing
	#RCS_transfer['Index'] = peptideDF[inrange_peptide_bool].index.tolist()
	RCS_transfer['Accession'] = peptideDF[inrange_peptide_bool]['Accession']
	RCS_transfer['Peptide'] = peptideDF[inrange_peptide_bool]['Peptide']
	RCS_transfer['Start'] = peptideDF[inrange_peptide_bool]['Start']
	RCS_transfer['End'] = peptideDF[inrange_peptide_bool]['End']
	RCS_transfer['trim_CHalf'] = peptideDF[inrange_peptide_bool]['trim_CHalf']
	RCS_transfer['trim_r_squared'] = peptideDF[inrange_peptide_bool]['trim_r_squared']
	RCS_transfer['trim_ratioTOrange'] = peptideDF[inrange_peptide_bool]['trim_ratioTOrange']
	RCS_transfer['trim_CHalf_ConfidenceInterval'] = peptideDF[inrange_peptide_bool]['trim_CHalf_ConfidenceInterval']
	RCS_transfer['trim_slope'] = peptideDF[inrange_peptide_bool]['trim_slope']
	RCS_transfer['trim_b'] = peptideDF[inrange_peptide_bool]['trim_b']
	RCS_transfer["Peptide"] = RCS_transfer["Peptide"].str.replace("\\(" + "\\+" + "57.02" + "\\)","") #Remove unneeded tags
	RCS_transfer["Peptide"] = RCS_transfer["Peptide"].str.replace("\\(" + "\\-" + "17.03" + "\\)","")
	RCS_transfer = RCS_transfer.merge(peptideDF[inrange_peptide_bool][peptideDF.columns.tolist()[peptideDF.columns.tolist().index('End')+1:peptideDF.columns.tolist().index('#pts')]],how='left',left_index=True,right_index=True)

	RCS_transfer = RCS_transfer.progress_apply(make_label_site_function, axis = 1)
	RCS_transfer.drop(RCS_transfer.loc[RCS_transfer['Label Site']=='N/A'].index, inplace=True)
	#RCS_transfer = RCS_transfer.reset_index(drop=True)
	RCS_transfer['Label@Accession'] = RCS_transfer['Label Type'].astype(str) + '_' + RCS_transfer['Label Site'].astype(str) + '_' + RCS_transfer['Accession'].astype(str)
	RCS_transfer.sort_values(by=['Accession','Residue Number'],ignore_index=True,inplace=True)
	RCS_transfer.rename_axis(version,axis='index',inplace=True)
	RCS_transfer['Peptide Length'] = RCS_transfer['End'] - RCS_transfer['Start']

	#has >1 reporter (conditions of conf int in range plus out#reporter > 1)
	hasreporteraccessionlst = []
	outreporterDict = {}
	outreporterDF = peptideDF.groupby(by='Accession')
	for key in list(outreporterDF.groups.keys()):
		groupDF = outreporterDF.get_group(key)
		outreporter = len(groupDF)
		outreporterDict.update({key:outreporter})
	hasreporterDF = pd.DataFrame(columns = ['Accession@Peptide','Out Reporter'])
	hasreporterDF['Accession@Peptide'] = inrange_lst
	hasreporterDF['index_0'] = inrange_lst_index
	hasreporterDF = hasreporterDF.apply(AtoOR,axis=1,dictionary=outreporterDict)
	hasreporter_peptide_lst = hasreporterDF[hasreporterDF['Out Reporter']>1]['Accession@Peptide'].tolist()
	hasreporter_peptide_lst_index = hasreporterDF[hasreporterDF['Out Reporter']>1]['index_0'].tolist()
	hasreporter_peptide = len(hasreporter_peptide_lst)

	'''for i in range(len(inrange_lst)):
		outreporterlst = getIndexes(fittingDF, peptideDF[inrange_peptide_bool]['Accession'].tolist()[i])
		outreporter = len(outreporterlst)
		if outreporter > 1:
			hasreporter_peptide += 1
			hasreporter_peptide_lst.append(inrange_lst[i])
	hasreporter_protein_lst = []
	for i in range(len(hasreporter_peptide_lst)):
		if hasreporter_peptide_lst[i].split('@')[0] not in hasreporter_protein_lst:
			hasreporter_protein_lst.append(hasreporter_peptide_lst[i].split('@')[0])
	hasreporter_protein = len(hasreporter_protein_lst)'''

	''' PROTEINS '''
	#Protein grouping   
	proteinGroups = fittingDF.groupby(by='Accession')
	proteinKey = list(proteinGroups.groups.keys()) #list of groups by key
	fittingDict = {'can be fit':[], 'C1/2 in range':[], 'r^2 > 0.6':[],'Conf Int in range':[], 'has >1 reporter':[]}

	#Total Proteins
	raw_protein = len(proteinGroups) #len(peptideTOproteinDF(fittingDF))

	#Grouping loop for calculating the rest
	for key in proteinKey:
		group = proteinGroups.get_group(key)
		#Remove peptides with 'cnc' trim_CHalf because they will not be needed for later calculations
		group = group[group['trim_CHalf'] != 'cnc'].reset_index(drop=True)
		group['trim_CHalf'] = group['trim_CHalf'].astype(float) #modifying type to allow for calculations later
		if len(group) > 0:
			fittingDict['can be fit'].append(True)
		else:
			fittingDict['can be fit'].append(False)
		Pchalf_inrange_bool = np.logical_and(np.array(group['trim_CHalf'] >= CHalflow), np.array(group['trim_CHalf'] <= CHalfhigh))
		cond1 = combineBool(Pchalf_inrange_bool,'or')
		fittingDict['C1/2 in range'].append(cond1)
		if cond1 and combineBool(np.array(group['trim_r_squared'].astype(float) > rsquared),'or'):
			cond2 = True
			fittingDict['r^2 > 0.6'].append(cond2)
		else:
			cond2 = False
			fittingDict['r^2 > 0.6'].append(cond2)
		if cond2 and combineBool(np.logical_and(np.array(group['trim_ratioTOrange'].astype(float) >= confintlow), np.array(group['trim_ratioTOrange'].astype(float) <= confinthigh)),'or'):
			cond3 = True
			fittingDict['Conf Int in range'].append(cond3)
		else:
			cond3 = False
			fittingDict['Conf Int in range'].append(cond3)
		if cond3 and len(group)>1:
			cond4 = True
			fittingDict['has >1 reporter'].append(cond4)
		else:
			cond4 = False
			fittingDict['has >1 reporter'].append(cond4)

	#Counts    
	can_be_fit_protein = np.array(fittingDict['can be fit']).sum()
	chalf_inrange_protein = np.array(fittingDict['C1/2 in range']).sum()
	rsquared_protein = np.array(fittingDict['r^2 > 0.6']).sum()
	inrange_protein = np.array(fittingDict['Conf Int in range']).sum()
	hasreporter_protein = np.array(fittingDict['has >1 reporter']).sum()
		
	''' EXPORT '''
	print('Current: Preparing Exports')
	#Fitting Efficiency Summary Table
	outputDF = pd.DataFrame(columns=[name + ' Fitting Efficiency ' + '(' + version + ')', 'peptide', 'protein', 'peptide %', 'protein %'])

	keyList = ['Raw','can be fit', 'C1/2 in range (' + str(CHalflow) + ':' + str(CHalfhigh) + ')', 'r^2 > ' + str(rsquared),'Conf Int in range (' + str(confintlow) + ':' + str(confinthigh) + ')', 'has >1 reporter']

	peptide_output = [raw_peptide, can_be_fit_peptide, chalf_inrange, rsquared_peptide,
		inrange_peptide, hasreporter_peptide]
	peptide_percent_output = ['-', str(can_be_fit_peptide/raw_peptide*100) + '%', str(chalf_inrange/raw_peptide*100) + '%', str(rsquared_peptide/raw_peptide*100) + '%',
		str(inrange_peptide/raw_peptide*100) + '%', str(hasreporter_peptide/raw_peptide*100) + '%']

	protein_output = [raw_protein, can_be_fit_protein, chalf_inrange_protein, rsquared_protein,
		inrange_protein, hasreporter_protein]
	protein_percent_output = ['-', str(can_be_fit_protein/raw_protein*100) + '%', str(chalf_inrange_protein/raw_protein*100) + '%', str(rsquared_protein/raw_protein*100) + '%',
		str(inrange_protein/raw_protein*100) + '%', str(hasreporter_protein/raw_protein*100) + '%']

	outputDF[name + ' Fitting Efficiency ' + '(' + version + ')'] = keyList
	outputDF['peptide'] = peptide_output
	outputDF['peptide %'] = peptide_percent_output
	outputDF['protein'] = protein_output
	outputDF['protein %'] = protein_percent_output

	#List of accession@peptide that meet conditions
	lenDF = max(len(chalf_inrange_peptide_lst),len(rsquared_lst),len(inrange_lst),len(hasreporter_peptide_lst))
	lenlst = [chalf_inrange_peptide_lst,rsquared_lst,inrange_lst,hasreporter_peptide_lst]
	for lst in lenlst:
		while len(lst) < lenDF:
			lst.append(np.nan)
	listDF = pd.DataFrame(columns=[version, 'C1/2 in range (' + str(CHalflow) + ':' + str(CHalfhigh) + ')', 'index_1', 'r^2 > ' + str(rsquared), 'index_2', 'Conf Int in range (' + str(confintlow) + ':' + str(confinthigh) + ')', 'index_3', 'has >1 reporter']) #fitting list of peptides
	listDF['C1/2 in range (' + str(CHalflow) + ':' + str(CHalfhigh) + ')'] = chalf_inrange_peptide_lst
	listDF[version] = chalf_inrange_peptide_lst_index
	listDF['r^2 > ' + str(rsquared)] = rsquared_lst
	listDF['index_1'] = rsquared_lst_index + [np.nan]*(len(listDF)-len(rsquared_lst_index))
	listDF['Conf Int in range (' + str(confintlow) + ':' + str(confinthigh) + ')'] = inrange_lst
	listDF['index_2'] = inrange_lst_index + [np.nan]*(len(listDF)-len(inrange_lst_index))
	listDF['has >1 reporter'] = hasreporter_peptide_lst
	listDF['index_3'] = hasreporter_peptide_lst_index + [np.nan]*(len(listDF)-len(hasreporter_peptide_lst_index))

	return [outputDF,RCS_transfer,listDF]

''' COMBINED SITE '''
def CombinedSite(inputlst,RCS_output_dir,RCS_input,version="",dynamic=False,min=0,max=3.6,file_type='.svg'): #Accepts list of 'Label Sites.csv' files (os.path.realpath format), output directory location, and project name (also can specify if y axis is dynamic or set between max and min) to produce Combined Site box plots and a stats table
	#For reference for CHalf integration
	'''
	print('Please input desired output name:')
	RCS_input = input()
	RCS_output_dir = RCS_input + ' RCS Boxplots'
	os.makedirs(RCS_output_dir)
	print('Ouput Directory: ' + RCS_output_dir)
	'''
	RCS_transfer_lst = inputlst
	'''RCS_dir_lst = os.listdir(inputdir)
	for file in range(len(RCS_dir_lst)): #Extracting "Label Sites.csv" files to be used as data frames
		if '_labesite_OUTPUT.csv' in RCS_dir_lst[file]:
			RCS_transfer_lst.append(inputdir + '/' + RCS_dir_lst[file])'''
	RCS_DF_lst = []
	RCS_conditions = ['Label@Accession']
	for file in range(len(RCS_transfer_lst)):
		if '.csv' not in RCS_transfer_lst[file]:
			RCS_transfer_lst[file] += '.csv'
	for file in range(len(RCS_transfer_lst)):
		RCS_DF_lst.append(getDataFrame(RCS_transfer_lst[file])) #makes a list of the dataframes of each individual "Label Sites.csv"
		head = os.path.dirname(RCS_transfer_lst[file])
		condition = RCS_transfer_lst[file].replace(head,'').replace(' Label Sites.csv','')
		RCS_conditions.append(condition) #collects condition names for column names
	conditionDict = {}
	for i in range(len(RCS_conditions[1:])):
		conditionDict.update({RCS_conditions[i+1]:RCS_DF_lst[i]})
	RCS_DF = pd.DataFrame(columns=RCS_conditions) #create main data frame for analysis
	labeled_lst = []
	for df in RCS_DF_lst: #creates list of present Label@Accession in all data frames
		for label in df['Label@Accession'].tolist():
			if label not in labeled_lst:
				labeled_lst.append(label)
	labels_to_box = [] #for determining if label present in multiple dataframes
	for label in labeled_lst:
		present_array = np.array([])
		for df in RCS_DF_lst:
			present_array = np.append(present_array,label in df['Label@Accession'].tolist())
		if present_array.sum()>1:
			labels_to_box.append(label)
	RCS_DF['Label@Accession'] = labels_to_box
	for column in RCS_DF.columns[1:]: #adding new columns for stats values
		RCS_DF.insert(RCS_DF.columns.get_loc(column)+1,'max'+column,np.nan)
		RCS_DF.insert(RCS_DF.columns.get_loc(column)+1,'Q3'+column,np.nan)
		RCS_DF.insert(RCS_DF.columns.get_loc(column)+1,'median'+column,np.nan)
		RCS_DF.insert(RCS_DF.columns.get_loc(column)+1,'Q1'+column,np.nan)
		RCS_DF.insert(RCS_DF.columns.get_loc(column)+1,'min'+column,np.nan)
		RCS_DF.insert(RCS_DF.columns.get_loc(column)+1,'std'+column,np.nan)
		RCS_DF.insert(RCS_DF.columns.get_loc(column)+1,'mean'+column,np.nan)
		RCS_DF.insert(RCS_DF.columns.get_loc(column)+1,'count'+column,np.nan)
	RCS_DF = RCS_DF.apply(describe_apply,axis=1,conditionDict=conditionDict) #fills in stats for labels across conditions   
			
	RCS_DF.apply(CS_graph_apply,axis=1,conditionDict=conditionDict,min=min,max=max,dynamic=dynamic,file_type=file_type,RCS_output_dir=RCS_output_dir)
	RCS_DF.rename_axis(version,axis='index',inplace=True)
	RCS_DF.to_csv(RCS_output_dir + '/' + RCS_input + ' Shared_OUTPUT.csv')

''' RESIDUE MAPPER 2 '''
def ResidueMapper_2(input,outputdir,version="",dynamic=False,min=0,max=3.6,file_type='.svg',labels=['Y(+125.90)', 'Y(+251.79)', 'H(+125.90)', 'H(+251.79)', 'C(+47.98)', 'C(+31.99)', 'C(+15.99)', 'M(+15.99)', 'M(+31.99)', 'W(+125.90)']): #Accepts input of 'Combined Label Sites.csv' file and output directory location (also can specify if y axis is dynamic or set between max and min) to produce Protein Map figures
	inputDF = pd.read_csv(input)
	proteinlst = inputDF['Accession'].unique().tolist()
	proteindict = {}
	poplst = []
	for protein in proteinlst:
		proteindict.update({protein:inputDF[inputDF['Accession'] == protein][['Label Site','Label Type','trim_CHalf','trim_CHalf_ConfidenceInterval','Count']]})
	for protein in proteindict:
		df = proteindict[protein]
		if len(df) > 1:
			df['Label'] = df['Label Type']
			df['Site'] = df['Label Site'].str[1:].astype(float).astype(int)
		else:
			poplst.append(protein)
	for entry in poplst: #remove proteins without more than 1 peptide
		proteindict.pop(entry)
	for protein in proteindict:
		proteindict[protein] = proteindict[protein][['Label Site','Label','Site','Count','trim_CHalf','trim_CHalf_ConfidenceInterval']] #reorder columns

	for protein in proteindict: #Group proteinDF's by Label Site for calculating stats
		boxDF = pd.DataFrame(columns=['Label','Site','trim_CHalf','trim_CHalf_ConfidenceInterval','Count']) #Merge stats into single table for making plots
		boxDF['Label'] = proteindict[protein]['Label']
		boxDF['Site'] = proteindict[protein]['Site']
		boxDF['trim_CHalf'] = proteindict[protein]['trim_CHalf']
		boxDF['trim_CHalf_ConfidenceInterval'] = proteindict[protein]['trim_CHalf_ConfidenceInterval']
		boxDF['Count'] = proteindict[protein]['Count']

		bool_list = []
		for label in labels: #Remove labels not searched for
			bool_list.append(label == boxDF['Label'])
		final_bool = np.array([False]*len(boxDF))
		for boolx in bool_list:
			final_bool = np.logical_or(final_bool,boolx)
		boxDF = boxDF[final_bool]
		if len(boxDF)>1:
			groups2 = boxDF.groupby("Label") #Group each plot based on Amino Acid
			marker = itertools.cycle(('s', 'v', '^', 'o', 'D'))
			if not dynamic:
				plt.figure(figsize=(8,6))
				for name, group in groups2:
					plt.errorbar(group["Site"], group["trim_CHalf"], yerr=group["trim_CHalf_ConfidenceInterval"], linestyle="", label=name, fmt=next(marker))
				plt.ylabel('trim_CHalf')
				plt.xlabel('Site')
				plt.legend()
				plt.title(protein)
				plt.autoscale(enable=True)
				plt.ylim(top=max)
				plt.ylim(bottom=min)
				plt.savefig(outputdir + '/' + protein.replace('|','_') + file_type) #Make and save plot of protein
				plt.clf()
				plt.close()
			else:
				plt.figure(figsize=(8,6))
				for name, group in groups2:
					plt.errorbar(group["Site"], group["trim_CHalf"], yerr=group["trim_CHalf_ConfidenceInterval"], linestyle="", label=name, fmt=next(marker))
				plt.ylabel('trim_CHalf')
				plt.xlabel('Site')
				plt.legend()
				plt.title(protein)
				plt.autoscale(enable=True)
				plt.savefig(outputdir + '/' + protein.replace('|','_') + file_type) #Make and save plot of protein
				plt.clf()
				plt.close()
			boxDF = boxDF[['Label','Site','Count','trim_CHalf','trim_CHalf_ConfidenceInterval']] #reorder
			boxDF.sort_values('Site',inplace=True)
			boxDF.reset_index(drop=True,inplace=True)
			boxDF.rename_axis(version,axis='index',inplace=True)
			boxDF.to_csv(outputdir + '/' + protein.replace('|','_') + '.csv') #Export stats for reference

''' LABEL FINDER ''' #Version used by CHalf in place of Label Efficiency
def LabelFinder(inp,out,version='',labels=['Y(+125.90)', 'Y(+251.79)', 'H(+125.90)', 'H(+251.79)', 'C(+47.98)', 'C(+31.99)', 'C(+15.99)', 'M(+15.99)', 'M(+31.99)', 'W(+125.90)']): #accepts input file, labels to find (list), and project name; produces label efficiency file and tags file
	''' SET UP '''
	inpDF = pd.read_csv(inp)
	inpDF = trim_ends(inpDF) #remove beginning and end of peptides (PEAKS format) and TMT tags
	aalst = [] #list of amino acids to look for
	for label in labels:
		if label[0] not in aalst:
			aalst.append(label[0]) #appends first character of tag (should be amino acid) i.e Y in 'Y(+125.90)'
	aadict = {}
	for aa in aalst: #creates dictionary of amino acids to find and associated tags
		templst = []
		for label in labels:
			if aa in label:
				templst.append(label)
		aadict.update({aa:templst})
	keys = list(aadict)
	efflst = [] #for producing table key
	for key in keys:
		efflst.append(key)
		for tag in aadict[key]:
			efflst.append(tag)
	outputDF = pd.DataFrame(columns=[out + ' Label Efficiency', 'peptide', 'protein', 'peptide %', 'protein %'])
	keyList = ['Raw', 'enough valid pts'] + efflst + ['has any', 'has any tag', 'can be fit and has any tag']
	outputDF[out + ' Label Efficiency'] = keyList
	outputDF.rename_axis(out + ' Label Efficiency ' + '(' + version + ')', axis='index', inplace=True)

	''' PEPTIDES '''
	indexList = outputDF[out + ' Label Efficiency'].tolist()
	outputDF.iloc[0]['peptide'] = len(inpDF)
	validArray = np.array([inpDF['#Non_Zero'] > 3])
	outputDF.iloc[1]['peptide'] = validArray.sum()
	arraydict = {}
	for i in range(len(indexList)-5): #Counts number of peptides with desired amino acids and tags
		labelarray = np.array([inpDF['Peptide'].str.contains(re.escape(indexList[i+2]))])
		arraydict.update({re.escape(indexList[i+2]):labelarray}) #saves findings as boolean arrays in dictionary for future calculations
		outputDF['peptide'][i+2] = labelarray.sum()
	arraydictKey = list(arraydict)
	hasanyArraysList = []
	anytagArraysList = []
	for key in arraydictKey:
		if len(key) == 1:
			hasanyArraysList.append(arraydict[key]) #sorts out amino acid boolean arrays
		else:
			anytagArraysList.append(arraydict[key]) #sorts out tag boolean arrays
	hasanyArray = np.array([False]*len(inpDF))
	anytagArray = np.array([False]*len(inpDF))
	for array in hasanyArraysList: #makes boolean array for hasany amino acid in search
		hasanyArray = np.logical_or(hasanyArray,array)
	for array in anytagArraysList: #makes boolean array for hasany tag in search
		anytagArray = np.logical_or(anytagArray,array)
	outputDF.iloc[-3]['peptide'] = hasanyArray.sum()
	outputDF.iloc[-2]['peptide'] = anytagArray.sum()
	fittingtags = np.logical_and(validArray,anytagArray)[0] #for export of fittable tagged peptides
	outputDF.iloc[-1]['peptide'] = fittingtags.sum() #counts if has >3 points and has any tag in search

	''' PROTEINS '''
	proteinGroups = inpDF.groupby(by='Accession') #groups peptides by protein
	outputDF.iloc[0]['protein'] = len(proteinGroups) #counts number of proteins
	proteinKey = list(proteinGroups.groups.keys()) #list of groups by key
	PvalidArray = np.array([]) #making empty array for construction of proteins with >3 pts
	for key in proteinKey:
		group = proteinGroups.get_group(key)
		PvalidArray = np.append(PvalidArray,combineBool(np.array(group['#Non_Zero'] > 3),'or'))
	outputDF.iloc[1]['protein'] =  PvalidArray.sum()
	Parraydict = {}
	for i in range(len(indexList)-5): #Counts number of protein groups with desired amino acids and tags
		PlabelArray = np.array([])
		for key in proteinKey:
			group = proteinGroups.get_group(key)
			PlabelArray = np.append(PlabelArray,combineBool(np.array([group['Peptide'].str.contains(re.escape(indexList[i+2])).tolist()]),'or'))
		Parraydict.update({re.escape(indexList[i+2]):PlabelArray}) #saves findings as boolean arrays in dictionary for future calculations
		outputDF['protein'][i+2] = PlabelArray.sum()
	ParraydictKey = list(Parraydict)
	PhasanyArraysList = []
	PanytagArraysList = []
	for key in ParraydictKey:
		if len(key) == 1:
			PhasanyArraysList.append(Parraydict[key]) #sorts out amino acid boolean arrays
		else:
			PanytagArraysList.append(Parraydict[key]) #sorts out tag boolean arrays
	PhasanyArray = np.array([False]*len(proteinGroups))
	PanytagArray = np.array([False]*len(proteinGroups))
	for array in PhasanyArraysList: #makes boolean array for hasany amino acid in search
		PhasanyArray = np.logical_or(PhasanyArray,array)
	for array in PanytagArraysList: #makes boolean array for hasany tag in search
		PanytagArray = np.logical_or(PanytagArray,array)
	outputDF.iloc[-3]['protein'] = PhasanyArray.sum()
	outputDF.iloc[-2]['protein'] = PanytagArray.sum()
	outputDF.iloc[-1]['protein'] = np.logical_and(PvalidArray,PanytagArray).sum() #counts if has >3 points and has any tag in search

	''' PERCENTAGES '''
	outputDF.iloc[0]['peptide %'] = '-'
	outputDF.iloc[0]['protein %']= '-'
	outputDF.iloc[1]['peptide %'] = str(outputDF.iloc[1]['peptide']/outputDF.iloc[0]['peptide']*100) + '%'
	outputDF.iloc[1]['protein %']= str(outputDF.iloc[1]['protein']/outputDF.iloc[0]['protein']*100) + '%'
	outputDF.iloc[-3]['peptide %'] = str(outputDF.iloc[-3]['peptide']/outputDF.iloc[0]['peptide']*100) + '%'
	outputDF.iloc[-3]['protein %']= str(outputDF.iloc[-3]['protein']/outputDF.iloc[0]['protein']*100) + '%'
	outputDF.iloc[-2]['peptide %'] = str(outputDF.iloc[-2]['peptide']/outputDF.iloc[-3]['peptide']*100) + '%'
	outputDF.iloc[-2]['protein %']= str(outputDF.iloc[-2]['protein']/outputDF.iloc[-3]['protein']*100) + '%'
	outputDF.iloc[-1]['peptide %'] = str(outputDF.iloc[-1]['peptide']/outputDF.iloc[-3]['peptide']*100) + '%'
	outputDF.iloc[-1]['protein %']= str(outputDF.iloc[-1]['protein']/outputDF.iloc[-3]['protein']*100) + '%'
	for i in range(len(indexList)-5):
		if len(outputDF[out + ' Label Efficiency'].tolist()[i+2]) == 1:
			outputDF['peptide %'][i+2] = str(outputDF.iloc[i+2]['peptide']/outputDF.iloc[0]['peptide']*100) + '%'
			outputDF['protein %'][i+2] = str(outputDF.iloc[i+2]['protein']/outputDF.iloc[0]['protein']*100) + '%'
		else:
			val = outputDF[out + ' Label Efficiency'].tolist()[i+2][0]
			for j in range(len(outputDF[out + ' Label Efficiency'].tolist())):
				if val == outputDF[out + ' Label Efficiency'].tolist()[j]:
					outputDF['peptide %'][i+2] = str(outputDF.iloc[i+2]['peptide']/outputDF.iloc[j]['peptide']*100) + '%'
					outputDF['protein %'][i+2] = str(outputDF.iloc[i+2]['protein']/outputDF.iloc[j]['protein']*100) + '%'
	''' OUTPUTS '''
	outputDF.rename(mapper={outputDF.columns[0]:outputDF.index.name},axis=1,inplace=True)
	tagged = inpDF[fittingtags]#.drop(axis=1,labels='Unnamed: 0')
	tagged.rename_axis(version, axis='index', inplace=True)
	#tagged.to_csv(out + ' Label Finder Project/' + out + ' Tags.csv')
	#outputDF.to_csv(out + ' Label Finder Project/' + out + ' Label Efficiency.csv')
	return [outputDF,tagged]

def CRM_Stats_Converter(df):
	df['Label@Site'] = df['Label'] + '@' + df['Site'].astype(int).astype(str)
	items = df['Label@Site'].unique().tolist()
	labels = []
	sites = []
	labelsites = []
	for item in items:
		labels.append(item.split('@')[0])
		sites.append(item.split('@')[1])
		labelsites.append(item.split('@')[0]+'@'+item.split('@')[1])
	data = {
		'Label@Site' : labelsites,
		'Label' : labels,
		'Site' : sites
	}
	outDF = pd.DataFrame(data).set_index('Label@Site')
	groups = df.groupby(by='Condition')
	for name, group in groups:
		group = group[['Label','Site']].join(group[['Count','trim_CHalf','trim_CHalf_ConfidenceInterval','trim_slope']].add_suffix('_' + str(name)))
		group['Label@Site'] = group['Label'] + '@' + group['Site'].astype(int).astype(str)
		outDF = outDF.join(group.set_index('Label@Site')[group.set_index('Label@Site').columns.tolist()[2:]])
	return outDF

''' COMBINED RESIDUE MAPPER 2''' #Combined Residue Mapper adjusted for Combined Label Sites Files
def CombinedResidueMapper_2(file_list,out_dir,project_name,version='',dynamic=False,min=0,max=3.6,file_type='.svg',labels=['Y(+125.90)', 'Y(+251.79)', 'H(+125.90)', 'H(+251.79)', 'C(+47.98)', 'C(+31.99)', 'C(+15.99)', 'M(+15.99)', 'M(+31.99)', 'W(+125.90)']): #takes Label Site.csv's and performs residue mapper across conditions for easier total protein comparison
	try:
		condition_dir = {} #for storing dataframes with condition names
		for file in file_list:
			df = pd.read_csv(file) #make data frame
			name = os.path.realpath(file).split('/')[-1].split('\\')[-1].split('Combined Label Sites.csv')[0] #isolates condition name from file name
			condition_dir.update({name:df})
		proteins_dict = {}
		for key in list(condition_dir):
			conDF = condition_dir[key]
			conList = conDF['Accession'].unique().tolist()
			for protein in conList:
				if protein not in list(proteins_dict): #makes a directory of proteins and their associated condition
					proteins_dict.update({protein:[key]})
				elif protein in list(proteins_dict):
					proteins_dict[protein].append(key)
		proteinDF_dict = {}
		for protein in list(proteins_dict):
			proteinDF = pd.DataFrame(columns=['Condition','Label Type','Site','Count','trim_CHalf','trim_CHalf_ConfidenceInterval','trim_slope'])
			if len(proteins_dict[protein]) > 1: #checks if protein is present in more than one condition
				for condition in proteins_dict[protein]:
					df = condition_dir[condition]
					df = df[df['Accession'] == protein][['Label Type','Residue Number','Count','trim_CHalf','trim_CHalf_ConfidenceInterval','trim_slope']]
					df['Condition'] = condition #Add condition name
					df.rename(columns={'Residue Number':'Site'},inplace=True)
					df = df[['Condition','Label Type','Site','Count','trim_CHalf','trim_CHalf_ConfidenceInterval','trim_slope']] #Reorder
					proteinDF = proteinDF.append(df,ignore_index=True)
				proteinDF.rename(columns={'Label Type':'Label'},inplace=True)
				bool_list = []
				for label in labels: #Remove labels not searched for
					bool_list.append(label == proteinDF['Label'])
				final_bool = np.array([False]*len(proteinDF))
				for boolx in bool_list:
					final_bool = np.logical_or(final_bool,boolx)
				proteinDF = proteinDF[final_bool]
				proteinDF_dict.update({protein:proteinDF})
				proteinDF.sort_values(by='Site',inplace=True)
				proteinDF.reset_index(drop=True,inplace=True) #Reset index for cleaner look
				proteinDF.rename_axis(version,axis='index',inplace=True)
				try:
					os.mkdir(out_dir + '/' + project_name + ' CRM Outputs')
				except:
					None
				try: #save as csv for reference
					file = out_dir + '/' + project_name + ' CRM Outputs' + '/' + protein.replace('|','_') + ' CRM Stats.csv'
					proteinDF = CRM_Stats_Converter(proteinDF)
					proteinDF.to_csv(file)
				except:
					file = out_dir + '/' + project_name + ' ' + protein.replace('|','_') + ' CRM Stats.csv'
					proteinDF = CRM_Stats_Converter(proteinDF)
					proteinDF.to_csv(file)
		megaDataDF = pd.DataFrame()
		label_sites = []
		for condition in list(condition_dir):
			conDF = condition_dir[condition]
			label_sites += conDF['Label@Accession'].tolist()
		label_sites = list(set(label_sites))
		megaDataDF['Label@Accession'] = label_sites
		megaDataDF['Accession'] = megaDataDF['Label@Accession'].str.split('_').str[-2] + '_' + megaDataDF['Label@Accession'].str.split('_').str[-1]
		megaDataDF['Label Type'] = megaDataDF['Label@Accession'].str.split('_').str[0]
		megaDataDF['Site'] = megaDataDF['Label@Accession'].str.split('_').str[1].str[1:]
		for condition in list(condition_dir):
			conDF = condition_dir[condition][['Label@Accession','Count','trim_CHalf','trim_CHalf_ConfidenceInterval','trim_slope']].add_suffix('_' + condition)
			conDF['Label@Accession'] = conDF[['Label@Accession'+'_'+condition]]
			del conDF['Label@Accession'+'_'+condition]
			megaDataDF = megaDataDF.merge(conDF,how='left')
			#megaDataDF[['Count','trim_CHalf','trim_CHalf_ConfidenceInterval','trim_slope']] = megaDataDF[['Count','trim_CHalf','trim_CHalf_ConfidenceInterval','trim_slope']].add_suffix('_' + condition)
		megaDataDF = megaDataDF.sort_values(by=['Accession','Site']) #Rearranging collumns
		megaDataDF.reset_index(drop=True,inplace=True)
		try: #save as csv for reference
			file = out_dir + '/' + project_name + ' CRM Outputs' + '/' + '[' + project_name + '] RCS Summary.csv'
			megaDataDF.to_csv(file)   
		except:
			try:
				os.mkdir(out_dir + '/' + project_name + ' CRM Outputs')
			except:
				None
			file = out_dir + '/' + project_name + ' CRM Outputs' + '/' + '[' + project_name + '] RCS Summary.csv'
			megaDataDF.to_csv(file)
	
		for protein in list(proteinDF_dict): #start boxplots 
			df = proteinDF_dict[protein]
			groups = df.groupby(by='Condition')
			marker = itertools.cycle(('s', 'v', '^', 'o', 'D'))
			if not dynamic:
				plt.figure(figsize=(8,6))
				for name, group in groups:
					plt.errorbar(group["Site"], group["trim_CHalf"], yerr=group["trim_CHalf_ConfidenceInterval"], linestyle="", label=name, fmt=next(marker))
				plt.ylabel('trim_CHalf')
				plt.xlabel('Site')
				plt.legend()
				plt.title(protein)
				plt.autoscale(enable=True)
				plt.ylim(top=max)
				plt.ylim(bottom=min)
				try:
					plt.savefig(out_dir + '/' + project_name + ' CRM Outputs' + '/' + protein.replace('|','_') + ' Combined Residue Map' + file_type) #Make and save plot of protein
				except:
					plt.savefig(out_dir + project_name + ' ' + protein.replace('|','_') + ' Combined Residue Map' + file_type) #Make and save plot of protein
				plt.clf()
				plt.close()
			else:
				plt.figure(figsize=(8,6))
				for name, group in groups:
					plt.errorbar(group["Site"], group["trim_CHalf"], yerr=group["trim_CHalf_ConfidenceInterval"], linestyle="", label=name, fmt=next(marker))
				plt.ylabel('trim_CHalf')
				plt.xlabel('Site')
				plt.legend()
				plt.title(protein)
				plt.autoscale(enable=True)
				try:
					plt.savefig(out_dir + '/' + project_name + ' CRM Outputs' + '/' + protein.replace('|','_') + ' Combined Residue Map' + file_type) #Make and save plot of protein
				except:
					plt.savefig(out_dir + project_name + ' ' + protein.replace('|','_') + ' Combined Residue Map' + file_type) #Make and save plot of protein
				plt.clf()
				plt.close() 
	except KeyError:
		print('No shared sites found.')

''' CHALF_v4.3 AUXILARY FUNCTIONS '''
def getDataFrame(file):
		""" Returns pandas DataFrame of file.  Can use either .csv, .xls, or .xlsx files. """
		if ".csv" in file:
			df = pd.read_csv(file)
		elif ".xls" in file:
			df = pd.read_excel(file)
		else:
			print("*** ERROR: Incorrec t file name: \"" + file + "\". Must include ending ('.csv' or '.xls' or '.xlsx') ***")
			return
		return df

def rep_filecombine(repInfo):
	""" COMBINES proteinpeptide.csv and protein.csv files from PEAKS analysis into a single DataFrame w/wanted data """
	''' repInfo = [condition, rep#, proteinpeptide.csv, protein.csv, CD/HD, conc/temp list] '''

	# Get DataFrames from protein-peptides.csv and protein.csv files
	protein_peptideDF = getDataFrame(repInfo['protein-peptide infile'])
	proteinDF = getDataFrame(repInfo['protein infile'])

	# Gets conc/temp Start and End header index, by method of finding first header cell with an integer
	conc_tempStartIndex = -1  # initialized for easy debugging
	# noinspection PyUnusedLocal
	conc_tempEndIndex = -1  # initialized for easy debugging
	headers = ['-10lgP','m/z','RT','Fraction','scan','Source File','#Feature']
	for header in headers:
		try: #remove columns that can break CHalf if they are present
			del protein_peptideDF[header]
		except:
			pass
	try:
		del proteinDF['-10lgP']
	except:
		None
	for headerName in protein_peptideDF:
		while conc_tempStartIndex == -1:  # stop looping once conc/temp StartIndex is found
			if 'Unnamed' not in headerName:  # empty cells have "Unnamed = 0", we want to ingore these...
				for character in str(headerName):
					if character.isdigit():  # Checks characters in header name, if number is found, that is our start
						#print(headerName)
						conc_tempStartIndex = protein_peptideDF.columns.get_loc(
							headerName)  # assigns header index location
						break  # Once start is found, we can stop looping
			break
	conc_tempEndIndex = conc_tempStartIndex + len(repInfo['conc-temp list'])  # End is Start plus # of Conc/Temp values

	''' Create new rep_combinedDF with combined info from protein_peptideDF and proteinDF '''
	# Get desired columns from protein-peptides.csv
	repCombinedInfileDF = protein_peptideDF[['Protein Accession', 'Peptide', 'Start', 'End']]
	# rename 'Protein Accession' to 'Accession' for ease of use/reading
	repCombinedInfileDF.rename(columns={'Protein Accession': 'Accession'}, inplace=True)
	# Create combined Accession@Peptide column. For use with combining multiple rep data later in cond_filecombine
	#     Ex: P04004|VTNC_HUMAN@R.FEDGVLDPDY(+125.90)PR.N
	repCombinedInfileDF['Accession@Peptide'] = repCombinedInfileDF['Accession'] + "@" + repCombinedInfileDF['Peptide']

	# Adds 'Description' from protein.csv where 'Accession' matches
	repCombinedInfileDF = pd.merge(repCombinedInfileDF, proteinDF[['Accession', 'Description']], how='left',
								   on='Accession')

	# Add '#Non_Zero' header...
	repCombinedInfileDF['#Non_Zero'] = 0

	# Setting the order of data
	repCombinedInfileDF = repCombinedInfileDF[
		['Accession@Peptide', 'Accession', 'Description', 'Peptide', 'Start', 'End', '#Non_Zero']]

	# Add Conc/Temp Data (w/old headers)
	repCombinedInfileDF = pd.concat(
		[repCombinedInfileDF, protein_peptideDF.iloc[:, conc_tempStartIndex:conc_tempEndIndex]], axis=1)

	# Get combined's indices for start and end of conc/temp values.
	combined_CT_EndIndex = repCombinedInfileDF.shape[1] - 1  # Sets end as last index in dataframe
	combined_CT_StartIndex = combined_CT_EndIndex - len(repInfo['conc-temp list']) + 1

	# Add '#Non_Zero' data...
	'''for index, row in repCombinedInfileDF.iterrows():
		nonZeroCount = 0
		for cell in row[combined_CT_StartIndex:combined_CT_EndIndex + 1]:
			if float(cell) != 0:
				nonZeroCount += 1
		repCombinedInfileDF.at[index, '#Non_Zero'] = nonZeroCount'''
	tqdm.pandas(desc=repInfo['condition'] + ' Rep Combination')
	repCombinedInfileDF = repCombinedInfileDF.progress_apply(non_zero_apply,axis=1,combined_CT_StartIndex=combined_CT_StartIndex,combined_CT_EndIndex=combined_CT_EndIndex)

	# Rename Conc/Temp Headers
	conc_tempHeaderList = []
	for x in repInfo['conc-temp list']:  # Make list of strings for headers for conc/temp
		conc_tempHeaderList.append(str(x))

	# Gets list of headers up until start of conc/temp data, then adds updated c/t headers and assigns this new list as the headers
	repCombinedInfileDF.columns = repCombinedInfileDF.columns[:combined_CT_StartIndex].tolist() + conc_tempHeaderList

	# Add repCombined InfileName and DataFrame to repInfo for later reference/use
	repInfo['ct start index'] = combined_CT_StartIndex
	repInfo['ct end index'] = combined_CT_EndIndex
	#print(repInfo)
	repCombinedInfileDF['Range/Mean'] = 0

	return repCombinedInfileDF

#POSSIBLE getMinMax methods
''' These are methods to use to get max and min values.  We always use the first one, absolute max/min '''
def getMinMax_Absolute(list):
	# NOTE: This uses absolute min and max values of data set to choose Normalize data value...
	minNum = min(list)
	maxNum = max(list)
	return minNum, maxNum

def getMinMax_AbsoluteNoneZero(list):
	# NOTE: This uses absolute min and max values of data set to choose Normalize data value...
	nonZlist = []
	for num in list:
		if float(num) != 0:
			nonZlist.append(num)
	minNum = min(nonZlist)
	maxNum = max(nonZlist)
	return minNum, maxNum

def getMinMax_FirstLast(list):
	# NOTE: Gets min/max as first and last data points in CT data...
	minNum = list[0]
	maxNum = list[-1]
	if minNum > maxNum:
		temp = 0
		temp = minNum
		minNum = maxNum
		maxNum = temp

	return minNum, maxNum

def getMinMax_FirstLastNoneZero(list):
	# NOTE: Gets min/max as first and last data points that aren't 0 in CT data...
	minNum = 0
	maxNum = 0
	for num in list:
		if float(num) != 0:
			minNum = num
			break
	for num in reversed(list):
		if float(num) != 0:
			maxNum = num
			break
	if minNum > maxNum:
		temp = 0
		temp = minNum
		minNum = maxNum
		maxNum = temp
	return minNum, maxNum

# test lines...
# list = [5, 4, 3, 2, 1]
# mn, mx = getMinMax_FirstLast(list)
# print(f"MINMAX TEST:\nMin:{mn}\tMax:{mx}")
""" ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ """

def normalize_data(repDF, repInfo):
			''' takes data and normalizes values to between 0 and 1 '''

			#print(f"IN NORMALIZE_DATA: {repInfo['condition']} Rep{repInfo['repNum']}")
			CTstart = repInfo['ct start index']
			CTend   = repInfo['ct end index']

			# Set up headers for Normalized Data [ex: '2.41_Norm' ]
			repDF['Delta 6-0'] = 0
			norm_header_list = []
			for head in repInfo['conc-temp list']:
				repDF[str(head)+"_Norm"] = 0  # Adds '###_Norm' header for each conc/temp value and initializes row values to 0
				norm_header_list.append(str(head) + "_Norm")

			for rowIndex in range(0, repDF.shape[0]):
				#print(f"normalize: {repInfo['condition']} Rep{repInfo['repNum']}, row {rowIndex}")
				# gets list of raw data for each row
				numList = repDF.iloc[rowIndex, CTstart:CTend+1].values.tolist()

				# gets min / max value of raw data... ### Multiple options here, pending on how we want to do this...
				minCT, maxCT = getMinMax_Absolute(numList)
				norm_denominator = maxCT - minCT
				repDF.loc[repDF.index[rowIndex], 'Delta 6-0'] = norm_denominator

				normList = []
				for num in numList:
					if norm_denominator != 0:
						num = (num - minCT) / norm_denominator
					else: num = 0  # should only happen if all values are 0, pending min/max method
					normList.append(num)
				repDF.loc[repDF.index[rowIndex], str(repInfo['conc-temp list'][0])+"_Norm" : str(repInfo['conc-temp list'][-1])+"_Norm"] = normList

			repNormFilename = str(repInfo['condition']) + '_Rep' + str(int(repInfo['repNum'])) + '_Norm.csv'
			#print(f"Rep{repInfo['repNum']} Norm Headers: {norm_header_list}")
			repInfo['norm ct headers'] = norm_header_list
			repInfo['norm filename'] = repNormFilename
			# repDF.to_csv(repNormFilename)

def sigmoid(x, B, A, Chalf, b):
			""" Fitting Equation
			- Fits data to sigmoid curve.
			- Returns y
			"""
			y = B + ((A - B) / (1 + np.exp((-1 / b) * (Chalf - x))))		### ORIGINAL CHalf Program
			# y = A + ((B - A) / (1 + np.exp(-Chalf - x / b)))		### Copying paper...

			return y

#Functions to be applied for in place of iterating

def non_zero_apply(row,combined_CT_StartIndex,combined_CT_EndIndex):
	nonZeroCount = (row[combined_CT_StartIndex:combined_CT_EndIndex + 1] != 0).sum()
	row['#Non_Zero'] = nonZeroCount
	return row

def denormalize(y,maxVal,minVal):
	x = ((maxVal - minVal)*y)+minVal
	return x

def normalize(x,maxVal,minVal):
	y = (x-minVal)/(maxVal - minVal)
	return y

def normalize_data_apply(row, repInfo, CTstart, CTend):
	rowIndex = row.name
	#print(f"normalize: {repInfo['condition']} Rep{repInfo['repNum']}, row {rowIndex}")
	# gets list of raw data for each row
	numList = row[CTstart:CTend + 1].values.tolist()

	# gets min / max value of raw data... ### Multiple options here, pending on how we want to do this...
	minCT, maxCT = getMinMax_Absolute(numList)
	norm_denominator = maxCT - minCT
	row['Delta 6-0'] = norm_denominator
	try:
		row['Range/Mean'] = norm_denominator/(sum(numList)/len(numList))
	except:
		row['Range/Mean'] = np.nan

	normList = []
	for num in numList:
		if norm_denominator != 0:
			num = (num - minCT) / norm_denominator
		else:
			num = 0  # should only happen if all values are 0, pending min/max method
		normList.append(num)
	row[str(repInfo['conc-temp list'][0]) + "_Norm": str(repInfo['conc-temp list'][-1]) + "_Norm"] = normList
	return row

def normalize_data(repDF, repInfo):
	""" takes data and normalizes values to between 0 and 1 """

	#print(f"IN NORMALIZE_DATA: {repInfo['condition']} Rep{repInfo['repNum']}")
	CTstart = repInfo['ct start index']
	CTend = repInfo['ct end index']

	# Set up headers for Normalized Data [ex: '2.41_Norm' ]
	repDF['Delta 6-0'] = 0
	norm_header_list = []
	for head in repInfo['conc-temp list']:
		repDF[
			str(head) + "_Norm"] = 0  # Adds '###_Norm' header for each conc/temp value and initializes row values to 0
		norm_header_list.append(str(head) + "_Norm")

	tqdm.pandas(desc=repInfo['condition'] + ' Rep Normalization')
	repDF = repDF.progress_apply(normalize_data_apply, axis=1, repInfo=repInfo, CTstart=CTstart, CTend=CTend)
	repNormFilename = str(repInfo['condition']) + '_Rep' + str(int(repInfo['repNum'])) + '_Norm.csv'
	#print(f"Rep{repInfo['repNum']} Norm Headers: {norm_header_list}")
	repInfo['norm ct headers'] = norm_header_list
	repInfo['norm filename'] = repNormFilename
	return repDF, repInfo

def seperate_rep_analysis_apply(sCurveDF, repDF, repInfo, MINIMUM_PTS, OUTLIER_CUTOFF):
	x = sCurveDF.name
	row = repDF.loc[x]
	row_t = row[repInfo['norm ct headers']]
	# print(f"rep_analysis: {repInfo['condition']} Rep{repInfo['repNum']}, row {row_t.name+1}")
	if row['#Non_Zero'] >= MINIMUM_PTS:
		normDataList = row_t.values.tolist()
		""" fit_scurve calculations """
		# print(f"Reps \tRow: {row.name}\nx:{repInfo['conc-temp list']}\ny:{normDataList}")
		try:
			popt, pcov = curve_fit(sigmoid, repInfo['conc-temp list'], normDataList, maxfev=100000)
			# ,p0=[.5, .5, .5, .2]  # maxfev is number of fit tries, 1000 being standard; p0=[0, 0.5, 2, 0.2]
			stdError = np.sqrt(np.diag(pcov))  # stdError[ B-error, A-error, CHalf-error, b-error]
			B_stderror, A_stderror, CHalf_stderror, b_stderror = stdError[:]

			numPoints = float(len(repInfo['conc-temp list']))  # This is number of data points used to estimate curve
			fitCurve_B, fitCurve_A, CHalf, fitCurve_b = popt[:]
			if fitCurve_B > fitCurve_A:
				slope = 'Positive'
			else:
				slope = 'Negative'

			CHalf_ConfidenceInterval = t.ppf(.975, (numPoints - 1)) * CHalf_stderror / np.sqrt(
				numPoints)  ### Figure out where this .975 comes from... and whatever this line means and is doing...
			CHalf_confidenceInterval_lowBound = CHalf - CHalf_ConfidenceInterval
			CHalf_confidenceInterval_upBound = CHalf + CHalf_ConfidenceInterval

			b_confidenceInterval = t.ppf(.975, (numPoints - 1)) * b_stderror / np.sqrt(numPoints)
			b_confidenceInterval_lowBound = fitCurve_b - b_confidenceInterval
			b_confidenceInterval_upBound = fitCurve_b + b_confidenceInterval


			''' NOTE: This if/else block of code deals with negative vs. positive slope. A and B change on the
				y-axis, while CHalf changes on the x-axis. So we need to switch the sign on CHalf to get the correct
				confidence interval variables for a confidence interval curve. '''
			if fitCurve_B <= fitCurve_A:
				popt_lowBound = [fitCurve_B - (OUTLIER_CUTOFF * B_stderror),
								 fitCurve_A - (OUTLIER_CUTOFF * A_stderror),
								 CHalf - (OUTLIER_CUTOFF * CHalf_stderror),
								 fitCurve_b]
				popt_upBound = [fitCurve_B + (OUTLIER_CUTOFF * B_stderror),
								fitCurve_A + (OUTLIER_CUTOFF * A_stderror),
								CHalf + (OUTLIER_CUTOFF * CHalf_stderror),
								fitCurve_b]
			else:
				popt_lowBound = [fitCurve_B + (OUTLIER_CUTOFF * B_stderror),
								 fitCurve_A + (OUTLIER_CUTOFF * A_stderror),
								 CHalf - (OUTLIER_CUTOFF * CHalf_stderror),
								 fitCurve_b]
				popt_upBound = [fitCurve_B - (OUTLIER_CUTOFF * B_stderror),
								fitCurve_A - (OUTLIER_CUTOFF * A_stderror),
								CHalf + (OUTLIER_CUTOFF * CHalf_stderror),
								fitCurve_b]

			# print(f"conc-temp: {repInfo['conc-temp list']}") #Test print
			ctList = repInfo['conc-temp list']
			concRange = max(ctList) - min(ctList)
			ratioTOrange = CHalf_ConfidenceInterval / concRange

			sCurve_xValues = np.linspace(min(ctList) - (concRange / 20), max(ctList) + (concRange / 20), 50)
			# 50 points in conc/temp range (with small 1/20 margin on each side); determines resolution of graph
			sCurve_yValues = sigmoid(sCurve_xValues, *popt)  # assigns yValues according to sigmoid curve at xValues

			""" r_squared calculations """
			residuals = normDataList - sigmoid(repInfo['conc-temp list'], *popt)
			ss_res = np.sum(residuals ** 2)
			ss_tot = np.sum(normDataList - np.mean(normDataList) ** 2)
			r_squared = 1 - (ss_res / ss_tot)
			CHalf_normalized = CHalf / concRange

			# Note: popt contains following in list: popt[B, A, CHalf, b]
			sCurveDF['numPoints'] = numPoints
			sCurveDF['popt'] = popt
			sCurveDF['popt_lowBound'] = popt_lowBound
			sCurveDF['popt_upBound'] = popt_upBound
			sCurveDF['pcov'] = pcov
			sCurveDF['sCurve_xValues'] = sCurve_xValues
			sCurveDF['sCurve_yValues'] = sCurve_yValues
			sCurveDF['B_stderror'] = B_stderror
			sCurveDF['A_stderror'] = A_stderror
			sCurveDF['CHalf_stderror'] = CHalf_stderror
			sCurveDF['b_stderror'] = b_stderror
			sCurveDF['CHalf_ConfidenceInterval'] = CHalf_ConfidenceInterval
			sCurveDF['concRange'] = concRange
			sCurveDF['ratioTOrange'] = ratioTOrange
			sCurveDF['fitCurve_B'] = fitCurve_B
			sCurveDF['fitCurve_A'] = fitCurve_A
			sCurveDF['CHalf'] = CHalf
			sCurveDF['fitCurve_b'] = fitCurve_b
			sCurveDF['slope'] = slope
			sCurveDF['CHalf_confidenceInterval_lowBound'] = CHalf_confidenceInterval_lowBound
			sCurveDF['CHalf_confidenceInterval_upBound'] = CHalf_confidenceInterval_upBound
			sCurveDF['b_confidenceInterval'] = b_confidenceInterval
			sCurveDF['b_confidenceInterval_lowBound'] = b_confidenceInterval_lowBound
			sCurveDF['b_confidenceInterval_upBound'] = b_confidenceInterval_upBound
			sCurveDF['residuals'] = residuals
			sCurveDF['ss_res'] = ss_res
			sCurveDF['ss_tot'] = ss_tot
			sCurveDF['r_squared'] = r_squared
			sCurveDF['CHalf_normalized'] = CHalf_normalized

			#print(f"Accession@Protein:{row['Accession@Peptide']}\n\tCHalf:{CHalf}\n\tB:{fitCurve_B}\n\tA:{fitCurve_A}\n\tb:{fitCurve_b}")

		except RuntimeError:
			#print(f"ERROR, Row{row_t.name}:  Could not find fit...")
			sCurveDF[['popt','popt_lowBound','popt_upBound','pcov','sCurve_xValues','sCurve_yValues','B_stderror','A_stderror','CHalf_stderror','b_stderror','CHalf_ConfidenceInterval','concRange','ratioTOrange','fitCurve_B','fitCurve_A','CHalf','fitCurve_b','slope','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound','b_confidenceInterval','b_confidenceInterval_lowBound','b_confidenceInterval_upBound','residuals','ss_res','ss_tot','r_squared','CHalf_normalized']] = "no fit found"
	else:
		sCurveDF[['popt','popt_lowBound','popt_upBound','pcov','sCurve_xValues','sCurve_yValues','B_stderror','A_stderror','CHalf_stderror','b_stderror','CHalf_ConfidenceInterval','concRange','ratioTOrange','fitCurve_B','fitCurve_A','CHalf','fitCurve_b','slope','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound','b_confidenceInterval','b_confidenceInterval_lowBound','b_confidenceInterval_upBound','residuals','ss_res','ss_tot','r_squared','CHalf_normalized']] = "insufficient data"   # IF less than 4 data points... Program has difficulty calculating curve with so few points
	return sCurveDF

def denormalize_apply(row,repInfo,columns,other): #denormalizes heat data for export and plotting
	for header in columns:
		if type(row[header]) != str:
			row[header] = (row[header]*(max(repInfo['original-temp list'])-min(repInfo['original-temp list'])))+min(repInfo['original-temp list'])
	for header in other:
		if type(row[header]) != str:
			row[header] = row[header]*(max(repInfo['original-temp list'])-min(repInfo['original-temp list']))
	return row

def makegraph_reps_apply(row, repInfo, file_type, OUTLIER_CUTOFF):
	""" plot_color """
	x = row.name
	CHalf_temp = row['CHalf']
	range_temp = repInfo['conc-temp list'][-1] - repInfo['conc-temp list'][0]
	if (row=='insufficient data').sum()==0 and (row=='no fit found').sum()==0:
		if repInfo['conc-temp list'][0] - (2 * range_temp) < CHalf_temp < repInfo['conc-temp list'][-1] + (2 * range_temp) and row['CHalf_ConfidenceInterval'] < row['concRange'] / 2:
			if repInfo['CD or HD'] == 'HD':
				xheaderlist = repInfo['original-temp list']
				if type(row['sCurve_xValues']) != str:
					row['sCurve_xValues'] = denormalize(row['sCurve_xValues'],max(repInfo['original-temp list']),min(repInfo['original-temp list']))
			else:
				xheaderlist = repInfo['conc-temp list']
			ydatalist = row[repInfo['norm ct headers']].values.tolist()
			# print(f"x:{xheaderlist}\ny:{ydatalist}")
	
			# Plot real data
			plt.plot(xheaderlist, ydatalist, color='b', ls=':', marker='o', label="Original Data")
			# EXAMPLES: plt.plot(xheaderlist, ydatalist, color='b', ls=':', marker='o', label=repInfo['condition'])
			# EXAMPLES: plt.plot(xheaderlist, ydatalist, 'b:' , marker='.', linewidth=3 label=repInfo['condition'])
			# plt.xticks(np.arange(len(xheaderlist)), (repInfo['conc-temp list']))
	
			# Plot fitted Curve
			# print(f"x:{repInfo['sCurve data dict'][x]['sCurve_xValues']}\ny:{repInfo['sCurve data dict'][x]['sCurve_yValues']}")
		   
			plt.plot(row['sCurve_xValues'], row['sCurve_yValues'],
					 color='k', marker=',', ls='-', label='Fitted Curve')
			
			if repInfo['CD or HD'] == 'HD':
				# Plot lowBound Curve
				sCurve_yValues_lowBound = sigmoid(normalize(row['sCurve_xValues'],max(repInfo['original-temp list']),min(repInfo['original-temp list'])),
												  *row['popt_lowBound'])
				plt.plot(row['sCurve_xValues'], sCurve_yValues_lowBound,
						 color='m', marker=',', ls='-.', label=f"Standard Error (x{OUTLIER_CUTOFF})")
		
				# Plot upBound Curve
				sCurve_yValues_upBound = sigmoid(normalize(row['sCurve_xValues'],max(repInfo['original-temp list']),min(repInfo['original-temp list'])),
												 *row['popt_upBound'])
				plt.plot(row['sCurve_xValues'], sCurve_yValues_upBound,
						 color='m', marker=',', ls='-.')
			else:
				# Plot lowBound Curve
				sCurve_yValues_lowBound = sigmoid(row['sCurve_xValues'],
												  *row['popt_lowBound'])
				plt.plot(row['sCurve_xValues'], sCurve_yValues_lowBound,
						 color='m', marker=',', ls='-.', label=f"Standard Error (x{OUTLIER_CUTOFF})")
		
				# Plot upBound Curve
				sCurve_yValues_upBound = sigmoid(row['sCurve_xValues'],
												 *row['popt_upBound'])
				plt.plot(row['sCurve_xValues'], sCurve_yValues_upBound,
						 color='m', marker=',', ls='-.')
	
			# Plot CHalf line
			if repInfo['CD or HD'] == 'HD' and type(row['CHalf']) != str:
				row['CHalf'] = denormalize(row['CHalf'],max(repInfo['original-temp list']),min(repInfo['original-temp list']))
			CHalf_temp = row['CHalf']
			if repInfo['CD or HD'] == 'HD':
				range_temp = max(repInfo['original-temp list']) - min(repInfo['original-temp list'])
			else:
				range_temp = repInfo['conc-temp list'][-1] - repInfo['conc-temp list'][0]
	
			# plots CHalf is it is within two range spans from lowest conc value and highest conc value  (prevents CHalf lines way out of scope of graphed points)
			is_CHalf_plot = False
			if repInfo['CD or HD'] == 'HD':
				if min(repInfo['original-temp list']) - (2 * range_temp) < CHalf_temp < max(repInfo['conc-temp list']) + (
						2 * range_temp):
					plt.axvline(CHalf_temp, color='k', ls='-.', label='CHalf')
					is_CHalf_plot = True
			else:
				if repInfo['conc-temp list'][0] - (2 * range_temp) < CHalf_temp < repInfo['conc-temp list'][-1] + (
						2 * range_temp):
					plt.axvline(CHalf_temp, color='k', ls='-.', label='CHalf')
					is_CHalf_plot = True
	
			# Plot CHalf Confidence Interval span
			# checks if CHalf confidence interval is reasonable.  (prevents spans that go way outside graphed points))
			is_CHalf_CI_plot = False
			if repInfo['CD or HD'] == 'HD' and type(row['CHalf_ConfidenceInterval']) != str and type(row['concRange']) != str:
				row['CHalf_ConfidenceInterval'] = row['CHalf_ConfidenceInterval']*(max(repInfo['original-temp list'])-min(repInfo['original-temp list']))
				row['concRange'] = max(repInfo['original-temp list']) - min(repInfo['original-temp list'])
			if row['CHalf_ConfidenceInterval'] < row['concRange'] / 2:
				plt.axvspan(CHalf_temp - row['CHalf_ConfidenceInterval'],
							CHalf_temp + row['CHalf_ConfidenceInterval'],
							color='#d5d5d5', label='CHalf Confidence Interval', zorder=0)
				is_CHalf_CI_plot = True
	
			# print(plt.style.available)  #['Solarize_Light2', '_classic_test_patch', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark', 'seaborn-dark-palette', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'tableau-colorblind10']
			plt.style.use('seaborn-deep')
			if repInfo['CD or HD'] == 'HD':
				plt.xlabel('Temperature Values')
			else:
				plt.xlabel('Concentration Values')
			plt.ylabel('Amount of Protein Present\n(Normalized)')
			plt.title(f"{repInfo['condition']}: Rep{repInfo['repNum']}  Line:{x}\n{row['Accession@Peptide']}"
					  f"\nLine Fit r^2 = {row['r_squared']}")
			plt.grid(True)
			# plt.legend()
			lgd = plt.legend(loc=9, bbox_to_anchor=(1.32, .85))  # ([right],[up])
			#print(f"Graph {repInfo['condition']}, Rep{repInfo['repNum']}, Line:{x}")

		# EXPORT GRAPH TO FILES
		# if there is a valid CHalf and CHalf confidence interval on plot, export plot
			if is_CHalf_plot and is_CHalf_CI_plot:
				a_p_filefriendly = 'index==' + str(x)
				figure_filename = f"Graph Outputs/{repInfo['condition']}_Rep{repInfo['repNum']}=={a_p_filefriendly}==Graph" + file_type
				plt.savefig(figure_filename, bbox_extra_artists=(lgd,), bbox_inches='tight')
	plt.clf()  # clearfig, start a new piece, make sure do it before or after a set of instruction

def combined_fit_apply(row,con_conctemp_labeledheaders,con_conctemp_headers,MINIMUM_PTS,removeOutlier_2xStdErr,condition,OUTLIER_CUTOFF):
		''' Count Number of Points and Non-Zero, per line'''
		numPoints = (row[con_conctemp_labeledheaders[0]:con_conctemp_labeledheaders[-1]].notna()).sum()
		numNonZero = (row[con_conctemp_labeledheaders[0]:con_conctemp_labeledheaders[-1]][row[con_conctemp_labeledheaders[0]:con_conctemp_labeledheaders[-1]].notna()] != 0).sum()
		row['#pts'] = numPoints
		row['#non Zero'] = numNonZero
		'''----------------------------------------------'''
		valid_yValues = row[con_conctemp_labeledheaders[0]:con_conctemp_labeledheaders[-1]][row[con_conctemp_labeledheaders[0]:con_conctemp_labeledheaders[-1]].notna()].tolist()
		valid_xValues = list(np.array(con_conctemp_headers)[(row[con_conctemp_labeledheaders[0]:con_conctemp_labeledheaders[-1]].notna())])
		row['valid_xValues'] = valid_xValues
		row['valid_yValues'] = valid_yValues
		row['ydata'] = row[con_conctemp_labeledheaders].tolist()
		if row['#non Zero']>= MINIMUM_PTS:	### THIS CHECK IS WORKING, BUT OLD VALUES FOR sCurveData carry over to the next line when this filter prevents new calculations.
			#print(f"cond_analysis: {condition}, row {row.name+1}")
			try:
				popt, pcov = curve_fit(sigmoid, row['valid_xValues'], row['valid_yValues'], maxfev=100000)  # , p0=[.5, .5, .5, .2]
				# maxfev is number of fit tries, 1000 being standard; p0=[0, 0.5, 2, 0.2]
				stdError = np.sqrt(np.diag(pcov))  # stdError[ B-error, A-error, CHalf-error, b-error]
				B_stderror, A_stderror, CHalf_stderror, b_stderror = stdError[:]
	
				fitCurve_B, fitCurve_A, CHalf, fitCurve_b = popt[:]
				if fitCurve_B > fitCurve_A:
					slope = 'Positive'
				else: slope = 'Negative'
				numPoints = row['#pts']
				CHalf_ConfidenceInterval = t.ppf(.975, (numPoints - 1)) * CHalf_stderror / np.sqrt(
						numPoints)  ### Figure out where this .975 comes from... and whatever this line means and is doing...
				CHalf_confidenceInterval_lowBound = CHalf - CHalf_ConfidenceInterval
				CHalf_confidenceInterval_upBound = CHalf + CHalf_ConfidenceInterval
	
				b_confidenceInterval = t.ppf(.975, (numPoints - 1)) * b_stderror / np.sqrt(numPoints)
				b_confidenceInterval_lowBound = fitCurve_b - b_confidenceInterval
				b_confidenceInterval_upBound = fitCurve_b + b_confidenceInterval
	
				''' NOTE: This if/else block of code deals with negative vs. positive slope. A and B change on the
					y-axis, while CHalf changes on the x-axis. So we need to switch the sign on CHalf to get the correct
					confidence interval variables for a confidence interval curve. '''
				if fitCurve_B <= fitCurve_A:
					popt_lowBound = [fitCurve_B - (OUTLIER_CUTOFF * B_stderror),
										 fitCurve_A - (OUTLIER_CUTOFF * A_stderror),
										 CHalf - (OUTLIER_CUTOFF * CHalf_stderror),
										 fitCurve_b]
					popt_upBound = [fitCurve_B + (OUTLIER_CUTOFF * B_stderror),
										fitCurve_A + (OUTLIER_CUTOFF * A_stderror),
										CHalf + (OUTLIER_CUTOFF * CHalf_stderror),
										fitCurve_b]
				else:
					popt_lowBound = [fitCurve_B + (OUTLIER_CUTOFF * B_stderror),
										 fitCurve_A + (OUTLIER_CUTOFF * A_stderror),
										 CHalf - (OUTLIER_CUTOFF * CHalf_stderror),
										 fitCurve_b]
					popt_upBound = [fitCurve_B - (OUTLIER_CUTOFF * B_stderror),
										fitCurve_A - (OUTLIER_CUTOFF * A_stderror),
										CHalf + (OUTLIER_CUTOFF * CHalf_stderror),
										fitCurve_b]
	
				valid_xValues = row['valid_xValues']
				concRange = max(valid_xValues) - min(valid_xValues)
				ratioTOrange = CHalf_ConfidenceInterval / concRange
	
				sCurve_xValues = np.linspace(min(valid_xValues)-(concRange/20), max(valid_xValues)+(concRange/20), 50)
				# 50 points in conc/temp range (with small 1/20 margin on each side); determines resolution of graph
				sCurve_yValues = sigmoid(sCurve_xValues, *popt)  # assigns yValues according to sigmoid curve at xValues
	
				row['sCurve_xValues'] = sCurve_xValues
				row['sCurve_yValues'] = sCurve_yValues
	
				
				""" r_squared calculations """
				valid_yValues = row['valid_yValues']
				residuals = valid_yValues - sigmoid(valid_xValues, *popt)
				ss_res = np.sum(residuals ** 2)
				ss_tot = np.sum(valid_yValues - np.mean(valid_yValues) ** 2)
				r_squared = 1 - (ss_res / ss_tot)
				CHalf_normalized = CHalf / concRange
	
				# Note: popt contains following in list: popt[B, A, CHalf, b]
				row['enough_points'] = True
				row['popt'] = popt
				row['popt_lowBound'] = popt_lowBound
				row['popt_upBound'] = popt_upBound
				row['pcov'] = pcov
				row['sCurve_xValues'] = sCurve_xValues
				row['sCurve_yValues'] = sCurve_yValues
				row['B_stderror'] = B_stderror
				row['A_stderror'] = A_stderror
				row['CHalf_stderror'] = CHalf_stderror
				row['b_stderror'] = b_stderror
				row['CHalf_ConfidenceInterval'] = CHalf_ConfidenceInterval
				row['concRange'] = concRange
				row['ratioTOrange'] = ratioTOrange
				row['fitCurve_B'] = fitCurve_B
				row['fitCurve_A'] = fitCurve_A
				row['CHalf'] = CHalf
				row['fitCurve_b'] = fitCurve_b
				row['slope'] = slope
				row['CHalf_confidenceInterval_lowBound'] = CHalf_confidenceInterval_lowBound
				row['CHalf_confidenceInterval_upBound'] = CHalf_confidenceInterval_upBound
				row['b_confidenceInterval'] = b_confidenceInterval
				row['b_confidenceInterval_lowBound'] = b_confidenceInterval_lowBound
				row['b_confidenceInterval_upBound'] = b_confidenceInterval_upBound
				row['residuals'] = residuals
				row['ss_res'] = ss_res
				row['ss_tot'] = ss_tot
				row['r_squared'] = r_squared
				row['CHalf_normalized'] = CHalf_normalized
			except RuntimeError:
				print(f"ERROR, Row{row.name}:  Could not find fit...")
				row['enough_points'] = False
				print ("here, ", row.name)
		else:
			row['enough_points'] = False


		""" REMOVING OUTLIERS AND PERFORMING TRIMMED DATA CURVE FIT """
		if removeOutlier_2xStdErr == True:
			if row['enough_points'] == False:
				row['trim_VALID'] = False
				#print ("there, ", row.name)
				row[['slope','fitCurve_B','fitCurve_A','CHalf','fitCurve_b','B_stderror','A_stderror','CHalf_stderror','b_stderror','CHalf_ConfidenceInterval','ratioTOrange','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound','b_confidenceInterval','b_confidenceInterval_lowBound','b_confidenceInterval_upBound','r_squared','CHalf_normalized']]=0
				row['trim_#pts'] = np.nan
				row['trim_slope'] = np.nan
				row['trim_B'] = np.nan
				row['trim_A'] = np.nan
				row['trim_CHalf'] = np.nan
				row['trim_b'] = np.nan
				row['trim_B_stderror'] = np.nan
				row['trim_A_stderror'] = np.nan
				row['trim_CHalf_stderror'] = np.nan
				row['trim_b_stderror'] = np.nan
				row['trim_CHalf_ConfidenceInterval'] = np.nan
				row['trim_ratioTOrange'] = np.nan
				row['trim_CHalf_confidenceInterval_lowBound'] = np.nan
				row['trim_CHalf_confidenceInterval_upBound'] = np.nan
				row['trim_b_confidenceInterval'] = np.nan
				row['trim_b_confidenceInterval_lowBound'] = np.nan
				row['trim_b_confidenceInterval_upBound'] = np.nan
				row['trim_r_squared'] = np.nan
				row[ 'trim_CHalf_normalized'] = np.nan
				return row
			# print(f"trim-calculations: Row {index}")
				# Get trimmed values by checking if within 2 Confidence Intervals of B, A, and CHalf
			trim_yValues = []
			trim_xValues = []
			count = 0
			for ydata in row['ydata']:
				# popt up / low bound are B,A,b,CHalf with B,A, and CHalf two confidence intervals up or down
				if (row['fitCurve_B'] <= row['fitCurve_A']):
					if (ydata > sigmoid(con_conctemp_headers[count], *row['popt_lowBound'])) and (
							ydata < sigmoid(con_conctemp_headers[count], *row['popt_upBound'])):
						trim_yValues.append(ydata)
						trim_xValues.append(con_conctemp_headers[count])
	
				else:
					if (ydata < sigmoid(con_conctemp_headers[count], *row['popt_lowBound'])) and (
									ydata > sigmoid(con_conctemp_headers[count], *row['popt_upBound'])):
						trim_yValues.append(ydata)
						trim_xValues.append(con_conctemp_headers[count])
				count += 1
			trim_numPoints = len(trim_yValues)
	
			if trim_numPoints <= MINIMUM_PTS:  # CHECK for number of data points.
				row['trim_VALID'] = False
				row[['slope','fitCurve_B','fitCurve_A','CHalf','fitCurve_b','B_stderror','A_stderror','CHalf_stderror','b_stderror','CHalf_ConfidenceInterval','ratioTOrange','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound','b_confidenceInterval','b_confidenceInterval_lowBound','b_confidenceInterval_upBound','r_squared','CHalf_normalized']]=0
				row['trim_#pts'] = np.nan
				row['trim_slope'] = np.nan
				row['trim_B'] = np.nan
				row['trim_A'] = np.nan
				row['trim_CHalf'] = np.nan
				row['trim_b'] = np.nan
				row['trim_B_stderror'] = np.nan
				row['trim_A_stderror'] = np.nan
				row['trim_CHalf_stderror'] = np.nan
				row['trim_b_stderror'] = np.nan
				row['trim_CHalf_ConfidenceInterval'] = np.nan
				row['trim_ratioTOrange'] = np.nan
				row['trim_CHalf_confidenceInterval_lowBound'] = np.nan
				row['trim_CHalf_confidenceInterval_upBound'] = np.nan
				row['trim_b_confidenceInterval'] = np.nan
				row['trim_b_confidenceInterval_lowBound'] = np.nan
				row['trim_b_confidenceInterval_upBound'] = np.nan
				row['trim_r_squared'] = np.nan
				row[ 'trim_CHalf_normalized'] = np.nan
				return row
	
	
			try:
				trim_popt, trim_pcov = curve_fit(sigmoid, trim_xValues, trim_yValues,
												 maxfev=100000)  # , p0=[.5, .5, .5, .2]
				# maxfev is number of fit tries, 1000 being standard; p0=[0, 0.5, 2, 0.2]
				# print(f"len(trim_x):{len(trim_xValues)}\nlen(trim_y):{len(trim_yValues)}")
				# print(f"trim_popt:\n{trim_popt}\ntrim_pcov:\n{trim_pcov}")
			except RuntimeError:
				#print(f"ERROR, Row{row.name}:  Could not find fit...")
				row['trim_VALID'] = False
				#print ("anywhere, ", row.name)
				row[['slope','fitCurve_B','fitCurve_A','CHalf','fitCurve_b','B_stderror','A_stderror','CHalf_stderror','b_stderror','CHalf_ConfidenceInterval','ratioTOrange','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound','b_confidenceInterval','b_confidenceInterval_lowBound','b_confidenceInterval_upBound','r_squared','CHalf_normalized']]=0
				row['trim_#pts'] = np.nan
				row['trim_slope'] = np.nan
				row['trim_B'] = np.nan
				row['trim_A'] = np.nan
				row['trim_CHalf'] = np.nan
				row['trim_b'] = np.nan
				row['trim_B_stderror'] = np.nan
				row['trim_A_stderror'] = np.nan
				row['trim_CHalf_stderror'] = np.nan
				row['trim_b_stderror'] = np.nan
				row['trim_CHalf_ConfidenceInterval'] = np.nan
				row['trim_ratioTOrange'] = np.nan
				row['trim_CHalf_confidenceInterval_lowBound'] = np.nan
				row['trim_CHalf_confidenceInterval_upBound'] = np.nan
				row['trim_b_confidenceInterval'] = np.nan
				row['trim_b_confidenceInterval_lowBound'] = np.nan
				row['trim_b_confidenceInterval_upBound'] = np.nan
				row['trim_r_squared'] = np.nan
				row[ 'trim_CHalf_normalized'] = np.nan
				return row
	
			trim_popt, trim_pcov = curve_fit(sigmoid, trim_xValues, trim_yValues, maxfev=100000)  #, p0=[.5, .5, .5, .2]
			# maxfev is number of fit tries, 1000 being standard; p0=[0, 0.5, 2, 0.2]
	   			# print(f"len(trim_x):{len(trim_xValues)}\nlen(trim_y):{len(trim_yValues)}")
			# print(f"trim_popt:\n{trim_popt}\ntrim_pcov:\n{trim_pcov}")
	
			trim_stdError = np.sqrt(np.diag(trim_pcov))  # stdError[ B-error, A-error, CHalf-error, b-error]
			trim_B_stderror, trim_A_stderror, trim_CHalf_stderror, trim_b_stderror = trim_stdError[:]
	
			trim_B, trim_A, trim_CHalf, trim_b = trim_popt[:]
			if trim_B > trim_A:
				trimSlope = 'Positive'
			else: trimSlope = 'Negative'
	
			trim_CHalf_ConfidenceInterval = t.ppf(.975, (trim_numPoints - 1)) * trim_CHalf_stderror / np.sqrt(
					trim_numPoints)  ### Figure out where this .975 comes from... and whatever this line means and is doing...
			trim_CHalf_confidenceInterval_lowBound = trim_CHalf - trim_CHalf_ConfidenceInterval
			trim_CHalf_confidenceInterval_upBound = trim_CHalf + trim_CHalf_ConfidenceInterval
	
			trim_b_confidenceInterval = t.ppf(.975, (trim_numPoints - 1)) * trim_b_stderror / np.sqrt(trim_numPoints)
			trim_b_confidenceInterval_lowBound = trim_b - trim_b_confidenceInterval
			trim_b_confidenceInterval_upBound = trim_b + trim_b_confidenceInterval
	
			''' NOTE: This if/else block of code deals with negative vs. positive slope. A and B change on the
					y-axis, while CHalf changes on the x-axis. So we need to switch the sign on CHalf to get the correct
					confidence interval variables for a confidence interval curve. '''
			if trim_B <= trim_A:
				trim_popt_lowBound = [trim_B - (OUTLIER_CUTOFF * trim_B_stderror),
											  trim_A - (OUTLIER_CUTOFF * trim_A_stderror),
											  trim_CHalf - (OUTLIER_CUTOFF * trim_CHalf_stderror),
											  trim_b]
				trim_popt_upBound = [trim_B + (OUTLIER_CUTOFF * trim_B_stderror),
											 trim_A + (OUTLIER_CUTOFF * trim_A_stderror),
											 trim_CHalf + (OUTLIER_CUTOFF * trim_CHalf_stderror),
											 trim_b]
			else:
				trim_popt_lowBound = [trim_B + (OUTLIER_CUTOFF * trim_B_stderror),
											  trim_A + (OUTLIER_CUTOFF * trim_A_stderror),
											  trim_CHalf - (OUTLIER_CUTOFF * trim_CHalf_stderror),
											  trim_b]
				trim_popt_upBound = [trim_B - (OUTLIER_CUTOFF * trim_B_stderror),
											 trim_A - (OUTLIER_CUTOFF * trim_A_stderror),
											 trim_CHalf + (OUTLIER_CUTOFF * trim_CHalf_stderror),
											 trim_b]
	
	
			trim_concRange = max(trim_xValues) - min(trim_xValues)
			trim_ratioTOrange = trim_CHalf_ConfidenceInterval / trim_concRange
	
			trim_sCurve_xValues = row['sCurve_xValues']
			trim_sCurve_yValues = sigmoid(trim_xValues, *trim_popt)  # assigns yValues according to sigmoid curve at xValues
	
			trim_sCurve_xValues = row['sCurve_xValues']
	
	
			""" r_squared calculations """
			trim_residuals = trim_yValues - sigmoid(trim_xValues, *trim_popt)
			trim_ss_res = np.sum(trim_residuals ** 2)
			trim_ss_tot = np.sum(trim_yValues - np.mean(trim_yValues) ** 2)
			trim_r_squared = 1 - (trim_ss_res / trim_ss_tot)
			trim_CHalf_normalized = trim_CHalf / trim_concRange
	
			# print(f"\n\ntrim_PCOV:\n{trim_pcov}\n\n")
			# Note: popt contains following in list: popt[B, A, CHalf, b]
			row['trim_VALID'] = True
			row['trim_xValues'] = trim_xValues
			row['trim_yValues'] = trim_yValues
			row['trim_#pts'] = trim_numPoints
			row['trim_popt'] = trim_popt
			row['trim_popt_lowBound'] = trim_popt_lowBound
			row['trim_popt_upBound'] = trim_popt_upBound
			row['trim_pcov'] = trim_pcov
			row['trim_sCurve_xValues'] = trim_sCurve_xValues
			row['trim_sCurve_yValues'] = trim_sCurve_yValues
			row['trim_B_stderror'] = trim_B_stderror
			row['trim_A_stderror'] = trim_A_stderror
			row['trim_CHalf_stderror'] = trim_CHalf_stderror
			row['trim_b_stderror'] = trim_b_stderror
			row['trim_CHalf_ConfidenceInterval'] = trim_CHalf_ConfidenceInterval
			row['trim_concRange'] = trim_concRange
			row['trim_ratioTOrange'] = trim_ratioTOrange
			row['trim_B'] = trim_B
			row['trim_A'] = trim_A
			row['trim_CHalf'] = trim_CHalf
			row['trim_b'] = trim_b
			row['trim_slope'] = trimSlope
			row['trim_CHalf_confidenceInterval_lowBound'] = trim_CHalf_confidenceInterval_lowBound
			row['trim_CHalf_confidenceInterval_upBound'] = trim_CHalf_confidenceInterval_upBound
			row['trim_b_confidenceInterval'] = trim_b_confidenceInterval
			row['trim_b_confidenceInterval_lowBound'] = trim_b_confidenceInterval_lowBound
			row['trim_b_confidenceInterval_upBound'] = trim_b_confidenceInterval_upBound
			row['trim_residuals'] = trim_residuals
			row['trim_ss_res'] = trim_ss_res
			row['trim_ss_tot'] = trim_ss_tot
			row['trim_r_squared'] = trim_r_squared
			row['trim_CHalf_normalized'] = trim_CHalf_normalized
		if row['trim_VALID']==False:
			row[['slope','fitCurve_B','fitCurve_A','CHalf','fitCurve_b','B_stderror','A_stderror','CHalf_stderror','b_stderror','CHalf_ConfidenceInterval','ratioTOrange','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound','b_confidenceInterval','b_confidenceInterval_lowBound','b_confidenceInterval_upBound','r_squared','CHalf_normalized']]=0
			row['trim_#pts'] = np.nan
			row['trim_slope'] = np.nan
			row['trim_B'] = np.nan
			row['trim_A'] = np.nan
			row['trim_CHalf'] = np.nan
			row['trim_b'] = np.nan
			row['trim_B_stderror'] = np.nan
			row['trim_A_stderror'] = np.nan
			row['trim_CHalf_stderror'] = np.nan
			row['trim_b_stderror'] = np.nan
			row['trim_CHalf_ConfidenceInterval'] = np.nan
			row['trim_ratioTOrange'] = np.nan
			row['trim_CHalf_confidenceInterval_lowBound'] = np.nan
			row['trim_CHalf_confidenceInterval_upBound'] = np.nan
			row['trim_b_confidenceInterval'] = np.nan
			row['trim_b_confidenceInterval_lowBound'] = np.nan
			row['trim_b_confidenceInterval_upBound'] = np.nan
			row['trim_r_squared'] = np.nan
			row[ 'trim_CHalf_normalized'] = np.nan
		return row

def combined_graph_apply(row,condition_repnumlist,removeOutlier_2xStdErr,R_SQUARED_CUTOFF,repInfo,condition,file_type,CDHD_list,original_temps,CHALF_RANGE_CUTOFF,CONFIDENCE_INTERVAL_CUTOFF,OUTLIER_CUTOFF,RepInfoLists):
	"""for every line"""
	HD = False
	if 'HD' in CDHD_list:
		HD = True
		maxTemp = max(original_temps)
		minTemp = min(original_temps)
	if (row['enough_points'] and removeOutlier_2xStdErr and row['trim_VALID']):
		if(row['trim_r_squared'] >= R_SQUARED_CUTOFF and
		   row['trim_CHalf'] <= row['trim_xValues'][-1] + row['trim_concRange']*CHALF_RANGE_CUTOFF and  # if range is 0 to 4, and cutoff is .5, (0-(4*.5)) >= CHalf >= (4+(4*.5))
		   row['trim_CHalf'] >= row['trim_xValues'][0] - row['trim_concRange']*CHALF_RANGE_CUTOFF and
		   row['trim_CHalf_ConfidenceInterval']*2 <= row['trim_concRange']*CONFIDENCE_INTERVAL_CUTOFF):  #if has MINIMUM_POINTS or more, and fit can be calculated...
			sCurve_xValues = row['sCurve_xValues']
			if HD:
				row['sCurve_xValues'] = denormalize(row['sCurve_xValues'],maxTemp,minTemp)
			combined_sCurve_yValues = sigmoid(sCurve_xValues, *row['popt'])

			'''graph original combined fit line'''
			plt.plot(row['sCurve_xValues'], combined_sCurve_yValues, color='k', marker=',', ls='-.', label='Combined Fitted Curve')
			'''graph fit curves'''
			'''if HD:
				combined_sCurve_yValues_lowBound = sigmoid(normalize(sCurve_xValues,maxTemp,minTemp), *row['popt_lowBound'])
				combined_sCurve_yValues_upBound = sigmoid(normalize(sCurve_xValues,maxTemp,minTemp), *row['popt_upBound'])
			else:'''
			combined_sCurve_yValues_lowBound = sigmoid(sCurve_xValues, *row['popt_lowBound'])
			combined_sCurve_yValues_upBound = sigmoid(sCurve_xValues, *row['popt_upBound'])
			plt.plot(row['sCurve_xValues'], combined_sCurve_yValues_lowBound, color='m', marker=',', ls=':', label=f"Standard Error (x{OUTLIER_CUTOFF})(pre-trim)")
			plt.plot(row['sCurve_xValues'], combined_sCurve_yValues_upBound, color='m', marker=',', ls=':')
			'''graph CHalf line'''
			if HD:
				row['CHalf'] = denormalize(row['CHalf'],maxTemp,minTemp)
			plt.axvline(row['CHalf'], color='k', ls='-.', label='CHalf [vertical]')
			# # CHalf Standard Error Span
			# plt.axvspan(con_sCurveDataList[index]['CHalf'] - con_sCurveDataList[index]['CHalf_ConfidenceInterval'],
			# 			con_sCurveDataList[index]['CHalf'] + con_sCurveDataList[index]['CHalf_ConfidenceInterval'],
			# 			color='#d5d5d5', label='CHalf StdError')

			for repInfo in RepInfoLists:
				if repInfo['condition'] == condition:
					if not pd.isnull(row[repInfo['replabeled_headers'][0]]):
						'''graph rep data points in unique colors'''
						# Either 'Plot' the rep lines, or 'Scatter'plot the rep data points
						# plt.plot(repInfo['conc-temp list'], row.loc[repInfo['replabeled_headers']].tolist(), color=repInfo['plot color'], marker='o', ls='--', label=(f"Rep{repInfo['repNum']}"))
						if HD:
							plt.scatter(repInfo['original-temp list'], row[repInfo['replabeled_headers']].tolist(), color=repInfo['plot color'], marker='o', label=(f"Rep{repInfo['repNum']}"))
						else:
							plt.scatter(repInfo['conc-temp list'], row[repInfo['replabeled_headers']].tolist(), color=repInfo['plot color'], marker='o', label=(f"Rep{repInfo['repNum']}"))

			if row['trim_VALID']:
				'''graph trimmed combined fit line'''
				trim_combined_sCurve_yValues = sigmoid(sCurve_xValues, *row['trim_popt'])
				plt.plot(row['sCurve_xValues'], trim_combined_sCurve_yValues, color='k', marker=',', ls='-', label='Trimmed Combined Curve')
				'''graph new CHalf line'''
				if HD:
					row['trim_CHalf'] = denormalize(row['trim_CHalf'],maxTemp,minTemp)
					row['trim_CHalf_ConfidenceInterval'] = row['trim_CHalf_ConfidenceInterval']*(maxTemp-minTemp)
				plt.axvline(row['trim_CHalf'], color='k', ls='-', label='Trimmed CHalf [vertical]')
				'''graph CHalf Confidence Error Span'''
				plt.axvspan(row['trim_CHalf'] - row['trim_CHalf_ConfidenceInterval'],
							row['trim_CHalf'] + row['trim_CHalf_ConfidenceInterval'],
							color='#d5d5d5', label='CHalf Confidence Interval (trimmed)', zorder=0)
				# plt.annotate(f"r^2 = {con_sCurveDataList[index]['trim_r_squared']}", xytext=(1,1))
				if HD:
					plt.xlabel('Temperature Values')
				else:
					plt.xlabel('Concentration Values')
				plt.ylabel('Amount of Protein Present\n(Normalized)')
				if row['trim_VALID']:
					plt.title(f"{condition}: {row['Accession@Peptide']}\nLine Fit r^2 = {row['r_squared']}\ntrimmed r^2 = {row['trim_r_squared']}")
				else:
					plt.title(f"{condition}: {row['Accession@Peptide']}")
				plt.grid(True)
				lgd = plt.legend(loc=9, bbox_to_anchor=(1.32, .85))  # ([right],[up])
				# plt.legend()
				#print(f"Combined Graph: {condition}, {row.name}")
				# plt.show()
				filename = "Graph Outputs/" + condition + "_Combined==Index==" + str(row.name) + "==Graph" + file_type
				plt.savefig(filename, bbox_extra_artists=(lgd,), bbox_inches='tight')
				plt.clf()

def second_fitting(row,con_conctemp_labeledheaders,con_conctemp_headers,MINIMUM_PTS,OUTLIER_CUTOFF,removeOutlier_2xStdErr=True): #Performs Second Fitting on Label Sites with Multiple Hits for Label Sites Combined
		''' Count Number of Points and Non-Zero, per line'''
		numPoints = (row[con_conctemp_labeledheaders[0]:con_conctemp_labeledheaders[-1]].notna()).sum()
		numNonZero = (row[con_conctemp_labeledheaders[0]:con_conctemp_labeledheaders[-1]][row[con_conctemp_labeledheaders[0]:con_conctemp_labeledheaders[-1]].notna()] != 0).sum()
		row['#pts'] = numPoints
		row['#non Zero'] = numNonZero
		'''----------------------------------------------'''
		valid_yValues = row[con_conctemp_labeledheaders[0]:con_conctemp_labeledheaders[-1]][row[con_conctemp_labeledheaders[0]:con_conctemp_labeledheaders[-1]].notna()].tolist()
		valid_xValues = list(np.array(con_conctemp_headers)[(row[con_conctemp_labeledheaders[0]:con_conctemp_labeledheaders[-1]].notna())])
		row['valid_xValues'] = valid_xValues
		row['valid_yValues'] = valid_yValues
		row['ydata'] = row[con_conctemp_labeledheaders].tolist()
		if row['#non Zero']>= MINIMUM_PTS:	### THIS CHECK IS WORKING, BUT OLD VALUES FOR sCurveData carry over to the next line when this filter prevents new calculations.
			try:
				popt, pcov = curve_fit(sigmoid, row['valid_xValues'], row['valid_yValues'], maxfev=100000)  # , p0=[.5, .5, .5, .2]
				# maxfev is number of fit tries, 1000 being standard; p0=[0, 0.5, 2, 0.2]
				stdError = np.sqrt(np.diag(pcov))  # stdError[ B-error, A-error, CHalf-error, b-error]
				B_stderror, A_stderror, CHalf_stderror, b_stderror = stdError[:]
	
				fitCurve_B, fitCurve_A, CHalf, fitCurve_b = popt[:]
				if fitCurve_B > fitCurve_A:
					slope = 'Positive'
				else: slope = 'Negative'
				numPoints = row['#pts']
				CHalf_ConfidenceInterval = t.ppf(.975, (numPoints - 1)) * CHalf_stderror / np.sqrt(
						numPoints)  ### Figure out where this .975 comes from... and whatever this line means and is doing...
				CHalf_confidenceInterval_lowBound = CHalf - CHalf_ConfidenceInterval
				CHalf_confidenceInterval_upBound = CHalf + CHalf_ConfidenceInterval
	
				b_confidenceInterval = t.ppf(.975, (numPoints - 1)) * b_stderror / np.sqrt(numPoints)
				b_confidenceInterval_lowBound = fitCurve_b - b_confidenceInterval
				b_confidenceInterval_upBound = fitCurve_b + b_confidenceInterval
	
				''' NOTE: This if/else block of code deals with negative vs. positive slope. A and B change on the
					y-axis, while CHalf changes on the x-axis. So we need to switch the sign on CHalf to get the correct
					confidence interval variables for a confidence interval curve. '''
				if fitCurve_B <= fitCurve_A:
					popt_lowBound = [fitCurve_B - (OUTLIER_CUTOFF * B_stderror),
										 fitCurve_A - (OUTLIER_CUTOFF * A_stderror),
										 CHalf - (OUTLIER_CUTOFF * CHalf_stderror),
										 fitCurve_b]
					popt_upBound = [fitCurve_B + (OUTLIER_CUTOFF * B_stderror),
										fitCurve_A + (OUTLIER_CUTOFF * A_stderror),
										CHalf + (OUTLIER_CUTOFF * CHalf_stderror),
										fitCurve_b]
				else:
					popt_lowBound = [fitCurve_B + (OUTLIER_CUTOFF * B_stderror),
										 fitCurve_A + (OUTLIER_CUTOFF * A_stderror),
										 CHalf - (OUTLIER_CUTOFF * CHalf_stderror),
										 fitCurve_b]
					popt_upBound = [fitCurve_B - (OUTLIER_CUTOFF * B_stderror),
										fitCurve_A - (OUTLIER_CUTOFF * A_stderror),
										CHalf + (OUTLIER_CUTOFF * CHalf_stderror),
										fitCurve_b]
	
				valid_xValues = row['valid_xValues']
				concRange = max(valid_xValues) - min(valid_xValues)
				ratioTOrange = CHalf_ConfidenceInterval / concRange
	
				sCurve_xValues = np.linspace(min(valid_xValues)-(concRange/20), max(valid_xValues)+(concRange/20), 50)
				# 50 points in conc/temp range (with small 1/20 margin on each side); determines resolution of graph
				sCurve_yValues = sigmoid(sCurve_xValues, *popt)  # assigns yValues according to sigmoid curve at xValues
	
				row['sCurve_xValues'] = sCurve_xValues
				row['sCurve_yValues'] = sCurve_yValues
	
				
				""" r_squared calculations """
				valid_yValues = row['valid_yValues']
				residuals = valid_yValues - sigmoid(valid_xValues, *popt)
				ss_res = np.sum(residuals ** 2)
				ss_tot = np.sum(valid_yValues - np.mean(valid_yValues) ** 2)
				r_squared = 1 - (ss_res / ss_tot)
				CHalf_normalized = CHalf / concRange
	
				# Note: popt contains following in list: popt[B, A, CHalf, b]
				row['enough_points'] = True
				row['popt'] = popt
				row['popt_lowBound'] = popt_lowBound
				row['popt_upBound'] = popt_upBound
				row['pcov'] = pcov
				row['sCurve_xValues'] = sCurve_xValues
				row['sCurve_yValues'] = sCurve_yValues
				row['B_stderror'] = B_stderror
				row['A_stderror'] = A_stderror
				row['CHalf_stderror'] = CHalf_stderror
				row['b_stderror'] = b_stderror
				row['CHalf_ConfidenceInterval'] = CHalf_ConfidenceInterval
				row['concRange'] = concRange
				row['ratioTOrange'] = ratioTOrange
				row['fitCurve_B'] = fitCurve_B
				row['fitCurve_A'] = fitCurve_A
				row['CHalf'] = CHalf
				row['fitCurve_b'] = fitCurve_b
				row['slope'] = slope
				row['CHalf_confidenceInterval_lowBound'] = CHalf_confidenceInterval_lowBound
				row['CHalf_confidenceInterval_upBound'] = CHalf_confidenceInterval_upBound
				row['b_confidenceInterval'] = b_confidenceInterval
				row['b_confidenceInterval_lowBound'] = b_confidenceInterval_lowBound
				row['b_confidenceInterval_upBound'] = b_confidenceInterval_upBound
				row['residuals'] = residuals
				row['ss_res'] = ss_res
				row['ss_tot'] = ss_tot
				row['r_squared'] = r_squared
				row['CHalf_normalized'] = CHalf_normalized
			except RuntimeError:
				print(f"ERROR, Row{row.name}:  Could not find fit...")
				row['enough_points'] = False
				print ("here, ", row.name)
		else:
			row['enough_points'] = False


		""" REMOVING OUTLIERS AND PERFORMING TRIMMED DATA CURVE FIT """
		if removeOutlier_2xStdErr == True:
			if row['enough_points'] == False:
				row['trim_VALID'] = False
				print ("there, ", row.name)
				row[['slope','fitCurve_B','fitCurve_A','CHalf','fitCurve_b','B_stderror','A_stderror','CHalf_stderror','b_stderror','CHalf_ConfidenceInterval','ratioTOrange','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound','b_confidenceInterval','b_confidenceInterval_lowBound','b_confidenceInterval_upBound','r_squared','CHalf_normalized']]=0
				row['trim_#pts'] = np.nan
				row['trim_slope'] = np.nan
				row['trim_B'] = np.nan
				row['trim_A'] = np.nan
				row['trim_CHalf'] = np.nan
				row['trim_b'] = np.nan
				row['trim_B_stderror'] = np.nan
				row['trim_A_stderror'] = np.nan
				row['trim_CHalf_stderror'] = np.nan
				row['trim_b_stderror'] = np.nan
				row['trim_CHalf_ConfidenceInterval'] = np.nan
				row['trim_ratioTOrange'] = np.nan
				row['trim_CHalf_confidenceInterval_lowBound'] = np.nan
				row['trim_CHalf_confidenceInterval_upBound'] = np.nan
				row['trim_b_confidenceInterval'] = np.nan
				row['trim_b_confidenceInterval_lowBound'] = np.nan
				row['trim_b_confidenceInterval_upBound'] = np.nan
				row['trim_r_squared'] = np.nan
				row[ 'trim_CHalf_normalized'] = np.nan
				return row
			# print(f"trim-calculations: Row {index}")
				# Get trimmed values by checking if within 2 Confidence Intervals of B, A, and CHalf
			trim_yValues = []
			trim_xValues = []
			count = 0
			for ydata in row['ydata']:
				# popt up / low bound are B,A,b,CHalf with B,A, and CHalf two confidence intervals up or down
				if (row['fitCurve_B'] <= row['fitCurve_A']):
					if (ydata > sigmoid(con_conctemp_headers[count], *row['popt_lowBound'])) and (
							ydata < sigmoid(con_conctemp_headers[count], *row['popt_upBound'])):
						trim_yValues.append(ydata)
						trim_xValues.append(con_conctemp_headers[count])
	
				else:
					if (ydata < sigmoid(con_conctemp_headers[count], *row['popt_lowBound'])) and (
									ydata > sigmoid(con_conctemp_headers[count], *row['popt_upBound'])):
						trim_yValues.append(ydata)
						trim_xValues.append(con_conctemp_headers[count])
				count += 1
			trim_numPoints = len(trim_yValues)
	
			if trim_numPoints <= MINIMUM_PTS:  # CHECK for number of data points.
				row['trim_VALID'] = False
				row[['slope','fitCurve_B','fitCurve_A','CHalf','fitCurve_b','B_stderror','A_stderror','CHalf_stderror','b_stderror','CHalf_ConfidenceInterval','ratioTOrange','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound','b_confidenceInterval','b_confidenceInterval_lowBound','b_confidenceInterval_upBound','r_squared','CHalf_normalized']]=0
				row['trim_#pts'] = np.nan
				row['trim_slope'] = np.nan
				row['trim_B'] = np.nan
				row['trim_A'] = np.nan
				row['trim_CHalf'] = np.nan
				row['trim_b'] = np.nan
				row['trim_B_stderror'] = np.nan
				row['trim_A_stderror'] = np.nan
				row['trim_CHalf_stderror'] = np.nan
				row['trim_b_stderror'] = np.nan
				row['trim_CHalf_ConfidenceInterval'] = np.nan
				row['trim_ratioTOrange'] = np.nan
				row['trim_CHalf_confidenceInterval_lowBound'] = np.nan
				row['trim_CHalf_confidenceInterval_upBound'] = np.nan
				row['trim_b_confidenceInterval'] = np.nan
				row['trim_b_confidenceInterval_lowBound'] = np.nan
				row['trim_b_confidenceInterval_upBound'] = np.nan
				row['trim_r_squared'] = np.nan
				row[ 'trim_CHalf_normalized'] = np.nan
				return row
	
	
			try:
				trim_popt, trim_pcov = curve_fit(sigmoid, trim_xValues, trim_yValues,
												 maxfev=100000)  # , p0=[.5, .5, .5, .2]
				# maxfev is number of fit tries, 1000 being standard; p0=[0, 0.5, 2, 0.2]
				# print(f"len(trim_x):{len(trim_xValues)}\nlen(trim_y):{len(trim_yValues)}")
				# print(f"trim_popt:\n{trim_popt}\ntrim_pcov:\n{trim_pcov}")
			except RuntimeError:
				print(f"ERROR, Row{row.name}:  Could not find fit...")
				row['trim_VALID'] = False
				print ("anywhere, ", row.name)
				row[['slope','fitCurve_B','fitCurve_A','CHalf','fitCurve_b','B_stderror','A_stderror','CHalf_stderror','b_stderror','CHalf_ConfidenceInterval','ratioTOrange','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound','b_confidenceInterval','b_confidenceInterval_lowBound','b_confidenceInterval_upBound','r_squared','CHalf_normalized']]=0
				row['trim_#pts'] = np.nan
				row['trim_slope'] = np.nan
				row['trim_B'] = np.nan
				row['trim_A'] = np.nan
				row['trim_CHalf'] = np.nan
				row['trim_b'] = np.nan
				row['trim_B_stderror'] = np.nan
				row['trim_A_stderror'] = np.nan
				row['trim_CHalf_stderror'] = np.nan
				row['trim_b_stderror'] = np.nan
				row['trim_CHalf_ConfidenceInterval'] = np.nan
				row['trim_ratioTOrange'] = np.nan
				row['trim_CHalf_confidenceInterval_lowBound'] = np.nan
				row['trim_CHalf_confidenceInterval_upBound'] = np.nan
				row['trim_b_confidenceInterval'] = np.nan
				row['trim_b_confidenceInterval_lowBound'] = np.nan
				row['trim_b_confidenceInterval_upBound'] = np.nan
				row['trim_r_squared'] = np.nan
				row[ 'trim_CHalf_normalized'] = np.nan
				return row
	
			trim_popt, trim_pcov = curve_fit(sigmoid, trim_xValues, trim_yValues, maxfev=100000)  #, p0=[.5, .5, .5, .2]
			# maxfev is number of fit tries, 1000 being standard; p0=[0, 0.5, 2, 0.2]
	   			# print(f"len(trim_x):{len(trim_xValues)}\nlen(trim_y):{len(trim_yValues)}")
			# print(f"trim_popt:\n{trim_popt}\ntrim_pcov:\n{trim_pcov}")
	
			trim_stdError = np.sqrt(np.diag(trim_pcov))  # stdError[ B-error, A-error, CHalf-error, b-error]
			trim_B_stderror, trim_A_stderror, trim_CHalf_stderror, trim_b_stderror = trim_stdError[:]
	
			trim_B, trim_A, trim_CHalf, trim_b = trim_popt[:]
			if trim_B > trim_A:
				trimSlope = 'Positive'
			else: trimSlope = 'Negative'
	
			trim_CHalf_ConfidenceInterval = t.ppf(.975, (trim_numPoints - 1)) * trim_CHalf_stderror / np.sqrt(
					trim_numPoints)  ### Figure out where this .975 comes from... and whatever this line means and is doing...
			trim_CHalf_confidenceInterval_lowBound = trim_CHalf - trim_CHalf_ConfidenceInterval
			trim_CHalf_confidenceInterval_upBound = trim_CHalf + trim_CHalf_ConfidenceInterval
	
			trim_b_confidenceInterval = t.ppf(.975, (trim_numPoints - 1)) * trim_b_stderror / np.sqrt(trim_numPoints)
			trim_b_confidenceInterval_lowBound = trim_b - trim_b_confidenceInterval
			trim_b_confidenceInterval_upBound = trim_b + trim_b_confidenceInterval
	
			''' NOTE: This if/else block of code deals with negative vs. positive slope. A and B change on the
					y-axis, while CHalf changes on the x-axis. So we need to switch the sign on CHalf to get the correct
					confidence interval variables for a confidence interval curve. '''
			if trim_B <= trim_A:
				trim_popt_lowBound = [trim_B - (OUTLIER_CUTOFF * trim_B_stderror),
											  trim_A - (OUTLIER_CUTOFF * trim_A_stderror),
											  trim_CHalf - (OUTLIER_CUTOFF * trim_CHalf_stderror),
											  trim_b]
				trim_popt_upBound = [trim_B + (OUTLIER_CUTOFF * trim_B_stderror),
											 trim_A + (OUTLIER_CUTOFF * trim_A_stderror),
											 trim_CHalf + (OUTLIER_CUTOFF * trim_CHalf_stderror),
											 trim_b]
			else:
				trim_popt_lowBound = [trim_B + (OUTLIER_CUTOFF * trim_B_stderror),
											  trim_A + (OUTLIER_CUTOFF * trim_A_stderror),
											  trim_CHalf - (OUTLIER_CUTOFF * trim_CHalf_stderror),
											  trim_b]
				trim_popt_upBound = [trim_B - (OUTLIER_CUTOFF * trim_B_stderror),
											 trim_A - (OUTLIER_CUTOFF * trim_A_stderror),
											 trim_CHalf + (OUTLIER_CUTOFF * trim_CHalf_stderror),
											 trim_b]
	
	
			trim_concRange = max(trim_xValues) - min(trim_xValues)
			trim_ratioTOrange = trim_CHalf_ConfidenceInterval / trim_concRange
	
			trim_sCurve_xValues = row['sCurve_xValues']
			trim_sCurve_yValues = sigmoid(trim_xValues, *trim_popt)  # assigns yValues according to sigmoid curve at xValues
	
			trim_sCurve_xValues = row['sCurve_xValues']
	
	
			""" r_squared calculations """
			trim_residuals = trim_yValues - sigmoid(trim_xValues, *trim_popt)
			trim_ss_res = np.sum(trim_residuals ** 2)
			trim_ss_tot = np.sum(trim_yValues - np.mean(trim_yValues) ** 2)
			trim_r_squared = 1 - (trim_ss_res / trim_ss_tot)
			trim_CHalf_normalized = trim_CHalf / trim_concRange
	
			# print(f"\n\ntrim_PCOV:\n{trim_pcov}\n\n")
			# Note: popt contains following in list: popt[B, A, CHalf, b]
			row['trim_VALID'] = True
			row['trim_xValues'] = trim_xValues
			row['trim_yValues'] = trim_yValues
			row['trim_#pts'] = trim_numPoints
			row['trim_popt'] = trim_popt
			row['trim_popt_lowBound'] = trim_popt_lowBound
			row['trim_popt_upBound'] = trim_popt_upBound
			row['trim_pcov'] = trim_pcov
			row['trim_sCurve_xValues'] = trim_sCurve_xValues
			row['trim_sCurve_yValues'] = trim_sCurve_yValues
			row['trim_B_stderror'] = trim_B_stderror
			row['trim_A_stderror'] = trim_A_stderror
			row['trim_CHalf_stderror'] = trim_CHalf_stderror
			row['trim_b_stderror'] = trim_b_stderror
			row['trim_CHalf_ConfidenceInterval'] = trim_CHalf_ConfidenceInterval
			row['trim_concRange'] = trim_concRange
			row['trim_ratioTOrange'] = trim_ratioTOrange
			row['trim_B'] = trim_B
			row['trim_A'] = trim_A
			row['trim_CHalf'] = trim_CHalf
			row['trim_b'] = trim_b
			row['trim_slope'] = trimSlope
			row['trim_CHalf_confidenceInterval_lowBound'] = trim_CHalf_confidenceInterval_lowBound
			row['trim_CHalf_confidenceInterval_upBound'] = trim_CHalf_confidenceInterval_upBound
			row['trim_b_confidenceInterval'] = trim_b_confidenceInterval
			row['trim_b_confidenceInterval_lowBound'] = trim_b_confidenceInterval_lowBound
			row['trim_b_confidenceInterval_upBound'] = trim_b_confidenceInterval_upBound
			row['trim_residuals'] = trim_residuals
			row['trim_ss_res'] = trim_ss_res
			row['trim_ss_tot'] = trim_ss_tot
			row['trim_r_squared'] = trim_r_squared
			row['trim_CHalf_normalized'] = trim_CHalf_normalized
		if row['trim_VALID']==False:
			row[['slope','fitCurve_B','fitCurve_A','CHalf','fitCurve_b','B_stderror','A_stderror','CHalf_stderror','b_stderror','CHalf_ConfidenceInterval','ratioTOrange','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound','b_confidenceInterval','b_confidenceInterval_lowBound','b_confidenceInterval_upBound','r_squared','CHalf_normalized']]=0
			row[['trim_#pts','trim_slope', 'trim_B', 'trim_A', 'trim_CHalf', 'trim_b', 'trim_B_stderror',
												'trim_A_stderror', 'trim_CHalf_stderror', 'trim_b_stderror',
												'trim_CHalf_ConfidenceInterval', 'trim_ratioTOrange',
												'trim_CHalf_confidenceInterval_lowBound',
												'trim_CHalf_confidenceInterval_upBound', 'trim_b_confidenceInterval',
												'trim_b_confidenceInterval_lowBound','trim_b_confidenceInterval_upBound',
												'trim_r_squared', 'trim_CHalf_normalize']] = np.nan
		return row

''' COMBINED LABEL SITES '''
def LabelSites_Combined(file,version,MINIMUM_PTS = 4,OUTLIER_CUTOFF = 2,CHalflow = 0,CHalfhigh = 3.48,rsquared = 0.6,confintlow = 0,confinthigh = 0.35): #Creates Combined Label Sites file
	df = pd.read_csv(file)
	df.set_index(df.columns.tolist()[0],inplace=True)
	conc_start = df.columns.tolist().index('Label@Accession') + 1
	conc_header_list = df.columns.tolist()[conc_start:]
	conc_list = []
	conc_dict = {}
	for header in conc_header_list: #gets concentrations
		conc_list.append(float(header.split('_')[0]))
	conc_list = list(set(conc_list)) #removes duplicates
	conc_list.sort() #sorts by accending
	for conc in conc_list: #matches headers to concetrations
		temp = []
		for header in conc_header_list:
			if str(conc) in header:
				temp.append(header)
		conc_dict.update({conc:temp})
	groups = df.groupby(by='Label@Accession') #sort by label sites on each protein
	outDF = pd.DataFrame(columns=['Accession',"Peptide","Label@Accession","Label Site",'Label Type','Residue Number','Count','trim_CHalf','trim_r_squared','trim_ratioTOrange','trim_CHalf_ConfidenceInterval','trim_slope','trim_b'])
	removedDF = pd.DataFrame(columns=['Accession',"Peptide","Label@Accession","Label Site",'Label Type','Residue Number','Count','trim_CHalf','trim_r_squared','trim_ratioTOrange','trim_CHalf_ConfidenceInterval','trim_slope','trim_b'])
	for key in groups.groups.keys():
		group = groups.get_group(key)
		group['Count'] = len(group)
		if len(group) == 1:
			outDF = outDF.append(group[['Accession',"Peptide","Label@Accession","Label Site",'Label Type','Residue Number','Count','trim_CHalf','trim_r_squared','trim_ratioTOrange','trim_CHalf_ConfidenceInterval','trim_slope','trim_b']],ignore_index=True)
		else:
			data = {"Accession" : [group.reset_index(drop=True).loc[0]['Accession']],
					"Peptide" : [group['Peptide'].tolist()],
					"Label@Accession" : [group.reset_index(drop=True).loc[0]['Label@Accession']],
					"Label Site" : [group.reset_index(drop=True).loc[0]['Label Site']],
					"Label Type" : [group.reset_index(drop=True).loc[0]['Label Type']],
					"Residue Number" : [group.reset_index(drop=True).loc[0]['Residue Number']],
					"Count" : [group.reset_index(drop=True).loc[0]['Count']]          
				}
			tempDF = pd.DataFrame(data)
			group.reset_index(drop=True,inplace=True)
			for i in range(len(group)):
				row = group.loc[i]
				row = row[conc_header_list].to_frame().transpose().reset_index(drop=True).add_suffix('_' + str(i))
				tempDF = pd.concat([tempDF,row],axis=1)
			con_conctemp_labeledheaders = tempDF.columns.tolist()[7:]
			con_conctemp_headers = []
			for conc in con_conctemp_labeledheaders:
				con_conctemp_headers.append(float(conc.split('_')[0]))
			tempDF['valid_xValues'] = [np.nan]*len(tempDF)
			tempDF['valid_yValues'] = [np.nan]*len(tempDF)
			tempDF = tempDF.apply(second_fitting,axis=1,con_conctemp_labeledheaders=con_conctemp_labeledheaders,con_conctemp_headers=con_conctemp_headers,MINIMUM_PTS=MINIMUM_PTS,removeOutlier_2xStdErr=True,OUTLIER_CUTOFF=OUTLIER_CUTOFF)
			outDF = outDF.append(tempDF[['Accession',"Peptide","Label@Accession","Label Site",'Label Type','Residue Number','Count','trim_CHalf','trim_r_squared','trim_ratioTOrange','trim_CHalf_ConfidenceInterval','trim_slope','trim_b']].reset_index(drop=True).loc[0],ignore_index=True)
	outDF = outDF[outDF['trim_CHalf'] != 'cnc'].reset_index(drop=True)
	removedDF = removedDF.append(outDF[outDF['trim_CHalf'] == 'cnc'],ignore_index=True) #saving removed sites for reference
	outDF['trim_CHalf'] = outDF['trim_CHalf'].astype(float) #modifying type to allow for calculations later
	chalf_inrange_bool = np.logical_and(np.array(outDF['trim_CHalf'] >= CHalflow), np.array(outDF['trim_CHalf'] <= CHalfhigh))
	rsquared_peptide_bool = np.logical_and(chalf_inrange_bool, np.array(outDF['trim_r_squared'].astype(float) > rsquared))
	inrange_peptide_bool = np.logical_and(rsquared_peptide_bool, np.logical_and(np.array(outDF['trim_ratioTOrange'].astype(float) >= confintlow), np.array(outDF['trim_ratioTOrange'].astype(float) <= confinthigh)))
	removedDF = removedDF.append(outDF[np.invert(inrange_peptide_bool)],ignore_index=True) #adding removed sites to df
	outDF = outDF[inrange_peptide_bool]
	outDF.sort_values(by=['Accession','Residue Number'],ignore_index=True,inplace=True)
	outDF.rename_axis(version,axis='index',inplace=True)
	removedDF.sort_values(by=['Accession','Residue Number'],ignore_index=True,inplace=True)
	removedDF.rename_axis(version,axis='index',inplace=True)
	return [outDF,removedDF]

''' GUI AUXILARY FUNCTIONS '''
def boolTOword(inp): #Turns boolean outputs into yes/no for masterfile
	if inp == False:
		out = 'No'
	else:
		out = 'Yes'
	return out
dir_name = None

''' LABEL FINDER GUI '''
def LabelFinder2(inp,labels,out,dir_): #accepts input file, labels to find (list), and project name
	''' SET UP '''
	inpDF = pd.read_csv(inp)
	inpDF = trim_ends(inpDF) #remove beginning and end of peptides (PEAKS format) and TMT tags
	aalst = [] #list of amino acids to look for
	for label in labels:
		if label[0] not in aalst:
			aalst.append(label[0]) #appends first character of tag (should be amino acid) i.e Y in 'Y(+125.90)'
	aadict = {}
	for aa in aalst: #creates dictionary of amino acids to find and associated tags
		templst = []
		for label in labels:
			if aa in label:
				templst.append(label)
		aadict.update({aa:templst})
	keys = list(aadict)
	efflst = [] #for producing table key
	for key in keys:
		efflst.append(key)
		for tag in aadict[key]:
			efflst.append(tag)
	outputDF = pd.DataFrame(columns=[out + ' Label Efficiency', 'peptide', 'protein', 'peptide %', 'protein %'])
	keyList = ['Raw', 'enough valid pts'] + efflst + ['has any', 'has any tag', 'can be fit and has any tag']
	outputDF[out + ' Label Efficiency'] = keyList
	outputDF.set_index(out + ' Label Efficiency', inplace=True)

	''' PEPTIDES '''
	indexList = outputDF.index.tolist()
	outputDF.iloc[0]['peptide'] = len(inpDF)
	validArray = np.array([inpDF['#Non_Zero'] > 3])
	outputDF.iloc[1]['peptide'] = validArray.sum()
	arraydict = {}
	for i in range(len(indexList)-5): #Counts number of peptides with desired amino acids and tags
		labelarray = np.array([inpDF['Peptide'].str.contains(re.escape(indexList[i+2]))])
		arraydict.update({re.escape(indexList[i+2]):labelarray}) #saves findings as boolean arrays in dictionary for future calculations
		outputDF['peptide'][i+2] = labelarray.sum()
	arraydictKey = list(arraydict)
	hasanyArraysList = []
	anytagArraysList = []
	for key in arraydictKey:
		if len(key) == 1:
			hasanyArraysList.append(arraydict[key]) #sorts out amino acid boolean arrays
		else:
			anytagArraysList.append(arraydict[key]) #sorts out tag boolean arrays
	hasanyArray = np.array([False]*len(inpDF))
	anytagArray = np.array([False]*len(inpDF))
	for array in hasanyArraysList: #makes boolean array for hasany amino acid in search
		hasanyArray = np.logical_or(hasanyArray,array)
	for array in anytagArraysList: #makes boolean array for hasany tag in search
		anytagArray = np.logical_or(anytagArray,array)
	outputDF.iloc[-3]['peptide'] = hasanyArray.sum()
	outputDF.iloc[-2]['peptide'] = anytagArray.sum()
	fittingtags = np.logical_and(validArray,anytagArray)[0] #for export of fittable tagged peptides
	outputDF.iloc[-1]['peptide'] = fittingtags.sum() #counts if has >3 points and has any tag in search

	''' PROTEINS '''
	proteinGroups = inpDF.groupby(by='Accession') #groups peptides by protein
	outputDF.iloc[0]['protein'] = len(proteinGroups) #counts number of proteins
	proteinKey = list(proteinGroups.groups.keys()) #list of groups by key
	PvalidArray = np.array([]) #making empty array for construction of proteins with >3 pts
	for key in proteinKey:
		group = proteinGroups.get_group(key)
		PvalidArray = np.append(PvalidArray,combineBool(np.array(group['#Non_Zero'] > 3),'or'))
	outputDF.iloc[1]['protein'] =  PvalidArray.sum()
	Parraydict = {}
	for i in range(len(indexList)-5): #Counts number of protein groups with desired amino acids and tags
		PlabelArray = np.array([])
		for key in proteinKey:
			group = proteinGroups.get_group(key)
			PlabelArray = np.append(PlabelArray,combineBool(np.array([group['Peptide'].str.contains(re.escape(indexList[i+2])).tolist()]),'or'))
		Parraydict.update({re.escape(indexList[i+2]):PlabelArray}) #saves findings as boolean arrays in dictionary for future calculations
		outputDF['protein'][i+2] = PlabelArray.sum()
	ParraydictKey = list(Parraydict)
	PhasanyArraysList = []
	PanytagArraysList = []
	for key in ParraydictKey:
		if len(key) == 1:
			PhasanyArraysList.append(Parraydict[key]) #sorts out amino acid boolean arrays
		else:
			PanytagArraysList.append(Parraydict[key]) #sorts out tag boolean arrays
	PhasanyArray = np.array([False]*len(proteinGroups))
	PanytagArray = np.array([False]*len(proteinGroups))
	for array in PhasanyArraysList: #makes boolean array for hasany amino acid in search
		PhasanyArray = np.logical_or(PhasanyArray,array)
	for array in PanytagArraysList: #makes boolean array for hasany tag in search
		PanytagArray = np.logical_or(PanytagArray,array)
	outputDF.iloc[-3]['protein'] = PhasanyArray.sum()
	outputDF.iloc[-2]['protein'] = PanytagArray.sum()
	outputDF.iloc[-1]['protein'] = np.logical_and(PvalidArray,PanytagArray).sum() #counts if has >3 points and has any tag in search

	''' PERCENTAGES '''
	outputDF.iloc[0]['peptide %'] = '-'
	outputDF.iloc[0]['protein %']= '-'
	outputDF.iloc[1]['peptide %'] = str(outputDF.iloc[1]['peptide']/outputDF.iloc[0]['peptide']*100) + '%'
	outputDF.iloc[1]['protein %']= str(outputDF.iloc[1]['protein']/outputDF.iloc[0]['protein']*100) + '%'
	outputDF.iloc[-3]['peptide %'] = str(outputDF.iloc[-3]['peptide']/outputDF.iloc[0]['peptide']*100) + '%'
	outputDF.iloc[-3]['protein %']= str(outputDF.iloc[-3]['protein']/outputDF.iloc[0]['protein']*100) + '%'
	outputDF.iloc[-2]['peptide %'] = str(outputDF.iloc[-2]['peptide']/outputDF.iloc[-3]['peptide']*100) + '%'
	outputDF.iloc[-2]['protein %']= str(outputDF.iloc[-2]['protein']/outputDF.iloc[-3]['protein']*100) + '%'
	outputDF.iloc[-1]['peptide %'] = str(outputDF.iloc[-1]['peptide']/outputDF.iloc[-3]['peptide']*100) + '%'
	outputDF.iloc[-1]['protein %']= str(outputDF.iloc[-1]['protein']/outputDF.iloc[-3]['protein']*100) + '%'
	for i in range(len(indexList)-5):
		if len(outputDF.index.tolist()[i+2]) == 1:
			outputDF['peptide %'][i+2] = str(outputDF.iloc[i+2]['peptide']/outputDF.iloc[0]['peptide']*100) + '%'
			outputDF['protein %'][i+2] = str(outputDF.iloc[i+2]['protein']/outputDF.iloc[0]['protein']*100) + '%'
		else:
			val = outputDF.index.tolist()[i+2][0]
			for j in range(len(outputDF.index.tolist())):
				if val == outputDF.index.tolist()[j]:
					outputDF['peptide %'][i+2] = str(outputDF.iloc[i+2]['peptide']/outputDF.iloc[j]['peptide']*100) + '%'
					outputDF['protein %'][i+2] = str(outputDF.iloc[i+2]['protein']/outputDF.iloc[j]['protein']*100) + '%'
	''' OUTPUTS '''
	tagged = inpDF[fittingtags]#.drop(axis=1,labels='Unnamed: 0')
	tagged.to_csv(dir_ + '/' + out + ' Tags.csv', index=False)
	outputDF.to_csv(dir_ + '/' + out + ' Label Efficiency.csv')

class Ui_LabelFinder(QtWidgets.QMainWindow):
	def __init__(self): #setupUi(self, MainWindow):
		super().__init__()
		self.setObjectName("MainWindow")
		self.resize(910, 615)
		global icon2
		self.setWindowIcon(QtGui.QIcon(icon2))
		self.centralwidget = QtWidgets.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
		self.textBrowser.setGeometry(QtCore.QRect(20, 10, 871, 161))
		self.textBrowser.setObjectName("textBrowser")
		self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox.setGeometry(QtCore.QRect(380, 180, 251, 371))
		self.groupBox.setObjectName("groupBox")
		self.list_labeldictionary = QtWidgets.QListWidget(self.groupBox)
		self.list_labeldictionary.setGeometry(QtCore.QRect(10, 20, 231, 341))
		self.list_labeldictionary.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
		self.list_labeldictionary.setDefaultDropAction(QtCore.Qt.MoveAction)
		self.list_labeldictionary.setObjectName("list_labeldictionary")
		self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_3.setGeometry(QtCore.QRect(640, 180, 251, 371))
		self.groupBox_3.setObjectName("groupBox_3")
		self.list_labeltofind = QtWidgets.QListWidget(self.groupBox_3)
		self.list_labeltofind.setGeometry(QtCore.QRect(10, 20, 231, 341))
		self.list_labeltofind.setDragEnabled(True)
		self.list_labeltofind.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
		self.list_labeltofind.setDefaultDropAction(QtCore.Qt.MoveAction)
		self.list_labeltofind.setObjectName("list_labeltofind")
		self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_4.setGeometry(QtCore.QRect(20, 180, 351, 371))
		self.groupBox_4.setObjectName("groupBox_4")
		self.textBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_4)
		self.textBrowser_2.setGeometry(QtCore.QRect(10, 20, 331, 201))
		self.textBrowser_2.setObjectName("textBrowser_2")
		self.formLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_4)
		self.formLayoutWidget_2.setGeometry(QtCore.QRect(10, 230, 331, 31))
		self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
		self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget_2)
		self.formLayout.setContentsMargins(0, 0, 0, 0)
		self.formLayout.setObjectName("formLayout")
		self.label = QtWidgets.QLabel(self.formLayoutWidget_2)
		self.label.setObjectName("label")
		self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
		self.lineEdit = QtWidgets.QLineEdit(self.formLayoutWidget_2)
		self.lineEdit.setObjectName("lineEdit")
		self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
		self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_4)
		self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 260, 331, 31))
		self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
		self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.pb_input = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
		self.pb_input.setObjectName("pb_input")
		self.pb_input.clicked.connect(self.inputfile)
		self.horizontalLayout_2.addWidget(self.pb_input)
		self.pb_output = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
		self.pb_output.setObjectName("pb_output")
		self.pb_output.clicked.connect(self.outputdir)
		self.horizontalLayout_2.addWidget(self.pb_output)
		self.pb_process = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
		self.pb_process.setObjectName("pb_process")
		self.pb_process.clicked.connect(self.process)
		self.horizontalLayout_2.addWidget(self.pb_process)
		self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_4)
		self.groupBox_2.setGeometry(QtCore.QRect(10, 300, 331, 61))
		self.groupBox_2.setObjectName("groupBox_2")
		self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox_2)
		self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 20, 331, 31))
		self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.pb_open = QtWidgets.QPushButton(self.horizontalLayoutWidget)
		self.pb_open.setObjectName("pb_open")
		self.pb_open.clicked.connect(self.opendict)
		self.horizontalLayout.addWidget(self.pb_open)
		self.pb_refresh = QtWidgets.QPushButton(self.horizontalLayoutWidget)
		self.pb_refresh.setObjectName("pb_refresh")
		self.pb_refresh.clicked.connect(self.refresh)
		self.horizontalLayout.addWidget(self.pb_refresh)
		self.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(self)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 910, 26))
		self.menubar.setObjectName("menubar")
		self.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(self)
		self.statusbar.setObjectName("statusbar")
		self.setStatusBar(self.statusbar)
		self.projectname = None  
		self.fname = None
		self.outdir = None
		self.pb_return = QtWidgets.QPushButton(self.centralwidget)
		self.pb_return.setGeometry(QtCore.QRect(800, 560, 93, 28))
		self.pb_return.setObjectName("pb_return")
		self.pb_return.clicked.connect(self.close)   

		self.retranslateUi(self)
		QtCore.QMetaObject.connectSlotsByName(self)
		self.workingdir = os.getcwd()
		try:
			global labelfinderpath
			dictDF = pd.read_csv(labelfinderpath) #labels that can be read
			defaultlst = []
			dictlst = []
			for row in range(len(dictDF)): #prepares label dictionary based on default vs not default
				if dictDF.iloc[row]['Default:'].astype(str).upper() == "TRUE":
					defaultlst.append(dictDF.iloc[row]['Label ID:'])
				else:
					dictlst.append(dictDF.iloc[row]['Label ID:'])
			self.list_labeldictionary.addItems(dictlst)
			self.list_labeltofind.addItems(defaultlst)
		except:
			self.Error1()

	def retranslateUi(self, MainWindow):
		global lfLogo
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Label Finder"))
		self.textBrowser.setHtml(_translate("MainWindow", f"<img src=\"{lfLogo}\">"))
		self.groupBox.setTitle(_translate("MainWindow", "Label Dictionary"))
		self.groupBox_3.setTitle(_translate("MainWindow", "Labels to Find"))
		self.groupBox_4.setTitle(_translate("MainWindow", "Instructions"))
		self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
		"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
		"p, li { white-space: pre-wrap; }\n"
		"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Label Finder:</p>\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. Specify project name.</p>\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. Select either Combined or Rep OUTPUT data from CHalf and an output directory.</p>\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. Drag and drop labels from Label Dictionary to Labels to Find.</p>\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4. Press Process.</p>\n"
		"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Expanding Label Dictionary:</p>\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. Press Open.</p>\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. Specify the Name, Amino Acid, Label ID, and Default setting (automatically sets it as a label to find if true)</p>\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. Press Refresh</p>\n"
		"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Note: Check documentation for using non PEAKS formatted labels or non CHalf data output files.</p></body></html>"))
		self.label.setText(_translate("MainWindow", "Project Name:"))
		self.pb_input.setText(_translate("MainWindow", "Select Input File"))
		self.pb_output.setText(_translate("MainWindow", "Output Directory"))
		self.pb_process.setText(_translate("MainWindow", "Process"))
		self.groupBox_2.setTitle(_translate("MainWindow", "Label Dictionary:"))
		self.pb_open.setText(_translate("MainWindow", "Open"))
		self.pb_refresh.setText(_translate("MainWindow", "Refresh"))
		self.pb_return.setText(_translate("MainWindow", "Return"))
	def Error1(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('Label Finder Dictionary.csv not found. Please add to ' + self.workingdir)
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error2(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('Output directory not specified. Please select an output directory.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
		self.outputdir()
	def Error3(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('No input file selected.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
		self.inputfile()
	def Error4(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('Error occurred. See print statement.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def inputfile(self):
		self.fname = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, 'Open file', self.workingdir,"Rep[n]_OUTPUT (*.csv)")[0]
		print('Input File: ' + self.fname)
	def refresh(self):
		try:
			global labelfinderpath
			dictDF = pd.read_csv(labelfinderpath)
			left = [self.list_labeldictionary.item(x).text() for x in range(self.list_labeldictionary.count())]
			right = [self.list_labeltofind.item(y).text() for y in range(self.list_labeltofind.count())]
			combined = right + left
			labels = dictDF['Label ID:'].tolist()
			for label in labels:
				if label not in combined:
					left.append(label)
			self.list_labeldictionary.clear()
			self.list_labeldictionary.addItems(left)
		except FileNotFoundError:
			self.Error1()
	def opendict(self):
		try:
			os.startfile('Label Finder Dictionary.csv')
		except FileNotFoundError:
			self.Error1()
	def process(self):
		if self.outdir != None:
			if self.fname != None:
				try:
					self.projectname = self.lineEdit.text()
					labels = [self.list_labeltofind.item(y).text() for y in range(self.list_labeltofind.count())]
					self.Message2()
					out = LabelFinder(self.fname,self.projectname,version='v4.3',labels=labels)
					out[0].to_csv(self.outdir + '/' + self.projectname + ' Label Efficiency.csv',index=False)
					out[1].to_csv(self.outdir + '/' + self.projectname + ' Tags.csv',index=False)
					self.Message1()
				except:
					traceback.print_exc()
					self.Error4()
			else:
				self.Error3()
		else:
			self.Error2()
	def Message1(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Message')
		msg.setText('Label Finder Complete. Files may be viewed at ' + self.outdir)
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Message2(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Message')
		msg.setText('Label Finder Initialized. Press OK to continue. A popup will appear when your run is complete.')
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def outputdir(self):
		self.outdir = QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, "Select Output Directory", self.workingdir)
		print('Output Directory: ' + self.outdir)

''' FITTING EFFICIENCY GUI '''
class Ui_FittingEfficiency(QtWidgets.QMainWindow):
	def __init__(self):
		global FEdefaultslst, icon
		self.FEdefaultslst = FEdefaultslst
		super().__init__()
		self.setObjectName("MainWindow")
		self.setWindowIcon(QtGui.QIcon(icon))
		self.resize(614, 440)
		self.centralwidget = QtWidgets.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.logo = QtWidgets.QTextBrowser(self.centralwidget)
		self.logo.setGeometry(QtCore.QRect(20, 10, 571, 111))
		self.logo.setObjectName("logo")
		self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox.setGeometry(QtCore.QRect(20, 220, 571, 121))
		self.groupBox.setObjectName("groupBox")
		self.formLayoutWidget = QtWidgets.QWidget(self.groupBox)
		self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 551, 88))
		self.formLayoutWidget.setObjectName("formLayoutWidget")
		self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
		self.formLayout.setContentsMargins(0, 0, 0, 0)
		self.formLayout.setObjectName("formLayout")
		self.label = QtWidgets.QLabel(self.formLayoutWidget)
		self.label.setObjectName("label")
		self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_2.setObjectName("label_2")
		self.horizontalLayout_2.addWidget(self.label_2)
		self.sb_CHlow = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
		self.sb_CHlow.setSingleStep(0.01)
		self.sb_CHlow.setProperty("value", float(self.FEdefaultslst[0]))
		self.sb_CHlow.setObjectName("sb_CHlow")
		self.horizontalLayout_2.addWidget(self.sb_CHlow)
		self.horizontalLayout.addLayout(self.horizontalLayout_2)
		self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_3.setObjectName("label_3")
		self.horizontalLayout.addWidget(self.label_3)
		self.sb_CHhigh = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
		self.sb_CHhigh.setSingleStep(0.01)
		self.sb_CHhigh.setProperty("value", float(self.FEdefaultslst[1]))
		self.sb_CHhigh.setObjectName("sb_CHhigh")
		self.horizontalLayout.addWidget(self.sb_CHhigh)
		self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
		self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_4.setObjectName("label_4")
		self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_4)
		self.sb_rsquared = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
		self.sb_rsquared.setMaximum(0.99)
		self.sb_rsquared.setSingleStep(0.01)
		self.sb_rsquared.setProperty("value", float(self.FEdefaultslst[2]))
		self.sb_rsquared.setObjectName("sb_rsquared")
		self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sb_rsquared)
		self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_5.setObjectName("label_5")
		self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
		self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_4.setObjectName("horizontalLayout_4")
		self.label_6 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_6.setObjectName("label_6")
		self.horizontalLayout_4.addWidget(self.label_6)
		self.sb_CI_low = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
		self.sb_CI_low.setSingleStep(0.01)
		self.sb_CI_low.setProperty("value", float(self.FEdefaultslst[3]))
		self.sb_CI_low.setObjectName("sb_CI_low")
		self.horizontalLayout_4.addWidget(self.sb_CI_low)
		self.horizontalLayout_3.addLayout(self.horizontalLayout_4)
		self.label_7 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_7.setObjectName("label_7")
		self.horizontalLayout_3.addWidget(self.label_7)
		self.sb_CI_high = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
		self.sb_CI_high.setSingleStep(0.01)
		self.sb_CI_high.setProperty("value", float(self.FEdefaultslst[4]))
		self.sb_CI_high.setObjectName("sb_CI_high")
		self.horizontalLayout_3.addWidget(self.sb_CI_high)
		self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
		self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_2.setGeometry(QtCore.QRect(20, 130, 571, 91))
		self.groupBox_2.setObjectName("groupBox_2")
		self.widget = QtWidgets.QWidget(self.groupBox_2)
		self.widget.setGeometry(QtCore.QRect(10, 20, 551, 24))
		self.widget.setObjectName("widget")
		self.formLayout_2 = QtWidgets.QFormLayout(self.widget)
		self.formLayout_2.setContentsMargins(0, 0, 0, 0)
		self.formLayout_2.setObjectName("formLayout_2")
		self.label_8 = QtWidgets.QLabel(self.widget)
		self.label_8.setObjectName("label_8")
		self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
		self.le_name = QtWidgets.QLineEdit(self.widget)
		self.le_name.setObjectName("le_name")
		self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_name)
		self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_2)
		self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 50, 549, 31))
		self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
		self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
		self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout_5.setObjectName("horizontalLayout_5")
		self.pb_input = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
		self.pb_input.setObjectName("pb_input")
		self.pb_input.pressed.connect(self.inputfile)
		self.horizontalLayout_5.addWidget(self.pb_input)
		self.pb_output = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
		self.pb_output.setObjectName("pb_output")
		self.pb_output.pressed.connect(self.outputdir)
		self.horizontalLayout_5.addWidget(self.pb_output)
		self.pb_process = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
		self.pb_process.setObjectName("pb_process")
		self.pb_process.clicked.connect(self.process)
		self.horizontalLayout_5.addWidget(self.pb_process)
		self.pb_return = QtWidgets.QPushButton(self.centralwidget)
		self.pb_return.setGeometry(QtCore.QRect(500, 350, 93, 28))
		self.pb_return.setObjectName("pb_return")
		self.pb_return.clicked.connect(self.close)
		self.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(self)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 614, 26))
		self.menubar.setObjectName("menubar")
		self.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(self)
		self.statusbar.setObjectName("statusbar")
		self.setStatusBar(self.statusbar)
		self.workingdir = os.getcwd()
		self.fname = None
		self.outdir = None

		self.retranslateUi(self)
		QtCore.QMetaObject.connectSlotsByName(self)

	def retranslateUi(self, MainWindow):
		global feLogo
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Fitting Efficiency"))
		self.logo.setHtml(_translate("MainWindow", f"<p style=\"text-align:center;\"><img src = \"{feLogo}\"></p>"))
		self.groupBox.setTitle(_translate("MainWindow", "Options"))
		self.label.setText(_translate("MainWindow", "1. CHalf Range:"))
		self.label_2.setText(_translate("MainWindow", "Low:"))
		self.label_3.setText(_translate("MainWindow", "High:"))
		self.label_4.setText(_translate("MainWindow", "2. R Squared"))
		self.label_5.setText(_translate("MainWindow", "3. Confidence Interval"))
		self.label_6.setText(_translate("MainWindow", "Low:"))
		self.label_7.setText(_translate("MainWindow", "High:"))
		self.groupBox_2.setTitle(_translate("MainWindow", "Project Information"))
		self.label_8.setText(_translate("MainWindow", "Output Name:"))
		self.pb_input.setText(_translate("MainWindow", "Select Input File"))
		self.pb_output.setText(_translate("MainWindow", "Select Output Directory"))
		self.pb_process.setText(_translate("MainWindow", "Process"))
		self.pb_return.setText(_translate("MainWindow", "Return"))
	
	def inputfile(self):
		self.fname = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, 'Open file', self.workingdir,"Combined_OUTPUT (*.csv)")[0]
		print('Input File: ' + self.fname)
	def outputdir(self):
		self.outdir = QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, "Select Output Directory", self.workingdir)
		print('Output Directory: ' + self.outdir)
	def process(self):
		if self.fname != None:
			if self.outdir != None:
				self.name = str(self.le_name.text())
				CHalflow = round(self.sb_CHlow.value(),2)
				CHalfhigh = round(self.sb_CHhigh.value(),2)
				rsquared = round(self.sb_rsquared.value(),2)
				confintlow = round(self.sb_CI_low.value(),2)
				confinthigh = round(self.sb_CI_high.value(),2)
				try:
					self.Message2()
					outputs = FittingEfficiency(self.fname,self.name,version='v4.3',CHalflow=CHalflow,CHalfhigh=CHalfhigh,rsquared=rsquared,confintlow=confintlow,confinthigh=confinthigh)
					os.chdir(self.outdir)
					outputs[0].to_csv(self.name + ' Fitting Efficiency.csv',index=False)
					outputs[1].to_csv(self.name + ' Label Sites.csv')
					outputs[2].to_csv(self.name + ' Fitted Peptides.csv',index=False)
					CLS = LabelSites_Combined(self.name + ' Label Sites.csv',version='4.2',MINIMUM_PTS=4,OUTLIER_CUTOFF=2,CHalflow=float(self.FEdefaultslst[0]),CHalfhigh=float(self.FEdefaultslst[1]),rsquared=float(self.FEdefaultslst[2]),confintlow=float(self.FEdefaultslst[3]),confinthigh=float(self.FEdefaultslst[4]))
					CLS[0].to_csv(self.name + ' Combined Label Sites.csv',index=True)
					CLS[1].to_csv(self.name + ' Removed Sites.csv',index=True)
					self.Message1()
				except Exception as e:
					self.error = e
					print(e)
					traceback.print_exc()
					self.Error3()
			else:
				self.Error2()
		else:
			self.Error1()
	def Error1(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('No input file selected. Please select one.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
		self.inputfile()
	def Error2(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('No output directory selected. Please select one.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
		self.outdir
	def Error3(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('Error in run. Check Print Statement.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Message1(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Message')
		msg.setText('Fitting Efficiency Complete. Files may be viewed at ' + str(self.outdir))
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Message2(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Message')
		msg.setText('Fitting Efficiency Initialized. Press OK to continue. A popup will appear when your run is complete.')
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def close(self):
		self.hide()
	
''' COMBINED SITE GUI '''
class Ui_CombinedSite(QtWidgets.QMainWindow):
	def __init__(self):
		global CSdefaultslst, icon
		self.CSdefaultslst = CSdefaultslst
		super().__init__()
		self.setObjectName("MainWindow")
		self.setWindowIcon(QtGui.QIcon(icon))
		self.resize(786, 464)
		self.centralwidget = QtWidgets.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_2.setGeometry(QtCore.QRect(20, 130, 421, 91))
		self.groupBox_2.setObjectName("groupBox_2")
		self.layoutWidget = QtWidgets.QWidget(self.groupBox_2)
		self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 401, 24))
		self.layoutWidget.setObjectName("layoutWidget")
		self.formLayout_2 = QtWidgets.QFormLayout(self.layoutWidget)
		self.formLayout_2.setContentsMargins(0, 0, 0, 0)
		self.formLayout_2.setObjectName("formLayout_2")
		self.label_8 = QtWidgets.QLabel(self.layoutWidget)
		self.label_8.setObjectName("label_8")
		self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
		self.le_name = QtWidgets.QLineEdit(self.layoutWidget)
		self.le_name.setObjectName("le_name")
		self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_name)
		self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_2)
		self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 50, 401, 31))
		self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
		self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
		self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout_5.setObjectName("horizontalLayout_5")
		self.pb_output = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
		self.pb_output.setObjectName("pb_output")
		self.pb_output.clicked.connect(self.outputdir)
		self.horizontalLayout_5.addWidget(self.pb_output)
		self.pb_process = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
		self.pb_process.setObjectName("pb_process")
		self.pb_process.clicked.connect(self.process)
		self.horizontalLayout_5.addWidget(self.pb_process)
		self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox.setGeometry(QtCore.QRect(450, 130, 311, 281))
		self.groupBox.setObjectName("groupBox")
		self.listWidget = QtWidgets.QListWidget(self.groupBox)
		self.listWidget.setGeometry(QtCore.QRect(10, 20, 291, 211))
		self.listWidget.setObjectName("listWidget")
		self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox)
		self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 240, 291, 31))
		self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.pb_add = QtWidgets.QPushButton(self.horizontalLayoutWidget)
		self.pb_add.setObjectName("pb_add")
		self.pb_add.clicked.connect(self.inputfile)
		self.horizontalLayout.addWidget(self.pb_add)
		self.pb_remove = QtWidgets.QPushButton(self.horizontalLayoutWidget)
		self.pb_remove.setObjectName("pb_remove")
		self.pb_remove.clicked.connect(self.del_item)
		self.horizontalLayout.addWidget(self.pb_remove)
		self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_3.setGeometry(QtCore.QRect(20, 220, 421, 141))
		self.groupBox_3.setObjectName("groupBox_3")
		self.formLayoutWidget = QtWidgets.QWidget(self.groupBox_3)
		self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 401, 106))
		self.formLayoutWidget.setObjectName("formLayoutWidget")
		self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
		self.formLayout.setContentsMargins(0, 0, 0, 0)
		self.formLayout.setObjectName("formLayout")
		self.label = QtWidgets.QLabel(self.formLayoutWidget)
		self.label.setObjectName("label")
		self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
		self.cb_file_type = QtWidgets.QComboBox(self.formLayoutWidget)
		self.cb_file_type.setObjectName("cb_file_type")
		self.cb_file_type.addItem("")
		self.cb_file_type.addItem("")
		self.cb_file_type.addItem("")
		self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cb_file_type)
		self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_2.setObjectName("label_2")
		self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
		self.sb_low = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
		self.sb_low.setSingleStep(0.01)
		self.sb_low.setProperty("value", float(self.CSdefaultslst[1]))
		self.sb_low.setObjectName("sb_low")
		self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sb_low)
		self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_3.setObjectName("label_3")
		self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
		self.sb_high = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
		self.sb_high.setMaximum(150.0)
		self.sb_high.setSingleStep(0.01)
		self.sb_high.setProperty("value", float(self.CSdefaultslst[2]))
		self.sb_high.setObjectName("sb_high")
		self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.sb_high)
		self.chb_dynamic = QtWidgets.QCheckBox(self.formLayoutWidget)
		self.chb_dynamic.setChecked(bool(self.CSdefaultslst[3]))
		self.chb_dynamic.setObjectName("chb_dynamic")
		self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.chb_dynamic)
		self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_4.setObjectName("label_4")
		self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
		self.logo = QtWidgets.QTextBrowser(self.centralwidget)
		self.logo.setGeometry(QtCore.QRect(20, 10, 741, 111))
		self.logo.setObjectName("logo")
		self.pb_return = QtWidgets.QPushButton(self.centralwidget)
		self.pb_return.setGeometry(QtCore.QRect(350, 370, 93, 28))
		self.pb_return.setObjectName("pb_return")
		self.pb_return.clicked.connect(self.close)
		self.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(self)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 786, 26))
		self.menubar.setObjectName("menubar")
		self.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(self)
		self.statusbar.setObjectName("statusbar")
		self.setStatusBar(self.statusbar)
		self.fname_lst = []
		self.outdir = None
		self.workingdir = os.getcwd()

		self.retranslateUi(self)
		QtCore.QMetaObject.connectSlotsByName(self)

	def retranslateUi(self, MainWindow):
		global csLogo
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Combined Site"))
		self.groupBox_2.setTitle(_translate("MainWindow", "Project Information"))
		self.label_8.setText(_translate("MainWindow", "Output Name:"))
		self.pb_output.setText(_translate("MainWindow", "Select Output Directory"))
		self.pb_process.setText(_translate("MainWindow", "Process"))
		self.groupBox.setTitle(_translate("MainWindow", "Files"))
		self.pb_add.setText(_translate("MainWindow", "Add"))
		self.pb_remove.setText(_translate("MainWindow", "Remove"))
		self.groupBox_3.setTitle(_translate("MainWindow", "Options"))
		self.label.setText(_translate("MainWindow", "File Type:"))
		self.cb_file_type.setItemText(0, _translate("MainWindow", ".svg"))
		self.cb_file_type.setItemText(1, _translate("MainWindow", ".jpg"))
		self.cb_file_type.setItemText(2, _translate("MainWindow", ".png"))
		if self.CSdefaultslst[0] == '.svg':
			self.cb_file_type.setCurrentIndex(0)
		elif self.CSdefaultslst[0] == '.jpg':
			self.cb_file_type.setCurrentIndex(1)
		elif self.CSdefaultslst[0] == '.png':
			self.cb_file_type.setCurrentIndex(2)
		else:
			self.cb_file_type.setCurrentIndex(0)
		self.label_2.setText(_translate("MainWindow", "Low Bound:"))
		self.label_3.setText(_translate("MainWindow", "High Bound:"))
		self.chb_dynamic.setText(_translate("MainWindow", "Dynamic Y-Axis"))
		self.label_4.setText(_translate("MainWindow", "Other:"))
		self.logo.setHtml(_translate("MainWindow", f"<p style=\"text-align:center;\"><img src = \"{csLogo}\"></p>"))
		self.pb_return.setText(_translate("MainWindow", "Return"))
	
	def inputfile(self):
		self.fname_lst += QtWidgets.QFileDialog.getOpenFileNames(self.centralwidget, 'Open file', self.workingdir,"Label Sites.csv (*.csv)")[0]
		print('Input Files:')
		print(*self.fname_lst, sep='\n')
		self.listWidget.clear()
		self.listWidget.addItems(self.fname_lst)
	def outputdir(self):
		self.outdir = QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, "Select Output Directory", self.workingdir)
		print('Output Directory: ' + self.outdir)
	def del_item(self):
		items = self.listWidget.selectedItems()
		for item in items:
			self.fname_lst.remove(item.text())
		self.listWidget.clear()
		self.listWidget.addItems(self.fname_lst)
	def process(self):
		if self.outdir != None:
			if len(self.fname_lst) > 1:
				try:
					self.Message2()
					self.name = self.le_name.text()
					dynamic = self.chb_dynamic.isChecked()
					ymin = self.sb_low.value()
					ymax = self.sb_high.value()
					file_type = self.cb_file_type.currentText()
					CombinedSite(self.fname_lst,self.outdir,self.name,version='v4.3',dynamic=dynamic,min=ymin,max=ymax,file_type=file_type)
					self.Message1()
				except:
					self.Error3()
					traceback.print_exc()
			else:
				self.Error1()
		else:
			self.Error2()
	def Error1(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('Not enough inputs selected. Please select at least two.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error2(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('No output directory selected. Please select one.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error3(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('Error in run. Check Print Statement.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Message1(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Message')
		msg.setText('Combined Site Complete. Files may be viewed at ' + str(self.outdir))
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Message2(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Message')
		msg.setText('Combined Site Initialized. Press OK to continue. A popup will appear when your run is complete.')
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def close(self):
		self.hide()

''' PROTEIN MAPPER GUI (Residue Mapper) '''
class Ui_ProteinMapper(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		global RMdefaultslst, CHdefaultslst, icon
		self.RMdefaultslst = RMdefaultslst
		self.labels = CHdefaultslst[23]
		self.setObjectName("MainWindow")
		self.setWindowIcon(QtGui.QIcon(icon))
		self.resize(616, 448)
		self.centralwidget = QtWidgets.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_2.setGeometry(QtCore.QRect(20, 130, 571, 91))
		self.groupBox_2.setObjectName("groupBox_2")
		self.layoutWidget = QtWidgets.QWidget(self.groupBox_2)
		self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 551, 24))
		self.layoutWidget.setObjectName("layoutWidget")
		self.formLayout_2 = QtWidgets.QFormLayout(self.layoutWidget)
		self.formLayout_2.setContentsMargins(0, 0, 0, 0)
		self.formLayout_2.setObjectName("formLayout_2")
		#self.label_8 = QtWidgets.QLabel(self.layoutWidget)
		#self.label_8.setObjectName("label_8")
		#self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
		#self.le_name = QtWidgets.QLineEdit(self.layoutWidget)
		#self.le_name.setObjectName("le_name")
		#self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_name)
		self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_2)
		self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 25, 549, 31))
		self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
		self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
		self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout_5.setObjectName("horizontalLayout_5")
		self.pb_input = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
		self.pb_input.setObjectName("pb_input")
		self.horizontalLayout_5.addWidget(self.pb_input)
		self.pb_output = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
		self.pb_output.setObjectName("pb_output")
		self.horizontalLayout_5.addWidget(self.pb_output)
		self.pb_process = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
		self.pb_process.setObjectName("pb_process")
		self.horizontalLayout_5.addWidget(self.pb_process)
		self.logo = QtWidgets.QTextBrowser(self.centralwidget)
		self.logo.setGeometry(QtCore.QRect(20, 10, 571, 111))
		self.logo.setObjectName("logo")
		self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_3.setGeometry(QtCore.QRect(20, 220, 571, 141))
		self.groupBox_3.setObjectName("groupBox_3")
		self.formLayoutWidget = QtWidgets.QWidget(self.groupBox_3)
		self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 551, 106))
		self.formLayoutWidget.setObjectName("formLayoutWidget")
		self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
		self.formLayout.setContentsMargins(0, 0, 0, 0)
		self.formLayout.setObjectName("formLayout")
		self.label = QtWidgets.QLabel(self.formLayoutWidget)
		self.label.setObjectName("label")
		self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
		self.cb_file_type = QtWidgets.QComboBox(self.formLayoutWidget)
		self.cb_file_type.setObjectName("cb_file_type")
		self.cb_file_type.addItem("")
		self.cb_file_type.addItem("")
		self.cb_file_type.addItem("")
		self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cb_file_type)
		self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_2.setObjectName("label_2")
		self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
		self.sb_low = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
		self.sb_low.setSingleStep(0.01)
		self.sb_low.setProperty("value", float(self.RMdefaultslst[1]))
		self.sb_low.setObjectName("sb_low")
		self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sb_low)
		self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_3.setObjectName("label_3")
		self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
		self.sb_high = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
		self.sb_high.setMaximum(150.0)
		self.sb_high.setSingleStep(0.01)
		self.sb_high.setProperty("value", float(self.RMdefaultslst[2]))
		self.sb_high.setObjectName("sb_high")
		self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.sb_high)
		self.chb_dynamic = QtWidgets.QCheckBox(self.formLayoutWidget)
		self.chb_dynamic.setChecked(bool(self.RMdefaultslst[3]))
		self.chb_dynamic.setObjectName("chb_dynamic")
		self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.chb_dynamic)
		self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_4.setObjectName("label_4")
		self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
		self.pb_return = QtWidgets.QPushButton(self.centralwidget)
		self.pb_return.setGeometry(QtCore.QRect(500, 370, 93, 28))
		self.pb_return.setObjectName("pb_return")
		self.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(self)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 616, 26))
		self.menubar.setObjectName("menubar")
		self.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(self)
		self.statusbar.setObjectName("statusbar")
		self.setStatusBar(self.statusbar)
		self.fname = None
		self.outdir = None
		self.pb_input.clicked.connect(self.inputfile)
		self.pb_output.clicked.connect(self.outputdir)
		self.pb_process.clicked.connect(self.process)
		self.pb_return.clicked.connect(self.close)
		self.workingdir = os.getcwd()

		self.retranslateUi(self)
		QtCore.QMetaObject.connectSlotsByName(self)

	def retranslateUi(self, MainWindow):
		global pmLogo
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Residue Mapper"))
		self.groupBox_2.setTitle(_translate("MainWindow", "Project Information"))
		#self.label_8.setText(_translate("MainWindow", "Output Name:"))
		self.pb_input.setText(_translate("MainWindow", "Select Input File"))
		self.pb_output.setText(_translate("MainWindow", "Select Output Directory"))
		self.pb_process.setText(_translate("MainWindow", "Process"))
		self.logo.setHtml(_translate("MainWindow", f"<p style=\"text-align:center;\"><img src = \"{pmLogo}\"></p>"))
		self.groupBox_3.setTitle(_translate("MainWindow", "Options"))
		self.label.setText(_translate("MainWindow", "File Type:"))
		self.cb_file_type.setItemText(0, _translate("MainWindow", ".svg"))
		self.cb_file_type.setItemText(1, _translate("MainWindow", ".jpg"))
		self.cb_file_type.setItemText(2, _translate("MainWindow", ".png"))
		if self.RMdefaultslst[0] == '.svg':
			self.cb_file_type.setCurrentIndex(0)
		elif self.RMdefaultslst[0] == '.jpg':
			self.cb_file_type.setCurrentIndex(1)
		elif self.RMdefaultslst[0] == '.png':
			self.cb_file_type.setCurrentIndex(2)
		else:
			self.cb_file_type.setCurrentIndex(0)
		self.label_2.setText(_translate("MainWindow", "Low Bound:"))
		self.label_3.setText(_translate("MainWindow", "High Bound:"))
		self.chb_dynamic.setText(_translate("MainWindow", "Dynamic Y-Axis"))
		self.label_4.setText(_translate("MainWindow", "Other:"))
		self.pb_return.setText(_translate("MainWindow", "Return"))

	def inputfile(self):
		self.fname = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, 'Open file', self.workingdir,"Combined Label Sites.csv (*.csv)")[0]
		print('Input File: ' + self.fname)
	def outputdir(self):
		self.outdir = QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, "Select Output Directory", self.workingdir)
		print('Output Directory: ' + self.outdir)
	def process(self):
		if self.outdir != None:
			if self.fname != None:
				try:
					self.Message2()
					#self.name = self.le_name.text()
					dynamic = self.chb_dynamic.isChecked()
					ymin = self.sb_low.value()
					ymax = self.sb_high.value()
					file_type = self.cb_file_type.currentText()
					ResidueMapper_2(self.fname,self.outdir,version='v4.3',dynamic=dynamic,min=ymin,max=ymax,file_type=file_type,labels=self.labels)
					self.Message1()
				except:
					self.Error3()
					traceback.print_exc()
			else:
				self.Error2()
		else:
			self.Error1()
	def Error1(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('No input selected. Please select one.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
		self.inputfile()
	def Error2(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('No output directory selected. Please select one.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
		self.outputdir()
	def Error3(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('Error in run. Check Print Statement.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Message1(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Message')
		msg.setText('Residue Mapper Complete. Files may be viewed at ' + str(self.outdir))
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Message2(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Message')
		msg.setText('Residue Mapper Initialized. Press OK to continue. A popup will appear when your run is complete.')
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def close(self):
		self.hide()

''' COMBINED RESIDUE MAPPER GUI '''
class Ui_CombinedResidueMapper(QtWidgets.QMainWindow):
	def __init__(self):
		global CRMdefaultslst, CHdefaultslst, icon
		self.CRMdefaultslst = CRMdefaultslst
		self.labels = CHdefaultslst[23]
		super().__init__()
		self.setObjectName("MainWindow")
		self.setWindowIcon(QtGui.QIcon(icon))
		self.resize(786, 464)
		self.centralwidget = QtWidgets.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_2.setGeometry(QtCore.QRect(20, 130, 421, 91))
		self.groupBox_2.setObjectName("groupBox_2")
		self.layoutWidget = QtWidgets.QWidget(self.groupBox_2)
		self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 401, 24))
		self.layoutWidget.setObjectName("layoutWidget")
		self.formLayout_2 = QtWidgets.QFormLayout(self.layoutWidget)
		self.formLayout_2.setContentsMargins(0, 0, 0, 0)
		self.formLayout_2.setObjectName("formLayout_2")
		self.label_8 = QtWidgets.QLabel(self.layoutWidget)
		self.label_8.setObjectName("label_8")
		self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
		self.le_name = QtWidgets.QLineEdit(self.layoutWidget)
		self.le_name.setObjectName("le_name")
		self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_name)
		self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_2)
		self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(10, 50, 401, 31))
		self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
		self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
		self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout_5.setObjectName("horizontalLayout_5")
		self.pb_output = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
		self.pb_output.setObjectName("pb_output")
		self.pb_output.clicked.connect(self.outputdir)
		self.horizontalLayout_5.addWidget(self.pb_output)
		self.pb_process = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
		self.pb_process.setObjectName("pb_process")
		self.pb_process.clicked.connect(self.process)
		self.horizontalLayout_5.addWidget(self.pb_process)
		self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox.setGeometry(QtCore.QRect(450, 130, 311, 281))
		self.groupBox.setObjectName("groupBox")
		self.listWidget = QtWidgets.QListWidget(self.groupBox)
		self.listWidget.setGeometry(QtCore.QRect(10, 20, 291, 211))
		self.listWidget.setObjectName("listWidget")
		self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox)
		self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 240, 291, 31))
		self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.pb_add = QtWidgets.QPushButton(self.horizontalLayoutWidget)
		self.pb_add.setObjectName("pb_add")
		self.pb_add.clicked.connect(self.inputfile)
		self.horizontalLayout.addWidget(self.pb_add)
		self.pb_remove = QtWidgets.QPushButton(self.horizontalLayoutWidget)
		self.pb_remove.setObjectName("pb_remove")
		self.pb_remove.clicked.connect(self.del_item)
		self.horizontalLayout.addWidget(self.pb_remove)
		self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_3.setGeometry(QtCore.QRect(20, 220, 421, 141))
		self.groupBox_3.setObjectName("groupBox_3")
		self.formLayoutWidget = QtWidgets.QWidget(self.groupBox_3)
		self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 401, 106))
		self.formLayoutWidget.setObjectName("formLayoutWidget")
		self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
		self.formLayout.setContentsMargins(0, 0, 0, 0)
		self.formLayout.setObjectName("formLayout")
		self.label = QtWidgets.QLabel(self.formLayoutWidget)
		self.label.setObjectName("label")
		self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
		self.cb_file_type = QtWidgets.QComboBox(self.formLayoutWidget)
		self.cb_file_type.setObjectName("cb_file_type")
		self.cb_file_type.addItem("")
		self.cb_file_type.addItem("")
		self.cb_file_type.addItem("")
		self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cb_file_type)
		self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_2.setObjectName("label_2")
		self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
		self.sb_low = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
		self.sb_low.setSingleStep(0.01)
		self.sb_low.setProperty("value", float(self.CRMdefaultslst[1]))
		self.sb_low.setObjectName("sb_low")
		self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sb_low)
		self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_3.setObjectName("label_3")
		self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
		self.sb_high = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
		self.sb_high.setMaximum(150.0)
		self.sb_high.setSingleStep(0.01)
		self.sb_high.setProperty("value", float(self.CRMdefaultslst[2]))
		self.sb_high.setObjectName("sb_high")
		self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.sb_high)
		self.chb_dynamic = QtWidgets.QCheckBox(self.formLayoutWidget)
		self.chb_dynamic.setChecked(bool(self.CRMdefaultslst[3]))
		self.chb_dynamic.setObjectName("chb_dynamic")
		self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.chb_dynamic)
		self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_4.setObjectName("label_4")
		self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
		self.logo = QtWidgets.QTextBrowser(self.centralwidget)
		self.logo.setGeometry(QtCore.QRect(20, 10, 741, 111))
		self.logo.setObjectName("logo")
		self.pb_return = QtWidgets.QPushButton(self.centralwidget)
		self.pb_return.setGeometry(QtCore.QRect(350, 370, 93, 28))
		self.pb_return.setObjectName("pb_return")
		self.pb_return.clicked.connect(self.close)
		self.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(self)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 786, 26))
		self.menubar.setObjectName("menubar")
		self.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(self)
		self.statusbar.setObjectName("statusbar")
		self.setStatusBar(self.statusbar)
		self.fname_lst = []
		self.outdir = None
		self.workingdir = os.getcwd()

		self.retranslateUi(self)
		QtCore.QMetaObject.connectSlotsByName(self)

	def retranslateUi(self, MainWindow):
		global crmLogo
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Combined Residue Mapper"))
		self.groupBox_2.setTitle(_translate("MainWindow", "Project Information"))
		self.label_8.setText(_translate("MainWindow", "Output Name:"))
		self.pb_output.setText(_translate("MainWindow", "Select Output Directory"))
		self.pb_process.setText(_translate("MainWindow", "Process"))
		self.groupBox.setTitle(_translate("MainWindow", "Files"))
		self.pb_add.setText(_translate("MainWindow", "Add"))
		self.pb_remove.setText(_translate("MainWindow", "Remove"))
		self.groupBox_3.setTitle(_translate("MainWindow", "Options"))
		self.label.setText(_translate("MainWindow", "File Type:"))
		self.cb_file_type.setItemText(0, _translate("MainWindow", ".svg"))
		self.cb_file_type.setItemText(1, _translate("MainWindow", ".jpg"))
		self.cb_file_type.setItemText(2, _translate("MainWindow", ".png"))
		if self.CRMdefaultslst[0] == '.svg':
			self.cb_file_type.setCurrentIndex(0)
		elif self.CRMdefaultslst[0] == '.jpg':
			self.cb_file_type.setCurrentIndex(1)
		elif self.CRMdefaultslst[0] == '.png':
			self.cb_file_type.setCurrentIndex(2)
		else:
			self.cb_file_type.setCurrentIndex(0)
		self.label_2.setText(_translate("MainWindow", "Low Bound:"))
		self.label_3.setText(_translate("MainWindow", "High Bound:"))
		self.chb_dynamic.setText(_translate("MainWindow", "Dynamic Y-Axis"))
		self.label_4.setText(_translate("MainWindow", "Other:"))
		self.logo.setHtml(_translate("MainWindow", f"<p style=\"text-align:center;\"><img src = \"{crmLogo}\"></p>"))
		self.pb_return.setText(_translate("MainWindow", "Return"))
	
	def inputfile(self):
		self.fname_lst += QtWidgets.QFileDialog.getOpenFileNames(self.centralwidget, 'Open file', self.workingdir,"Combined Label Sites.csv (*.csv)")[0]
		print('Input Files:')
		print(*self.fname_lst, sep='\n')
		self.listWidget.clear()
		self.listWidget.addItems(self.fname_lst)
	def outputdir(self):
		self.outdir = QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, "Select Output Directory", self.workingdir)
		print('Output Directory: ' + self.outdir)
	def del_item(self):
		items = self.listWidget.selectedItems()
		for item in items:
			self.fname_lst.remove(item.text())
		self.listWidget.clear()
		self.listWidget.addItems(self.fname_lst)
	def process(self):
		if self.outdir != None:
			if len(self.fname_lst) > 1:
				try:
					self.Message2()
					self.name = self.le_name.text()
					dynamic = self.chb_dynamic.isChecked()
					ymin = self.sb_low.value()
					ymax = self.sb_high.value()
					file_type = self.cb_file_type.currentText()
					CombinedResidueMapper_2(self.fname_lst,self.outdir,self.name,version='v4.3',dynamic=dynamic,min=ymin,max=ymax,file_type=file_type,labels=self.labels)
					self.Message1()
				except:
					self.Error3()
					traceback.print_exc()
			else:
				self.Error1()
		else:
			self.Error2()
	def Error1(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('Not enough inputs selected. Please select at least two.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error2(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('No output directory selected. Please select one.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error3(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('Error in run. Check Print Statement.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Message1(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Message')
		msg.setText('Combined Residue Mapper Complete. Files may be viewed at ' + str(self.outdir))
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Message2(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Message')
		msg.setText('Combined Residue Mapper Initialized. Press OK to continue. A popup will appear when your run is complete.')
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def close(self):
		self.hide()

''' CONDITION CREATOR GUI '''
class Ui_ConditionCreator(QtWidgets.QMainWindow):
	def __init__(self): #setupUi(self, MainWindow)
		super().__init__()
		global CHdefaultslst, FEdefaultslst, icon
		self.CHdefaultslst = CHdefaultslst
		self.FEdefaultslst = FEdefaultslst
		self.create_done = False
		self.condition_created = False
		self.setObjectName("MainWindow")
		self.setWindowIcon(QtGui.QIcon(icon))
		self.resize(806, 605)
		self.centralwidget = QtWidgets.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
		self.textBrowser.setGeometry(QtCore.QRect(40, 0, 721, 111))
		self.textBrowser.setObjectName("textBrowser")
		self.instructions = QtWidgets.QLabel(self.centralwidget)
		self.instructions.setGeometry(QtCore.QRect(40, 510, 340, 41))
		self.instructions.setText('Instructions: Specify condition settings; press Create; add input files; press Process; press Return.')
		self.instructions.setWordWrap(True)
		self.instructions.setObjectName('instructions')
		self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
		self.horizontalLayoutWidget.setGeometry(QtCore.QRect(390, 510, 371, 41))
		self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.pb_input = QtWidgets.QPushButton(self.horizontalLayoutWidget)
		self.pb_input.setObjectName("pb_input")
		self.pb_input.clicked.connect(self.create)
		self.horizontalLayout.addWidget(self.pb_input)
		self.pb_process = QtWidgets.QPushButton(self.horizontalLayoutWidget)
		self.pb_process.setObjectName("pb_process")
		self.pb_process.clicked.connect(self.process)
		self.horizontalLayout.addWidget(self.pb_process)
		self.pb_return = QtWidgets.QPushButton(self.horizontalLayoutWidget)
		self.pb_return.setObjectName("pb_return")
		self.pb_return.clicked.connect(self.returnbutton)
		self.horizontalLayout.addWidget(self.pb_return)
		self.pb_cancel = QtWidgets.QPushButton(self.horizontalLayoutWidget)
		self.pb_cancel.setObjectName("pb_cancel")
		self.pb_cancel.clicked.connect(self.cancel)
		self.horizontalLayout.addWidget(self.pb_cancel)
		self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
		self.tabWidget.setGeometry(QtCore.QRect(40, 120, 721, 391))
		self.tabWidget.setObjectName("tabWidget")
		self.tab = QtWidgets.QWidget()
		self.tab.setObjectName("tab")
		self.formLayoutWidget = QtWidgets.QWidget(self.tab)
		self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 691, 111))
		self.formLayoutWidget.setObjectName("formLayoutWidget")
		self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
		self.formLayout.setContentsMargins(0, 0, 0, 0)
		self.formLayout.setObjectName("formLayout")
		self.label = QtWidgets.QLabel(self.formLayoutWidget)
		self.label.setObjectName("label")
		self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
		self.le_conditionname = QtWidgets.QLineEdit(self.formLayoutWidget)
		self.le_conditionname.setObjectName("le_conditionname")
		self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_conditionname)
		self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_3.setObjectName("label_3")
		self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
		self.spinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
		self.spinBox.setMinimum(1)
		self.spinBox.setValue(int(self.CHdefaultslst[1]))
		self.spinBox.setObjectName("spinBox") #Reps
		self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBox)
		self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_4.setObjectName("label_4")
		self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
		self.cb_CDHD = QtWidgets.QComboBox(self.formLayoutWidget)
		self.cb_CDHD.setObjectName("cb_CDHD")
		self.cb_CDHD.addItem("")
		self.cb_CDHD.addItem("")
		self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cb_CDHD)
		self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
		self.label_5.setObjectName("label_5")
		self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
		self.sb_conc = QtWidgets.QSpinBox(self.formLayoutWidget)
		self.sb_conc.setMinimum(2)
		self.sb_conc.setProperty("value", int(self.CHdefaultslst[3]))
		self.conc = self.sb_conc.value()
		self.sb_conc.setObjectName("sb_conc")
		self.sb_conc.valueChanged.connect(self.sbchange)
		self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.sb_conc)
		self.CalculationOPtions = QtWidgets.QGroupBox(self.tab)
		self.CalculationOPtions.setGeometry(QtCore.QRect(0, 130, 471, 231))
		self.CalculationOPtions.setObjectName("CalculationOPtions")
		self.formLayoutWidget_2 = QtWidgets.QWidget(self.CalculationOPtions)
		self.formLayoutWidget_2.setGeometry(QtCore.QRect(20, 30, 171, 191))
		self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
		self.gridLayout = QtWidgets.QGridLayout(self.formLayoutWidget_2)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.cb_RepGr = QtWidgets.QCheckBox(self.formLayoutWidget_2)
		self.cb_RepGr.setChecked(bool(self.CHdefaultslst[5]))
		self.cb_RepGr.setObjectName("cb_RepGr")
		self.gridLayout.addWidget(self.cb_RepGr, 1, 0, 1, 1)
		self.cb_RemOut = QtWidgets.QCheckBox(self.formLayoutWidget_2)
		self.cb_RemOut.setChecked(bool(self.CHdefaultslst[7]))
		self.cb_RemOut.setObjectName("cb_RemOut")
		self.gridLayout.addWidget(self.cb_RemOut, 3, 0, 1, 1)
		self.cb_GOut = QtWidgets.QCheckBox(self.formLayoutWidget_2)
		self.cb_GOut.setChecked(bool(self.CHdefaultslst[9]))
		self.cb_GOut.setObjectName("cb_GOut")
		self.gridLayout.addWidget(self.cb_GOut, 5, 0, 1, 1)
		self.cb_CombAn = QtWidgets.QCheckBox(self.formLayoutWidget_2)
		self.cb_CombAn.setChecked(bool(self.CHdefaultslst[6]))
		self.cb_CombAn.setObjectName("cb_CombAn")
		self.gridLayout.addWidget(self.cb_CombAn, 2, 0, 1, 1)
		self.cb_GrComb = QtWidgets.QCheckBox(self.formLayoutWidget_2)
		self.cb_GrComb.setChecked(bool(self.CHdefaultslst[8]))
		self.cb_GrComb.setObjectName("cb_GrComb")
		self.gridLayout.addWidget(self.cb_GrComb, 4, 0, 1, 1)
		self.cb_IndRepAn = QtWidgets.QCheckBox(self.formLayoutWidget_2)
		self.cb_IndRepAn.setChecked(bool(self.CHdefaultslst[4]))
		self.cb_IndRepAn.setObjectName("cb_IndRepAn")
		self.gridLayout.addWidget(self.cb_IndRepAn, 0, 0, 1, 1)
		self.gridLayoutWidget_2 = QtWidgets.QWidget(self.CalculationOPtions)
		self.gridLayoutWidget_2.setGeometry(QtCore.QRect(210, 30, 241, 61))
		self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
		self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
		self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_3.setObjectName("gridLayout_3")
		self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget_2)
		self.label_2.setObjectName("label_2")
		self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
		self.spin_minpts = QtWidgets.QSpinBox(self.gridLayoutWidget_2)
		self.spin_minpts.setProperty("value", int(self.CHdefaultslst[10]))
		self.spin_minpts.setObjectName("spin_minpts")
		self.gridLayout_3.addWidget(self.spin_minpts, 0, 1, 1, 1)
		self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget_2)
		self.label_6.setObjectName("label_6")
		self.gridLayout_3.addWidget(self.label_6, 1, 0, 1, 1)
		self.spin_stderror = QtWidgets.QSpinBox(self.gridLayoutWidget_2)
		self.spin_stderror.setProperty("value", int(self.CHdefaultslst[11]))
		self.spin_stderror.setObjectName("spin_stderror")
		self.gridLayout_3.addWidget(self.spin_stderror, 1, 1, 1, 1)
		self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.CalculationOPtions)
		self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(210, 90, 241, 131))
		self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
		self.GraphFilters = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
		self.GraphFilters.setContentsMargins(0, 0, 0, 0)
		self.GraphFilters.setObjectName("GraphFilters")
		self.groupBox_3 = QtWidgets.QGroupBox(self.verticalLayoutWidget_2)
		self.groupBox_3.setObjectName("groupBox_3")
		self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox_3)
		self.gridLayoutWidget.setGeometry(QtCore.QRect(60, 20, 179, 80))
		self.gridLayoutWidget.setObjectName("gridLayoutWidget")
		self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
		self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label_7.setObjectName("label_7")
		self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 1, QtCore.Qt.AlignRight)
		self.le_CI = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
		self.le_CI.setObjectName("le_CI")
		self.gridLayout_2.addWidget(self.le_CI, 1, 1, 1, 1)
		self.le_R2 = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
		self.le_R2.setObjectName("le_R2")
		self.gridLayout_2.addWidget(self.le_R2, 2, 1, 1, 1)
		self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label_8.setObjectName("label_8")
		self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1, QtCore.Qt.AlignRight)
		self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
		self.label_9.setObjectName("label_9")
		self.gridLayout_2.addWidget(self.label_9, 3, 0, 1, 1, QtCore.Qt.AlignRight)
		self.le_CHrange = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
		self.le_CHrange.setObjectName("le_CHrange")
		self.gridLayout_2.addWidget(self.le_CHrange, 3, 1, 1, 1)
		self.GraphFilters.addWidget(self.groupBox_3)
		self.OtherFeatures = QtWidgets.QGroupBox(self.tab)
		self.OtherFeatures.setGeometry(QtCore.QRect(470, 130, 241, 231))
		self.OtherFeatures.setObjectName("OtherFeatures")
		self.gridLayoutWidget_7 = QtWidgets.QWidget(self.OtherFeatures)
		self.gridLayoutWidget_7.setGeometry(QtCore.QRect(20, 30, 197, 191))
		self.gridLayoutWidget_7.setObjectName("gridLayoutWidget_7")
		self.gridLayout_6 = QtWidgets.QGridLayout(self.gridLayoutWidget_7)
		self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_6.setObjectName("gridLayout_6")
		self.cb_PM = QtWidgets.QCheckBox(self.gridLayoutWidget_7)
		self.cb_PM.setChecked(True)
		self.cb_PM.setObjectName("cb_PM")
		self.cb_PM.clicked.connect(self.FE_CS_PM)
		self.gridLayout_6.addWidget(self.cb_PM, 3, 0, 1, 1)
		self.cb_LE = QtWidgets.QCheckBox(self.gridLayoutWidget_7)
		self.cb_LE.setChecked(True)
		self.cb_LE.setObjectName("cb_LE")
		self.gridLayout_6.addWidget(self.cb_LE, 0, 0, 1, 1)
		self.cb_RCS = QtWidgets.QCheckBox(self.gridLayoutWidget_7)
		self.cb_RCS.setChecked(True)
		self.cb_RCS.setObjectName("cb_RCS")
		self.cb_RCS.clicked.connect(self.FE_CS_PM)
		self.gridLayout_6.addWidget(self.cb_RCS, 2, 0, 1, 1)
		self.label_dynamic = QtWidgets.QLabel(self.gridLayoutWidget_7)
		self.label_dynamic.setObjectName("label_dynamic")
		self.label_dynamic.setText('Y-axis options for CS and RM:') #(Note: these must be the same across all conditions for CS)
		self.gridLayout_6.addWidget(self.label_dynamic, 4, 0, 1, 1)
		self.cb_RCS_dynamic = QtWidgets.QCheckBox(self.gridLayoutWidget_7)
		self.cb_RCS_dynamic.setChecked(False)
		self.cb_RCS_dynamic.setObjectName("cb_RCS_dynamic")
		self.gridLayout_6.addWidget(self.cb_RCS_dynamic, 5, 0, 1, 1)
		self.minmax_gridwidget = QtWidgets.QWidget(self.gridLayoutWidget_7)
		self.minmax_gridwidget.setGeometry(QtCore.QRect(20, 30, 197, 191))
		self.minmax_gridwidget.setObjectName("minmax_gridwidget")
		self.minmaxLayout = QtWidgets.QGridLayout(self.minmax_gridwidget)
		self.minmaxLayout.setContentsMargins(0, 0, 0, 0)
		self.minmaxLayout.setObjectName("gridLayout_6")
		self.gridLayout_6.addWidget(self.minmax_gridwidget, 6, 0, 1, 1)
		self.cb_FE = QtWidgets.QCheckBox(self.gridLayoutWidget_7)
		self.cb_FE.setChecked(True)
		self.cb_FE.setObjectName("cb_FE")
		self.cb_FE.clicked.connect(self.FE_CS_PM)
		self.gridLayout_6.addWidget(self.cb_FE, 1, 0, 1, 1)
		self.label_min = QtWidgets.QLabel(self.minmax_gridwidget)
		self.label_min.setObjectName("label_min")
		self.minmaxLayout.addWidget(self.label_min, 5, 0, 1, 1)
		self.le_min = QtWidgets.QDoubleSpinBox(self.minmax_gridwidget)
		self.le_min.setObjectName("le_min")
		self.le_min.valueChanged.connect(self.nodynamic)
		self.minmaxLayout.addWidget(self.le_min, 5, 1, 1, 1)
		self.label_max = QtWidgets.QLabel(self.minmax_gridwidget)
		self.label_max.setObjectName("label_max")
		self.minmaxLayout.addWidget(self.label_max, 5, 2, 1, 1)
		self.le_max = QtWidgets.QDoubleSpinBox(self.minmax_gridwidget)
		self.le_max.setObjectName("le_max")
		self.le_max.valueChanged.connect(self.nodynamic)
		self.minmaxLayout.addWidget(self.le_max, 5, 3, 1, 1)
		self.label_note = QtWidgets.QLabel(self.gridLayoutWidget_7)
		self.label_note.setObjectName("label_note")
		self.label_note.setText('Note: these must be the same across all conditions for CS')
		self.label_note.setWordWrap(True)
		self.gridLayout_6.addWidget(self.label_note, 7, 0, 2, 1)
		self.tabWidget.addTab(self.tab, "")
		self.tab_2 = QtWidgets.QWidget()
		self.tab_2.setObjectName("tab_2")
		self.table_conc = QtWidgets.QTableWidget(self.tab_2)
		self.table_conc.setGeometry(QtCore.QRect(10, 10, 691, 341))
		self.table_conc.setDragEnabled(False)
		self.table_conc.setAlternatingRowColors(True)
		self.table_conc.setObjectName("table_conc")
		self.table_conc.horizontalHeader().setStretchLastSection(True)
		self.table_conc.setColumnCount(1)
		self.table_conc.setRowCount(self.conc)
		item = QtWidgets.QTableWidgetItem()
		self.table_conc.setHorizontalHeaderItem(0, item)
		defaultconc = self.CHdefaultslst[22] #[0,0.43,0.87,1.3,1.74,2.17,2.61,3.04,3.48,3.59]
		for i in range(len(defaultconc)):
			item = QtWidgets.QTableWidgetItem()
			item.setText(str(defaultconc[i]))
			self.table_conc.setItem(i,0, item)
		self.tabWidget.addTab(self.tab_2, "")
		self.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(self)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 806, 26))
		self.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(self)
		self.statusbar.setObjectName("statusbar")
		self.setStatusBar(self.statusbar)
		self.retranslateUi(self)
		self.tabWidget.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(self)

	def retranslateUi(self, MainWindow):
		global mainLogo
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Condition Creator"))
		self.textBrowser.setHtml(_translate("MainWindow", f"<p style=\"text-align:center;\"><img src = \"{mainLogo}\"></p>"))
		self.pb_input.setToolTip(_translate("MainWindow", "<html><head/><body><p>Creates condition folder and opens for inputting \'protein-peptides.csv\' and \'proteins.csv\' files</p></body></html>"))
		self.pb_input.setText(_translate("MainWindow", "1. Create"))
		self.pb_process.setToolTip(_translate("MainWindow", "<html><head/><body><p>Creates Masterfile for condition</p></body></html>"))
		self.pb_process.setText(_translate("MainWindow", "2. Process"))
		self.pb_return.setToolTip(_translate("MainWindow", "<html><head/><body><p>Saves condition and returns to main menu</p></body></html>"))
		self.pb_return.setText(_translate("MainWindow", "3. Return"))
		self.pb_cancel.setToolTip(_translate("MainWindow", "<html><head/><body><p>Cancels condition creation and returns to main menu</p></body></html>"))
		self.pb_cancel.setText(_translate("MainWindow", "Cancel"))
		self.label.setText(_translate("MainWindow", "1. Condition Name:"))
		self.label_3.setText(_translate("MainWindow", "2. Replicate:"))
		self.label_4.setText(_translate("MainWindow", "3. Heat/Chemical Denature:"))
		self.cb_CDHD.setItemText(0, _translate("MainWindow", "CD"))
		self.cb_CDHD.setItemText(1, _translate("MainWindow", "HD"))
		if self.CHdefaultslst[2] == 'CD':
			self.cb_CDHD.setCurrentIndex(0)
		elif self.CHdefaultslst[2] == 'HD':
			self.cb_CDHD.setCurrentIndex(1)
		else:
			self.cb_CDHD.setCurrentIndex(0)
		self.label_5.setText(_translate("MainWindow", "4. Concentrations/Temperatures:"))
		self.CalculationOPtions.setTitle(_translate("MainWindow", "Calculation Options"))
		self.cb_RepGr.setText(_translate("MainWindow", "Rep Graphs"))
		self.cb_RemOut.setText(_translate("MainWindow", "Remove Outlier Analysis"))
		self.cb_GOut.setText(_translate("MainWindow", "Giant Ouput"))
		self.cb_CombAn.setText(_translate("MainWindow", "Combined Analysis"))
		self.cb_GrComb.setText(_translate("MainWindow", "Graph Combined"))
		self.cb_IndRepAn.setText(_translate("MainWindow", "Individiual Rep Analysis"))
		self.label_2.setText(_translate("MainWindow", "Minimum Points for Calculation"))
		self.label_6.setText(_translate("MainWindow", "Outlier StdErr Cutoff (StdErr x #)"))
		self.groupBox_3.setTitle(_translate("MainWindow", "Graph Filters"))
		self.label_7.setText(_translate("MainWindow", "R^2 Cutoff"))
		self.le_CI.setValue(float(self.CHdefaultslst[12]))
		self.le_CI.setSingleStep(0.1)
		self.le_R2.setValue(float(self.CHdefaultslst[13]))
		self.le_R2.setSingleStep(0.1)
		self.label_8.setText(_translate("MainWindow", "CI Mx% of Range"))
		self.label_9.setText(_translate("MainWindow", "CHalf Range Cutoff"))
		self.le_CHrange.setValue(float(self.CHdefaultslst[14]))
		self.le_CHrange.setSingleStep(0.1)
		self.OtherFeatures.setTitle(_translate("MainWindow", "Other Features (CS and RM need FE)"))
		self.cb_PM.setText(_translate("MainWindow", "Residue Mapper"))
		self.cb_LE.setText(_translate("MainWindow", "Label Efficiency"))
		self.cb_RCS.setText(_translate("MainWindow", "Combined Site and CRM"))
		self.cb_FE.setText(_translate("MainWindow", "Fitting Efficiency"))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Condition"))
		item = self.table_conc.horizontalHeaderItem(0)
		item.setText(_translate("MainWindow", "Concentrations/Temperatures"))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Concentrations/Temperatures"))
		self.cb_RCS_dynamic.setText(_translate("MainWindow", "Dynamic y-axis"))
		self.label_min.setText(_translate("MainWindow", "yMin:"))
		self.le_min.setValue(float(self.CHdefaultslst[20]))
		self.le_min.setMinimum(-100)
		self.le_min.setSingleStep(0.01)
		self.label_max.setText(_translate("MainWindow", "yMax:"))
		self.le_max.setValue(float(self.CHdefaultslst[21]))
		self.le_max.setMinimum(-100)
		self.le_max.setSingleStep(0.01)
		self.cb_LE.setChecked(bool(self.CHdefaultslst[15]))
		self.cb_FE.setChecked(bool(self.CHdefaultslst[16]))
		self.cb_RCS.setChecked(bool(self.CHdefaultslst[17]))
		self.cb_PM.setChecked(bool(self.CHdefaultslst[18]))
		self.cb_RCS_dynamic.setChecked(bool(self.CHdefaultslst[19]))
	def nodynamic(self):
		self.cb_RCS_dynamic.setChecked(False)
	def sbchange(self):
		self.conc = self.sb_conc.value()
		self.table_conc.setRowCount(self.conc)
	def create(self):
		self.inp_conditionname = self.le_conditionname.text() #condition name
		self.inp_rep = self.spinBox.value() #rep number
		self.dirname = dir_name
		print(self.dirname)
		if os.path.exists(dir_name):
			if not os.path.exists(dir_name + '/' + self.inp_conditionname + ' CHalf Condition'):
				self.conddir = dir_name + '/' + self.inp_conditionname + ' CHalf Condition'
				os.mkdir(self.conddir)
				for i in range(self.inp_rep):
					os.mkdir(self.conddir + '/' + 'Rep' + str(i+1))
				self.Popup1()
				os.startfile(self.conddir)
				self.create_done = True
			else:
				self.Error1()
		else:
			self.Error2()
	def process(self):
		try:
			inp_conc_test = []
			for i in range(self.table_conc.rowCount()): #test if concentrations are filled out
				inp_conc_test.append(self.table_conc.item(i,0).text())
			conctab = True
		except:
			conctab = False
		if conctab == False:
			self.Error3()
		else:
			if self.create_done and conctab:
				if os.path.exists(self.conddir):
					os.chdir(self.conddir)
					masterfileDF = pd.DataFrame(columns=['## CALCULATION OPTIONS ##','','']) #,'Run Description','Condition','Replicate','Protein-Peptides Infile','Protein Infile','CD or HD','Conc/Temp Start'])
					masterfileDF['## CALCULATION OPTIONS ##'] = pd.Series(data=['Individual Rep Analysis','Rep Graphs','Combined Analysis','Remove Outlier Analysis','Graph Combined','Giant Output','Minimum Points for Calculatation','Outlier StdErr Cutoff (StdErr x #)',np.nan,'## GRAPH FILTERS ##','CI Mx% of Range','R^2 Cutoff','CHalf Range Cutoff'] + [np.nan] + ['## OTHER FEATURES ##','Label Efficiency', 'Fitting Efficiency','Combined Site and Combined Residue Mapper','Protein Map','Dynamic Y-axis','Min:','Max'] + [np.nan] + ['CHalf Version:'])
					dirlst = []
					proteinpeptides_lst = []
					proteins_lst = []
					reps = []
					dirs = os.listdir() #fetch rep folder paths
					for i in range(self.inp_rep):
						if 'Rep' + str(i+1) in dirs:
							dirlst.append(os.path.realpath(dirs[i]))
							reps.append(i+1)
					for folder in dirlst:
						os.chdir(folder)
						file_tree = os.listdir(folder)
						for file in file_tree:
							if 'protein-peptides.csv' in file: #fetch list of _protein-peptides.csv files
								proteinpeptides_lst.append(os.path.realpath(file))
							if 'proteins.csv' in file: #fetch list of _proteins.csv files
								proteins_lst.append(os.path.realpath(file))
					if self.inp_rep != len(proteinpeptides_lst) == False:
						self.Error4()
					elif self.inp_rep != len(proteins_lst):
						self.Error4()
					else:
						os.chdir(self.conddir)
						inp_cdhd = self.cb_CDHD.currentText() #chemical or heat denature
						inp_IndRepAn = self.cb_IndRepAn.isChecked() #Individual Rep Analysis Boolean
						inp_RepGR = self.cb_RepGr.isChecked() #Rep Graphs Boolean
						inp_CombAn = self.cb_CombAn.isChecked() #Combined Analysis Boolean
						inp_RemOutAn = self.cb_RemOut.isChecked() #Remove Outlier Analysis Boolean
						inp_GrComb = self.cb_GrComb.isChecked() #Graph Combined Boolean
						inp_GOut = self.cb_GOut.isChecked() #Giant output Boolean
						inp_minpts = self.spin_minpts.value() #Minimum number of points for calculation
						inp_stderror = self.spin_stderror.value() #Outlier StdErr Cutoff (StdErr x #)
						inp_CI = self.le_CI.value() #CI Mx%Range
						inp_R2 = self.le_R2.value() #R^2 cutoff
						inp_CHrange = self.le_CHrange.value() #CHalf range cutoff
						inp_LE = self.cb_LE.isChecked() #label eff
						inp_FE = self.cb_FE.isChecked() #fitting eff
						inp_RCS = self.cb_RCS.isChecked() #combined site
						inp_PM = self.cb_PM.isChecked() #protein mapper (residue mapper)
						inp_conc = []
						inp_dynamic = self.cb_RCS_dynamic.isChecked() #dynamic y axis
						if not inp_dynamic:
							inp_ymin = self.le_min.value() #fig ymin
							inp_ymax = self.le_max.value() #fig ymax
						else:
							inp_ymin = 'Null'
							inp_ymax = 'Null'
						try:
							if inp_LE or inp_FE:
								os.mkdir('Efficiency Outputs')
							if inp_PM:
								os.mkdir('Residue Mapper Outputs')
						except:
							None
						for i in range(self.table_conc.rowCount()): #retrieve concentrations
							inp_conc.append(self.table_conc.item(i,0).text())
						masterfileDF.iloc[:,1] = [boolTOword(inp_IndRepAn),boolTOword(inp_RepGR),boolTOword(inp_CombAn),boolTOword(inp_RemOutAn),boolTOword(inp_GrComb),boolTOword(inp_GOut),inp_minpts,inp_stderror,np.nan,np.nan,inp_CI,inp_R2,inp_CHrange,np.nan,np.nan,boolTOword(inp_LE),boolTOword(inp_FE),boolTOword(inp_RCS),boolTOword(inp_PM),boolTOword(inp_dynamic),inp_ymin,inp_ymax,np.nan,'v4.3']
						masterfileDF = masterfileDF.join(pd.DataFrame(data=[self.inp_conditionname] * self.inp_rep, columns=['Run Description']))
						masterfileDF = masterfileDF.join(pd.DataFrame(data=[self.inp_conditionname] * self.inp_rep, columns=['Condition']))
						masterfileDF = masterfileDF.join(pd.DataFrame(data=reps, columns=['Replicate']))
						masterfileDF = masterfileDF.join(pd.DataFrame(data=proteinpeptides_lst, columns=['Protein-Peptides Infile']))
						masterfileDF = masterfileDF.join(pd.DataFrame(data=proteins_lst, columns=['Protein Infile']))
						masterfileDF = masterfileDF.join(pd.DataFrame(data=[inp_cdhd] * self.inp_rep, columns=['CD or HD']))
						masterfileDF = masterfileDF.join(pd.DataFrame(data=[inp_conc[0]] * self.inp_rep, columns=['Conc/Temp Start']))
						for i in range(1,len(inp_conc)): #adds following concentrations
							masterfileDF = masterfileDF.join(pd.DataFrame(columns=[str(i)], data=[inp_conc[i]] * self.inp_rep))
						toprow = pd.DataFrame(columns=masterfileDF.columns.values.tolist(),data=[['## CALCULATION OPTIONS ##','','','Run Description','Condition','Replicate','Protein-Peptides Infile','Protein Infile','CD or HD','Conc/Temp Start'] + [''] * (len(inp_conc)-1)])
						outputDF = pd.concat([toprow,masterfileDF],ignore_index=True).reset_index(drop=True) #cleaning up masterfile column names for export
						outputDF.to_csv(self.inp_conditionname + ' CHalf Condition Masterfile.csv', header=False, index=False)
						self.Popup2()
						self.condition_created = True    

				else:
					self.Error5()
			else:
				self.Error5()
	def returnbutton(self):
		if self.condition_created:
			os.chdir(dir_name)
			#sys.exit(app.exec_())
			self.hide()
		else:
			self.Error6()
	def cancel(self):
		global dir_name
		self.dir_name = dir_name
		if self.create_done:
			os.chdir(self.dir_name)
			shutil.rmtree(self.conddir)
		os.chdir(self.dir_name)
		self.hide()
		#sys.exit(app.exec_())

	def FE_CS_PM(self):
		if not self.cb_FE.isChecked():
			self.cb_RCS.setChecked(False)
			self.cb_PM.setChecked(False)
		if self.cb_RCS.isChecked() or self.cb_PM.isChecked():
			self.cb_FE.setChecked(True)
	def Error1(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("Condition directory by that name already exists. Choose a new name.")
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error2(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("Cannot find project directory. Press Cancel and specify Project Name.")
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error3(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("You must fill out the concentrations/temperatures table.")
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error4(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("Input files missing. Please add to Rep folders in: " + self.inp_conditionname)
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error5(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("Condition directory does not exist. Please Create First.")
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error6(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("No condition created to save. Please create or press cancel.")
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Popup1(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Message')
		msg.setText("Add 'protein_peptides.csv' and 'proteins.csv' files to each Rep folder. After adding input files, check that the rest of your specifications are correct and press Process to generate a master file for the condition. Note: Only put one of each file type in each Rep folder. Furthermore, the endings must be exactly as previously listed.")
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Popup2(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Message')
		msg.setText("Condition created. Press Return.")
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x

''' MAIN WINDOW GUI '''
class Ui_MainWindow(QtWidgets.QMainWindow):
	def __init__(self): #setupUi(self, MainWindow)
		super().__init__()
		global CHdefaultslst, FEdefaultslst, icon, directory_set
		self.directory_set = directory_set
		self.CHdefaultslst = CHdefaultslst
		self.FEdefaultslst = FEdefaultslst
		self.setObjectName("MainWindow")
		self.setWindowIcon(QtGui.QIcon(icon))
		self.main_directory = os.getcwd()
		self.resize(801, 525)
		self.centralwidget = QtWidgets.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.logo = QtWidgets.QTextBrowser(self.centralwidget)
		self.logo.setGeometry(QtCore.QRect(40, 10, 711, 111))
		self.logo.setObjectName("logo")
		self.logo.setAlignment(QtCore.Qt.AlignRight)
		self.ProjectInformation = QtWidgets.QGroupBox(self.centralwidget)
		self.ProjectInformation.setGeometry(QtCore.QRect(40, 130, 719, 61))
		self.ProjectInformation.setObjectName("ProjectInformation")
		self.gridLayoutWidget_3 = QtWidgets.QWidget(self.ProjectInformation)
		self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 701, 30))
		self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.gridLayoutWidget_3)
		self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget_3)
		self.label_3.setObjectName("label_3")
		self.horizontalLayout_2.addWidget(self.label_3)
		self.le_projectname = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
		self.le_projectname.setObjectName("le_projectname")
		self.horizontalLayout_2.addWidget(self.le_projectname)
		self.pb_createproject = QtWidgets.QPushButton(self.gridLayoutWidget_3)
		self.pb_createproject.setObjectName("pb_createproject")
		self.pb_createproject.clicked.connect(self.createproject)
		self.horizontalLayout_2.addWidget(self.pb_createproject)
		self.pb_openproject = QtWidgets.QPushButton(self.gridLayoutWidget_3)
		self.pb_openproject.setObjectName("pb_createproject")
		self.pb_openproject.clicked.connect(self.openproject)
		self.horizontalLayout_2.addWidget(self.pb_openproject)
		self.pb_workdir = QtWidgets.QPushButton(self.gridLayoutWidget_3)
		self.pb_workdir.setObjectName("pb_workdir")
		self.pb_workdir.clicked.connect(self.workdir)
		self.horizontalLayout_2.addWidget(self.pb_workdir)
		self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox.setGeometry(QtCore.QRect(40, 200, 281, 271))
		self.groupBox.setObjectName("groupBox")
		self.lst_condition = QtWidgets.QListWidget(self.groupBox)
		self.lst_condition.setGeometry(QtCore.QRect(10, 20, 261, 201))
		self.lst_condition.setObjectName("lst_condition")
		self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox)
		self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 230, 261, 31))
		self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
		self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
		self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		self.pb_add = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
		self.pb_add.setObjectName("pb_add")
		self.pb_add.clicked.connect(self.add)
		self.horizontalLayout_3.addWidget(self.pb_add)
		self.pb_refresh = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
		self.pb_refresh.setObjectName("pb_add")
		self.pb_refresh.clicked.connect(self.refresh)
		self.horizontalLayout_3.addWidget(self.pb_refresh)
		self.pb_delete = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
		self.pb_delete.setObjectName("pb_delete")
		self.pb_delete.clicked.connect(self.delete)
		self.horizontalLayout_3.addWidget(self.pb_delete)
		self.pb_open = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
		self.pb_open.setObjectName("pb_open")
		self.pb_open.clicked.connect(self.open)
		self.horizontalLayout_3.addWidget(self.pb_open)
		self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_2.setGeometry(QtCore.QRect(330, 200, 431, 271))
		self.groupBox_2.setObjectName("groupBox_2")
		self.textBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_2)
		self.textBrowser_2.setGeometry(QtCore.QRect(10, 20, 411, 201))
		self.textBrowser_2.setObjectName("textBrowser_2")
		self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox_2)
		self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 230, 411, 31))
		self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
		self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
		self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.pb_readme = QtWidgets.QPushButton(self.horizontalLayoutWidget)
		self.pb_readme.setObjectName("pb_readme")
		self.pb_readme.clicked.connect(self.readme)
		self.horizontalLayout.addWidget(self.pb_readme)
		self.pb_start = QtWidgets.QPushButton(self.horizontalLayoutWidget)
		self.pb_start.setObjectName("pb_start")
		self.pb_start.clicked.connect(self.start)
		self.horizontalLayout.addWidget(self.pb_start)
		self.pb_openfolder = QtWidgets.QPushButton(self.horizontalLayoutWidget)
		self.pb_openfolder.setObjectName("pb_openfolder")
		self.pb_openfolder.clicked.connect(self.openfolder)
		self.horizontalLayout.addWidget(self.pb_openfolder)
		self.pb_cancel = QtWidgets.QPushButton(self.horizontalLayoutWidget)
		self.pb_cancel.setObjectName("pb_cancel")
		self.pb_cancel.clicked.connect(self.cancel)
		self.horizontalLayout.addWidget(self.pb_cancel)
		self.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(self)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 801, 26))
		self.menubar.setObjectName("menubar")
		self.menuCHalf_Tools = QMenu(self.menubar)
		self.menuCHalf_Tools.setObjectName(u"menuCHalf_Tools")
		self.menubar.addMenu(self.menuCHalf_Tools)
		self.menuGraphics = QMenu(self.menubar)
		self.menuGraphics.setObjectName(u"menuGraphics")
		self.menubar.addMenu(self.menuGraphics)
		self.setMenuBar(self.menubar)
		self.menuMoreSettings = QMenu(self.menubar)
		self.menuMoreSettings.setObjectName(u"menuMoreSettings")
		self.menubar.addMenu(self.menuMoreSettings)
		self.statusbar = QtWidgets.QStatusBar(self)
		self.statusbar.setObjectName("statusbar")
		self.setStatusBar(self.statusbar)
		self.LabelFinderAction = QAction('Label Finder (Label Efficiency)', self)
		self.LabelFinderAction.triggered.connect(self.LabelFinderConnector)
		self.FittingEfficiencyAction = QAction('Fitting Efficiency', self)
		self.FittingEfficiencyAction.triggered.connect(self.FittingEfficiencyConnector)
		self.CombinedSiteAction = QAction('Combined Site', self)
		self.CombinedSiteAction.triggered.connect(self.CombinedSiteConnector)
		self.ProteinMapperAction = QAction('Residue Mapper', self)
		self.ProteinMapperAction.triggered.connect(self.ProteinMapperConnector)
		self.CombinedResidueMapperAction = QAction('Combined Residue Mapper', self)
		self.CombinedResidueMapperAction.triggered.connect(self.CombinedResidueMapperConnector)
		self.menuCHalf_Tools.addAction(self.LabelFinderAction)
		self.menuCHalf_Tools.addAction(self.FittingEfficiencyAction)
		self.menuCHalf_Tools.addAction(self.CombinedSiteAction)
		self.menuCHalf_Tools.addAction(self.ProteinMapperAction)
		self.menuCHalf_Tools.addAction(self.CombinedResidueMapperAction)
		self.MoreSettingsAction = QAction('More Settings', self)
		self.MoreSettingsAction.triggered.connect(self.MoreSettings)
		self.menuMoreSettings.addAction(self.MoreSettingsAction)
		self.svgAction = QAction('.svg',self)
		self.svgAction.setCheckable(True)
		self.svgAction.triggered.connect(self.togglecheck_svg)
		self.menuGraphics.addAction(self.svgAction)
		self.jpgAction = QAction('.jpg',self)
		self.jpgAction.setCheckable(True)
		self.jpgAction.triggered.connect(self.togglecheck_jpg)
		self.menuGraphics.addAction(self.jpgAction)
		self.pngAction = QAction('.png',self)
		self.pngAction.setCheckable(True)
		self.pngAction.triggered.connect(self.togglecheck_png)
		self.menuGraphics.addAction(self.pngAction)
		if self.CHdefaultslst[0] == '.svg':
			self.svgAction.setChecked(True)
		elif self.CHdefaultslst[0] == '.jpg':
			self.jpgAction.setChecked(True)
		elif self.CHdefaultslst[0] == '.png':
			self.pngAction.setChecked(True)
		else:
			self.svgAction.setChecked(True)
		self.dirname = None
		self.retranslateUi(self)
		QtCore.QMetaObject.connectSlotsByName(self)
		self.workingdir = self.main_directory

	def retranslateUi(self, MainWindow):
		global mainLogo
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "CHalf v4.3"))
		self.logo.setHtml(_translate("MainWindow", f"<p style=\"text-align:center;\"><img src = \"{mainLogo}\"></p>"))
		self.ProjectInformation.setTitle(_translate("MainWindow", "Project Information"))
		self.label_3.setText(_translate("MainWindow", "Project Name:"))
		self.pb_createproject.setToolTip(_translate("MainWindow", "<html><head/><body><p>Creates project directory<img src=\":/Logo/CHalf Logo Full.png\"/></p></body></html>"))
		self.pb_createproject.setText(_translate("MainWindow", "Create Project"))
		self.pb_openproject.setText(_translate("MainWindow", "Open Project"))
		self.pb_workdir.setText(_translate("MainWindow", "Set Dir"))
		self.groupBox.setTitle(_translate("MainWindow", "Conditions"))
		__sortingEnabled = self.lst_condition.isSortingEnabled()
		self.lst_condition.setSortingEnabled(False)
		'''item = self.lst_condition.item(0)
		item.setText(_translate("MainWindow", "Condition 1"))'''
		self.lst_condition.setSortingEnabled(__sortingEnabled)
		self.pb_add.setToolTip(_translate("MainWindow", "<html><head/><body><p>Opens Condition Creator </p></body></html>"))
		self.pb_add.setText(_translate("MainWindow", "Add"))
		self.pb_refresh.setToolTip(_translate("MainWindow", "<html><head/><body><p>Refreshes condition list </p></body></html>"))
		self.pb_refresh.setText(_translate("MainWindow", "Refresh"))
		self.pb_delete.setToolTip(_translate("MainWindow", "<html><head/><body><p>Deletes Masterfile of selected condition</p></body></html>"))
		self.pb_delete.setText(_translate("MainWindow", "Delete"))
		self.pb_open.setToolTip(_translate("MainWindow", "<html><head/><body><p>Opens Masterfile of selected condition</p></body></html>"))
		self.pb_open.setText(_translate("MainWindow", "Open"))
		self.groupBox_2.setTitle(_translate("MainWindow", "Instructions"))
		self.textBrowser_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
		"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
		"p, li { white-space: pre-wrap; }\n"
		"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. Unless you have a default directory set, press Set Dir to set your output directory.</p>\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. Input Project Name and press Create Project or press Open Project to select an existing project.</p>\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3. Press Add Condition to add conditions to your project. This opens the Condition Creator.</p>\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">4. You may delete or edit a condition by selecting it in the list and clicking Delete or Open. If you edit a condition, refer to the README to avoid improper formatting of the Masterfile.</p>\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">5. After you are finished inputting conditions, press Start, and CHalf will process your data. A dialog box will indicate that CHalf has engaged.</p>\n"
		"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">6. When CHalf is done running, a dialog box will indicate that CHalf is finished. Press Open Folder to access output files directories.</p></body></html>"))
		self.pb_readme.setToolTip(_translate("MainWindow", "<html><head/><body><p>Opens README file</p></body></html>"))
		self.pb_readme.setText(_translate("MainWindow", "README"))
		self.pb_start.setToolTip(_translate("MainWindow", "<html><head/><body><p>Runs CHalf</p></body></html>"))
		self.pb_start.setText(_translate("MainWindow", "Start"))
		self.pb_openfolder.setToolTip(_translate("MainWindow", "<html><head/><body><p>Opens project directory</p></body></html>"))
		self.pb_openfolder.setText(_translate("MainWindow", "Open Folder"))
		self.pb_cancel.setToolTip(_translate("MainWindow", "<html><head/><body><p>Closes program</p></body></html>"))
		self.pb_cancel.setText(_translate("MainWindow", "Cancel"))
		self.menuCHalf_Tools.setTitle(_translate("MainWindow", u"Other Tools", None))
		self.menuGraphics.setTitle(_translate("MainWindow", u"Graphics Options", None))
		self.menuMoreSettings.setTitle(_translate("MainWindow", u"More Settings", None))

	def togglecheck_svg(self):
		if self.svgAction.isChecked():
			self.jpgAction.setChecked(False)
			self.pngAction.setChecked(False)
	def togglecheck_jpg(self):
		if self.jpgAction.isChecked():
			self.svgAction.setChecked(False)
			self.pngAction.setChecked(False)
	def togglecheck_png(self):
		if self.pngAction.isChecked():
			self.jpgAction.setChecked(False)
			self.svgAction.setChecked(False)
	def createproject(self):
		if self.directory_set == False:
			self.Error13()
			self.workdir()
		else:
			os.chdir(self.main_directory)
			if not os.path.exists(self.le_projectname.text() + " CHalf Project"):
				projectname  = self.le_projectname.text()
				os.mkdir(projectname + " CHalf Project")
				self.dirname = os.path.realpath(projectname + " CHalf Project")
				'''dir_temp = open('dir_temp','w+') #makes a temporary file to let the conditions GUI know where the working directory is
				dir_temp.write(os.path.realpath(self.dirname))'''
				self.Message1()
			else:
				self.Error1()
			global dir_name 
			dir_name = self.dirname
	'''def transfer(self):
		Filler.transfer(self.dirname)'''
	def add(self):
		if not self.dirname == None:
			os.chdir(self.main_directory)
			self.sub = Ui_ConditionCreator()
			self.togglewindow()
			os.chdir(self.dirname)
		else:
			self.Error2()
	def openfolder(self):
		try:
			os.startfile(self.dirname)
		except:
			self.Error3()
	def refresh(self):
			self.lst_condition.clear()
			try:
				os.chdir(self.dirname)
				files = os.listdir()
				self.conditions = []
				for file in files:
					if 'CHalf Condition' in file and file not in self.conditions:
						item = QtWidgets.QListWidgetItem()
						item.setText(file)
						self.lst_condition.addItem(item)
						self.conditions.append(os.path.realpath(file))
			except:
				self.Error4()
	def workdir(self):
		self.main_directory = QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, "Select Working Directory", self.main_directory)
		self.directory_set = True
	def delete(self):
		try:
			selection = self.lst_condition.currentRow()
			item = self.lst_condition.item(selection)
			item = item.text()
			self.Message5()
			if self.reply:
				for condition in self.conditions:
					if item in condition:
						shutil.rmtree(condition)
				self.lst_condition.takeItem(selection)
		except (PermissionError, FileNotFoundError):
			traceback.print_exc()
			self.Error12()
		except:
			traceback.print_exc()
			self.Error5()
		try: #refreshes list
			self.lst_condition.clear()
			os.chdir(self.dirname)
			files = os.listdir()
			self.conditions = []
			for file in files:
				if 'CHalf Condition' in file and file not in self.conditions:
					item = QtWidgets.QListWidgetItem()
					item.setText(file)
					self.lst_condition.addItem(item)
					self.conditions.append(os.path.realpath(file))
		except:
			None
	def open(self):
		opened = False
		try:
			selection = self.lst_condition.currentRow()
			item = self.lst_condition.item(selection)
			item = item.text()
			try:
				for condition in self.conditions:
					if item in condition:
						os.chdir(condition)
						files = os.listdir()
						for file in files:
							if 'Masterfile' in file:
								os.system('"' + file + '"')
								opened = True
				if not opened:
					self.Error6()
				os.chdir(self.dirname)
			except:
				self.Error6
		except:
			self.Error5()
	def readme(self):
		try:
			"""os.chdir(self.main_directory)
			os.system('README.md')"""
			webbrowser.open('https://github.com/JC-Price/Chalf_public/blob/main/README.md',new=1)
		except:
			self.Error7()
	def cancel(self):
		sys.exit(app.exec_())
	def Error1(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("Project name already in use. Select new project title.")
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error2(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("You must create a project before adding conditions.")
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error3(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("You must create a project before opening it.")
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error4(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("You must create a project before refreshing the condition list.")
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error5(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("No condition selected.")
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error6(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("Masterfile not found.")
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error7(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("Unable to open README in web browser. A text version can be found in your CHalf directory as README.md or you can visit fakeurl.com to read CHalf's documentation online.")
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error8(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("No conditions to run.")
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error9(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("Error. Check Print Statement")
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error10(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("Common Input Error Likely: Number of points in " + self.repInfo['condition'] + ' does not match between condition files and the masterfile. Check that your number of concentration/temperature columns in your proteins.csv and protein-peptides.csv files are the same as in your masterfile. You may also check the printed error statement.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error11(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText("CHalf Defaults.csv not found. Please add to folder.")
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error12(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('Unable to delete condition. Check print statement and check if condition files/folders are open.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Error13(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Error')
		msg.setText('You must select an output directory before creating a project.')
		msg.setIcon(QtWidgets.QMessageBox.Critical)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Message1(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Message')
		msg.setText('Project created. You may add conditions.')
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Message2(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Message')
		msg.setText('CHalf initialized. Press OK to continue. A popup will appear when your run is complete.')
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Message3(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Message')
		msg.setText('CHalf complete. Press Open Folder to view files.')
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Message4(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Warning')
		msg.setText('Tampering with CHalf defaults can cause errors if done improperly. Read the documentation on modifying defualts before making any changes.')
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def Message5(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Warning')
		msg.setText('Are you sure you want to delete this condition? Deleting this condition will also delete its folder and associated files including data inputs.')
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
		x = msg.exec_()
		if x == QtWidgets.QMessageBox.Ok:
			self.reply = True
		elif x == QtWidgets.QMessageBox.Cancel:
			self.reply = False
	def Message6(self):
			msg = QtWidgets.QMessageBox()
			msg.setWindowTitle('Warning')
			msg.setText('If you run an opened CHalf project, files in the folders will be overwritten.')
			msg.setIcon(QtWidgets.QMessageBox.Information)
			msg.setStandardButtons(QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
			x = msg.exec_()
			if x == QtWidgets.QMessageBox.Ok:
				self.reply2 = True
			elif x == QtWidgets.QMessageBox.Cancel:
				self.reply2 = False
	def togglewindow(self):
		if self.sub.isHidden():
			self.sub.show()
		else:
			self.sub.hide()
	def success(self):
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle('Message')
		msg.setText("CHalf run complete.")
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		x = msg.exec_()
		x
	def FittingEfficiencyConnector(self):
		os.chdir(self.main_directory)
		self.FEsub = Ui_FittingEfficiency()
		self.FEtogglewindow()
	def FEtogglewindow(self):
		if self.FEsub.isHidden():
			self.FEsub.show()
		else:
			self.FEsub.hide()
	def CombinedSiteConnector(self):
		os.chdir(self.main_directory)
		self.CSsub = Ui_CombinedSite()
		self.CStogglewindow()
	def CStogglewindow(self):
		if self.CSsub.isHidden():
			self.CSsub.show()
		else:
			self.CSsub.hide()
	def ProteinMapperConnector(self):
		os.chdir(self.main_directory)
		self.PMsub = Ui_ProteinMapper()
		self.PMtogglewindow()
	def PMtogglewindow(self):
		if self.PMsub.isHidden():
			self.PMsub.show()
		else:
			self.PMsub.hide()
	def CombinedResidueMapperConnector(self):
		os.chdir(self.main_directory)
		self.CRMsub = Ui_CombinedResidueMapper()
		self.CRMtogglewindow()
	def CRMtogglewindow(self):
		if self.CRMsub.isHidden():
			self.CRMsub.show()
		else:
			self.CRMsub.hide()
	def LabelFinderConnector(self):
		os.chdir(self.main_directory)
		self.LFsub = Ui_LabelFinder()
		self.LFtogglewindow()
	def LFtogglewindow(self):
		if self.LFsub.isHidden():
			self.LFsub.show()
		else:
			self.LFsub.hide()
	def openproject(self):
		self.reply2 = True
		self.Message6()
		try:
			if self.reply2:
				self.dirname = QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, "Select Existing CHalf Project", self.main_directory)
				self.main_directory = self.dirname
				global dir_name
				dir_name = self.dirname
				print('Project: ' + self.dirname)
				self.refresh()
		except:
			self.Error9()
			traceback.print_exc()
	def MoreSettings(self):
		try:
			self.Message4()
			os.startfile('CHalf Defaults.csv')
		except:
			self.Error11()
	def start(self):
			try:
				self.lst_condition.clear()
				os.chdir(self.dirname)
				files = os.listdir()
				self.conditions = []
				for file in files:
					if 'CHalf Condition' in file and file not in self.conditions:
						item = QtWidgets.QListWidgetItem()
						item.setText(file)
						self.lst_condition.addItem(item)
						self.conditions.append(os.path.realpath(file))
				if len(self.conditions) > 0:
					os.chdir(self.main_directory)
					try:
						self.Message2()
						directory = self.dirname
						if self.svgAction.isChecked():
							file_type = '.svg'
						elif self.jpgAction.isChecked():
							file_type = '.jpg'
						elif self.pngAction.isChecked():
							file_type = '.png'
						pd.options.mode.chained_assignment = None  # default='warn'
						dir_name = directory
						os.chdir(dir_name)

						# Get conditions folder directories and masterfiles
						conditions_lst = []
						masterfiles_lst = []
						for folder in os.listdir():
							if "CHalf Condition" in folder:
								conditions_lst.append(os.path.realpath(folder))
						for condition in conditions_lst:
							os.chdir(condition)
							files = os.listdir(condition)
							for file in files:
								if "Masterfile.csv" in file:
									masterfiles_lst.append(os.path.realpath(file))
						os.chdir(dir_name) #Return to original directory

						


						""" ================================================================ """
						""" ==================== BEGIN MAIN PROGRAM ======================== """
						""" ================================================================ """

						combinedsite_conditions = []
						giantoutput_conditions = []
						
						for z in tqdm(range(len(masterfiles_lst)),desc='Condition Loop'):
							MASTERFILE = masterfiles_lst[z]
							# Get 'pandas' DataFrame of entire Mastefile
							os.chdir(os.path.dirname(MASTERFILE))
							masterDF = pd.read_csv(MASTERFILE,dtype={'Condition':str})
							# print(masterDF)  # (test print)

							# Assign local constant variables from Masterfile user input
							RUN_DESCRIPTION = masterDF.iloc[0]['Run Description']  # Could be used to name final output file

							R_SQUARED_CUTOFF = float(masterDF.iloc[11][1])
							CHALF_RANGE_CUTOFF = float(masterDF.iloc[12][1])
							CONFIDENCE_INTERVAL_CUTOFF = float(masterDF.iloc[10][1])  # CI Cutoff, usually .3
							MINIMUM_PTS = float(masterDF.iloc[6][1])  # Minimum number of data points acceptable, usually 4
							OUTLIER_CUTOFF = float(masterDF.iloc[7][1])  # How many CI's away from fit curve a pt can be before becoming an outlier

							#  ---DEVELOPER NOTE---: boolean values below can be changed to 'True' to test them without changing Masterfile'''
							SEPARATE_REP_ANALYSIS = False
							MAKEGRAPH_REPS = False  # Only occurs if SEPARATE_REP_ANALYSIS is also True.
							COMBINED_CONDITION_ANALYSIS = False
							GRAPH_COMBINED = False
							removeOutlier_2xStdErr = False
							GIANT_OUTPUT = False
							LE = False  # Label efficiency
							FE = False  # Fitting efficiency
							CS = False  # Combined Site
							PM = False  # Protein Mapper (residue mapper)
							DYNAMIC = False  # dynamic y-axis
							YMIN = 0  # fig ymin
							YMAX = 3  # fig ymax
							VERSION = 'v4.3'
							# Checks for the above Boolean variables
							if masterDF.iloc[0][1].upper() == "YES":
								SEPARATE_REP_ANALYSIS = True
							if masterDF.iloc[1][1].upper() == "YES":
								MAKEGRAPH_REPS = True
							if masterDF.iloc[2][1].upper() == "YES":
								COMBINED_CONDITION_ANALYSIS = True
							if masterDF.iloc[3][1].upper() == "YES":
								removeOutlier_2xStdErr = True
							if masterDF.iloc[4][1].upper() == "YES":
								GRAPH_COMBINED = True
							if masterDF.iloc[5][1].upper() == "YES":
								GIANT_OUTPUT = True
								giantoutput_conditions.append(os.path.dirname(MASTERFILE))
							if masterDF.iloc[15][1].upper() == "YES":
								LE = True
							if masterDF.iloc[16][1].upper() == "YES":
								FE = True
							if masterDF.iloc[17][1].upper() == "YES":
								CS = True
								combinedsite_conditions.append(os.path.dirname(MASTERFILE))
							if masterDF.iloc[18][1].upper() == "YES":
								PM = True
							if masterDF.iloc[19][1].upper() == "YES":
								DYNAMIC = True
								YMIN = None
								YMAX = None
							else:
								YMIN = float(masterDF.iloc[20][1])
								YMAX = float(masterDF.iloc[21][1])
							try:
								if masterDF.iloc[23][1] != VERSION:
									raise ValueError('Wrong version of CHalf masterfile in use. Please change your masterfile version to ' + VERSION)
							except IndexError:
									raise ValueError('Masterfile missing version number. Please add ' + VERSION + ' to B25 in the masterfile.')
							"""--------------- Graph and Curve Fit Functions -----------------------------------------------------"""
							# plot color code, usually don't need to change
							colors = {
								# 'data' is for data and fit
								3: {'data': '#1f77b4', 'C half': '#aec7e8', 'CI': '#c6dbef'},  # blue
								2: {'data': '#ff7f0e', 'C half': '#ffbb78', 'CI': '#fdd0a2'},  # orange
								1: {'data': '#5254a3', 'C half': '#9e9ac8', 'CI': '#dadaeb'},  # purple
								4: {'data': '#8c6d31', 'C half': '#e7ba52', 'CI': '#e7cb94'}}  # brown
							plot_markers = {1: 'o', 2: '^', 3: 's', 4: '*'}

							plot_colors = {
								0: 'b', 1: 'g', 2: 'm', 3: 'c', 4: 'r', 5: 'y'
							}
							''' Check if "Graph Outputs" folder is present; if not, create it '''
							if MAKEGRAPH_REPS or GRAPH_COMBINED:
								if not os.path.exists('Graph Outputs'):
									os.makedirs('Graph Outputs')

							''' Create RepInfoLists, which will hold all description/file info for reps from Masterfile '''  ### May want to change to Condition List with this RepInfo inside...
							# Format: RepInfoLists[[Condition, Rep#, Protein-Peptide file name, Protein file name, CD or HD, [conc/temp list]]]
							RepInfoLists = []
							for i in range(0, len(masterDF['Condition'])):  # for every cell (every rep) in the 'Condition' column
								if not pd.isnull(masterDF.iloc[i]['Condition']):  # that is not empty		(this stops the read after an empty line)

									# Get the conc/temp header list
									conc_tempList = []
									for j in range(masterDF.columns.get_loc('Conc/Temp Start'), masterDF.shape[1]):  # j = columns from start to end
										if not pd.isnull(
												masterDF.iloc[i][j]):  # excludes empty cells (occurs if a rep has more conc/temp pts than others)
											conc_tempList.append(float(masterDF.iloc[i][j]))

									# Populate repInfo for each rep (each row) from Masterfile
									self.repInfo = {}
									self.repInfo['condition'] = str(masterDF.iloc[i]['Condition'])
									self.repInfo['repNum'] = masterDF.iloc[i]['Replicate']
									self.repInfo['protein-peptide infile'] = masterDF.iloc[i]['Protein-Peptides Infile']
									self.repInfo['protein infile'] = masterDF.iloc[i]['Protein Infile']
									self.repInfo['CD or HD'] = masterDF.iloc[i]['CD or HD']
									if self.repInfo['CD or HD'] == 'HD':
										self.repInfo['original-temp list'] = conc_tempList.copy()
										conc_tempList = list((np.array(conc_tempList)-min(conc_tempList))/(max(conc_tempList)-min(conc_tempList)))
									self.repInfo['conc-temp list'] = conc_tempList

									# Check if infile names have '.csv' ending; add ending if not present
									if '.csv' not in self.repInfo['protein-peptide infile']:
										self.repInfo['protein-peptide infile'] += ".csv"
									if '.csv' not in self.repInfo['protein infile']:
										self.repInfo['protein infile'] += ".csv"
									RepInfoLists.append(self.repInfo)  # then add the list to our list of rep info
								else:  # Ex: RepInfoLists[[rep1Info][rep2Info][rep3Info]etc.]
									break  # RepInfoLists[rep1Info] = [Condition,Rep#,Pro-Pep.csv,Pro.csv,CD,[0,1.1,2.5]]

							#print("RepInfoLists:", RepInfoLists)
							for self.repInfo in RepInfoLists:
								# Combine proteins-peptides.csv and proteins.csv files for each rep; returns DataFrame
								repDF = rep_filecombine(self.repInfo)
								# Normalizes data in repDF, exports in a .csv file the original and normalized data
								''' takes data and normalizes values to between 0 and 1 '''

								#print(f"IN NORMALIZE_DATA: {repInfo['condition']} Rep{repInfo['repNum']}")
								CTstart = self.repInfo['ct start index']
								CTend = self.repInfo['ct end index']

								# Set up headers for Normalized Data [ex: '2.41_Norm' ]
								repDF['Delta 6-0'] = 0
								norm_header_list = []
								for head in self.repInfo['conc-temp list']:
									repDF[
										str(head) + "_Norm"] = 0  # Adds '###_Norm' header for each conc/temp value and initializes row values to 0
									norm_header_list.append(str(head) + "_Norm")

								repNormFilename = str(self.repInfo['condition']) + '_Rep' + str(int(self.repInfo['repNum'])) + '_Norm.csv'
								#print(f"Rep{repInfo['repNum']} Norm Headers: {norm_header_list}")
								self.repInfo['norm ct headers'] = norm_header_list
								self.repInfo['norm filename'] = repNormFilename
								repDF, self.repInfo = normalize_data(repDF, self.repInfo)
								self.repInfo['DataFrame'] = repDF
							if SEPARATE_REP_ANALYSIS:  # determined from Masterfile
								for self.repInfo in RepInfoLists:
									# print(f"IN SEPARATE_REP ANALYSIS: {repInfo['condition']}, Rep{repInfo['repNum']}")

									""" Fit_SCurve Function """
									rep_sCurveDataList = []
									repDF = self.repInfo['DataFrame']
									sCurveDF = pd.DataFrame(
										columns=['Accession','Start','popt', 'popt_lowBound', 'popt_upBound', 'pcov', 'sCurve_xValues', 'sCurve_yValues', 'B_stderror',
												'A_stderror', 'CHalf_stderror', 'b_stderror', 'CHalf_ConfidenceInterval', 'concRange',
												'ratioTOrange', 'fitCurve_B', 'fitCurve_A', 'CHalf', 'fitCurve_b', 'slope',
												'CHalf_confidenceInterval_lowBound', 'CHalf_confidenceInterval_upBound', 'b_confidenceInterval',
												'b_confidenceInterval_lowBound', 'b_confidenceInterval_upBound', 'residuals', 'ss_res', 'ss_tot',
												'r_squared', 'CHalf_normalized'])
									for column in sCurveDF.columns.tolist():
										sCurveDF[column] = [[]] * len(repDF)
									sCurveDF[['Accession','Start']] = repDF[['Accession','Start']]
									tqdm.pandas(desc=self.repInfo['condition'] + ' Rep Processing')
									sCurveDF = sCurveDF.progress_apply(seperate_rep_analysis_apply, axis=1, repDF=repDF, repInfo=self.repInfo, MINIMUM_PTS=MINIMUM_PTS, OUTLIER_CUTOFF=OUTLIER_CUTOFF)
									sCurveDF = pd.concat([repDF[['Accession@Peptide']+self.repInfo['norm ct headers']],sCurveDF],axis=1)
									self.repInfo['sCurve data df'] = sCurveDF  # not actually faster repDF.apply(seperate_rep_analysis_apply,axis=1,repInfo=repInfo,rep_sCurveDataList=rep_sCurveDataList,MINIMUM_PTS=MINIMUM_PTS)

									""" Add curve fit data to DataFrame """
									curve_fitDFOutputHeaderList = ['slope', 'fitCurve_B', 'fitCurve_A', 'CHalf', 'fitCurve_b', 'B_stderror',
																'A_stderror',
																'CHalf_stderror', 'b_stderror', 'CHalf_ConfidenceInterval', 'ratioTOrange',
																'CHalf_confidenceInterval_lowBound', 'CHalf_confidenceInterval_upBound',
																'b_confidenceInterval', 'b_confidenceInterval_lowBound',
																'b_confidenceInterval_upBound', 'r_squared', 'CHalf_normalized']
									# initialize headers in DataFrame for curve_fit data
									# for header in curve_fitDFOutputHeaderList:
									# repDF[header] = 0
									# for every row in DF, add sCurveData where 'title' is...
									repDF = pd.concat([repDF, sCurveDF[curve_fitDFOutputHeaderList]], axis=1)
									''' REORDER repDF Data to Desired Arrangement and SORT '''
									origCTdata = [str(x) for x in self.repInfo['conc-temp list']]
									newDFheaderOrder = ['Accession@Peptide', 'Accession', 'Description', 'Peptide', 'Start',
														'End'] + curve_fitDFOutputHeaderList + self.repInfo['norm ct headers'] + [
														'#Non_Zero'] + origCTdata + ['Delta 6-0'] + ['Range/Mean']
									#print(newDFheaderOrder)

									repDF = repDF[newDFheaderOrder]
									repDF.sort_values(by=['Accession','Start'],ignore_index=True,inplace=True)
									repDF.rename_axis('v4.3',axis='index',inplace=True)
									if self.repInfo['CD or HD'] == 'HD':
										heatDF = repDF.copy()
										norm_temp_headers = []
										orig_temp_headers = []
										orig_temp_headers_norm = []
										for header in self.repInfo['conc-temp list']:
											norm_temp_headers.append(str(header))
										for header in self.repInfo['original-temp list']:
											orig_temp_headers.append(str(header))
											orig_temp_headers_norm.append(str(header)+'_Norm')
										self.repInfo['orig_temp_headers'] = orig_temp_headers
										heatDF.rename(columns=dict(zip(norm_temp_headers,orig_temp_headers)),inplace=True)
										heatDF.rename(columns=dict(zip(norm_temp_headers,orig_temp_headers)),inplace=True)
										heatDF.rename(columns=dict(zip(self.repInfo['norm ct headers'],orig_temp_headers_norm)),inplace=True)
										tqdm.pandas(desc= self.repInfo['condition'] + ' HD Adjustments')
										heatDF = heatDF.progress_apply(denormalize_apply,axis=1,repInfo=self.repInfo,columns=['CHalf','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound'],other=['CHalf_stderror','CHalf_ConfidenceInterval'])
										""" Export DataFrame w/ Original Data, Norm data, and Curve Fit Data to .csv file """
										#print(f"EXPORT TO .CSV: {repInfo['condition']}_Rep{repInfo['repNum']}_OUTPUT.csv")
										heatDF.to_csv(f"{self.repInfo['condition']}_Rep{str(int(self.repInfo['repNum']))}_OUTPUT.csv")
									else:
										""" Export DataFrame w/ Original Data, Norm data, and Curve Fit Data to .csv file """
										#print(f"EXPORT TO .CSV: {repInfo['condition']}_Rep{repInfo['repNum']}_OUTPUT.csv")
										repDF.to_csv(f"{self.repInfo['condition']}_Rep{str(int(self.repInfo['repNum']))}_OUTPUT.csv")
									""" ------------- GRAPHING FUNCTIONS ---------------- """
									if MAKEGRAPH_REPS == True:
										""" plot_color """
										tqdm.pandas(desc=self.repInfo['condition'] + ' Rep Graphs')
										sCurveDF.sort_values(by=['Accession','Start'],ignore_index=True,inplace=True)
										sCurveDF.progress_apply(makegraph_reps_apply, axis=1, repInfo=self.repInfo, file_type=file_type, OUTLIER_CUTOFF=OUTLIER_CUTOFF)
							if COMBINED_CONDITION_ANALYSIS:
								# Make list of condition types
								# then, for every condition,
								# 	for every repInfo that has 'condition', add it to list
								# Get all unique conditions in a list to sort reps later
								conditionsList = []
								for self.repInfo in RepInfoLists:
									# if the condition name is not already in the list, add it
									if self.repInfo['condition'] not in conditionsList:
										conditionsList.append(self.repInfo['condition'])
								#print(f"Conditions List: {conditionsList}")

								# For each condition, combine and analyze applicable rep data
								for condition in conditionsList:
									con_sCurveDataList = []
									# 'Accession@Peptide' is the label we use to combine rep data lines.
									accession_strtend_desc_dict = {}
									# Create DataFrame for condition, adding Accession@Peptide set with the unique peptides.
									conDF = pd.DataFrame(columns=['Accession@Peptide','Accession','Description','Peptide','Start','End']+['ydata','#pts','#non Zero','valid_xValues','valid_yValues','sCurve_xValues','sCurve_yValues','enough_points','popt','popt_lowBound','popt_upBound','pcov','B_stderror','A_stderror','CHalf_stderror','b_stderror','CHalf_ConfidenceInterval','concRange','ratioTOrange','fitCurve_B','fitCurve_A','CHalf','fitCurve_b','slope','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound','b_confidenceInterval','b_confidenceInterval_lowBound','b_confidenceInterval_upBound','residuals','ss_res','ss_tot','r_squared','CHalf_normalized']+['trim_VALID','trim_xValues','trim_yValues','trim_#pts','trim_popt','trim_popt_lowBound','trim_popt_upBound','trim_pcov','trim_sCurve_xValues','trim_sCurve_yValues','trim_B_stderror','trim_A_stderror','trim_CHalf_stderror','trim_b_stderror','trim_CHalf_ConfidenceInterval','trim_concRange','trim_ratioTOrange','trim_B','trim_A','trim_CHalf','trim_b','trim_slope','trim_CHalf_confidenceInterval_lowBound','trim_CHalf_confidenceInterval_upBound','trim_b_confidenceInterval','trim_b_confidenceInterval_lowBound','trim_b_confidenceInterval_upBound','trim_residuals','trim_ss_res','trim_ss_tot','trim_r_squared','trim_CHalf_normalized'])
									# for every rep
									for self.repInfo in RepInfoLists:
										# if the rep is from the current condition, add it's A@P to the set
										if self.repInfo['condition'] == condition:
											#print(repInfo['DataFrame'])
											conDF = pd.concat([conDF,self.repInfo['DataFrame'][['Accession@Peptide','Accession','Description','Peptide','Start','End']]],ignore_index=True)
									#Remove duplicates
									conDF = conDF.drop_duplicates(subset='Accession@Peptide',ignore_index=True)

									# Add labeled headers for each rep [###_Rep#], and merge rep norm data from repDF into conDF
									con_conctemp_labeledheaders = []
									con_conctemp_headers = []
									tempDFlist = []
									rep_labeled_headers_sCurve = []
									deltaDFlst = []
									rangeDFlst = []
									for self.repInfo in RepInfoLists:
										if self.repInfo['condition'] == condition:  # for every rep of the current condition
											# Create tempDF with A@P and Normalized Data
											tempDF = self.repInfo['DataFrame'][['Accession@Peptide']+self.repInfo['norm ct headers']]
											deltaDF = self.repInfo['DataFrame'][['Accession@Peptide']+['Delta 6-0']]
											deltaDF.columns = ['Accession@Peptide']+['Delta 6-0' + '_Rep' + str(int(self.repInfo['repNum']))]
											deltaDFlst.append(deltaDF)
											rangeDF = self.repInfo['DataFrame'][['Accession@Peptide']+['Range/Mean']]
											rangeDF.columns = ['Accession@Peptide']+['Range/Mean' + '_Rep' + str(int(self.repInfo['repNum']))]
											rangeDFlst.append(rangeDF)
											# Make list of rep labeled headers for the norm data. Ex: "###_Rep# headers"
											# Labels which rep the data came from and enables us to merge the data to one DataFrame
											replabeledheaders = []
											if self.repInfo['CD or HD'] == 'HD':
												for header in self.repInfo['original-temp list']:
													replabeledheaders.append(str(header) + '_Rep' + str(int(self.repInfo['repNum'])))
												rep_labeled_headers_sCurve += replabeledheaders
												self.repInfo['replabeled_headers'] = replabeledheaders
												con_conctemp_labeledheaders.extend(replabeledheaders)
												# Rename tempDF's columns to include the _Rep# identifiers
												tempDF.columns = ['Accession@Peptide'] + replabeledheaders
												conDF = pd.merge(conDF, tempDF, on=['Accession@Peptide'], how='left')
												# This merge puts normalized data from Rep1 into ###_Rep1 columns for each rep (Rep2 in ###_Rep2, etc.)
												# If there is no data for that protein from a particular rep, that cell is left blank
												# Adds original conc/temp values to this list for use later...
												con_conctemp_headers.extend(self.repInfo['conc-temp list'])
											else:
												for header in self.repInfo['conc-temp list']:
													replabeledheaders.append(str(header) + '_Rep' + str(int(self.repInfo['repNum'])))
												rep_labeled_headers_sCurve += replabeledheaders
												self.repInfo['replabeled_headers'] = replabeledheaders
												con_conctemp_labeledheaders.extend(replabeledheaders)
												# Rename tempDF's columns to include the _Rep# identifiers
												tempDF.columns = ['Accession@Peptide'] + replabeledheaders
												conDF = pd.merge(conDF, tempDF, on=['Accession@Peptide'], how='left')
												# This merge puts normalized data from Rep1 into ###_Rep1 columns for each rep (Rep2 in ###_Rep2, etc.)
												# If there is no data for that protein from a particular rep, that cell is left blank
												# Adds original conc/temp values to this list for use later...
												con_conctemp_headers.extend(self.repInfo['conc-temp list'])
									
									conDF['valid_xValues'] = [np.nan]*len(conDF)
									conDF['valid_yValues'] = [np.nan]*len(conDF)
									#conDF[['ydata','#pts','#non Zero','valid_xValues','valid_yValues','sCurve_xValues','sCurve_yValues','enough_points','popt','popt_lowBound','popt_upBound','pcov','B_stderror','A_stderror','CHalf_stderror','b_stderror','CHalf_ConfidenceInterval','concRange','ratioTOrange','fitCurve_B','fitCurve_A','CHalf','fitCurve_b','slope','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound','b_confidenceInterval','b_confidenceInterval_lowBound','b_confidenceInterval_upBound','residuals','ss_res','ss_tot','r_squared','CHalf_normalized']+['trim_VALID','trim_xValues','trim_yValues','trim_#pts','trim_popt','trim_popt_lowBound','trim_popt_upBound','trim_pcov','trim_sCurve_xValues','trim_sCurve_yValues','trim_B_stderror','trim_A_stderror','trim_CHalf_stderror','trim_b_stderror','trim_CHalf_ConfidenceInterval','trim_concRange','trim_ratioTOrange','trim_B','trim_A','trim_CHalf','trim_b','trim_slope','trim_CHalf_confidenceInterval_lowBound','trim_CHalf_confidenceInterval_upBound','trim_b_confidenceInterval','trim_b_confidenceInterval_lowBound','trim_b_confidenceInterval_upBound','trim_residuals','trim_ss_res','trim_ss_tot','trim_r_squared','trim_CHalf_normalized']] = np.nan
									tqdm.pandas(desc=self.repInfo['condition'] + ' Combined Fitting')
									conDF = conDF.progress_apply(combined_fit_apply,axis=1,con_conctemp_labeledheaders=con_conctemp_labeledheaders,con_conctemp_headers=con_conctemp_headers,MINIMUM_PTS=MINIMUM_PTS,removeOutlier_2xStdErr=removeOutlier_2xStdErr,condition=condition,OUTLIER_CUTOFF=OUTLIER_CUTOFF)
									#sCurveDF = pd.DataFrame(columns=['Accession@Peptide','ydata','#pts','#non Zero','valid_xValues','valid_yValues','sCurve_xValues','sCurve_yValues','enough_points','popt','popt_lowBound','popt_upBound','pcov','B_stderror','A_stderror','CHalf_stderror','b_stderror','CHalf_ConfidenceInterval','concRange','ratioTOrange','fitCurve_B','fitCurve_A','CHalf','fitCurve_b','slope','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound','b_confidenceInterval','b_confidenceInterval_lowBound','b_confidenceInterval_upBound','residuals','ss_res','ss_tot','r_squared','CHalf_normalized']+['trim_VALID','trim_xValues','trim_yValues','trim_#pts','trim_popt','trim_popt_lowBound','trim_popt_upBound','trim_pcov','trim_sCurve_xValues','trim_sCurve_yValues','trim_B_stderror','trim_A_stderror','trim_CHalf_stderror','trim_b_stderror','trim_CHalf_ConfidenceInterval','trim_concRange','trim_ratioTOrange','trim_B','trim_A','trim_CHalf','trim_b','trim_slope','trim_CHalf_confidenceInterval_lowBound','trim_CHalf_confidenceInterval_upBound','trim_b_confidenceInterval','trim_b_confidenceInterval_lowBound','trim_b_confidenceInterval_upBound','trim_residuals','trim_ss_res','trim_ss_tot','trim_r_squared','trim_CHalf_normalized'] + rep_labeled_headers_sCurve)
									#sCurveDF[['Accession@Peptide','ydata','#pts','#non Zero','valid_xValues','valid_yValues'] + rep_labeled_headers_sCurve] = conDF[['Accession@Peptide','ydata','#pts','#non Zero','valid_xValues','valid_yValues'] + rep_labeled_headers_sCurve].copy()
									sCurveDF = conDF[['Accession','Start','Accession@Peptide','ydata','#pts','#non Zero','valid_xValues','valid_yValues','sCurve_xValues','sCurve_yValues','enough_points','popt','popt_lowBound','popt_upBound','pcov','B_stderror','A_stderror','CHalf_stderror','b_stderror','CHalf_ConfidenceInterval','concRange','ratioTOrange','fitCurve_B','fitCurve_A','CHalf','fitCurve_b','slope','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound','b_confidenceInterval','b_confidenceInterval_lowBound','b_confidenceInterval_upBound','residuals','ss_res','ss_tot','r_squared','CHalf_normalized','trim_VALID','trim_xValues','trim_yValues','trim_#pts','trim_popt','trim_popt_lowBound','trim_popt_upBound','trim_pcov','trim_sCurve_xValues','trim_sCurve_yValues','trim_B_stderror','trim_A_stderror','trim_CHalf_stderror','trim_b_stderror','trim_CHalf_ConfidenceInterval','trim_concRange','trim_ratioTOrange','trim_B','trim_A','trim_CHalf','trim_b','trim_slope','trim_CHalf_confidenceInterval_lowBound','trim_CHalf_confidenceInterval_upBound','trim_b_confidenceInterval','trim_b_confidenceInterval_lowBound','trim_b_confidenceInterval_upBound','trim_residuals','trim_ss_res','trim_ss_tot','trim_r_squared','trim_CHalf_normalized'] + rep_labeled_headers_sCurve]
									#sCurveDF = sCurveDF.apply(combined_fit_apply2,axis=1,MINIMUM_PTS=MINIMUM_PTS,removeOutlier_2xStdErr=removeOutlier_2xStdErr)
									conDF = conDF[['Accession@Peptide','Accession','Peptide','Description','Start','End'] +  rep_labeled_headers_sCurve + ['#pts','#non Zero','slope','fitCurve_B','fitCurve_A','CHalf','fitCurve_b','B_stderror','A_stderror','CHalf_stderror','b_stderror','CHalf_ConfidenceInterval','ratioTOrange','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound','b_confidenceInterval','b_confidenceInterval_lowBound','b_confidenceInterval_upBound','r_squared','CHalf_normalized','trim_#pts','trim_slope','trim_B','trim_A','trim_CHalf','trim_b','trim_B_stderror','trim_A_stderror','trim_CHalf_stderror','trim_b_stderror','trim_CHalf_ConfidenceInterval','trim_ratioTOrange','trim_CHalf_confidenceInterval_lowBound','trim_CHalf_confidenceInterval_upBound','trim_b_confidenceInterval','trim_b_confidenceInterval_lowBound','trim_b_confidenceInterval_upBound','trim_r_squared','trim_CHalf_normalized']]
									for df in deltaDFlst:
										conDF = pd.merge(conDF, df, on=['Accession@Peptide'], how='left')
									for df in rangeDFlst:
										conDF = pd.merge(conDF, df, on=['Accession@Peptide'], how='left')
									'''for column in ['ydata','#pts','#non Zero','valid_xValues','valid_yValues','sCurve_xValues','sCurve_yValues','enough_points','popt','popt_lowBound','popt_upBound','pcov','B_stderror','A_stderror','CHalf_stderror','b_stderror','CHalf_ConfidenceInterval','concRange','ratioTOrange','fitCurve_B','fitCurve_A','CHalf','fitCurve_b','slope','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound','b_confidenceInterval','b_confidenceInterval_lowBound','b_confidenceInterval_upBound','residuals','ss_res','ss_tot','r_squared','CHalf_normalized','trim_VALID','trim_xValues','trim_yValues','trim_#pts','trim_popt','trim_popt_lowBound','trim_popt_upBound','trim_pcov','trim_sCurve_xValues','trim_sCurve_yValues','trim_B_stderror','trim_A_stderror','trim_CHalf_stderror','trim_b_stderror','trim_CHalf_ConfidenceInterval','trim_concRange','trim_ratioTOrange','trim_B','trim_A','trim_CHalf','trim_b','trim_slope','trim_CHalf_confidenceInterval_lowBound','trim_CHalf_confidenceInterval_upBound','trim_b_confidenceInterval','trim_b_confidenceInterval_lowBound','trim_b_confidenceInterval_upBound','trim_residuals','trim_ss_res','trim_ss_tot','trim_r_squared','trim_CHalf_normalized']:
										del conDF[column] #remove unnecessary columns'''
									""" Add curve fit data to DataFrame """
									curve_fitDFOutputHeaderList = ['slope', 'fitCurve_B', 'fitCurve_A', 'CHalf', 'fitCurve_b', 'B_stderror', 'A_stderror',
																'CHalf_stderror', 'b_stderror', 'CHalf_ConfidenceInterval', 'ratioTOrange',
																'CHalf_confidenceInterval_lowBound', 'CHalf_confidenceInterval_upBound',
																'b_confidenceInterval', 'b_confidenceInterval_lowBound',
																'b_confidenceInterval_upBound', 'r_squared', 'CHalf_normalized']
									if removeOutlier_2xStdErr == True:
										trim_curve_fitDFOutputHeaderList = ['trim_#pts','trim_slope', 'trim_B', 'trim_A', 'trim_CHalf', 'trim_b', 'trim_B_stderror',
																			'trim_A_stderror', 'trim_CHalf_stderror', 'trim_b_stderror',
																			'trim_CHalf_ConfidenceInterval', 'trim_ratioTOrange',
																			'trim_CHalf_confidenceInterval_lowBound',
																			'trim_CHalf_confidenceInterval_upBound', 'trim_b_confidenceInterval',
																			'trim_b_confidenceInterval_lowBound','trim_b_confidenceInterval_upBound',
																			'trim_r_squared', 'trim_CHalf_normalized']
									# for every row in DF, add sCurveData where 'title' is...
									for header in curve_fitDFOutputHeaderList:
										conDF[header] = sCurveDF[header]
									#conDF[curve_fitDFOutputHeaderList] = conDF[curve_fitDFOutputHeaderList].fillna(0)
									if removeOutlier_2xStdErr == True:
										for header in trim_curve_fitDFOutputHeaderList:
											conDF[header] = sCurveDF[header]
										#conDF[trim_curve_fitDFOutputHeaderList] = conDF[trim_curve_fitDFOutputHeaderList].fillna('cnc')
								
									#print(f"Exporting {condition + '_Combined_OUTPUT.csv'} . . .")
									#print("\n")
									conDF.sort_values(by=['Accession','Start'],ignore_index=True,inplace=True)
									conDF.rename_axis('v4.3',axis='index',inplace=True)
									if self.repInfo['CD or HD'] == 'HD':
										heatDF = conDF.copy()
										tqdm.pandas(desc=self.repInfo['condition'] + ' HD Adjustments')
										heatDF = heatDF.progress_apply(denormalize_apply,axis=1,repInfo=self.repInfo,columns=['CHalf','CHalf_confidenceInterval_lowBound','CHalf_confidenceInterval_upBound']+['trim_CHalf','trim_CHalf_confidenceInterval_lowBound','trim_CHalf_confidenceInterval_upBound'],other=['CHalf_stderror','CHalf_ConfidenceInterval']+['trim_CHalf_stderror','trim_CHalf_ConfidenceInterval'])
										heatDF.to_csv(condition + '_Combined_OUTPUT.csv')
									else:
										conDF.to_csv(condition + '_Combined_OUTPUT.csv')

									"""=================== GRAPHING ================"""
									if GRAPH_COMBINED:

										# Graph the individual rep data points (not as curve) with unique indicators
										condition_repnumlist = []
										CDHD_list = []
										original_temps = None
										plot_colorcode = 0
										for self.repInfo in RepInfoLists:
											if self.repInfo['condition'] == condition:
												condition_repnumlist.append(self.repInfo['repNum'])
												CDHD_list.append(self.repInfo['CD or HD'])
												if self.repInfo['CD or HD'] == 'HD':
													original_temps = self.repInfo['original-temp list']
												self.repInfo['plot color'] = plot_colors[plot_colorcode]
												plot_colorcode += 1
												if plot_colorcode > 5:
													plot_colorcode = plot_colorcode%6
										tqdm.pandas(desc=self.repInfo['condition'] + ' Combined Graphs')
										sCurveDF.sort_values(by=['Accession','Start'],ignore_index=True,inplace=True)
										sCurveDF.progress_apply(combined_graph_apply,axis=1,condition_repnumlist=condition_repnumlist,removeOutlier_2xStdErr=removeOutlier_2xStdErr,R_SQUARED_CUTOFF=R_SQUARED_CUTOFF,repInfo=self.repInfo,condition=condition,file_type=file_type,CDHD_list=CDHD_list,original_temps=original_temps,CHALF_RANGE_CUTOFF=CHALF_RANGE_CUTOFF,CONFIDENCE_INTERVAL_CUTOFF=CONFIDENCE_INTERVAL_CUTOFF,OUTLIER_CUTOFF=OUTLIER_CUTOFF,RepInfoLists=RepInfoLists)
							os.chdir(os.path.dirname(MASTERFILE)) #reset just in case
							''' LABEL EFFICIENCY INTEGRATION '''
							if LE:
								for file in os.listdir():
									if "_Rep" in file and os.path.isfile(file):
										LEname = file.replace('_OUTPUT.csv','')
										file = os.path.realpath(file)
										LEDF = LabelFinder(file,LEname,version=VERSION,labels=self.CHdefaultslst[23])
										if os.path.exists('Efficiency Outputs'):
											LEDF[0].to_csv('Efficiency Outputs/' + LEname + ' Label Efficiency.csv',index=False)
											LEDF[1].to_csv('Efficiency Outputs/' + LEname + ' Tags.csv',index=False)
										else:
											os.mkdir('Efficiency Outputs')
											LEDF[0].to_csv('Efficiency Outputs/' + LEname + ' Label Efficiency.csv',index=False)
											LEDF[1].to_csv('Efficiency Outputs/' + LEname + ' Tags.csv',index=False)
							''' FITTING EFFICIENCY INTEGRATION '''
							if FE and removeOutlier_2xStdErr and COMBINED_CONDITION_ANALYSIS:
								for file in os.listdir():
									if "Combined_OUTPUT.csv" in file and os.path.isfile(file):
										FEname = file.replace('_Combined_OUTPUT.csv','')
										FElst = FittingEfficiency(file,FEname,version=VERSION,CHalflow=float(self.FEdefaultslst[0]),CHalfhigh=float(self.FEdefaultslst[1]),rsquared=float(self.FEdefaultslst[2]),confintlow=float(self.FEdefaultslst[3]),confinthigh=float(self.FEdefaultslst[4]))
										if os.path.exists('Efficiency Outputs'):
											FElst[0].to_csv('Efficiency Outputs/' + FEname + ' Fitting Efficiency.csv',index=False)
											FElst[2].to_csv('Efficiency Outputs/' + FEname + ' Fitted Peptides.csv',index=False)
										else:
											os.mkdir('Efficiency Outputs')
											FElst[0].to_csv('Efficiency Outputs/' + FEname + ' Fitting Efficiency.csv',index=False)
											FElst[2].to_csv('Efficiency Outputs/' + FEname + ' Fitted Peptides.csv',index=False)
										if CS or PM:
											FElst[1].to_csv(FEname + ' Label Sites.csv',index=True)
											CLS = LabelSites_Combined(FEname + ' Label Sites.csv',version=VERSION,MINIMUM_PTS=MINIMUM_PTS,OUTLIER_CUTOFF=OUTLIER_CUTOFF,CHalflow=float(self.FEdefaultslst[0]),CHalfhigh=float(self.FEdefaultslst[1]),rsquared=float(self.FEdefaultslst[2]),confintlow=float(self.FEdefaultslst[3]),confinthigh=float(self.FEdefaultslst[4]))
											CLS[0].to_csv(FEname + ' Combined Label Sites.csv',index=True)
											CLS[1].to_csv(FEname + ' Removed Sites.csv',index=True)
							''' PROTEIN MAPPER INTEGRATION (Residue Mapper)'''
							if PM:
								if not os.path.exists('Residue Mapper Outputs'):
									os.mkdir('Residue Mapper Outputs')
								for file in os.listdir():
									if "Combined Label Sites.csv" in file:
										ResidueMapper_2(file,'Residue Mapper Outputs',dynamic=DYNAMIC,min=YMIN,max=YMAX,file_type=file_type,labels=self.CHdefaultslst[23])
						''' COMBINED SITE AND COMBINED RESIDUE MAPPER INTEGRATION '''
						os.chdir(dir_name)
						CS_inputs = []
						CRM_inputs = []
						if len(combinedsite_conditions) > 1:
							for folder in combinedsite_conditions: #prepping list of "Label Sites.csv" files for processing
								os.chdir(folder)
								for file in os.listdir():
									if "Label Sites.csv" in file and "Combined Label Sites.csv" not in file:
										CS_inputs.append(os.path.realpath(file))
									if "Combined Label Sites.csv" in file:
										CRM_inputs.append(os.path.realpath(file))
							project_name = dir_name.split('\\')[-1].replace(' CHalf Project','')
							project_name = project_name.split('/')[-1].replace(' CHalf Project','')
							if not os.path.exists(dir_name + '/Combined Site Outputs'):
								os.mkdir(dir_name + '/Combined Site Outputs')
							CombinedSite(CS_inputs,dir_name + '/Combined Site Outputs',project_name,version=VERSION,dynamic=DYNAMIC,min=YMIN,max=YMAX,file_type=file_type)
							CombinedResidueMapper_2(CRM_inputs,dir_name,project_name,version=VERSION,dynamic=DYNAMIC,min=YMIN,max=YMAX,file_type=file_type,labels=self.CHdefaultslst[23])
						''' GIANT OUTPUT PREPARATION '''
						os.chdir(dir_name)
						if len(giantoutput_conditions) > 0:
							combinedDFlst = []
							print('GIANT OUTPUT CONDITIONS:')
							print(giantoutput_conditions)
							for folder in giantoutput_conditions: #grabbing combined outputs of participating conditions
								os.chdir(folder)
								for file in os.listdir():
									if '_Combined_OUTPUT.csv' in file:
										tempDF = pd.read_csv(file)
										combinedname = file.replace('_Combined_OUTPUT.csv','')
										columns_dict = {}
										columnslst = tempDF.columns.values.tolist()
										for i in range(len(columnslst)-7): #renaming columns
											columns_dict.update({columnslst[i+7]:combinedname + ' ' + columnslst[i+7]})
										tempDF = tempDF.rename(axis=1,mapper=columns_dict)#.drop(axis=1,labels='Unnamed: 0')
										combinedDFlst.append(tempDF) #adding dataframe to list of dataframes for composition
							#make a list of all Accession@Peptide
							accessionpeptidelst = []
							accessionlst = []
							peptidelst = []
							descriptionlst = []
							startlst = []
							endlst = []

							for df in combinedDFlst:
								for i in range(len(df['Accession@Peptide'].tolist())):
									if df['Accession@Peptide'].tolist()[i] not in accessionpeptidelst:
										accessionpeptidelst.append(df['Accession@Peptide'].tolist()[i])
										accessionlst.append(df['Accession'].tolist()[i])
										peptidelst.append(df['Peptide'].tolist()[i])
										descriptionlst.append(df['Description'].tolist()[i])
										startlst.append(df['Start'].tolist()[i])
										endlst.append(df['End'].tolist()[i])
							giantDF = pd.DataFrame(columns=['Accession@Peptide','Accession','Peptide','Description','Start','End'])
							giantDF['Accession@Peptide'] = accessionpeptidelst
							giantDF['Accession'] = accessionlst
							giantDF['Peptide'] = peptidelst
							giantDF['Description'] = descriptionlst
							giantDF['Start'] = startlst
							giantDF['End'] = endlst

							#Merge dataframes
							for i in range(len(combinedDFlst)):
								giantDF = giantDF.merge(combinedDFlst[i],how='left')#.drop(axis=1,labels='Unnamed: 0')
							#Export
							os.chdir(dir_name)
							giantDF.rename_axis('v4.3',axis='index',inplace=True)
							project_name = dir_name.split('\\')[-1].split('/')[-1].replace(' CHalf Project','')
							print(dir_name)
							giantDF.to_csv(project_name + '_GIANT_OUTPUT.csv')
						self.Message3()
					except TypeError:
						traceback.print_exc()
						self.Error10()
					except:
						traceback.print_exc()
						self.Error9()
					
			except FileNotFoundError:
				self.Error8()

''' WINDOW CALLER '''
if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	'''MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())'''
	gui = Ui_MainWindow()
	gui.show()
	app.exec_()

# END OF CHALF