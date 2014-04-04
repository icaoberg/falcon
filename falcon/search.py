# Copyright (C) 2014 Ivan E. Cao-Berg
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 2 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import numpy
import scipy
import os
import time

from operator import itemgetter, attrgetter

try:
    import cPickle as pickle
except Exception, e:
    import pickle

def query( good_set, candidates, alpha=-5, normalization='zscore', 
           debug=False ):
    '''
    Returns a ranked list

    :param alpha: alpha
    :type alpha: double
    :param candidates: list of image ids from candidates
    :type candidates: double
    :param good_set: list of image ids from members of the good set
    :type good_set: list of longs
    :param normalization: normalization parameter. default value is 'zscore'
    :type normalization: string
    :rtype: list of ranked image 
    '''

    #standard deviation of features in the dataset
    #std = numpy.std(numpy.array( good_set[2]) )

    #normalize the feature vectors
    workspace = {}
    workspace['candidates'] = candidates
    workspace['good_set'] = good_set

    [candidates, good_set] = feature_normalization( candidates, good_set, normalization, debug=debug )

    if debug:
      workspace['normalized_candidates'] = candidates
      workspace['normalized_good_set'] = good_set

    ratings = []
    iids = []
    candidate_distance = []

    for candidate in candidates:
        iids.append( candidate[0] )
        candidate_distance = distance( alpha, candidate, good_set, debug=debug )
        ratings.append( candidate_distance )
    
    tups = zip( iids, ratings ) # zip them as tuples

    result = sorted(tups, key=itemgetter(1))
    # note that this is sorting the tuples by the second element of the tuple
    # if you want to sort by the first element, then you should use itemgetter(0)
    sorted_iids = []
    sorted_scores = []
    for itm in result:
        sorted_iids.append(itm[0])
        sorted_scores.append(itm[1])

    return [sorted_iids, sorted_scores]

def distance( alpha, candidate, good_set, debug=False ):
    '''
    Calculates the distance between a candidate and every member of the good set

    :param alpha: alpha
    :type alpha: double
    :param candidate: a feature vector 
    :type candidates: list
    :param good_set: a list of feature vectors
    :type good_set: array
    :rtype: distance
    '''

    if debug:
        log_filename = './distance.log'
        if os.path.isfile( log_filename ):
            file = open( log_filename, 'a' )
        else:
            file = open( log_filename, 'w' )

    file.write( "#BEGIN\n")
    file.write( "alpha set to : " + str(alpha) + "\n" )

    very_big = float(numpy.finfo( numpy.float32 ).max)/2;
    flag_zero = False
    total = numpy.float64(0)

    #number of images
    counts = len( good_set )

    #pairwise distance
    weights = numpy.float64(0)

    for index in range( counts ):
        weight = numpy.float64(good_set[index][1])
        weights = weights + weight
        d = norm( candidate[2], good_set[index][2] )
        score = weight * numpy.power(d, numpy.float64(alpha)) 
        total = total + score

    if candidate[1] < 0:
        total = numpy.float64(0)
    else:
        total = numpy.float64(total)/numpy.float64(weights)
        if total != 0:
            total=numpy.float64(numpy.power(total,numpy.float64(alpha)))
        elif numpy.float64(candidate[1])>0:
            total = 0
        else:
            if numpy.float64(candidate[1])<0:
                total = very_big

    return total 

def norm( A, B, alpha=2 ):
    '''
    Calculates the norm between vectors A and B

    :param A: a vector
    :type A: list of doubles
    :param B: a vector 
    :type B: list of doubles
    :rtype: norm between vectors A and B
    '''

    alpha = numpy.float64(1.0*alpha)
    A = numpy.float64( numpy.array( A ) )
    B = numpy.float64( numpy.array( B ) )
    return numpy.float64(numpy.power(numpy.sum(numpy.abs((A-B))**alpha),numpy.float64(1.0/alpha)))

def feature_normalization( trainset, testset, normalization, debug=False ):
    '''
    Feature normalization.

    :param trainset: training set
    :type trainset: list of feature vectors
    :param testset: test set 
    :type testset: list of feature vectors
    :param normalization: zscore or standard
    :rtype: string
    :rtype: normalized train and test sets
    '''

    if normalization == 'standard':
        trainset_id = []
        trainset_wt = []
        trainset_feat = []

    for itm in trainset:
      	trainset_id.append(itm[0])
      	trainset_wt.append(itm[1])
      	trainset_feat.append(itm[2])

    trainset_feat = numpy.array(trainset_feat)
    min_col = trainset_feat.min(axis=0) + 1e-10
    max_col = trainset_feat.max(axis=0) + 1e-10

    trainset_normfeat = (trainset_feat-min_col)/numpy.float64(max_col) 

    testset_id = []
    testset_wt = []
    testset_feat = []

    for itm in testset:
        testset_id.append(itm[0])
        testset_wt.append(itm[1])
        testset_feat.append(itm[2])

    testset_feat = numpy.array(testset_feat)
    testset_normfeat = (testset_feat-min_col)/numpy.float64(max_col)

    new_trainset = []
    for i in range(len(trainset)):
        new_trainset.append([trainset_id[i], trainset_wt[i], trainset_normfeat[i]])

    new_testset = []
    for i in range(len(testset)):
        new_testset.append([testset_id[i], testset_wt[i], testset_normfeat[i]])

    return new_trainset, new_testset

  else:
      trainset_id = []
      trainset_wt = []
      trainset_feat = []

      for itm in trainset:
          trainset_id.append(itm[0])
          trainset_wt.append(itm[1])
          trainset_feat.append(itm[2])

      trainset_feat = numpy.array( trainset_feat )

      mean_col = trainset_feat.mean(axis=0)
      std_col = trainset_feat.std(axis=0) + 1e-10

      trainset_normfeat = (trainset_feat - mean_col)/numpy.float64(std_col)

      testset_id = []
      testset_wt = []
      testset_feat = []

      for itm in testset:
          testset_id.append(itm[0])
          testset_wt.append(itm[1])
          testset_feat.append(itm[2])

      testset_feat = numpy.array(testset_feat)
      testset_normfeat = (testset_feat-mean_col)/numpy.float64(std_col)

      new_trainset = []
      for i in range(len(trainset)):
          new_trainset.append([trainset_id[i], trainset_wt[i], trainset_normfeat[i]])

      new_testset = []
      for i in range(len(testset)):
          new_testset.append([testset_id[i], testset_wt[i], testset_normfeat[i]])

      return new_trainset, new_testset

  def counter( filename, word ):
      '''
      Helper function that counts the occurences of a word in a file
      '''

      count = 0
      try:
          file  = open('file', 'r')
      except:
          print "Unable to open file"
          return count
      
      for line in file:
          if word in line:
              total += 1

      file.close()
      return count

