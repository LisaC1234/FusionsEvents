#! /usr/bin/env python3
# coding: utf-8

# Import pandas package  
import pandas
import networkx as nx

def main():
	reduced_comp = pandas.read_csv('reduced.csv')
	G = nx.Graph()
	
	dico_status = {}
	dico_ch = {}
	for row in reduced_comp.itertuples():
		G.add_edge(row.composite, row.component)
		dico_ch[row.composite] = str(row.ch_composite)
		dico_ch[row.component] = str(row.ch_component)
		if row.composite in dico_status:
			dico_status[row.composite].add('composite')
		else:
			dico_status[row.composite] = set()
			dico_status[row.composite].add('composite')
		
		if row.component in dico_status:
			dico_status[row.component].add('component')
		else:
			dico_status[row.component] = set()
			dico_status[row.component].add('component')
			
		
	nx.set_node_attributes(G, dico_ch, 'ch')
	nx.set_node_attributes(G, dico_status, 'status')
		
if __name__ == "__main__":
	main()
	
#sp|Q5VV52|ZN691_HUMAN : both composite and component

