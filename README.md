# FusionsEvents

## Run the CompositeSearch algorithm, put the fasta with all the sequences in /Data 
```diff
$./launcher.sh
```
All the files generated will be found in the file 
```diff
$/Name_of_your_data_base_composites_from_CompositeSearch
```

## Run CompositeSearch on every chromosome (for the Human protéome only)
(it will generate a markdown file with the results as a table for every chromosomes)
```diff
$./human_genome.sh
```

## Analyse the results of Composite search compared to Diffuse
Note : the Diffuse results should have the same name as the database used to compute CompositeSearch, and should be placed in 
Result/Diffuse_result/database_name_diffuse.txt
```diff
$python3 Code/comparison.py -f *name of the database*
```


## Compare the results for the same proteome, chromosomes by chromosomes and all in once
Note : Only for the human proteome for now. 
```diff
$python3 Code/human_comparison.py 
```
