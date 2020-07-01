#! /usr/bin/env python3
# coding: utf-8
import argparse
import parseur_Diffuse



def extract_composites(path): # Return type : {composite_gene_ID : [[(family,ID of the hit), ...], ...]} and each sub-list is a domain
	res = {}
	with open(path, "r") as composites_file:
		temp= {}
		name = ''
		domain_list = []
		family = []
		for line in composites_file:
			if line.startswith(">"):
				if name != '':
					domain_list.append(family)
					res[name] = domain_list
					temp= {}
					name = ''
					domain_list = []
					family = []
				name = line.strip()[1:]
			elif line.startswith("["):
				if family != []:
					domain_list.append(family)
					family = []
			elif line.startswith("F"):
				liste = line.split()
				family.append((liste[0], liste[1]))
	
	domain_list.append(family)
	res[name] = domain_list
	return res
	
	

def extract_dictionary(path):
	res = {}
	with open(path, "r") as dico_file:
		for line in dico_file:
			assoc = line.split()
			res[assoc[1]] = assoc[0]
	return res

def list_of_uniprot_composites(dico_composites, dico_names):
	if dico_composites == {'': [[]]}:
		return []
	res = []
	for ID in dico_composites.keys():
		res.append(dico_names[ID[1:]])
	return res 




def list_for_all_chromosomes():
	res = []
	compt = 0
	l = list(range(1,23)) + ['x','y']
	for i in l:
		name = "chromosome_" + str(i)
		path_com ="Result/Human_by_chromosome/" + name + "_cleanNetwork_composites/" + name + "_cleanNetwork.composites"  
		dico_composites = extract_composites(path_com)
		
		path_dico = "Result/Human_by_chromosome/" +name+ "_cleanNetwork_composites/" + name + ".cleanNetwork.dico" 
		dico_names = extract_dictionary(path_dico)
		temps = list_of_uniprot_composites(dico_composites, dico_names)
		compt += len(temps)
		res = res + temps
	return res

def main():
	one_by_one = list_for_all_chromosomes()
	
	path_com ="Result/human_reviewed_cleanNetwork_composites/human_reviewed_cleanNetwork.composites"  
	dico_composites = extract_composites(path_com)
	path_dico = "Result/human_reviewed_cleanNetwork_composites/human_reviewed.cleanNetwork.dico"
	dico_names = extract_dictionary(path_dico)
	all_vs_all = list_of_uniprot_composites(dico_composites, dico_names)
	print(len(one_by_one), len(all_vs_all))
	intersect = [c for c in one_by_one if c in all_vs_all]
	print(intersect == one_by_one) # should be true, we want all the fusion event occuring in only one chromosome to appear in an all_vs_all chromosome analysis.
	print(len(intersect))
	print(intersect)
	print('\n\n\n')
	print([c for c in one_by_one if c not in all_vs_all])
if __name__ == "__main__":
	main()
	
	

