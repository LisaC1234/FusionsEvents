#! /usr/bin/env python3
# coding: utf-8

# Import pandas package  
import pandas
import plotly.graph_objects as go
import networkx as nx

def assign_pos(graph):
	dico_ch = {}
	dico_status = {}
	for edge in graph.edges:
		dico_ch[edge[0]] = graph[edge[0]][edge[1]]['ch_composite']
		dico_ch[edge[1]] = graph[edge[0]][edge[1]]['ch_component']
		if edge[0] not in dico_status:
			dico_status[edge[0]] = set()
			dico_status[edge[0]].add('composite')
		else:
			dico_status[edge[0]].add('composite')
		
		if edge[1] not in dico_status:
			dico_status[edge[1]] = set()
			dico_status[edge[1]].add('component')
		else:
			dico_status[edge[1]].add('component')
	nx.set_node_attributes(graph, dico_ch, 'ch')
	nx.set_node_attributes(graph, dico_status, 'status')
	
	working_graph = nx.Graph()
	working_graph.add_nodes_from(graph.nodes)
	for node1 in working_graph.nodes:
		for node2 in working_graph.nodes:
			if graph.nodes[node1]['ch'] == graph.nodes[node2]['ch']:
				working_graph.add_edge(node1, node2)
	pos = nx.fruchterman_reingold_layout(working_graph, k = 0.2)
	nx.set_node_attributes(graph, pos, 'pos')

def create_graph(reduced_comp,target):
	res = nx.from_pandas_edgelist(reduced_comp, "composite", "component", edge_attr=["ch_composite", "ch_component"])
	assign_pos(res)
	for node in res.nodes:
		print(node , res.nodes[node]['status'])
	return res



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
		
		
	edge_trace = go.Scatter(
	x=edge_x, y=edge_y,
	line=dict(width=0.5, color='#888'),
	hoverinfo='none',
	mode='lines')
	
	
	node_x = []
	node_y = []
	for node in G.nodes():
		x, y = G.nodes[node]['pos']
		node_x.append(x)
		node_y.append(y)
	
	
	node_trace = go.Scatter(
		x=node_x, y=node_y,
		mode='markers',
		hoverinfo='text',
		marker=dict(
		showscale=True,
		# colorscale options
		#'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
		#'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
		#'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
		colorscale='YlGnBu',
		reversescale=True,
		color=[],
		size=10,
		colorbar=dict(
			thickness=15,
			title='Node Connections',
			xanchor='left',
			titleside='right'
		),
		line_width=2)
	)
		
		
		
		
		
	node_adjacencies = []
	node_text = []
	for node in G.nodes:
		#print(node , G.nodes[node]['status'])
		node_text.append(node +"   " + str(G.nodes[node]['ch']))
		node_adjacencies.append(code(G.nodes[node]['status']))
#	for node, adjacencies in enumerate(G.adjacency()):
#		#print("\n\n\n",adjacencies)
#		node_adjacencies.append(len(adjacencies[1]))
#		#node_text.append('# of connections: '+str(len(adjacencies[1])))
#		node_text.append(adjacencies[0], )

	node_trace.marker.color = node_adjacencies
	node_trace.text = node_text
	
	fig = go.Figure(data=[edge_trace, node_trace],
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
		return 1
	if status == {'component'}:
		return 2
	return 3
	
def main():
	reduced_comp = pandas.read_csv('reduced.csv')
	print(len(set(reduced_comp["composite"])))
	print_network(reduced_comp, 1)
		
if __name__ == "__main__":
	main()
	
	
	
#('sp|Q5T5D7|ZN684_HUMAN',
#{	'sp|Q13401|PM2P3_HUMAN': {'ch_composite': 1, 'ch_component': '-1'}, 
#	'sp|C9JBD0|KRBX1_HUMAN': {'ch_composite': 1, 'ch_component': '3'}, 
#	'sp|Q5TYW1|ZN658_HUMAN': {'ch_composite': 1, 'ch_component': '9'}, 
#	'sp|A6NGD5|ZSA5C_HUMAN': {'ch_composite': 1, 'ch_component': '19'}, 
#	'sp|Q6ZRF7|ZN818_HUMAN': {'ch_composite': 1, 'ch_component': '-1'}}
#)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
