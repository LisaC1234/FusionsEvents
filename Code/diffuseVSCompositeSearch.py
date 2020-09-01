#! /usr/bin/env python3
# coding: utf-8
import pandas

def comparison(diff, comp, organism, output): 
	with open(output + organism + '_Diffuse_vs_CompositeSearch.txt', 'w') as res :
		intersect_composites = set(comp["composite"]).intersection(set(diff["composite"]))
		if intersect_composites == []:
			res.write('none of the composites found by Diffuse are detectd by CompositeSearch')
		else :
			res.write('Diffuse         found ' + str(len(set(diff["composite"]))) + ' different composites.\n')
			res.write('CompositeSearch found ' + str(len(set(comp["composite"]))) + ' different composites.\n')
			res.write('Among them,           ' + str(len(intersect_composites)) + ' are in both results composites list.\n\n\n')
			for composite in intersect_composites:
				res.write("\n###############################################\nThe composite :"+ composite)
				events_diff = diff.loc[diff['composite'] == composite]
				events_comp = comp.loc[comp['composite'] == composite]
				intersect_components = set(events_diff["component"]).intersection(set(events_comp["component"]))
				res.write(" is unanimously composed with the following components : ")
				for c in intersect_components:
					res.write(c + ',')
				res.write( str(len(intersect_components)) + '\n')
				set_diffuse = set(events_diff["component"])
				res.write("among : "+ str(len(list(set(events_diff["component"]))))+ " components found by Diffuse")
				res.write(" and : "+ str(len(list(set(events_comp["component"]))))+ " components found by CompositeSearch")
				#res.write('\nComponent from Diffuse :\n')
				#for com in set_diffuse :
				#	res.write('\t' + com + '\n')
				


