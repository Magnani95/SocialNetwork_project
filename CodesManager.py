from alive_progress import alive_bar
import csv

class CodesManager(object):
	"""docstring for CodesManager."""

	def __init__(self, dir_path):
		super(CodesManager, self).__init__()
		self.path = dir_path
		self.countries = {}
		self.categories = {}
		self.products_by_category= {}		# { k_c , ( desc_c , {k_p, desc_p} ) }
		self.n_prod = 0
		self.n_cat = 0

		self.__load_countryCodes()
		self.__load_productsAndCategories()

#	PRIVATE METHODs-------------------------------------------------------------
#-------------------------------------------------------------------------------
	def __load_countryCodes(self):
		print("--Loading countries codes...")
		file_name = 'country_codes_V202102.csv'
		with open( str(self.path+file_name), newline='', encoding='ISO-8859-15') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
			first_it = True
			for row in csv_reader:
				if first_it == True:
					first_it = False
					continue
				code = int(row[0])
				country = {'name':row[1], '2D':row[3], '3D':row[4]}
				self.countries[code] = country
			#print(self.countries); exit(1)

	def __load_productsAndCategories(self):
		print("--Loading products & categories...")
		cat_fname = '00-products_categories.csv'
		prod_fname = 'product_codes_HS92_V202102.csv'
		print("[",cat_fname,"]")
		print("[",prod_fname,"]")
		#	Categories
		with open( str(self.path+cat_fname), newline='' ) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
			first_it = True
			for row in csv_reader:
				if first_it == True:
					first_it = False
					continue
				code = row[0]
				desc = row[1]
				#print("c\t", code,"\t", desc, "\n-----")
				self.products_by_category[code] = (desc, {})
				self.n_cat +=1
			#print(self.prod_categories)
			#print(self.products_by_category)
		print("n_cat: ", self.n_cat)

		#	Products
		with open( str(self.path+prod_fname), newline='' ) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
			first_it = True
			for row in csv_reader:
				if first_it == True:
					first_it = False
					continue
				cat_code = row[0][0:2]
				prod_code = row[0]
				prod_desc = row[1]
				#print("c\t", cat_code,"-", prod_code, "\t", prod_desc, "\n-----")
				self.products_by_category[cat_code][1][prod_code] = prod_desc
				self.n_prod +=1
		print("n_prod: ", self.n_prod)


#	PUBLIC METHODs--------_-----------------------------------------------------
#-------------------------------------------------------------------------------

	def code2country(self, c_code):
		return self.countries.get(c_code, None )

	def c_code2name(self, c_code):
		ret = self.products_by_category.get(c_code, '[NOT REGISTERED]')
		if type(ret) is str:
			return ret
		elif type(ret) is tuple:
			return ret[0]
		else:
			print("FATAL ERROR IN 'CodesManager/c_code2name'")
			print("-->(args)\tc_code: ",c_code)
			print("-->type(ret):\t", type(ret))
			exit(1)

	def p_code2cat(self, p_code):
		c_code = p_code[0:2]
		return self.c_code2name(c_code)

	def p_code2name(self, p_code):
		c_code = p_code[0:2]
		return self.products_by_category[c_code][1].get(p_code, '[NOT REGISTERED]')
