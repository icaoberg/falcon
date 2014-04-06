#this example will download the iris dataset from the machine learning repository at uci
#located in http://archive.ics.uci.edu/ml/datasets/Iris
#and will attempt to query using one image against the whole dataset

from sys import exit

try:
	import numpy
except:
	exit("Unable to import numpy. Exiting example.")

try:
	import falcon
except:
	exit("Unable to import falcon. Exiting example.")

from time import time
from math import floor 

number_of_synthetic_features = 100
number_of_synthetic_vectors_in_dataset = 100

t = time()
print 'Generating random query image'
print 'Query image name: img'
query_image = [ 'img', 1 ]
synthetic_feature_vector = numpy.random.rand(1,number_of_synthetic_features).tolist()[0]
query_image.append( synthetic_feature_vector )
query_set = [ query_image ]
t = time() - t
print "Elapsed time: " + str(t) + " seconds\n"

t = time()
print "Generating random dataset"
dataset = []
dataset.append( query_image )
for i in range(number_of_synthetic_vectors_in_dataset):
	datum = [str(i),1]
	synthetic_feature_vector = numpy.random.rand(1,number_of_synthetic_features).tolist()[0]
	datum.append( synthetic_feature_vector )
	dataset.append( datum )

t = time() - t
print "Elapsed time: " + str(t) + " seconds\n"

t = time()
print "Querying with one images"
[iids, scores] = falcon.search.query( query_set, dataset, normalization='standard', debug=True )
t = time() - t
print "Elapsed time: " + str(t) + " seconds\n"

#icaoberg: you can ignore the next part of the code. i was just trying to prettify the results
#there is a probably a quicker, leaner, cleaner way
print "Top Ten Results!"

#icaoberg: i will only display the top ten results
iids = iids[0:9]
scores = scores[0:9]

try:
	from tabulate import tabulate
	rank = 0
	table = []
	for index in range(len(iids)):
		table.append([str(rank), str(iids[index]), str(scores[index])])
		rank = rank + 1

	print tabulate(table, headers=["Ranking","Identifier", "Score"])
except:
	print "rank\tiid\t\tscore"

	rank = 0
	for iid, score in zip(iids,scores):
		print str(rank) + "\t" + str(iid) + "\t\t" + str(score)
		rank = rank + 1
