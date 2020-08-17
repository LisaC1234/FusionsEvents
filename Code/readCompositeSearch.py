#! /usr/bin/env python3
# coding: utf-8
import pandas
import os
from subprocess import Popen, PIPE, check_output
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
	organism = path.split('/')[-1][0:-24]
	res = pandas.DataFrame(columns=['component', 'composite', 'composite_start', 'composite_end', 'component_fam', 'domain', 'composite_fam', 'no_overlap_score']) # composite_fam will be added later
	
	if os.path.exists(path):
		dico = extract_dictionary(path + '/' + organism + '.cleanNetwork.dico')
		
		composites_infos = extract_composites_infos(path+'/'+organism+'_cleanNetwork.compositesinfo')
		
		ind = 0
		with open(path +'/' + organism + '_cleanNetwork.composites', "r") as result_file:
			#domain = 0
			for line in result_file :
				if line.startswith('>'):
					num = line.strip()[2:]
					composite = dico[num]
				elif line.startswith('F'):
					print(domain)
					infos = line.strip().split('\t')
					temp = [dico[infos[1]], composite, int(infos[2]), int(infos[3]), infos[0], domain]
					temp = temp + composites_infos[num]
					res.loc[ind] = temp
					ind +=1
				elif line.startswith('['):
					domain = int(line.strip().split('\t')[0][-2:-1])
					print('\n\n',domain)
	
	return res

####################################################
#                Reader for a list of paths
####################################################


def multiple_reader(paths):
	res = []
	for path in paths: 
		name = path.split('/')[-1][:-24].split('_')[-1]
		temp = reader(path)
		temp["ch_composite"]=name
		temp["ch_component"]=name
		res.append(temp)
	return res
	
	
	
####################################################
# Enrich pandas with infos about the chromosomes
####################################################
	
def enrich_blast(compositeSearch, path):
	dico_composite = {}
	dico_component = {}
	cmd =[ "ls", path]
	ls = check_output(cmd)
	list_ch = ls.split()
	list_path= []
	for name in list_ch:
		correct_name = str(name).strip('b')
		correct_name = correct_name.strip('\'')
		current_path = path + "/" + correct_name
		list_path.append(current_path)
	
	for comp in set(compositeSearch["composite"]):
		dico_composite[comp] = find_chromosome(comp, list_path)
	for comp in set(compositeSearch["component"]):
		dico_component[comp] = find_chromosome(comp, list_path)
	list_composite = []
	compositeSearch["ch_composite"] = [dico_composite[x] for x in compositeSearch["composite"]] 
	compositeSearch["ch_component"] = [dico_component[x] for x in compositeSearch["component"]] 
	return compositeSearch
	
def find_chromosome(comp, list_path):
	for path in list_path:
		cmd = ["grep", "-c", comp, path]
		p = Popen(cmd, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate()
		res = int(str(stdout).strip('b').strip("'").strip('n').strip('\\'))
		if res != 0:
			numb = path.split('/')[-1]
			numb = numb.split('_')[-1] # expecting the format to be /.../.../chromosome_numb_.........
			return numb
	return -1
