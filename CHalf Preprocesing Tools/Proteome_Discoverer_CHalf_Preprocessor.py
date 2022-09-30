# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 15:41:34 2022

@author: Chad D. Hyer

This tool is to aid in converting Proteome Discoverer (PD) outputs to CHalf compatible input files.

Documentation: https://github.com/JC-Price/Chalf_public
"""

import pandas as pd

'''
DIRECTIONS FOR CONVERTING PROTEOME DISCOVERER (PD) FILES TO THE PROPER CHALF FORMAT:
    
1. Set 'peptide_txt_path' to the path for your PeptideGroups.txt file from PD
2. Set 'proteins_txt_path' to the path for your Proteins.txt file from PD
3. Find the abundance columns in your PeptideGroups.txt file. Add their names as strings 
   to the list 'abundance_columns'
4. Set 'output_directory' to your desired output directory
5. Set 'output_name' to your desired output name
6. For every PTM searched for in your PD run, calculate the mass shift. Using
   these PTM names and mass shifts, edit 'reporters_dictionary'. It will take the format
   reporters_dictionary = {
       (PTM name 1) : (mass shift 1),
       (PTM name 2) : (mass shift 2),
       ...
       (PTM name n) : (mass shift n)
       }
   As an example of a key set: {'Oxidation' : '+15.99'}
   
   ***It is essential that every single PTM is accounted for, or there will be errors.***
7. Run the code.
8. Take the protein-peptides.csv and proteins.csv files outputed for use with CHalf
'''

#OD PeptideGroups.txt filepath
peptide_txt_path = 'path to PeptideGroups.txt file'

#PD Proteins.txt filepath
proteins_txt_path = 'path to Proteins.txt file'

#Column names of abundances in gradient
abundance_columns = ['Column1','Column2','etc']

#Output directory path
output_directory = 'path to output directory'

#Output name
output_name = 'output name'

#Fill the key section of the dictionary with the modification names reported by PD Ex: 'Oxidation'
#Fill the entry section of the dictionary with the mass shift of the modification in the format + (or -) number Ex: '+15.99'
reporters_dictionary = {
       'PTM name 1' : 'mass shift 1',
       'PTM name 2' : 'mass shift 2',
       '...'
       'PTM name n' : 'mass shift n'
       }

def peptide_mod_adder(row, reporters_dictionary):
    if type(row['Modifications']) == str:
        peptide_split = row['Annotated Sequence'].split('.')
        peptide_lengths = [len(length) for length in peptide_split]
        peptide_index = peptide_lengths.index(max(peptide_lengths))
        truncated_peptide = peptide_split[peptide_index]
        mod_list = []
        index_mod = {}
        indices = [0]
        mods = row['Modifications'].split(']; ')
        for mod in mods:
            cleaned_mod = mod[2:mod.find(' [')]
            corrected_mod = reporters_dictionary[cleaned_mod]
            mod_dict = {'Mod' : cleaned_mod, 'Corrected' : corrected_mod, 'Sites': [], 'Indices' : []}
            ind1 = mod.find('[')+1
            if mod.find(']') == -1:
                ind2 = None
            else:
                ind2 = mod.find(']')
            sites = mod[ind1:ind2].split('; ')
            mod_dict['Sites'] = sites
            for site in sites:
                if 'N-Term' not in site:
                    try:
                        corrected_site = int(site[1:])
                    except ValueError:
                        corrected_site = truncated_peptide.index(site[0])+1
                    indices.append(corrected_site)
                else:
                    corrected_site = 0
                mod_dict['Indices'].append(corrected_site)
                index_mod.update({corrected_site:corrected_mod})
            mod_list.append(mod_dict)
        indices.sort()
        parts = [truncated_peptide[i:j] for i,j in zip(indices, indices[1:]+[None])]
        parts_dict = dict(zip(indices,parts))
        for index in index_mod:
            mod = index_mod[index]
            parts_dict[index] = '(' + mod + ')' + parts_dict[index]
        corrected_sequence = ''.join(list(parts_dict.values()))
        #test = row['Annotated Sequence'].replace(truncated_peptide,corrected_sequence)
        row['Annotated Sequence'] = row['Annotated Sequence'].replace(truncated_peptide,corrected_sequence)
    else:
        None
    pep_range = row['Positions in Master Proteins'][row['Positions in Master Proteins'].index('[')+1:row['Positions in Master Proteins'].index(']')]
    pep_range = pep_range.split('-')
    row['Start'] = int(pep_range[0])
    row['End'] = int(pep_range[1])
    return row


pepDF = pd.read_table(peptide_txt_path)
protDF = pd.read_table(proteins_txt_path)

pepDF['Annotated Sequence'] = pepDF['Annotated Sequence'].str.replace('[','').str.replace(']','')
start_mask = pepDF['Annotated Sequence'].str[0] == '-'
end_mask = pepDF['Annotated Sequence'].str[-1] == '-'
pepDF['Annotated Sequence'] = pd.concat([pepDF['Annotated Sequence'][end_mask].str[:-2],pepDF['Annotated Sequence'][~end_mask]])
pepDF['Annotated Sequence'] = pd.concat([pepDF['Annotated Sequence'][start_mask].str[2:],pepDF['Annotated Sequence'][~start_mask]])
pepDF['Start'] = 0
pepDF['End'] = 0
pepDF = pepDF.apply(peptide_mod_adder,reporters_dictionary=reporters_dictionary,axis=1)

protein_peptides = pepDF[['Master Protein Accessions','Annotated Sequence']+abundance_columns+['Start','End']]
protein_peptides = protein_peptides.rename(columns={'Master Protein Accessions' : 'Protein Accession','Annotated Sequence' : 'Peptide'})
abundance_columns_dict = {}
for i in range(len(abundance_columns)):
    abundance_columns_dict.update({abundance_columns[i]:i})
protein_peptides = protein_peptides.rename(columns=abundance_columns_dict)
proteins = protDF[['Accession','Description']]

protein_peptides.to_csv(output_directory + '/' + output_name + '_protein-peptides.csv')
proteins.to_csv(output_directory + '/' + output_name + '_proteins.csv')