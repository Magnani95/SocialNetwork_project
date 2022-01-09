from alive_progress import alive_bar
import networkx as nx
import csv

from CodesManager import *


class GraphManager(object):
	"""docstring for Graph_Manager."""

	def __init__(self, datasets_path, **kwargs):
		super(GraphManager, self).__init__()
		self.datasets_path = datasets_path

		self.codes_manager = CodesManager('data/codes/')
		self.main_graph = nx.MultiDiGraph()
		self.categories_graph = nx.MultiDiGraph()
		self.trade_graph = nx.MultiDiGraph()
#	PRIVATE METHODs-------------------------------------------------------------
#-------------------------------------------------------------------------------
#	LV 0 ------------------------------
#--------------------------------------

	def _test(self):
		pass

	def _get_normalize_dict(self, d: dict, norm_val) -> dict:
		n_d = {}
		for k, v in d:
			n_d[k] = k / norm_val
		return n_d

	def _get_centrality_degree(self, weight: str=None, graph=None) -> dict:
		graph = self.main_graph if graph == None else graph

		n_max_or_edges = graph.number_of_nodes() * self.codes_manager.n_prod
		n_max_edges = n_max_or_edges *2

		deg = graph.degree(weight=weight)
		deg_n = self._get_normalize_dict(deg, n_max_edges)
		in_deg = graph.in_degree(weight=weight)
		in_deg_n = self._get_normalize_dict(in_deg, n_max_or_edges)
		out_deg = graph.in_degree(weight=weight)
		out_deg_n = self._get_normalize_dict(out_deg, n_max_or_edges)

		n_edges = self._get_n_edges_per_node(graph=graph)

		return {'all': deg, 'all_n': deg_n,
				'in': in_deg, 'in_n': in_deg_n,
				'out_deg':out_deg, 'out_n': out_deg_n}
#	LV 1 ------------------------------
#--------------------------------------

	def _get_n_edges_per_node(self, graph=None) -> dict:
		graph = self.main_graph if graph == None else graph

		r =  graph.reverse(copy=False)
		nodes = self._get_nodes_idx_list(graph=graph)
		in_edges = {};	out_edges = {}
		unique_edges = {};	unique_n = {}

		max_in = 0;	max_out= 0;	max_unique = 0

		for n in nodes:
			out_edges[n] = self._get_node_n_neighbors(n, graph=graph)
			in_edges[n] = self._get_node_n_neighbors(n, graph=r)
			unique_edges[n] = self._get_node_unique_n_neighbors(n, graph=graph)

			max_io = out_edges[n] if (out_edges[n] >= in_edges[n]) else in_edges[n]
			unique_n[n] = (unique_edges[n]-max_io) / (out_edges[n]+in_edges[n]-max_io)

			max_in  = in_edges[n]	if (in_edges[n]>max_in) 	else max_in
			max_out = out_edges[n]	if (out_edges[n]>max_out) 	else max_out
			max_unique = unique_edges[n] if (unique_edges[n]>max_unique) else max_unique

		max = {'in': max_in, 'out': max_out, 'unique': max_unique}

		return {'in': in_edges, 'out': out_edges,
				'unique': unique_edges, 'unique_n': unique_n,
				'max': max}

	def _get_nodes_idx_list(self, graph=None):
		graph = self.main_graph if graph == None else graph
		l = list(graph.nodes());
		l.sort()
		return l

	def _get_node_unique_neighbors(self, node: int, graph=None):
		graph = self.main_graph if graph == None else graph
		return set(list(graph.reverse(copy=False).neighbors(node)) + list(graph.neighbors(node)))

	def _get_node_n_neighbors(self, node: int, graph=None):
		graph = self.main_graph if graph == None else graph
		return len(list(graph.neighbors(node)))

	def _get_node_unique_n_neighbors(self, node: int, graph=None):
		graph = self.main_graph if graph == None else graph
		return len(self._get_node_unique_neighbors(node))
#	PUBLIC METHODs--------_-----------------------------------------------------
#-------------------------------------------------------------------------------
	def load_all_csv2graph(self, datasets: list):
		print("--Loading trade csv files...")
		print("Datasets:\n", datasets)

		i = 0
		for f in datasets:
			print("[", i ," on ",len(datasets),"]\t Loading file:\t", str(f))
			i += 1
			with open( str(self.datasets_path+f), newline='') as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

				first_it = True
				num_rows = len(csv_file.readlines())
				csv_file.seek(0)
				entries = [0,0,0]
				categories_data={}

				with alive_bar(num_rows) as bar:  # declare your expected total
					for row in csv_reader:
						if first_it == True:
							first_it = False
							bar()
							continue
						entries[0] += 1
						#	Main graph
						time = int(row[0])
						source = int(row[1])
						dest = int(row[2])
						prod_id =  row[3]		#str to keep leading zeros
						value = float(row[4]) if bool(row[4]) else float(0)
						qnt = float(row[5]) if bool(row[5]) else float(0)

						entries[1] = entries[1]+1 if (value==0)	else entries[1]
						entries[2] = entries[2]+1 if (qnt==0) else entries[2]
						self.main_graph.add_edge(source, dest, key=prod_id, prod_id=prod_id, value=value, qnt=qnt)

						#	Category graph
						cat_id = prod_id[0:2]

						if not self.categories_graph.has_edge(source, dest, key=cat_id):
							self.categories_graph.add_edge(source, dest, key=cat_id, cat_id=cat_id, value=value, qnt=qnt)
						else:
							old_edge = self.categories_graph.get_edge_data(source, dest, key=cat_id)
							new_value=old_edge['value']+value
							new_qnt=old_edge['qnt']+qnt
							self.categories_graph.add_edge(source, dest, key=cat_id, cat_id=cat_id, value=new_value, qnt=new_qnt )

						bar()      # call `bar()` at the end

				print("-> Entries:\t", entries)
				print("->(value-qnt)%\t", round(entries[1]/entries[0],2)," - ", round(entries[2]/entries[0],2))

				print("nodes:", self.main_graph.number_of_nodes(),"\tedges: ", self.main_graph.number_of_edges())


	def centrality_degree(self, graph=None):
		graph = self.main_graph if graph == None else graph

		d_std = self._get_centrality_degree(None)
		d_value = self._get_centrality_degree('value')
		d_qnt = self._get_centrality_degree('qnt')

		return { 'std': d_std, 'value': d_value, 'qnt': d_qnt }
