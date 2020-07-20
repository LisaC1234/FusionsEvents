#! /usr/bin/env python3
# coding: utf-8
import os
#import sys
import subprocess
import pandas
import readCompositeSearch
pwd = os.getcwd()
#sys.path.append(pwd+'/algoCluster/Input_Output') # Fonctionne sur windows et linux, et permet d'indiquer dans quel fichier sont les modules. 
E="1e-10" 
P="50"
C="80"
clean_b = "./Code/CompositeSearch-master/bin/cleanblastp"
compSearch = "./Code/CompositeSearch-master/bin/compositeSearch"


def prepare_option_g(g, repertory):
	if g == []:
		return g
	organism = repertory.split('/')[-1][:-24]
	if not os.path.exists(repertory):
		compositeSearch(file, [], core) # run compositeSearch a first time to get the dictionnary
	dico = readCompositeSearch.extract_dictionary(repertory+ '/'+ organism + '.cleanNetwork.dico')
	path = "Data/option_g/" + organism + ".txt"
	with open(path, "w") as target:
		for gene in g:
			for key, value in dico.items():
				if gene == value:
					target.write(key + "\n") # the CompositeSearch number is required
					break
					
	return ["-g", path]
	
	
def compositeSearch(file, g, core):

	name = file.split('/')[-1].split('.')[0]
	repertory = 'Result/' + name + '_cleanNetwork_composites'
	################# Running clean_blastp #####
	cmd1 = [clean_b , "-i",file , "-n", "1" ]
	step1 = subprocess.run(cmd1)
	############ Running CompositeSearch #######
	i = name + ".cleanNetwork"
	n = name + ".cleanNetwork.genes"
	cmd2 = [compSearch,  "-i", i , "-n", n, "-m", "composites", "-e", E, "-p", P, "-c", C, "-t", core]
	option_g = prepare_option_g(g, repertory)
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
		
		if os.path.exists(repertory):
			cmd = 'rm -r ' + repertory
			os.system(cmd)
		cmd = 'mv ' + name + '_cleanNetwork_composites Result/' 
		os.system(cmd)
	else :
		cmd = 'rm -r ' + name + '_cleanNetwork_composites'
		os.system(cmd)
	return repertory
		

def blast(file, g, core): # the input is a blast file, only CompositeSearch need to be applied
	return compositeSearch(file, g, core)
	
	
def fasta(file, g, core): # the input is a fasta file, a blast alignment is needed. 
	cmd = ['makeblastdb',  '-in' , file , '-dbtype','prot','-out','my_prot_blast_db']
	print(cmd)
	blast1 = subprocess.run(cmd)
	align = file.split('.')[0]
	cmd = ['blastp','-db','my_prot_blast_db','-query' ,file , '-out' ,align , '-seg','yes','-soft_masking','true','-max_target_seqs','10000','-outfmt','6 qseqid sseqid evalue pident bitscore qstart qend qlen sstart send slen','-num_threads', str(core)]
	blast2 = subprocess.run(cmd)
	if blast2.returncode == 0 :
		os.system('rm my_prot_blast_db.phr')
		os.system('rm my_prot_blast_db.pin')
		os.system('rm my_prot_blast_db.psq')
		os.system('mv ' + align + ' ' + 'Data/Blast_Alignments/')
		return compositeSearch('Data/Blast_Alignments/'+align, g, core)
	else :
		raise ValueError('There is a problem with blast, please unsure that you are using the right fasta format.')
	
