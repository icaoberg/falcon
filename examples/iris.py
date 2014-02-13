import urllib
from numpy import genfromtxt

#http://archive.ics.uci.edu/ml/datasets/Iris
url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
filename = 'iris.csv'
urllib.urlretrieve( url, filename )
data = genfromtxt( filename, delimiter=',' )