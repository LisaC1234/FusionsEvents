#! /usr/bin/env python3
# coding: utf-8
import argparse

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f","--fasta",help="""Name of the fasta database to use, after the launcher have been applied on the same database. The associated Diffuse result should be in Result/Diffuse_results/ with the same name + _diffuse.txt""")
	return parser.parse_args()

def extract_composites(fasta): # Return type : {composite_gene_ID : [[(family,ID of the hit), ...], ...]} and each sub-list is a domain
	path = "Result/Human_by_chromosome/" +fasta+ "_cleanNetwork_composites/" + fasta + "_cleanNetwork.composites"
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
	
	

def extract_dictionary(fasta):
	path = "Result/Human_by_chromosome/" +fasta+ "_cleanNetwork_composites/" + fasta + ".cleanNetwork.dico"
	res = {}
	with open(path, "r") as dico_file:
		for line in dico_file:
			assoc = line.split()
			res[assoc[1]] = assoc[0]
	return res

def list_of_uniprot_composites(dico_composites, dico_names):
	res = []
	with open("test_list_composite.txt", "w") as result:
		for ID in dico_composites.keys():
			nom_complet = dico_names[ID[1:]]
			nom = nom_complet.split('|')[1]
			res.append(nom)
			result.write(nom + "\n")
	return res 


def main():
	args = parse_arguments()
	fasta = args.fasta
	dico_composites = extract_composites(fasta)
	dico_names = extract_dictionary(fasta)
	list_uniprot_CompositeSearch = list_of_uniprot_composites(dico_composites, dico_names)
	print(list_uniprot_CompositeSearch)
	
if __name__ == "__main__":
	main()
	
	
