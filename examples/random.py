#this example will download the iris dataset from the machine learning repository at uci
#located in http://archive.ics.uci.edu/ml/datasets/Iris
#and will attempt to query using one image against the whole dataset

import numpy
import falcon

number_of_synthetic_features = 100
number_of_synthetic_vectors_in_dataset = 100

print 'Generating random query image'
print 'Query image name: foo'
query_image = [ 'foo', 0 ]
synthetic_feature_vector = numpy.random.rand(1,number_of_synthetic_features).tolist()[0]
query_image.append( synthetic_feature_vector )
query_set = [ query_image ]

print "Generating random dataset"
dataset = []
dataset.append( query_image )
for i in range(number_of_synthetic_vectors_in_dataset):
	datum = [str(i),0]
	synthetic_feature_vector = numpy.random.rand(1,number_of_synthetic_features).tolist()[0]
	datum.append( synthetic_feature_vector )
	dataset.append( datum )

[iids, scores] = falcon.search.query( query_set, dataset, normalization='standard', debug=True )