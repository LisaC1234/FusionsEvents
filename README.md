# FusionsEvents
## Pre-requisite to use this code (Python libraries): 
* Networkx
* dash
* pandas
* colour
* gprofiler official 1.0.0


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
--linker : This option will run the analysis of the linker region for the composite found by Diffuse.
```
## To change the parameters for CompositeSearch : 
The parameters are in the header of the "Code/applyCompositeSearch.py" file, it is therefore easy to change them. Change them carefully, because the output file will be replaced, and it is not possible to know afterward the parameters that were used in a particular computation. 

## Exemple : 
```diff
$python3 Code/main.py -c 4 -i Data/Blast_Alignments/meth_sach2 --diffuse Data/Diffuse_results/meth_sach2_diffuse.txt --gOption
```
```diff
$python3 Code/main.py -c 4 -i Data/Blast_Alignments/meth_sach2 --diffuse Data/Diffuse_results/meth_sach2_diffuse.txt --linker Data/fasta_databases/meth_sach2.fasta
```
```diff
$python3 Code/main.py -c 4 -i Data/Blast_Alignments/human_by_chromosome/chromosome_19 --gProfiler hsapiens
```
```diff
$python3 Code/main.py -c 4 -i Data/Blast_Alignments/human_reviewed --ch Data/Blast_Alignments/human_by_chromosome --target 19
```
