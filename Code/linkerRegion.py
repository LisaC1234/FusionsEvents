#! /usr/bin/env python3
# coding: utf-8
import pandas
from subprocess import Popen, PIPE, check_output
#<string>
aa = ['T', 'H', 'E', 'Y', 'Q', 'G', 'C', 'V', 'W', 'L', 'N', 'F', 'R', 'K', 'I', 'M', 'D', 'S', 'A', 'P']

def extract_linker(composite, comp_linker, fasta_path):
	res = []
	seq = []
	cmd = ["grep", composite, "-A30", fasta_path] # extract 30 ligne in the fasta file, in order to extract the sequence
	p = Popen(cmd, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p.communicate()
	out = str(stdout).strip('b').strip("'").strip('n').strip('\\').strip('>')
	list_out = out.split('n')
	sequence = ''
	for string in list_out[1:]:
		if string.startswith('>'):
			break
		sequence = sequence + string.strip('\\')
	#sequence contains the sequence of the composite
	seq.append(sequence)
	for i in range(1,len(comp_linker)):

		start_linker = comp_linker[i-1][1]
		end_linker = comp_linker[i][0]
		size = abs(comp_linker[i-1][1] - comp_linker[i][0])
		if size > 10 and size < 200 :
			res.append(sequence[start_linker:end_linker]) 
	return res , seq
	
	
	
def linkerRegion(data, fasta_path):
	no_overlap = data.loc[data["no_overlap_score"] == '1.00']
	res = [] #list of all the linker_regions
	sequences = []

	for composite in set(no_overlap["composite"]):
		sub_data = data.loc[data["composite"] == composite]
		list_domain = set(sub_data["domain"])
		comp_linker = []
		for d in list_domain:
			sub_sub = sub_data.loc[sub_data["domain"] == d]
			begin = max(sub_sub["composite_start"])
			end = min(sub_sub["composite_end"])
			comp_linker.append((begin, end))
		link, seq =  extract_linker(composite, comp_linker, fasta_path)
		res = res + link
		sequences = sequences + seq
	return res, seq
		
		
def average_aa(list_linker, organism, output):
	res = pandas.DataFrame(columns=aa)
	ind = 0
	for linker in list_linker :
		if linker != '':
			profile = []
			n = len(linker)
			for A in aa : 
				somme = 0
				for letter in linker:
					if letter == A:
						somme +=1
				profile.append(somme/n)
			res.loc[ind] = profile
			ind +=1
	res.to_csv(output+'profile_linker_regions_' + organism + '.csv')
	return res	
	
	
def av_aa(seq):
	res = [0 for i in range(len(aa))]
	n = len(seq)
	for letter in seq:
		if letter in aa:
			res[aa.index(letter)] +=1
		elif letter.upper() in aa:
			res[aa.index(letter.upper())] +=1
	for i in range(len(res)):
		res[i] = float(res[i])/n
	return res
	
def general_comparison(list_linker, list_seq, organism, output):
	res = pandas.DataFrame(columns=aa)
	master_linker = ''
	master_seq = ''
	for linker in list_linker:
		master_linker = master_linker + linker
	for sequences in list_seq:
		master_seq = master_seq + sequences
	res.loc["full sequences"] = av_aa(master_linker)
	res.loc["linker regions"] = av_aa(master_seq)
	res.to_csv(output+'profile_linker_regions_' + organism + '.csv')
	return res	
	
	
	
def compute_linkerRegion(data, fasta_file, organism, output):
	list_link, list_seq = linkerRegion(data, fasta_file)
	return general_comparison(list_link, list_seq, organism, output)

def main():
	data = pandas.read_csv("mouse_reviewedcompositeSearch_resutl.csv")
	general_comparison(linkerRegion(data, "Data/fasta_databases/mouse_reviewed.fasta"), 'mouse', '')

if __name__ == "__main__":
	main()

