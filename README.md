# FusionsEvents

To prepare the data in the good blast alignment format : 
- first : *makeblastdb -in XXX.fasta -dbtype prot -out my_prot_blast_db*
- then : *blastp -db my_prot_blast_db -query XXX.fasta -out all_vs_all.txt -seg yes -soft_masking true -max_target_seqs 5000 -outfmt "6 qseqid sseqid evalue pident bitscore qstart qend qlen sstart send slen"*


./cleanblastp -i all_vs_all.txt -n 1

./compositeSearch -i all_vs_all.txt.cleanNetwork -n all_vs_all.txt.cleanNetwork.genes -m composites -e 1e-05 -p 30 -c 80 -l 20 -t 4

