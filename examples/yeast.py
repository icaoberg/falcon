#this example will download the iris dataset from the machine learning repository at uci
#located in http://archive.ics.uci.edu/ml/datasets/Iris
#and will attempt to query using one image against the whole dataset

from pandas import read_csv
from urllib import urlopen
import numpy
import falcon

print 'Downloading dataset from Machine Learning Database at UCI'
url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/yeast/yeast.data'
print url
page = urlopen( url )
print 'Reading CSV file'
data_frame = read_csv( page, header=None, delim_whitespace=True, names=[ 'label', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9' ] )

print 'Parsing CSV file'
labels = numpy.unique( data_frame.ix[:,'f9'] )
mapping = {}

for index in range( len(labels) ):
	mapping[labels[index]] = index

data_frame = data_frame.replace({'f9': mapping})

names = data_frame.ix[:,'label'].values
features = data_frame.ix[:,1:].values

print "Using image:" + names[0] + " as query image"
query_list = []
query_list.append( names[0] )
query_list.extend( [0] )
query_list.extend( features[0,:].tolist() )
query_list = [ query_list ]

print "Making good set using all images in dataset"
candidates_list = []
for index in range( len( features ) ):
	candidate = []
	candidate.append( names[index] )
	candidate.extend( [0] )
	candidate.extend( features[index,:] )
	candidates_list.append( candidate )

[iids, scores] = falcon.search.query( query_list, candidates_list, normalization='standard', debug=True )
