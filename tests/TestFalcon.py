import sys

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from falcon import search
from numpy.random import rand

class TestFalcon(unittest.TestCase):
    def setUp(self):
    	number_of_synthetic_features = 100
    	self.alpha = -5.0
        self.vector1 = rand(1,number_of_synthetic_features)
        self.vector2 = rand(1,number_of_synthetic_features)

    def test_distances(self):
    	metrics = ['euclidean', 'mahalanobis',
    				'cityblock', 'hamming']

    	for metric in metrics:
    		norm = search.distance(self.vector1, self.vector2, 
    			self.alpha, metric )
    		print "(metric,norm):(" + metric + "," + str(norm) + ")"

    def test_big_distances(self):
    	metrics = ['euclidean', 'mahalanobis',
    				'cityblock', 'hamming']

    	for metric in metrics:
    		norm = search.distance(self.vector1, self.vector2, 
    			self.alpha, metric )
    		print "(metric,norm):(" + metric + "," + str(norm) + ")"

if __name__ == '__main__':
    unittest.main()