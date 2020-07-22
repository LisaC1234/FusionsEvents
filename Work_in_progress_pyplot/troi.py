#! /usr/bin/env python3
# coding: utf-8

# Import pandas package  
import pandas
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
from colour import Color

####################################################
#        Building the nx graph 
####################################################
def create_graph(reduced_comp,target):
	G = nx.Graph()
	
	dico_status = {}
	dico_ch = {}
	for row in reduced_comp.itertuples():
		G.add_edge(row.composite, row.component)
		dico_ch[row.composite] = str(row.ch_composite)
		dico_ch[row.component] = str(row.ch_component)
		if row.composite in dico_status:
			dico_status[row.composite].add('composite')
		else:
			dico_status[row.composite] = set()
			dico_status[row.composite].add('composite')
		
		if row.component in dico_status:
			dico_status[row.component].add('component')
		else:
			dico_status[row.component] = set()
			dico_status[row.component].add('component')
			
		
	nx.set_node_attributes(G, dico_ch, 'ch')
	nx.set_node_attributes(G, dico_status, 'status')
	assign_pos(G)
	return G
	
	
####################################################
#         defining nodes positions
####################################################	
def assign_pos(graph):
	working_graph = nx.Graph()
	working_graph.add_nodes_from(graph.nodes)
	for node1 in working_graph.nodes:
		for node2 in working_graph.nodes:
			if graph.nodes[node1]['ch'] == graph.nodes[node2]['ch']:
				working_graph.add_edge(node1, node2)
	pos = nx.fruchterman_reingold_layout(working_graph, k = 0.2)
	nx.set_node_attributes(graph, pos, 'pos')
	
	
	
def trad(x):
	if x =='x':
		return 23
	if x == 'y':
		return 24
	if x == -1:
		return 25
	else : 
		return int(x)

def print_network(comp,target):
	G = create_graph(comp,target)
	edge_x = []
	edge_y = []
	for edge in G.edges():
		x0, y0 = G.nodes[edge[0]]['pos']
		x1, y1 = G.nodes[edge[1]]['pos']
		edge_x.append(x0)
		edge_x.append(x1)
		edge_x.append(None)
		edge_y.append(y0)
		edge_y.append(y1)
		edge_y.append(None)
		
	trace_record = []	
	edge_trace = go.Scatter(
	x=edge_x, y=edge_y,
	line=dict(width=0.5, color='#888'),
	hoverinfo='none',
	mode='lines')
	
	trace_record.append(edge_trace)	
	
	
	colors = ['#C481A7', '#EDE342', '#F2BF6C', '#FB76C1', '#FF51EB', '#58EFEC', '#7CCAD5', '#A0A6BE','#C481A7', '#E85C90', '#C481A7', '#EDE342', '#F2BF6C', '#FB76C1', '#FF51EB', '#58EFEC', '#7CCAD5', '#A0A6BE','#C481A7', '#E85C90', '#C481A7', '#EDE342', '#F2BF6C', '#FB76C1', '#FF51EB', '#58EFEC', '#7CCAD5', '#A0A6BE','#C481A7', '#E85C90']
	dict_col= {val:key for val,key in enumerate(colors)}
	symbols = ['circle', 'square', 'star']
	
	for node in G.nodes():
		x, y = G.nodes[node]['pos']
		trace = go.Scatter(
			x=[x], y=[y],
			mode='markers',
			hoverinfo='text',
			marker = dict(
				showscale = True,
				color=colors[trad(G.nodes[node]['ch'])],
				size = 10,
				symbol = symbols[code(G.nodes[node]['status'])],
				line = dict(
					color = 'MediumPurple',
					width = 2
				),
				colorsrc = dict_col #######Continuer à chercher !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			),
			text = node + " " + G.nodes[node]['ch']
		)
		trace_record.append(trace)


	fig = go.Figure(data=trace_record,
			 layout=go.Layout(
				title='<br>Composites from the chromosome' + str(target) +' <br>',
				titlefont_size=16,
				showlegend=False,
				hovermode='closest',
				margin=dict(b=20,l=5,r=5,t=40),
				annotations=[ dict(
					text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
					showarrow=False,
					xref="paper", yref="paper",
					x=0.005, y=-0.002 ) ],
				xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
				yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
				)

			
	fig.show()
	
def code(status):
	if status == {'composite'}:
		return 0
	if status == {'component'}:
		return 1
	return 2
	
def main():
	target = 1
	reduced_comp = pandas.read_csv('reduced.csv')
	print_network(reduced_comp, target)
	
	
	
	
if __name__ == "__main__":
	main()
	

	
	
