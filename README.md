# FusionsEvents
## Pre-requisite to use this code : 
* R library gprofiler2
* Python library : Networkx, dash, pandas, colour


## How to get help : 
```diff
$python3 Code/main.py -h
```

## List of the options : 
### Mandatory :	
```diff
-c : Number of core available for the task (CompositeSearch is a multithreaded algorithm)
-i : The input (blast alignement, or fastafile with the option --fasta)
```
### Other options :
```diff
--diffuse : Diffuse output (dictionary format)
--gOption : Use the Diffuse output to apply the -g option of CompositeSearch
--ch : Should be a repertory with all the blast alignments for each chromosome (or fasta file with the option --fasta_ch)
--target : If information about the chromosome is given, the targetted chromosome will be displayed ('all' will display the whole network)
--gProfiler : should be the organisme to use for the g:Profiler analysis. (help at https://biit.cs.ut.ee/gprofiler/page/organism-list)
```

## Exemple : 
```diff
$python3 Code/main.py -c 4 -i Data/Blast_Alignments/meth_sach2 --diffuse Result/Diffuse_results/meth_sach2_diffuse.txt --gOption
```
```diff
$python3 Code/main.py -c 4 -i Data/Blast_Alignments/meth_sach2 --diffuse Result/Diffuse_results/meth_sach2_diffuse.txt --linker Data/fasta_databases/meth_sach2.fasta
```
```diff
$python3 Code/main.py -c 4 -i Data/Blast_Alignments/human_by_chromosome/chromosome_19 --gProfiler hsapiens
```
```diff
$python3 Code/main.py -c 4 -i Data/Blast_Alignments/human_reviewed --ch Data/Blast_Alignments/human_by_chromosome --target 19
```
