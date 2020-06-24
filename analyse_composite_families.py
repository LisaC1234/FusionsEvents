#! /usr/bin/env python3
# coding: utf-8
import argparse


def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f","--fasta",help="""Name of the fasta database used""")
	return parser.parse_args()



def extract_composites(fasta):
	path = fasta+ "_cleanNetwork_composites/" + fasta + "_cleanNetwork.composites"
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
				#domain_list = []
			elif line.startswith("F"):
				liste = line.split()
				family.append((liste[0], liste[1]))
	
	domain_list.append(family)
	res[name] = domain_list
	return res # Every composite gene is an entry to the dictionary, and the value is a list of the domains , and each domains is a list of the (Family, ID) of the hits

def analyse(dico): #find every composite that are composed with same-family components
	Composites = list(dico.keys())
	print(Composites)
	for i in range(len(Composites)):
		for j in range(i, len(Composites)): # every pair of composites is tested only once, to check if they are similar
			similarity(dico[Composites[i]],dico[Composites[j]])
	pass
				
def similarity(fam_c1, fam_c2): #analy two list of components of two composites and look for similarities. 
	num_matches  = 0
	for i in range(len(fam_c1)): #iterise on the domains
		for j in range(i, len(fam_c2)):
			print(fam_c2[j])
			# il faut ensuite déterminer si le ou les matchs sont de la même famille...
			#pour le moment il n'y pas pas de considérations d'ordre pour les composants. 
	#print('familles : ', fam_c1, fam_c2)
	pass
		
	

def main():
	args = parse_arguments()
	fasta = args.fasta
	dico = extract_composites(fasta)
	analyse(dico)
	
if __name__ == "__main__":
	main()


