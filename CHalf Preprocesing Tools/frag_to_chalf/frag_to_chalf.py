# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 17:25:38 2024

@author: chadhyer

Converts Fragpipe Outputs from IPSA_DDA and IPSA_DIA standard workflows into CHalf-compatible inputs
"""

import sys, os
import pandas as pd
import numpy as np


args = sys.argv
name = args[1]
#manifest = args[2]
method = args[2]
source = args[3]
try:
    args[4]
    custom_fasta = True
except:
    custom_fasta = False

returnValue = 0

#name, method, source, custom_fasta = 'C_GPE_New', 'DIA', 'C_FP_Hybrid_Group_PE', True

#manDF = pd.read_csv(manifest,delimiter='\t',names=['File','Experiment','Replicate','Method'])
#conc_dict = dict(zip(manDF['File'],manDF['Replicate'].tolist()))

def custom_fasta_extract(row,quan=False):
    protID = row['Protein ID']
    if ';' in protID:
        newID, mut, loc = protID.split(';')
        if not quan:
            newStart, newEnd = [int(x) for x in loc.split('-')]
            newEN = row['Entry Name'].split(';')[0]
            row['Start'] = newStart
            row['End'] = newEnd
            row['Entry Name'] = newEN
        row['Protein Description'] = f'{newID}_{mut}'
        row['Mutation'] = mut
        row['Protein ID'] = newID
    else:
        row['Mutation'] = ''
    return row

def DDA(name,source):
    ptm_dict = {
        '+15.9949' : '+15.99',
        '+31.9898' : '+31.99',
        '+47.9847' : '+47.98',
        '+-17.0265' : '-17.03',
        '+125.8966' : '+125.90',
        '+251.7933' : '+251.79',
        '+57.0215' : '+57.02'
        }
    file = f'{source}/combined_modified_peptide.tsv'
    #[f'{name}_{i} Intensity' for i in range(10)]

    df = pd.read_csv(file,delimiter='\t')
    points = [col for col in df.columns if 'Intensity' in col and 'Max' not in col]
    
    pepDF=pd.DataFrame()
    pepDF['Protein Accession'] = df['Protein'].str.replace('sp|','')
    pepDF['Peptide'] = df['Modified Sequence'].str.replace('[','(+').str.replace(']',')')
    for ptm in ptm_dict:
        repl = ptm_dict[ptm]
        pepDF['Peptide'] = pepDF['Peptide'].str.replace(ptm,repl,regex=False)
    pepDF[points] = df[points]
    pepDF[['Start','End']] = df[['Start','End']]
    protDF = pd.DataFrame()
    protDF['Description'] = df['Protein Description']
    protDF['Accession'] = df['Protein'].str.replace('sp\|','')
    protDF.drop_duplicates(inplace=True)
    try:
        os.mkdir(f'outputs/{name}')
    except FileExistsError:
        None
    pepDF.to_csv(f'outputs/{name}/{name}.protein-peptides.csv',index=False)
    protDF.to_csv(f'outputs/{name}/{name}.proteins.csv',index=False)
def DIA(name,source):
    ptm_dict = {
        'UniMod:35' : '+15.99',
        'UniMod:425' : '+31.99',
        'UniMod:1327' : '+31.99',
        'UniMod:345' : '+47.98',
        'UniMod:28' : '-17.03',
        'UniMod:129' : '+125.90',
        'UniMod:130' : '+251.79',
        }
    
    pep_file = f'{source}/peptide.tsv'
    quant_file = f'{source}/diann-output/report.pr_matrix.tsv'
    
    pepDF = pd.read_csv(pep_file,delimiter='\t')
    quanDF = pd.read_csv(quant_file,delimiter='\t')
    
    conc_cols = [col for col in quanDF.columns if '\\' in col]
    conc_list = [int(conc.split('\\')[-1].split('-')[-1][0]) for conc in conc_cols]
    conc_dict = dict(zip(conc_cols,conc_list))
    
    quanDF.rename(columns={'Protein.Ids':'Protein ID','Modified.Sequence':'Modified Peptide','Stripped.Sequence':'Peptide'},inplace=True)
    pepDF.rename(columns={'Protein Start':'Start','Protein End':'End'},inplace=True)
    if custom_fasta:
        pepDF = pepDF.apply(custom_fasta_extract,axis=1)
    pepDF['Protein Accession'] = pepDF['Protein ID'] + '|' + pepDF['Entry Name']
    if custom_fasta: pepDF = pepDF[['Protein ID','Protein Accession','Protein Description','Peptide','Start','End','Mutation']]
    else: pepDF = pepDF[['Protein ID','Protein Accession','Protein Description','Peptide','Start','End']]
    cols = [col for col in quanDF if '\\' in col]
    if custom_fasta: 
        quanDF = quanDF.apply(custom_fasta_extract,quan=True,axis=1)
        quanDF = quanDF[['Protein ID','Peptide','Modified Peptide','Mutation']+cols]
        quanDF = quanDF.merge(pepDF,how='left',on=['Protein ID','Peptide','Mutation'])
        quanDF = quanDF.groupby(by=['Protein ID', 'Peptide', 'Modified Peptide','Protein Accession', 'Protein Description', 'Start', 'End','Mutation']).sum().reset_index()

    else:
        quanDF = quanDF[['Protein ID','Peptide','Modified Peptide']+cols]
        quanDF = quanDF.merge(pepDF,how='left',on=['Protein ID','Peptide'])
        quanDF = quanDF.groupby(by=['Protein ID', 'Peptide', 'Modified Peptide','Protein Accession', 'Protein Description', 'Start', 'End']).sum().reset_index()

    quanDF[cols] = quanDF[cols].fillna(0)
    
    for ptm in ptm_dict:
        quanDF['Modified Peptide'] = quanDF['Modified Peptide'].str.replace(ptm,ptm_dict[ptm])
    quanDF.rename(columns=conc_dict,inplace=True)
    concentrations = list(conc_dict.values())
    concentrations.sort()
    if custom_fasta: prot_pep = quanDF[['Protein Accession','Modified Peptide']+concentrations+['Start','End','Mutation']].rename(columns={'Modified Peptide':'Peptide'})
    else: prot_pep = quanDF[['Protein Accession','Modified Peptide']+concentrations+['Start','End']].rename(columns={'Modified Peptide':'Peptide'})
    prot_pep = prot_pep.rename(columns=conc_dict)
    prot = quanDF[['Protein Description','Protein Accession']].rename(columns={'Protein Description':'Description','Protein Accession':'Accession'})
    prot = prot.drop_duplicates()
    try:
        os.mkdir(f'outputs/{name}')
    except FileExistsError:
        None
    prot_pep.to_csv(f'outputs/{name}/{name}.protein-peptides.csv',index=False)
    prot.to_csv(f'outputs/{name}/{name}.proteins.csv',index=False)
    return pepDF, quanDF, prot, prot_pep

if method == 'DDA':
    DDA(name,source)
elif method == 'DIA':
    pepDF, quanDF, prot, prot_pep = DIA(name,source)
else:
    print('Non-standard method specified. CHalf Analysis could not be run.')