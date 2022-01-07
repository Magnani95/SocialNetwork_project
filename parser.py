#!/bin/env python
import os
from GraphManager import *

#	MACROs
testing = False

#	GLOBAL VARs

graph_man = GraphManager('data/datasets/')
codes_man = graph_man.codes_manager
#	DEBUGGING AND UTILs
def __print(*args, **kargs):
	#print(*args, **kargs)
	pass
#	FUNCTIONs
def test(execute):
	if not execute:
		return
	global passed, g_passed
	g_passed = True

	print("[Testing...]\n")
	print("###\tTEST COUNTRIES\t###")
	for c in range(1,1000):
		n = codes_man.code2country(str(c))
		if n :
			print("Cod ", str(c), "\t", n)
		else:
			#print("Cod ", str(c) ,"\tis invalid")
			pass
	print("###\tDONE\t###")
	print("###\tTEST Cats&Prods\t###")
	#	CATEGORIES
	print("--Categories")
	passed = True
	def __test_cat(c,s):
		global passed, g_passed
		print(c,"\t\t",codes_man.c_code2name(c))
		print("->should be:\t",s)
		if not codes_man.c_code2name(c)==s:
			g_passed = False
			passed = False

	t = []
	t.append( ('01', 'Live animals; animal products') )
	t.append( ('77', 'UNDEFINED' ) )
	t.append( ('99','not elsewhere specified'))
	t.append( ('100', '[NOT REGISTERED]'))

	for e in t:
		__test_cat(*e)
	t.clear()
	print("--\tDONE",("passed" if bool(passed) else "failed"),"\t###")
	#PRODUCTS
	print("--Products")
	passed = True
	def __test_prod(c,s):
		global passed, gpassed
		print(c,"\t\t",codes_man.p_code2name(c))
		print("->should be:\t",s)
		if not codes_man.p_code2name(c) == s:
			g_passed = False
			passed = False

	t.append( ('030110', 'Fish: live, ornamental'))
	t.append( ('091010', 'Spices: ginger' ))
	t.append( ('110311', 'Cereal groats and meal: of wheat'))
	t.append( ('85640', '[NOT REGISTERED]'))

	for e in t:
		__test_prod(*e)
	t.clear()
	print("--\tDONE",("passed" if bool(passed) else "failed"),"\t###")
	print(bool(passed))
	print("[Testing done - ",("passed" if bool(g_passed) else "failed")," ]\n")


def main():
	test(testing)
	#datasets= os.listdir(DATASETS_PATH)
	datasets = ['BACI_HS92_Y1995_V202102.csv']
	print("Datasets:\n", datasets)
	main_g = graph_man.main_graph
	graph_man.load_all_csv2graph(datasets)

	print("nodes:", main_g.number_of_nodes(),"\tedges: ", main_g.number_of_edges())

	#print("+ NODES\t", len(graph.nodes))
	#print("+ EDGES\t", len(graph.edges))
	#print("+ DEGREE\t", graph.degree())

	source_country_id = 4 	# Italy 381
	target_country_id = 40
	__print("Single node data of country:\t", source_country_id)
	for n, edges in main_g.adj[source_country_id].items():
		__print("Neighbour_id\t", n, "[",codes_man.code2country(n)['name'] ,"]")
		i =0
		for e, attr in edges.items():
			__print("\t", e," Prod_id\t", attr['prod_id'], "-", codes_man.p_code2cat(attr['prod_id']))
		__print("+++")
	__print("###")

	c_degree = graph_man.centrality_degree()
	print("DEGREE STD_n",len(c_degree['std']['all']),"\n", c_degree['std']['all'])


if __name__ == '__main__':
	main()
