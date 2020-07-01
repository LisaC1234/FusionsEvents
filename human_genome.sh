#!/bin/bash

LISTE=`ls Data/Human_by_chromosome`
read -p 'Do you want to run the algorithm, or just the analysis ? (al or an)' run

E="1e-7" 
P="50"
C="80"

if [ $run = 'al' ];then
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
fi

LISTE_RES=`ls Result/Human_by_chromosome`
LISTE_TEST=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 x y)
RES_FILE="Result/Human_by_chromosome/composite_count_human_E$E""_P$P""_C$C.md"
if [ -f $RES_FILE ];then
	rm $RES_FILE
fi

echo "# CompositeSearch results"  >> $RES_FILE
echo "Parameters"  >> $RES_FILE
echo "E-value : $E"  >> $RES_FILE
echo "Pident  : $P"  >> $RES_FILE
echo "MinCov  : $C"  >> $RES_FILE
echo ""  >> $RES_FILE
echo "| Chromosome | Genes | Composites | Components (uniques) | Families of composites |"  >> $RES_FILE
echo "|------------|:-----:|:----------:|:--------------------:|:----------------------:|"  >> $RES_FILE

for numb in "${LISTE_TEST[@]}"
do
	name="chromosome_$numb""_cleanNetwork_composites"
	DATA="$PWD/Data/Human_by_chromosome/${name::-24}.fasta"
	COMPOSITE="Result/Human_by_chromosome/$name/${name::-11}.composites"
	COMPOSITE_FAM="Result/Human_by_chromosome/$name/${name::-11}.compositefamilies"
	STR1=$(grep -c ">" $DATA) # number of genes
	STR2=$(grep -c C $COMPOSITE) # number of composites
	STR3=$(grep -c F $COMPOSITE) # number of components (uniques)
	STR4=$(cut -f1 $COMPOSITE | grep F | sort -u | grep -c F) # number of components (uniques)
	STR5=$(grep -c ">CF" $COMPOSITE_FAM) # number of composites families
	echo "| ${name::-24} | $STR1 | $STR2 | $STR3 ($STR4) | $STR5 |" >> $RES_FILE
done 
#python3 test.py

