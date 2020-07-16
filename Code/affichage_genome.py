#! /usr/bin/env python3
# coding: utf-8
import argparse
from subprocess import Popen, PIPE

def read_fasta(dico_uniprot):
	res = {}
	list_inconnus = []
	l = list(range(1,23)) + ['x','y']
	for i in l:
		res[i] = []
	for gene in dico_uniprot.keys():
		trouv = False
		for numb in l:
			cmd = ["grep", "-c", gene, "Data/Human_by_chromosome/chromosome_"+str(numb)+".fasta"]
			p = Popen(cmd, stdout=PIPE, stderr=PIPE)
			stdout, stderr = p.communicate()
			if "1" in str(stdout):
				res[numb].append((gene, dico_uniprot[gene]))
				trouv = True
				break
		if not trouv:
			list_inconnus.append(gene)
	#print(list_inconnus)
	return res

def dico_chromosome(dico_uniprot):
	res = {}
	list_inconnus = []
	l = list(range(1,23)) + ['x','y']
	for gene in dico_uniprot.keys():
		trouv = False
		for numb in l:
			cmd = ["grep", "-c", gene, "Data/Human_by_chromosome/chromosome_"+str(numb)+".fasta"]
			p = Popen(cmd, stdout=PIPE, stderr=PIPE)
			stdout, stderr = p.communicate()
			if "1" in str(stdout):
				res[gene] = numb
				trouv = True
				break
		if not trouv:
			list_inconnus.append(gene)
	#print(list_inconnus)
	return res		

def extract_composites(path): # Return type : {composite_gene_ID : [[(family,ID of the hit), ...], ...]} and each sub-list is a domain
	res = {}
	with open(path, "r") as composites_file:
		temp= {}
		name = ''
		domain_list = []
		family = []
		for line in composites_file:
			#print(line)
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

def traduction(list_domain, dico_names):
	res = []
	for d in list_domain:
		temp = []
		for component in d:
			temp.append(dico_names[component[1]])
		res.append(temp)
	return res

def list_of_uniprot_composites(dico_composites, dico_names):
	if dico_composites == {'': [[]]}:
		return []
	res = {}
	for ID in dico_composites.keys():
		res[dico_names[ID[1:]]] = traduction(dico_composites[ID], dico_names)
	return res



def components(list_of_uniprot_ID, dico_composites, inv_dico_names): # return the list of components of the target composites genes, in the all_vs_all computation
	res = []
	for ID in list_of_uniprot_ID:
		name = "C" + inv_dico_names[ID]
		l = dico_composites[name]
		for domain in l:
			#print('\nla', domain)
			for comp in domain:
				res.append(comp[1])	
	return res


def composites_families(list_of_uniprot_ID, inv_dico_names):
	path = "Result/human_reviewed_cleanNetwork_composites/human_reviewed_cleanNetwork.compositesinfo"  
	list_names = [inv_dico_names[c] for c in list_of_uniprot_ID] 
	res = []
	with open(path, 'r') as families:
		for line in families:
			if not line.startswith('#'):
				infos = line.split()
				if infos[0][1:] in list_names:
					res.append(infos[2])
	return len(set(res))



def main():
	
	query = 19
	
	
	path_dico = "Result/human_reviewed_cleanNetwork_composites/human_reviewed.cleanNetwork.dico"
	dico_names = extract_dictionary(path_dico)

	path_com ="Result/human_reviewed_cleanNetwork_composites/human_reviewed_cleanNetwork.composites"  
	composites = extract_composites(path_com)
	uniprot_composites = list_of_uniprot_composites(composites, dico_names)

	
	
	
	composites_by_genes = read_fasta(uniprot_composites)
	composites_n = composites_by_genes[query] # At this point, we have the list of all the composites on the query chromosome. 
	print(composites_n)
	
	wich_chromosome = dico_chromosome(uniprot_composites) # On peut optimiser en donnant la liste des components
	
	# A faire : Il faut obtenir le même dico que composites_n mais à la place des id on veut des (id, chromosome), pour pouvoir ensuite construire le graphe
	
	
	inv_dico_names = {v:k for k,v in dico_names.items()}


	#print(composites_n)
	
	
	
	
	components_n = components(all_vs_all, composites_n, inv_dico_names)
	#print(components_n)


	
		
if __name__ == "__main__":
	main()
	
	

