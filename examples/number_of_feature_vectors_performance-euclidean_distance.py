#this example will download the iris dataset from the machine learning repository at uci
#located in http://archive.ics.uci.edu/ml/datasets/Iris
#and will attempt to query using one image against the whole dataset

from sys import exit
from sys import stdout
from os import path

try:
	from numpy import arange as range
	from numpy.random import rand
	from numpy import polyval
	from numpy import polyfit	
except:
	exit("Unable to import numpy. Exiting example.")

try:
	import halcon
except:
	exit("Unable to import halcon. Exiting example.")

from time import time
from math import floor 

#icaoberg: got this nice snippet from 
#http://stackoverflow.com/questions/3160699/python-progress-bar
toolbar_width = 80

filename = 'number_of_feature_vectors_performance-euclidean_distance'

# setup toolbar
stdout.write("[%s]" % (" " * toolbar_width))
stdout.flush()
stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

results = [];
print "Generating and querying on synthetic datasets, please wait..."
for number_of_synthetic_vectors_in_dataset in range(100,10E2,100):
	number_of_synthetic_features = 500

	query_image = [ 'img', 1 ]
	synthetic_feature_vector = rand(1,number_of_synthetic_features).tolist()[0]
	query_image.append( synthetic_feature_vector )
	query_set = [ query_image ]

	dataset = []
	dataset.append( query_image )
	for i in range(number_of_synthetic_vectors_in_dataset):
		datum = [str(i),1]
		synthetic_feature_vector = rand(1,number_of_synthetic_features).tolist()[0]
		datum.append( synthetic_feature_vector )
		dataset.append( datum )

	t = time()
	[iids, scores] = halcon.search.query( query_set, dataset, normalization='standard', debug=True )
	t = time() - t
	results.append([ number_of_synthetic_vectors_in_dataset, t])

	# update the bar
	stdout.write("-")
	stdout.flush()

stdout.write("\n")

try:
	from tabulate import tabulate

	print "\nThese are the results from this test\n"
	print tabulate(results, headers=["Number of Feature Vectors","Time (in seconds)"])
except:
	print "Oh no! I could not import tabulate. Do not worry I will save the results in a pickle file"

import pickle
output_file = open( filename + '.pkl', 'w')
pickle.dump( results, output_file )
output_file.close()

print "\nThere is a clear trend that is dependent on the number of feature vectors. You know what? Why don't we try making a pretty plot as well"

try:
	import matplotlib.pyplot as plt
	polynomial = polyfit([row[0] for row in results],[row[1] for row in results], 1)
	plt.plot( [row[0] for row in results], [row[1] for row in results], 'bo' )
	plt.plot( [row[0] for row in results], polyval( polynomial, [row[0] for row in results]), 'r-' )
	plt.ylabel('Time (seconds)')
	plt.xlabel('Number of feature vectors')
	plt.title('FALCON - Number of features Performance Test')
	plt.legend(["Euclidean distance"])
	plt.grid(True)
	plt.savefig( filename + '.png' )
except:
 	print "\nOh no! I could not import matplotlib. I cannot make a pretty plot :("

if not path.isfile( filename + '.png' ) and not path.isfile( filename + '.pkl' ):
 	exit("\nCould not find pickle file nor pretty plot")
else:
	exit(0)
