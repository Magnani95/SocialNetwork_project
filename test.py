import csv

with open('data/codes/country_codes_V202102.csv', newline='',  as file:
	for row in csv.reader(file):
		print(row)
