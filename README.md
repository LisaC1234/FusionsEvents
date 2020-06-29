# FusionsEvents

To run the CompositeSearch algorithm, put the fasta with all the sequences in /Data, and the run : 
```diff
$./launcher.sh
```
All the files generated will be found in the file 
```diff
$/Name_of_your_data_base_composites_from_CompositeSearch
```

To run CompositeSearch on every chromosome (for the Human protéome only), run : 
```diff
$./human_genome.sh
```

To analyse the results of Composite search compared to Diffuse, run : 
Note : the Diffuse results should have the same name as the database used to compute CompositeSearch, and should be placed in 
Result/Diffuse_result/database_name_diffuse.txt
```diff
$python3 Code/comparison.py -f *name of the database*
```

