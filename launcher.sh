#!/bin/bash

read -p 'Enter the name of the fasta file you want to analyse (for exemple uniprot-proteomeUP000000589) ' fasta 
read -p 'How much core do you want to allow to this work ? ' core

export DATA="$PWD/Data/$fasta.fasta"
export ALIGN="$PWD/all_vs_all$fasta.txt"
export FILE="all_vs_all$fasta""_txt_cleanNetwork_composites"
makeblastdb -in $DATA -dbtype prot -out my_prot_blast_db &
pid1=$!
wait $pid1


blastp -db my_prot_blast_db -query $DATA -out $ALIGN -seg yes -soft_masking true -max_target_seqs 5000 -outfmt "6 qseqid sseqid evalue pident bitscore qstart qend qlen sstart send slen" -num_threads $core &
pid2=$!
wait $pid2



#appliquer les deux algos de rechercher puis faire le ménage
./CompositeSearch-master/bin/cleanblastp -i $ALIGN -n 1 &
pid3=$!
wait $pid3




export E="1e-10"
export P="50"
export C="80"

./CompositeSearch-master/bin/compositeSearch -i "$ALIGN.cleanNetwork" -n "$ALIGN.cleanNetwork.genes" -m composites -e "$E" -p "$P" -c "$C" -t "$core" &
pid4=$!
wait $pid4

rm my_prot_blast_db.phr my_prot_blast_db.pin my_prot_blast_db.psq 
mv "$ALIGN.cleanNetwork" "$PWD/$FILE"
mv $ALIGN "$PWD/$FILE"
mv "$ALIGN.cleanNetwork.genes" "$PWD/$FILE"
mv "$ALIGN.cleanNetwork.dico" "$PWD/$FILE"

python3 test.py


