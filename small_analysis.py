import subprocess

def read_blast(path):
	res = []
	with open(path, 'r') as fichier:
		for line in fichier:
			lis = line.split('\t')
			res.append(float(lis[3]))
	return moy(res)

def moy(liste):
	res = 0
	for n in liste:
		res +=n
	return res/len(liste)
	
def main():
	with open("compare_id_percentage_among_human_ch.txt", 'w') as res:
		path = 'Data/Blast_Alignments/human_by_chromosome'
		cmd =[ "ls", path]
		ls = subprocess.check_output(cmd)
		liste = ls.split()
		for name in liste:
			correct_name = str(name).strip('b')
			correct_name = correct_name.strip('\'')
			current_path = path + "/" + correct_name
			res.write(current_path.split('/')[-1] + '   '+ str(read_blast(current_path))+ '\n')
	
if __name__ == "__main__":
	main()
	
