import argparse
from subprocess import Popen, PIPE

def read_fasta(list_uniprot):
	res = {}
	l = list(range(1,23)) + ['x','y']
	for gene in list_uniprot:
		for numb in l:
			cmd = ["grep", "-c", gene, "Data/Human_by_chromosome/chromosome_"+str(numb)+".fasta"]
			p = Popen(cmd, stdout=PIPE, stderr=PIPE)
			stdout, stderr = p.communicate()
			if "1" in str(stdout):
				res[gene] = numb
				break
	return res
	
def read_fasta(list_uniprot):
	res = {}
	l = list(range(1,23)) + ['x','y']
	for i in l:
		res[i] = []
	for gene in list_uniprot:
		for numb in l:
			cmd = ["grep", "-c", gene, "Data/Human_by_chromosome/chromosome_"+str(numb)+".fasta"]
			p = Popen(cmd, stdout=PIPE, stderr=PIPE)
			stdout, stderr = p.communicate()
			if "1" in str(stdout):
				res[numb].append(gene)
				break
	return res

def main():
	inp = ["sp|Q9NWL6|ASND1_HUMAN", "sp|O15254|ACOX3_HUMAN"]
	res = read_fasta(inp)
	print(res)
		
		
if __name__ == "__main__":
	main()
	
	

