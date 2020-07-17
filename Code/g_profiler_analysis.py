#! /usr/bin/env python3
# coding: utf-8
import argparse
from gprofiler import GProfiler

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f","--file",help="""Name of the file containing the list of the uniprot ID of the genes to analyse with g:Profiler""")
	return parser.parse_args()


def read_file(path):
	res = []
	with open(path, "r") as file:
		for l in file:
			res.append(l.strip())
	return res


def main():
	args = parse_arguments()
	file = args.file
	list_query = read_file(file)

	
	gp = GProfiler(
	    user_agent='ExampleTool', #optional user agent
	    return_dataframe=True, #return pandas dataframe or plain python structures    
	)
	
	res = gp.profile(organism='hsapiens',domain_scope = "annotated", sources = ["GO", "KEGG", "REAC"],
		    query=list_query)

	print(res["native"]) # ID du pathway dans la bdd
	print(res["name"]) # nom du pathway dans la bdd
	print(res["p_value"])
	print(res["intersection_size"]) # nombre de matchs pour cette entrée de la bdd
	print(res["precision"])
	print(res["recall"])

	minimal_res = res[["native", "name", "p_value", "intersection_size", "precision", "recall"]]
	minimal_res.sort_values(by = "p_value")
	minimal_res.to_csv("test.csv")
	print(minimal_res)
	
if __name__ == "__main__":
	main()
	
