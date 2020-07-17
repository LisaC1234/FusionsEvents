#! /usr/bin/env python3
# coding: utf-8
import os
#import sys
import subprocess
import pandas
pwd = os.getcwd()
#sys.path.append(pwd+'/algoCluster/Input_Output') # Fonctionne sur windows et linux, et permet d'indiquer dans quel fichier sont les modules. 
E="1e-10" 
P="50"
C="80"
clean_b = "./Code/CompositeSearch-master/bin/cleanblastp"
compSearch = "./Code/CompositeSearch-master/bin/compositeSearch"


def prepare_option_g(g):
	if g == []:
		return g
	path = "temp_option_g.txt"
	with open(path, "w") as target:
		for gene in g:
			target.write(gene + "\n") # it should be CompSearch id instead of uniprot id
	return ["-g", path]
	
	
def compositeSearch(file, g, core):
	################# Running clean_blastp #####
	cmd1 = [clean_b , "-i",file , "-n", "1" ]
	step1 = subprocess.run(cmd1)
	############ Running CompositeSearch #######
	name = file.split('/')[-1]
	i = name + ".cleanNetwork"
	n = name + ".cleanNetwork.genes"
	cmd2 = [compSearch,  "-i", i , "-n", n, "-m", "composites", "-e", E, "-p", P, "-c", C, "-t", core]
	option_g = prepare_option_g(g)
	cmd2 = cmd2 + option_g
	step2 = subprocess.run(cmd2)
	######## Cleaning the repertory ############
	if option_g != []:
		cmd = 'rm ' + option_g[1]
		os.system(cmd)
		
	if step2.returncode == 0:
		result_file = name + '_cleanNetwork_composites'
		cmd = 'mv ' + name + '.cleanNetwork ' + result_file
		os.system(cmd)
		cmd = 'mv ' + name + '.cleanNetwork.genes ' + result_file
		os.system(cmd)
		cmd = 'mv ' + name + '.cleanNetwork.dico ' + result_file
		os.system(cmd)
		#cmd = 'mv ' + name + '_cleanNetwork_composites Result/'  # check if it already exist before deleting it
		#os.system(cmd)
	else :
		pass
		

def blast(file, g, core): # the input is a blast file, only CompositeSearch need to be applied
	compositeSearch(file, g, core)
	
	
def fasta(file, g, core): # the input is a fasta file, a blast alignment is needed. 
	print('fasta here')
	
