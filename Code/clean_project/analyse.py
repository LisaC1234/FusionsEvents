#! /usr/bin/env python3
# coding: utf-8
import pandas

def comparison(diff, comp):
	intersect_composites = set(comp["composite"]).intersection(set(diff["composite"]))
	if intersect_composites == []:
		print('none of the composites found by Diffuse are detectd by CompositeSearch')
	for composite in intersect_composites:
		print("\n###############################################\nThe composite :", composite)
		events_diff = diff.loc[diff['composite'] == composite]
		events_comp = comp.loc[comp['composite'] == composite]
		intersect_components = set(events_diff["component"]).intersection(set(events_comp["component"]))
		print("is unanimously composed with the following components : ", intersect_components, len(intersect_components))
		print("among : ", len(list(set(events_diff["component"]))), "components found by Diffuse")
		print("and : ", len(list(set(events_comp["component"]))), "components found by CompositeSearch")




		
def by_chromosome(comp, list_ch):
	vert = '\\textcolor{vert}{\\textbf{'
	orange = '\\textcolor{orange}{\\textbf{'
	rose = '\\textcolor{rose}{\\textbf{'
	fin = '}} '
	output_path = "test.tex"
	with open(output_path, "w") as res:
		res.write("\\begin{table}[H]\n\t\\centering\n\t\\begin{tabular}{||l|c|c|c|c||}\n\t\t\\hline\\hline\n\t\tChromosome&Genes&Composites&Components (uniques)&Families of composites\\\\\n\t\t\\hline\\hline\n")
		for ch in list_ch:
			if not ch.empty: 
				numb = ch.loc[0]["ch_composite"]
				#first = ch.loc[0]["composite"]
				#first_assoc = comp.loc[comp["composite"] == first]
				#numb = first_assoc["ch_composite"].tolist()[0]
				res.write('chromosome ' + str(numb) + '&..&') # how to obtain le numer of genes per ch ?
				target_comp = comp.loc[comp["ch_composite"] == numb]
				
				res.write(vert + str(len(set(ch["composite"]))) + fin + orange +  str(len(set(target_comp["composite"]).intersection(set(ch["composite"])))) + fin + rose + str(len(set(target_comp["composite"]))) + fin + '&') # nb of composite for the all vs all analysis
				 # nb of composite for the one by one analysis 
				# intersection of the results
				one_by_one = str(len(ch["component"])) + ' (' + str(len(set(ch["component"]))) + ')'
				all_vs_all = str(len(target_comp["component"]))+ ' (' + str(len(set(target_comp["component"]))) + ')'
				res.write(vert + str(one_by_one) + fin + rose + str(all_vs_all) + fin + '&')
				
				
				res.write(vert + str(len(set(ch["composite_fam"]))) + fin + rose + str(len(set(target_comp["composite_fam"]))) + fin + '\\\\\n\\hline\n')
			else :
				#todo
				pass
		res.write("\\hline\n\t\t\\end{tabular}\n\t\\caption{TODO}\n\t\\label{tab:TODO}\n\\end{table}")

def translate(x):
	if x =='x':
		return 23
	if x == 'y':
		return 24
	if x == -1:
		return 25
	else : 
		return int(x)
