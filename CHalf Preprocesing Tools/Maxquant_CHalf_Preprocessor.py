# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 15:41:34 2022

@author: Chad D. Hyer

This tool is to aid in converting MaxQuant outputs to CHalf compatible input files.

Documentation: https://github.com/JC-Price/Chalf_public
"""

import pandas as pd
import re

'''
DIRECTIONS FOR CONVERTING MAXQUANT FILES TO THE PROPER CHALF FORMAT:
    
1. Set 'evidence_txt_path' to the path for your evidence.txt file from MaxQuant
2. Set 'peptides_txt_path' to the path for your peptides.txt file from MaxQuant
3. Find the abundance columns in your evidence.txt file. Add their names as strings 
   to the list 'abundance_columns'
4. Set 'output_directory' to your desired output directory
5. Set 'output_name' to your desired output name
6. For every PTM searched for in your MaxQuant run, calculate the mass shift. Using
   these PTM names and mass shifts, edit 'reporters_dictionary'. It will take the format
   reporters_dictionary = {
       (PTM name 1) : (mass shift 1),
       (PTM name 2) : (mass shift 2),
       ...
       (PTM name n) : (mass shift n)
       }
   As an example of a key set: {'Oxidation (M)' : '+15.99'}
   
   ***It is essential that every single PTM is accounted for, or there will be errors.***
7. Run the code.
8. Take the protein-peptides.csv and proteins.csv files outputed for use with CHalf
'''

#MaxQuant evidence.txt filepath
evidence_txt_path = 'path to evidence.txt file'

#MaxQuant peptides.txt filepath
peptides_txt_path = 'path to peptides.txt file'

#Column names of abundances in gradient
abundance_columns = ['Column1','Column2','etc']

#Output directory path
output_directory = 'path to output directory'

#Output name
output_name = 'output name'

#Fill the key section of the dictionary with the modification names reported by MaxQuant Ex: 'Oxidation (M)'
#Fill the entry section of the dictionary with the mass shift of the modification in the format + (or -) number Ex: '+15.99'
reporters_dictionary = {
       'PTM name 1' : 'mass shift 1',
       'PTM name 2' : 'mass shift 2',
       '...'
       'PTM name n' : 'mass shift n'
       }

evDF = pd.read_table(evidence_txt_path)
pepDF = pd.read_table(peptides_txt_path)
evDF = evDF[['Proteins','Modified sequence','Protein names','Peptide ID']+abundance_columns]
corrected_intensities = evDF.groupby('Modified sequence')[abundance_columns].sum().reset_index()
for column in abundance_columns:
    del evDF[column]
evDF = evDF.drop_duplicates()
evDF = evDF.merge(corrected_intensities,how='left',on='Modified sequence')
evDF['Proteins'].fillna('Unreported',inplace=True)
evDF = evDF.merge(pepDF[['Start position','End position','Amino acid before','Amino acid after','id']].rename(columns={'id':'Peptide ID'}),on='Peptide ID',how='left')
evDF['Modified sequence'] = evDF['Amino acid before'].str.replace('-','') + evDF['Modified sequence'] + evDF['Amino acid after'].str.replace('-','')
evDF['Modified sequence'] = evDF['Modified sequence'].str.replace('_','.')
start_mask= evDF['Modified sequence'].str[0] == '.'
end_mask = evDF['Modified sequence'].str[-1] == '.'
evDF['Modified sequence'] = pd.concat([evDF['Modified sequence'][end_mask].str[:-1],evDF['Modified sequence'][~end_mask]])
evDF['Modified sequence'] = pd.concat([evDF['Modified sequence'][start_mask].str[1:],evDF['Modified sequence'][~start_mask]])
for modification in list(reporters_dictionary):
    mass_shift = reporters_dictionary[modification]
    evDF['Modified sequence'] = evDF['Modified sequence'].str.replace(re.escape(modification),mass_shift)
protein_peptides = evDF[['Proteins','Modified sequence']+abundance_columns+['Start position','End position']]
abundance_columns_dict = {}
for i in range(len(abundance_columns)):
    abundance_columns_dict.update({abundance_columns[i]:i})
protein_peptides = protein_peptides.rename(columns={'Proteins':'Protein Accession','Modified sequence':'Peptide','Start position':'Start','End position':'End'})
protein_peptides = protein_peptides.rename(columns=abundance_columns_dict)
proteins = evDF[['Proteins','Protein names']].rename(columns={'Proteins':'Accession','Protein names':'Description'}).drop_duplicates().fillna('Unreported')

protein_peptides.to_csv(output_directory + '/' + output_name + '_protein-peptides.csv')
proteins.to_csv(output_directory + '/' + output_name + '_proteins.csv')