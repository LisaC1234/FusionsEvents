#! /usr/bin/env python3
# coding: utf-8
import argparse


def read_uniprot(path):
	res = []
	with open(path, "r") as fasta:
		for line in fasta:
			if line.startswith(">"):
				premier_split = line.split('GN=')
				name = premier_split[1].split(' ')[0]
				res.append(name)
				#print(name)
	return res
	
def read_ncbi(path):
	res = {}
	list_id_present = []
	with open(path, "r") as ncbi:
		for line in ncbi:
			infos = line.strip().split(",")
			res[infos[8]] = infos
			list_id_present.append(infos[6])
	return res, list_id_present


	
		
def find_correspondances(path, ncbi, uniprot, result):
	keep = {}
	with open(path, "r") as dico:
		for line in dico:
			infos = line.strip().split("\t")
			#print(infos)
			nom_ncbi = '"' + infos[7] + '"'
			if infos[2] in uniprot and infos[-1] == "reference standard" :
				#print(infos[2], nom_ncbi)
				#print(infos)
				if nom_ncbi in ncbi : 
					keep[infos[2]] = ncbi[nom_ncbi]
					#print(infos[2],"\n")
	with open(result, "w") as res:
		for name in keep.keys():
			res.write(name + "\t")
			for elem in keep[name]:
				res.write(elem +"\t")
			res.write(elem +"\n")	
		

		
				


def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-n","--number",help="""Name or Number of the chromosome to use""")
	return parser.parse_args()
	
def main():
	args = parse_arguments()
	number = args.number
	result_path = "Chromosome_" + number + "_position.txt"
	dico_ncbi, list_ncbi = read_ncbi("Data/NCBI_position/Chromosome" + number + ".csv")
	list_uniprot = read_uniprot("Data/Human_by_chromosome/chromosome_" + number + ".fasta")
	find_correspondances("Data/NCBI_position/Correspondance_uniprot_ncbi.txt", dico_ncbi, list_uniprot, result_path)
	intersection = [u for u in list_uniprot if '"'+u+'"' in list_ncbi]
	print(intersection, len(intersection))
	not_found = [u for u in list_uniprot if '"'+u+'"' not in list_ncbi]
	print(not_found, len(not_found))
	
	
	
if __name__ == "__main__":
	main()
	
	

