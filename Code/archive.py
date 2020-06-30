def extract_composites(fasta):
	path = fasta+ "_cleanNetwork_composites/" + fasta + "_cleanNetwork.composites"
	res = {}
	with open(path, "r") as composites_file:
		temp= {}
		name = ''
		domain = ''
		family = []
		for line in composites_file:
			if line.startswith(">"):
				if name != '':
					temp[domain] = family
					res[name] = temp
					temp= {}
					name = ''
					domain = ''
					family = []
				name = line.strip()[1:]
			elif line.startswith("["):
				if domain != '':
					temp[domain] = family
					family = []
				domain = line.strip()[1:10]
				if domain[-1] == ']':
					domain = domain[:-1]
			elif line.startswith("F"):
				liste = line.split()
				family.append((liste[0], liste[1]))
	temp[domain] = family
	res[name] = temp
	return res # Every composite gene is an entry to the dictionary, and the value is another dictionary {Domain : (family,ID) }
	
