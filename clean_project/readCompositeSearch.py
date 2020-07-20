#! /usr/bin/env python3
# coding: utf-8
import pandas
####################################################
#                Read the dictionnary
####################################################
def extract_dictionary(path):
	res = {}
	with open(path, "r") as dico_file:
		for line in dico_file:
			assoc = line.split()
			res[assoc[1]] = assoc[0]
	return res 	
	
def extract_composites_infos(path):
	res = {}
	with open(path, "r") as dico_file:
		for line in dico_file:
			assoc = line.split()
			res[assoc[0][1:]] = [assoc[2], assoc[-1]]
	return res 
	
####################################################
#                Reader
####################################################

def reader(path): #to the repertory with all the CompositeSearch results files
	print(path)
	organism = path.split('/')[-1][0:-24]
	print(organism)
	res = pandas.DataFrame(columns=['component', 'composite', 'composite_start', 'composite_end', 'component_fam', 'composite_fam', 'no_overlap_score']) # composite_fam will be added later
	
	
	dico = extract_dictionary(path + '/' + organism + '.cleanNetwork.dico')
	
	composites_infos = extract_composites_infos(path+'/'+organism+'_cleanNetwork.compositesinfo')
	
	ind = 0
	with open(path +'/' + organism + '_cleanNetwork.composites', "r") as result_file:
		for line in result_file :
			if line.startswith('>'):
				num = line.strip()[2:]
				composite = dico[num]
			elif line.startswith('F'):
				infos = line.strip().split('\t')
				temp = [dico[infos[1]], composite, int(infos[2]), int(infos[3]), infos[0]]
				temp = temp + composites_infos[num]
				res.loc[ind] = temp
				ind +=1
	
	return res
