import urllib
from numpy import genfromtxt
from os import remove
import halcon
from time import time
from sys import exit

print '''
This example uses the wine dataset from

Machine Learning Repository
Center for Machine Learning and Intelligent Systems
http://archive.ics.uci.edu/ml/datasets/Wine

This example uses this dataset to compare the different metrics available in FALCON
'''

url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data'
filename = 'data.csv'
urllib.urlretrieve( url, filename )
data = genfromtxt( filename, delimiter=',' )

query_wines = []
query_wines.append(['wine0', 1, data[0]])

#metrics
metrics = ['euclidean','cityblock','hamming']

remove(filename)

dataset = []
counter = 1
for datum in data:
	dataset.append([ 'wine' + str(counter), 1, datum ])
	counter = counter + 1

data = {}
for metric in metrics:
	[iids, scores] = halcon.search.query( query_wines, dataset, metric=metric, normalization='standard', debug=True )
	data[metric] = iids

#icaoberg: just in case people do not have the tabulate package
from tabulate import tabulate
table = []
for index in range(20):
	table.append([index, data['euclidean'][index], data['cityblock'][index], data['hamming'][index]])

print tabulate(table, headers=["Ranking","Euclidean", "City Block", "Hamming"])
exit(0)

