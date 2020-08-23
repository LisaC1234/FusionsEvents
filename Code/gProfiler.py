#! /usr/bin/env python3
# coding: utf-8
#import gprofiler
from gprofiler import GProfiler

def run_gProfiler(comp, org):
	gp = GProfiler( return_dataframe=True) #return pandas dataframe or plain python structures 
	#gp = GProfiler(user_agent = 'lisa' )
	list_id = []
	for name in list(set(comp["composite"])):
		i_d = name.split('|')[1]
		list_id.append(i_d)
	res = gp.profile(organism=org,domain_scope = "annotated", sources = ["GO", "KEGG", "REACTOME"], #exemple org : hsapiens
		query=list_id)
	return res
