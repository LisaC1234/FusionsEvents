#! /usr/bin/env python3
# coding: utf-8
import argparse
import readDiffuse
import compositeSearch

####################################################
#              Parse Arguments
####################################################

def parse_arguments():
	parser = argparse.ArgumentParser(description='Launch and compare the composites genes from CompositeSearch to the composites genes from Diffuse.')
	
	parser.add_argument("-i", metavar="[Database]",help="""By default : Path to the blast alignment to use. If the argument --fasta is used, the input should be a fasta file. The computation time will increase, therefore the blast alignment is to use in priority.""", required=True)
	
	parser.add_argument("-d", metavar="[Diffuse output]",help="""Path to the output file from Diffuse for the same database.""", required=True)
	
	parser.add_argument("-c", metavar="[# Core to use]",help="""Number of core to use for the computation.""", required=True)
	
	parser.add_argument("--fasta", dest='algo', action='store_const', const=compositeSearch.fasta, default=compositeSearch.blast,help="""To use only if the blast alignment is not available. Database should be a fasta database.""") # define an optional option, therefore algo is to use to run CompositeSearch on the input
	
	parser.add_argument("--g", action='store_true', dest= 'g_option', help="""This will take the composite of Diffuse to feed the option -g of CompositeSearch.""") # define an optional option, therefore algo is to use to run CompositeSearch on the input
	
	return parser.parse_args()
	
	
	
####################################################
#                  Main
####################################################

def main():
	########### Get the paths ##################
	args = parse_arguments()
	path_diffuse = args.d
	path_input = args.i
	core = args.c
	
	######## Extract the diffuse result ########
	diffuse = readDiffuse.reader(path_diffuse) #return a pandas object
	
	###### Apply CompositeSearch ###############
	g=[]
	if args.g_option :
		g = list(set(diffuse["composite"]))

	args.algo(path_input, g, core)
	
	###### Compare the results #################
	# Todo

		
if __name__ == "__main__":
	main()
	
