#! /usr/bin/env python3
# coding: utf-8
import pandas

def analyse(diff, comp):
	intersect_composites = set(comp["composite"]).intersection(set(diff["composite"]))
	for composite in intersect_composites:
		print("\n###############################################\nThe composite :", composite)
		events_diff = diff.loc[diff['composite'] == composite]
		events_comp = comp.loc[comp['composite'] == composite]
		intersect_components = set(events_diff["component"]).intersection(set(events_comp["component"]))
		print("is unanimously composed with the following components : ", intersect_components, len(intersect_components))
		print("among : ", len(list(set(events_diff["component"]))), "components found by Diffuse")
		print("and : ", len(list(set(events_comp["component"]))), "components found by CompositeSearch")
