#! /usr/bin/env python3
# coding: utf-8
import pandas


def by_chromosome(comp, list_ch, organism, output): # returns a non ordered recap (latex table) of all the chromosomes, compairing the one_by_one and the all_vs_all use of CompositeSearch. 
	vert = '\\textcolor{vert}{\\textbf{'
	orange = '\\textcolor{orange}{\\textbf{'
	rose = '\\textcolor{rose}{\\textbf{'
	fin = '}} '
	output_path = output + organism +".tex"
	already_analysed = []
	with open(output_path, "w") as res:
		res.write("\\begin{table}[H]\n\t\\centering\n\t\\begin{tabular}{||l|c|c|c|c||}\n\t\t\\hline\\hline\n\t\tChromosome&Genes&Composites&Components (uniques)&Families of composites\\\\\n\t\t\\hline\\hline\n")
		for ch in list_ch: # for every chromosomes that have some composites after the one by on CompositeSearch
			if not ch.empty: 
				numb = ch.loc[0]["ch_composite"]
				already_analysed.append(numb)
				res.write('chromosome ' + str(numb) + '&..&') # how to obtain le numer of genes per ch ?
				target_comp = comp.loc[comp["ch_composite"] == numb]
				
				res.write(vert + str(len(set(ch["composite"]))) + fin + orange +  str(len(set(target_comp["composite"]).intersection(set(ch["composite"])))) + fin + rose + str(len(set(target_comp["composite"]))) + fin + '&') 
				one_by_one = str(len(ch["component"])) + ' (' + str(len(set(ch["component"]))) + ')'
				all_vs_all = str(len(target_comp["component"]))+ ' (' + str(len(set(target_comp["component"]))) + ')'
				res.write(vert + str(one_by_one) + fin + rose + str(all_vs_all) + fin + '&')
				
				
				res.write(vert + str(len(set(ch["composite_fam"]))) + fin + rose + str(len(set(target_comp["composite_fam"]))) + fin + '\\\\\n\\hline\n')
				
				
		list_id = set(comp["ch_composite"])
		list_numb = list_id.difference(set(already_analysed)) #all the other chromosomes
		
		for numb in list_numb:
			res.write('chromosome ' + str(numb) + '&..&') # how to obtain le numer of genes per ch ?
			target_comp = comp.loc[comp["ch_composite"] == numb]
				
			res.write(vert + str(0) + fin + orange +  str(0) + fin + rose + str(len(set(target_comp["composite"]))) + fin + '&') 
			one_by_one = str(0) 
			all_vs_all = str(len(target_comp["component"]))+ ' (' + str(len(set(target_comp["component"]))) + ')'
			res.write(vert + str(one_by_one) + fin + rose + str(all_vs_all) + fin + '&')
			res.write(vert + str(0) + fin + rose + str(len(set(target_comp["composite_fam"]))) + fin + '\\\\\n\\hline\n')
				
				
		res.write("\\hline\n\t\t\\end{tabular}\n\t\\caption{TODO}\n\t\\label{tab:TODO}\n\\end{table}")


