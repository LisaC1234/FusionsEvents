#! /usr/bin/env python3
# coding: utf-8
import argparse
import parseur_Diffuse

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f","--fasta",help="""Name of the fasta database to use, after the launcher have been applied on the same database. The associated Diffuse result should be in Result/Diffuse_results/ with the same name + _diffuse.txt""")
	return parser.parse_args()

def extract_composites(fasta): # Return type : {composite_gene_ID : [[(family,ID of the hit), ...], ...]} and each sub-list is a domain
	path = "Result/" +fasta+ "_cleanNetwork_composites/" + fasta + "_cleanNetwork.composites"
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
	path = "Result/" +fasta+ "_cleanNetwork_composites/" + fasta + ".cleanNetwork.dico"
	res = {}
	with open(path, "r") as dico_file:
		for line in dico_file:
			assoc = line.split()
			res[assoc[1]] = assoc[0]
	return res

def list_of_uniprot_composites(dico_composites, dico_names):
	res = []
	for ID in dico_composites.keys():
		res.append(dico_names[ID[1:]])
	return res 

def read_Diffuse_results(fasta):
	path = "Result/Diffuse_results/" +fasta+ "_diffuse.txt"
	with open(path, "r") as result_file:
		for line in result_file:
			res = parseur_Diffuse.parse_Diffuse(line.strip())
	return res


def main():
	args = parse_arguments()
	fasta = args.fasta
	dico_composites = extract_composites(fasta)
	#print("\n dico_composites\n", dico_composites)
	dico_names = extract_dictionary(fasta)
	#print("\n dico_names\n", dico_names)
	list_uniprot_CompositeSearch = list_of_uniprot_composites(dico_composites, dico_names)
	print('##################################################')
	print('CompositeSearch list of composite (', len(list_uniprot_CompositeSearch), ') : ','\n', list_uniprot_CompositeSearch,'\n')
	diffuse_results = read_Diffuse_results(fasta)
	#print(diffuse_results)
	list_uniprot_Diffuse = []
	for event in diffuse_results.keys():
		compo = diffuse_results[event][0][1]
		if compo not in list_uniprot_Diffuse:
			list_uniprot_Diffuse.append(compo)
	print('##################################################')
	print('Diffuse list of composite (',len(list_uniprot_Diffuse),') : ','\n', list_uniprot_Diffuse,'\n')
	compteur = 0
	for Comp in list_uniprot_Diffuse:
		if Comp not in list_uniprot_CompositeSearch:
			print('Caution, the composite : ', Comp , ' is not detected by CompositeSearch')
		else :
			print('The composite : ', Comp, 'detected by Diffuse is also detected by CompositeSearch')
			compteur +=1
	print(compteur, ' composites are found both by CompositeSearch and Diffuse')
	
if __name__ == "__main__":
	main()
	
	

