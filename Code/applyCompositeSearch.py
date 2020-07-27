#! /usr/bin/env python3
# coding: utf-8
import os
import subprocess
import pandas
import readCompositeSearch
pwd = os.getcwd()

E="1e-10" 
P="50"
C="80"
clean_b = "./Code/CompositeSearch-master/bin/cleanblastp"
compSearch = "./Code/CompositeSearch-master/bin/compositeSearch"
data_option_g_path = "Data/"
result_path = 'Result/CompositeSearch_results/'
path_blast_alignments = 'Data/Blast_Alignments/'

def prepare_option_g(g, repertory): # the option g for compositeSearch require a list of CompositeSearch ID of the genes. 
	if g == []:
		return g
	organism = repertory.split('/')[-1][:-24]
	if not os.path.exists(repertory):
		compositeSearch(file, [], core) # run compositeSearch a first time to get the dictionnary
	dico = readCompositeSearch.extract_dictionary(repertory+ '/'+ organism + '.cleanNetwork.dico')
	path = data_option_g_path + organism + ".txt"
	with open(path, "w") as target:
		for gene in g:
			for key, value in dico.items():
				if gene == value:
					target.write(key + "\n") # the CompositeSearch number is required
					break
					
	return ["-g", path]
	
	
def compositeSearch(file, g, core):

	name = file.split('/')[-1].split('.')[0]
	repertory = result_path + name + '_cleanNetwork_composites'
	################# Running clean_blastp #####
	cmd1 = [clean_b , "-i",file , "-n", "1" ]
	step1 = subprocess.run(cmd1, capture_output=True)
	############ Running CompositeSearch #######
	i = name + ".cleanNetwork"
	n = name + ".cleanNetwork.genes"
	cmd2 = [compSearch,  "-i", i , "-n", n, "-m", "composites", "-e", E, "-p", P, "-c", C, "-t", core]
	option_g = prepare_option_g(g, repertory)
	cmd2 = cmd2 + option_g
	step2 = subprocess.run(cmd2, capture_output=True)
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
		cmd = 'mv ' + name + '_cleanNetwork_composites ' + result_path 
		os.system(cmd)
	else :
		cmd = 'rm -r ' + name + '_cleanNetwork_composites'
		os.system(cmd)
		cmd = 'rm ' + name + '.cleanNetwork'
		os.system(cmd)
		cmd = 'rm ' + name + '.cleanNetwork.genes'
		os.system(cmd)
		cmd = 'rm ' + name + '.cleanNetwork.dico'
		os.system(cmd)
	return repertory
		

def blast(file, g, core): # the input is a blast file, only CompositeSearch need to be applied
	return compositeSearch(file, g, core)
	
	
def fasta_path(file, g, core, path): # the input is a fasta file, a blast alignment is needed. 
	cmd = ['makeblastdb',  '-in' , file , '-dbtype','prot','-out','my_prot_blast_db']
	blast1 = subprocess.run(cmd)
	align = file.split('.')[0].split('/')[-1]
	cmd = ['blastp','-db','my_prot_blast_db','-query' ,file , '-out' ,align , '-seg','yes','-soft_masking','true','-max_target_seqs','10000','-outfmt','6 qseqid sseqid evalue pident bitscore qstart qend qlen sstart send slen','-num_threads', str(core)]
	blast2 = subprocess.run(cmd)
	
	os.system('rm my_prot_blast_db.phr')
	os.system('rm my_prot_blast_db.pin')
	os.system('rm my_prot_blast_db.psq')
	if blast2.returncode == 0 :
		os.system('mv ' + align + ' ' + path)
		if not path.endswith('/'):
			path = path + '/'
		return compositeSearch(path + align, g, core)
	else :
		raise ValueError('There is a problem with blast, please unsure that you are using the right fasta format.')
		
		
def fasta(file, g, core):
	return fasta_path(file, g, core, path_blast_alignments)	



def ch_blast(path, g, core): # apply CompositeSearch on all chromosomes
	cmd =[ "ls", path]
	ls = subprocess.check_output(cmd)
	liste = ls.split()
	res = []
	for name in liste:
		correct_name = str(name).strip('b')
		correct_name = correct_name.strip('\'')
		current_path = path + "/" + correct_name
		res.append(compositeSearch(current_path, g, core))
	return res , path
		
		
def ch_fasta(path, g, core): # apply CompositeSearch on all chromosomes
	cmd =[ "ls", path]
	ls = subprocess.check_output(cmd)
	liste = ls.split()
	res = []
	organisme = str(liste[0]).strip('b').strip('\'').split('_')[0]
	file = path_blast_alignments + organisme
	cmd = 'mkdir ' + file
	os.system(cmd)
	for name in liste:
		correct_name = str(name).strip('b')
		correct_name = correct_name.strip('\'')
		current_path = path + "/" + correct_name
		res.append(fasta_path(current_path, g, core, file))
	return res, path_blast_alignments
	
