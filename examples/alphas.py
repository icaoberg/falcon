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

This example uses this dataset to compare results at different alphas
'''

url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data'
filename = 'data.csv'
urllib.urlretrieve( url, filename )
data = genfromtxt( filename, delimiter=',' )

query_wines = []
query_wines.append(['wine0', 1, data[0]])

#alphas
alphas = [-100,-50,-5,5,50,100]

remove(filename)

dataset = []
counter = 1
for datum in data:
	dataset.append([ 'wine' + str(counter), 1, datum ])
	counter = counter + 1

data = {}
for alpha in alphas:
	#print "alpha:" + str(alpha)
	[iids, scores] = halcon.search.query( query_wines, dataset, alpha=alpha, metric='euclidean', normalization='standard', debug=True )
	data[alpha] = iids

#icaoberg: just in case people do not have the tabulate package
from tabulate import tabulate
table = []
for index in range(100):
	table.append([index, data[-100][index], data[-50][index], data[-5][index], 
		data[5][index], data[50][index], data[100][index]])

print tabulate(table, headers=["Ranking","alpha:-100", "alpha:-50", "alpha:-5", 
	"alpha:5", "alpha:50", "alpha:100"])

exit(0)

