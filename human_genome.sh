#!/bin/bash

LISTE=`ls Data/Human_by_chromosome`
read -p 'How much core do you want to allow to this work ? ' core



for name in $LISTE
do	
	fasta=${name::-6}
	echo $fasta
	export DATA="$PWD/Data/Human_by_chromosome/$fasta.fasta"
	export ALIGN="$PWD/$fasta"
	export FILE="$fasta""_cleanNetwork_composites"
	makeblastdb -in $DATA -dbtype prot -out my_prot_blast_db &
	pid1=$!
	wait $pid1


	blastp -db my_prot_blast_db -query $DATA -out $ALIGN -seg yes -soft_masking true -max_target_seqs 5000 -outfmt "6 qseqid sseqid evalue pident bitscore qstart qend qlen sstart send slen" -num_threads $core &
	pid2=$!
	wait $pid2

	./CompositeSearch-master/bin/cleanblastp -i $ALIGN -n 1 &
	pid3=$!
	wait $pid3


	#Ask the user for the parameters he wants

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

	if [ -d Result/Human_by_chromosome/$FILE ];then
		rm -r Result/Human_by_chromosome/$FILE;
	fi


	mv $FILE Result/Human_by_chromosome/  
done

LISTE_RES=`ls Result/Human_by_chromosome`

if [ -f composite_count_human.txt ];then
	rm "composite_count_human.txt"
fi


for name in $LISTE_RES 
do
	COMPOSITE="Result/Human_by_chromosome/$name/${name::-11}.composites"
	echo ${name::-24} >> "composite_count_human.txt"
	grep -c C $COMPOSITE >> "composite_count_human.txt"
done 
#python3 test.py

