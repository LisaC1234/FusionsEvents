#!/bin/bash

LISTE=`ls Data/Human_by_chromosome`
read -p 'How much core do you want to allow to this work ? ' core



for name in $LISTE
do	
	fasta=${name::-6}
	#echo $fasta
	export DATA="$PWD/Data/Human_by_chromosome/$fasta.fasta"
	export ALIGN="$PWD/$fasta"
	export FILE="$fasta""_cleanNetwork_composites"
	
	
	
	if [ -f Result/Human_by_chromosome/$FILE/$fasta ];then

		mv "$PWD/Result/Human_by_chromosome/$FILE/$fasta" "$PWD"

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
	export E="1e-7" 
	export P="50"
	export C="90"


	################################################ Applying CompositeSearch on the network 
	./CompositeSearch-master/bin/compositeSearch -i "$ALIGN.cleanNetwork" -n "$ALIGN.cleanNetwork.genes" -m composites -e "$E" -p "$P" -c "$C" -t "$core" &
	pid4=$!
	wait $pid4

	############################################## Cleaning the repertories

	
	
	
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
RES_FILE="Docs/composite_count_human_E$E""_P$P""_C$C.txt"

if [ -f $RES_FILE ];then
	rm $RES_FILE
fi

echo "CompositeSearch results, run with : "  >> $RES_FILE
echo "E-value : $E"  >> $RES_FILE
echo "Pident  : $P"  >> $RES_FILE
echo "MinCov  : $C"  >> $RES_FILE

for name in $LISTE_RES 
do
	COMPOSITE="Result/Human_by_chromosome/$name/${name::-11}.composites"
	echo ${name::-24} >> $RES_FILE
	grep -c C $COMPOSITE >> $RES_FILE
done 
#python3 test.py

