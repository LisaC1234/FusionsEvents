#! /usr/bin/env python3
# coding: utf-8
import argparse
import subprocess

import readDiffuse
import applyCompositeSearch
import readCompositeSearch
import analyse
import printChromosome

####################################################
#              Parse Arguments
####################################################

def parse_arguments():
	parser = argparse.ArgumentParser(description='Launch and compare the composites genes from CompositeSearch to the composites genes from Diffuse.')
	
########Required and general : 
	parser.add_argument("-i", metavar="[Database]",help="""By default : Path to the blast alignment to use. If the argument --fasta is used, the input should be a fasta file. The computation time will increase, therefore the blast alignment is to use in priority.""", required=True)
	
	parser.add_argument("-c", metavar="[# Core to use]",help="""Number of core to use for the computation.""", required=True)
	
	parser.add_argument("--fasta", dest='algo', action='store_const', const=applyCompositeSearch.fasta, default=applyCompositeSearch.blast,help="""To use only if the blast alignment is not available. Database should be a fasta database.""") # define an optional option, therefore algo is to use to run CompositeSearch on the input
	
########For the analyse with Diffuse
	parser.add_argument("--d", metavar="[Diffuse output]",help="""Path to the output file from Diffuse for the same database.""")
	
	parser.add_argument("--g", action='store_true', dest= 'g_option', help="""This will take the composite of Diffuse to feed the option -g of CompositeSearch.""") # define an optional option, therefore algo is to use to run CompositeSearch on the input
	
########For an analyse only with CompositeSearch, amond the genome in details
	parser.add_argument("-ch", metavar="[Chromosomes]", help="""With this option, you can add the details of each chromosome composition. The path must be a repertory containing a blast_alignment file for each chromosome. If only fasta files are available, the option --fasta_ch must be used.""") # define an optional option, therefore algo is to use to run CompositeSearch on the input
	
	
	parser.add_argument("--fasta_ch", dest='algo_ch', action='store_const', const=applyCompositeSearch.ch_fasta, default=applyCompositeSearch.ch_blast,help="""To use only if the blast alignments are not available. Repository database should be a fasta database.""") # define an optional option, therefore algo is to use to run CompositeSearch on the input
	return parser.parse_args()
	
	
	
####################################################
#                  Main
####################################################

def main():
	########### Get the paths ##################
	args = parse_arguments()
	path_input = args.i
	core = args.c
########Using a Diffuse input	
	######## Extract the diffuse result ########
	if args.d:
		print('you will see the comparison between Diffuse and Composite Search for the entry')
		path_diffuse = args.d
		diffuse = readDiffuse.reader(path_diffuse) #return a pandas object
	
	###### Apply CompositeSearch ###############
		g=[]
		if args.g_option :
			g = list(set(diffuse["composite"]))

		file = args.algo(path_input, g, core) #apply compositeSearch, either with the blast alignment or with a fasta file
		compositeSearch = readCompositeSearch.reader(file)
	
	###### Compare the results #################
	
	###### Analyse the results #################
		analyse.comparison(diffuse, compositeSearch)
	
	
	###### Get infos by chromosomes ############
	elif args.ch:
		print('you choose a detailed analysis of the genome')
		g = []
		file = args.algo(path_input, g, core) #apply compositeSearch, either with the blast alignment or with a fasta file
		compositeSearch = readCompositeSearch.reader(file)
		arg_path = args.ch
		list_repertories, path_blast = args.algo_ch(arg_path, [], core) #list_repertories is a list of the location of the result files
		
		compositeSearch = readCompositeSearch.enrich_blast(compositeSearch, path_blast)
		compositeSearch.to_csv(r'compositeSearch_resutl.csv')
		print('ici')
		list_ch = readCompositeSearch.multiple_reader(list_repertories) # list_ch is a list of pandas matrix for each chromosome
		print(type(list_ch[0]))
		analyse.by_chromosome(compositeSearch, list_ch)
		
		 # take some time, is it possible to optimise ? 
		printChromosome.print_network(compositeSearch,19)
	
	else :
		print('CompositeSearch will be applied on the entry')
		file = args.algo(path_input, [], core) # only apply CompositeSearch
if __name__ == "__main__":
	main()
	
