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




		
def by_chromosome(diff, comp, list_ch):
	
	output_path = "test.tex"
	with open(output_path, "w") as res:
		res.write("\\begin{table}[H]\n\t\\centering\n\t\\begin{tabular}{||l|c|c|c|c||}\n\t\t\\hline\\hline\n\t\tChromosome&Genes&Composites&Components (uniques)&Families of composites\\\\\n\t\t\\hline\\hline")
		for ch in list_ch:
			
			numb = ch.loc[0]["ch_composite"]
			print(numb)
			target_comp = comp.loc[comp["ch_composite"] == numb]
			print(len(set(target_comp["composite"]))) # nb of composite for the all vs all analysis
			print(len(set(ch["composite"]))) # nb of composite for the one by one analysis 
			print(len(set(target_comp["composite"]).intersection(set(ch["composite"])))) # intersection of the results
			
			print(len(set(ch["composite_fam"]))) # nb of families for the one by one analysis
			print(len(set(target_comp["composite_fam"]))) # nb of families for the all vs all analysis
			print(len(set(ch["component"])))
			print(len(set(target_comp["component"])))
			print(len(ch["component"]))
			print(len(target_comp["component"]))
		res.write("\\hline\n\t\t\\end{tabular}\n\t\\caption{TODO}\n\t\\label{tab:TODO}\n\\end{table}")


	#print(list_ch[23]["composite"])
