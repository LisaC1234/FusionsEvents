#! /usr/bin/env python3
# coding: utf-8
import argparse

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f","--fasta",help="""Name of the fasta database used""")
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
	
	

def analyse(dico): #find every composite that are composed with same-family components
	Composites = list(dico.keys())
	res = []
	pairs = 0
	for i in range(len(Composites)):
		for j in range(i+1, len(Composites)): # every pair of composites is tested only once, to check if they are similar
			pairs +=1
			similar = similarity(dico[Composites[i]],dico[Composites[j]])
			if similar != []:
				res.append(similar)
	probable = probable_families(res, pairs)
	return probable
			
			
				
def similarity(fam_c1, fam_c2): #analy two list of components of two composites and look for similarities. 
	num_matches  = 0
	list_matches = []
	fam_c1 = [[x for (x,y) in z] for z in fam_c1]
	fam_c2 = [[x for (x,y) in z] for z in fam_c2]
	for d1 in range(len(fam_c1)): #iterise on the domains
		for d2 in range(len(fam_c2)):
			for f1 in fam_c1[d1]:
				if f1 in fam_c2[d2]: # we found a match! 
					list_matches.append((f1,(d1,d2)))
					num_matches += 1	
	if verif_order(list_matches):
		return [f for (f, (x, y)) in list_matches]
	return []

		
def verif_order(list_matches):
	if  1 >= len(list_matches) :
		return False
	domains1 = [x for (f,(x,y)) in list_matches] # this list contains the sequential order of the domains that matches for the first Composite genes
	domains2 = [y for (f,(x,y)) in list_matches]
	for i in range(len(domains1) -1):
		if domains1[i] >= domains1[i+1]:
			return False
	for i in range(len(domains2) -1):
		if domains2[i] >= domains2[i+1]:
			return False
	return True


def probable_families(verified_matches, nb_pairs):
	res = []
	items = []
	for l in verified_matches:
		if l not in items:
			items.append(l)
	for family in items:
		tot = verified_matches.count(family)/nb_pairs
		res.append((family, tot ))
	return res



















def main():
	args = parse_arguments()
	fasta = args.fasta
	dico = extract_composites(fasta)
	print(analyse(dico))
	
if __name__ == "__main__":
	main()

