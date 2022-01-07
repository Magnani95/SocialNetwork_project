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
		self.datasets = []
		self.main_graph = nx.MultiDiGraph()
#	PRIVATE METHODs-------------------------------------------------------------
#-------------------------------------------------------------------------------
	def __get_normalize_dict(self, d, norm_val):
		n_d = {}
		for k, v in d:
			n_d[k] = k / norm_val
		return n_d
#	PUBLIC METHODs--------_-----------------------------------------------------
#-------------------------------------------------------------------------------
	def load_all_csv2graph(self, datasets):
		print("--Loading trade csv files...")
		print("Datasets:\n", datasets)

		i = 0
		for f in datasets:
			print("[", i ," on ",len(datasets),"]\t Loading file:\t", str(f))
			with open( str(self.datasets_path+f), newline='') as csv_file:
				csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

				first_it = True
				num_rows = len(csv_file.readlines())
				csv_file.seek(0)
				entries = [0,0,0]
				with alive_bar(num_rows) as bar:  # declare your expected total
					for row in csv_reader:
						if first_it == True:
							first_it = False
							bar()
							continue
						entries[0] += 1
						time = int(row[0])
						source = int(row[1])
						dest = int(row[2])
						prod_id =  row[3]		#str to keep leading zeros
						value = float(row[4]) if bool(row[4]) else float(0)
						qnt = float(row[5]) if bool(row[5]) else float(0)
						if value == float(0):
							entries[1] += 1
						if qnt == float(0):
							entries[2] += 1
						self.main_graph.add_edge(source, dest, prod_id=prod_id, value=value, qnt=qnt)
						bar()      # call `bar()` at the end
				print("-> Entries:\t", entries)
				print("->(value-qnt)%\t", round(entries[1]/entries[0],2)," - ", round(entries[2]/entries[0],2))

	def centrality_degree(self):
		n_max_or_edges = self.main_graph.number_of_nodes() * self.codes_manager.n_prod
		n_max_edges = n_max_or_edges *2

		#	vanilla degree
		std = self.main_graph.degree(weight=None)
		std_n = self.__get_normalize_dict(std, n_max_edges)
		in_std = self.main_graph.in_degree()
		in_std_n = self.__get_normalize_dict(in_std, n_max_or_edges)
		out_std = self.main_graph.in_degree()
		out_std_n = self.__get_normalize_dict(out_std, n_max_or_edges)

		d_std = {	'all': std, 'all_n': std_n,
					'in': in_std, 'in_n': in_std_n,
					'out_std':out_std, 'out_n': out_std_n}

		#	value degree
		value = self.main_graph.degree(weight='value')
		value_n = self.__get_normalize_dict(value, n_max_edges)
		in_value = self.main_graph.in_degree(weight='value')
		in_value_n = self.__get_normalize_dict(in_value, n_max_or_edges)
		out_value = self.main_graph.in_degree(weight='value')
		out_value_n = self.__get_normalize_dict(out_value, n_max_or_edges)

		d_value = {	'all': value, 'all_n': value_n,
					'in': in_value, 'in_n': in_value_n,
					'out_value':out_value, 'out_n': out_value_n}

		#	qnt degree
		qnt = self.main_graph.degree(weight='qnt')
		qnt_n = self.__get_normalize_dict(qnt, n_max_edges)
		in_qnt = self.main_graph.in_degree(weight='qnt')
		in_qnt_n = self.__get_normalize_dict(in_qnt, n_max_or_edges)
		out_qnt = self.main_graph.in_degree(weight='qnt')
		out_qnt_n = self.__get_normalize_dict(out_qnt, n_max_or_edges)

		d_qnt = {	'all': qnt, 'all_n': qnt_n,
					'in': in_qnt, 'in_n': in_qnt_n,
					'out_qnt':out_qnt, 'out_n': out_qnt_n}


		return { 'std': d_std, 'value': d_value, 'qnt': d_qnt }
