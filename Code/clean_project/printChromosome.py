#! /usr/bin/env python3
# coding: utf-8

# Import pandas package  
import pandas
import plotly.graph_objects as go
#import plotly.express as px
import networkx as nx
#from colour import Color

	
colors = ['#C481A7', '#EDE342', '#F2BF6C', '#FB76C1', '#FF51EB', '#58EFEC', '#7CCAD5', '#A0A6BE','#C481A7', '#E85C90', '#C481A7', '#EDE342', '#F2BF6C', '#FB76C1', '#FF51EB', '#58EFEC', '#7CCAD5', '#A0A6BE','#C481A7', '#E85C90', '#C481A7', '#EDE342', '#F2BF6C', '#FB76C1', '#FF51EB', '#58EFEC', '#7CCAD5', '#A0A6BE','#C481A7', '#E85C90']
	#dict_col= {val:key for val,key in enumerate(colors)}
symbols = ['circle', 'square', 'star']



####################################################
#        Building the nx graph 
####################################################
def create_graph(comp,target):
	reduced_comp = comp.loc[comp["ch_composite"] == str(target)]# only the edges involving target chromosome
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
	
####################################################
#            chromosomes name -> int 
####################################################		
	
def translate(x):
	if x =='x':
		return 23
	if x == 'y':
		return 24
	if x == -1:
		return 25
	else : 
		return int(x)
		

####################################################
#       building and printing the graph
####################################################

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
		
	###### Trace containing all the edges ######
	trace_record = []	
	edge_trace = go.Scatter(
		x=edge_x, y=edge_y,
		line=dict(width=0.5, color='#888'),
		hoverinfo='none',
		mode='lines',
		showlegend = False
	)
	trace_record.append(edge_trace)
	
	###### Building one trace per status #######
	list_composite_x = []
	list_composite_y = []
	text_composite = []
	color_composite = []
	
	list_component_x = []
	list_component_y = []
	text_component = []
	color_component = []
	
	list_both_x = []
	list_both_y = []
	text_both = []
	color_both = []
	
	for node in G.nodes():
		x, y = G.nodes[node]['pos']
		if "component" in G.nodes[node]['status'] and "composite" in G.nodes[node]['status']:
			list_both_x.append(x)
			list_both_y.append(y)
			text_both.append(node.split('|')[1] + ' from ch ' + G.nodes[node]['ch'])
			color_both.append(colors[translate(G.nodes[node]['ch'])])
		elif "composite" in G.nodes[node]['status']:
			list_composite_x.append(x)
			list_composite_y.append(y)
			text_composite.append(node.split('|')[1] + ' from ch ' + G.nodes[node]['ch'])
			color_composite.append(colors[translate(G.nodes[node]['ch'])])
		elif "component" in G.nodes[node]['status']:
			list_component_x.append(x)
			list_component_y.append(y)
			text_component.append(node.split('|')[1] + ' from ch ' + G.nodes[node]['ch'])
			color_component.append(colors[translate(G.nodes[node]['ch'])])
			
			
	list_x = [list_composite_x, list_component_x, list_both_x]
	list_y = [list_composite_y, list_component_y, list_both_y]
	list_text = [text_composite, text_component, text_both]
	list_color = [color_composite, color_component, color_both]
	list_name = ['composite (' + str(len(list_x[0]))+ ')', 'component (' + str(len(list_x[1]))+ ')', 'both composite and component (' + str(len(list_x[2]))+ ')']
	
	for i in range(len(list_x)):
		trace = go.Scatter(
			x=list_x[i], y=list_y[i],
			mode='markers',
			hoverinfo='text',
			marker = dict(
				showscale = False,
				size = 10,
				color = [],
				symbol = symbols[i],
				line = dict(
					color = 'Grey',
					width = 1
				),
			),
			
			name = list_name[i]
		)
		trace.marker.color = list_color[i]
		trace.text = list_text[i]
		trace_record.append(trace)
		
		
	###### Assembling the final figure  ########
	
	fig = go.Figure(data=trace_record,
			 layout=go.Layout(
				title='<br>Composites from the chromosome ' + str(target) +' <br>',
				titlefont_size=25,
				showlegend=True,
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
	
	
def main():
	target = 1
	reduced_comp = pandas.read_csv('reduced.csv')
	print_network(reduced_comp, target)
	
if __name__ == "__main__":
	main()
	
