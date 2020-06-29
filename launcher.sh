#!/bin/bash

read -p 'Enter the name of the fasta file you want to analyse (for exemple uniprot-proteomeUP000000589) ' fasta 
read -p 'How much core do you want to allow to this work ? ' core

export DATA="$PWD/Data/$fasta.fasta"
export ALIGN="$PWD/$fasta"
export FILE="$fasta""_cleanNetwork_composites"



if [ -f Result/$FILE/$fasta ];then

	mv "$PWD/Result/$FILE/$fasta" "$PWD"

else
#################################################Make blast Database
	makeblastdb -in $DATA -dbtype prot -out my_prot_blast_db &
	pid1=$!
	wait $pid1

	blastp -db my_prot_blast_db -query $DATA -out $ALIGN -seg yes -soft_masking true -max_target_seqs 10000 -outfmt "6 qseqid sseqid evalue pident bitscore qstart qend qlen sstart send slen" -num_threads $core &
	pid2=$!
	wait $pid2
	rm my_prot_blast_db.phr my_prot_blast_db.pin my_prot_blast_db.psq 
fi
################################################# Cleaning the network
./CompositeSearch-master/bin/cleanblastp -i $ALIGN -n 1 &
pid3=$!
wait $pid3

#Ask the user for the parameters he wants
export E="1e-10" 
export P="50"
export C="10"


################################################ Applying CompositeSearch on the network 
./CompositeSearch-master/bin/compositeSearch -i "$ALIGN.cleanNetwork" -n "$ALIGN.cleanNetwork.genes" -m composites -e "$E" -p "$P" -c "$C" -t "$core" &
pid4=$!
wait $pid4

############################################## Cleaning the repertories


mv "$ALIGN.cleanNetwork" "$PWD/$FILE"
mv $ALIGN "$PWD/$FILE"
mv "$ALIGN.cleanNetwork.genes" "$PWD/$FILE"
mv "$ALIGN.cleanNetwork.dico" "$PWD/$FILE"

if [ -d Result/$FILE ];then
	rm -r Result/$FILE;
fi


mv $FILE Result/  



#python3 test.py


