from gprofiler import GProfiler
gp = GProfiler(
    user_agent='ExampleTool', #optional user agent
    return_dataframe=True, #return pandas dataframe or plain python structures    
)

res = gp.profile(organism='hsapiens',
            query=['NR1H4','TRIP12','UBC','FCRL3','PLXNA3','GDNF','VPS11'])
print(res)
res = gp.profile(organism='hsapiens',domain_scope = "annotated", sources = ["GO", "KEGG", "REACTOME"],
            query=['NR1H4','TRIP12','UBC','FCRL3','PLXNA3','GDNF','VPS11'])
print(res)
