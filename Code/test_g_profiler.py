#! /usr/bin/env python3
# coding: utf-8
from gprofiler import GProfiler




gp = GProfiler(
    user_agent='ExampleTool', #optional user agent
    return_dataframe=True, #return pandas dataframe or plain python structures    
)

#res = gp.profile(organism='hsapiens',
#            query=['NR1H4','TRIP12','UBC','FCRL3','PLXNA3','GDNF','VPS11'])
#print(res)
res = gp.profile(organism='hsapiens',domain_scope = "annotated", sources = ["GO", "KEGG", "REACTOME"],
            query=['NR1H4','TRIP12','UBC','FCRL3','PLXNA3','GDNF','VPS11'])
print(res)
print(type(res))
res.info()
print(res["source"])
print(res["native"]) # ID du pathway dans la bdd
print(res["name"]) # nom du pathway dans la bdd
print(res["p_value"])
print(res["significant"])
print(res["description"])
print(res["term_size"])
print(res["query_size"])
print(res["intersection_size"]) # nombre de matchs pour cette entrée de la bdd
print(res["effective_domain_size"])
print(res["precision"])
print(res["recall"])
print(res["query"])
print(res["parents"])
