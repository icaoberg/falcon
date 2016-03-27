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
import scipy.spatial.distance as distances
from mpmath import *
from operator import itemgetter

def query(good_set, candidates, alpha=-5, metric='euclidean', normalization='zscore', debug=False):
    '''
    Returns a ranked list

    :param alpha: alpha
    :type alpha: double
    :param candidates: list of image ids from candidates
    :type candidates: double
    :param good_set: list of image ids from members of the good set
    :type good_set: list of longs
    :param metric: a valid metric
    :type metric: string
    :param normalization: normalization parameter. default value is 'zscore'
    :type normalization: string
    :rtype: list of ranked image
    '''

    #normalize the feature vectors
    if debug:
        workspace = {}
        workspace['candidates'] = candidates
        workspace['good_set'] = good_set

    [candidates, good_set] = feature_normalization(candidates, good_set,
        normalization, debug=debug)

    if debug:
        workspace['normalized_candidates'] = candidates
        workspace['normalized_good_set'] = good_set

    ratings = []
    iids = []
    candidate_distance = []

    for candidate in candidates:
        iids.append(candidate[0])
        if debug:
            print "Analyzing candidate: " + candidate[0]

        candidate_distance = big_distance(alpha, candidate,
            good_set, metric=metric, debug=debug)
        if debug:
            print "Candidate distance: " + str(candidate_distance)

        if candidate_distance != 'NaN':
            ratings.append(candidate_distance)

    tups = zip(iids, ratings) # zip them as tuples

    result = sorted(tups, key=itemgetter(1))
    # note that this is sorting the tuples by the second element of the tuple
    # if you want to sort by the first element,
    #then you should use itemgetter(0)

    sorted_iids = []
    sorted_scores = []
    for itm in result:
        sorted_iids.append(itm[0])
        sorted_scores.append(itm[1])

    return [sorted_iids, sorted_scores]

def big_distance(alpha, candidate, good_set, weighted=True,
        metric='euclidean', debug=True):
    '''
    Calculates the distance between a candidate and every member of the good set

    :param alpha:alpha
    :type alpha:double
    :param candidate:a feature vector
    :type candidates:list
    :param good_set:a list of feature vectors
    :type good_set:array
    :param weight:weight
    :type weight:double
    :rtype: total_distance
    '''

    try:
        mp.dps = 50
        very_big = float(numpy.finfo(numpy.float32).max)/2

        total = mpf('0')

        if debug:
            print "very_big:"+str(very_big)
            print "total:"+str(total)

        #number of images
        counts = len(good_set)

        #pairwise distance
        weights = mpf('0')
        if debug:
            print "weights:"+str(weights)

        for index in range(counts):
            if weighted:
                weight = mpf(good_set[index][1])
            else:
                weight = mpf('1')

            if debug:
                print "count:"+str(index)
                print "weight:"+str(weight)

            weights = weights+weight
            score = distance(candidate[2],
                good_set[index][2], alpha=alpha, metric=metric )

            if debug:
                print "score:"+str(score)

            if alpha < 0 and score == 0:
                total_distance = 0
                return total_distance

            score = mpf(weight)*numpy.power(mpf(score), mpf(alpha))
            total = total + score

        total_distance = mpf(total)/mpf(weights)
        total_distance = total_distance**mpf(1.0/1.0*alpha)
    except:
        if debug:
            print 'Unable to calculate big distance'
        total_distance = 'NaN'

    return total_distance

def distance(vector1, vector2, alpha=2, metric='euclidean' ):
    '''
    Helper function that calculates the alpha

    :param vector1:a vector
    :type vector1:list of doubles
    :param vector2:a vector
    :type vector2:list of doubles
    :param metric: euclidean, mahalanobis, seuclidean, cityblock
    :type metric:string
    :rtype: norm between vectors A and B
    '''

    mp.dps = 50
    alpha = mpf(1.0*alpha)
    vector1 = matrix(numpy.array(vector1))
    vector2 = matrix(numpy.array(vector2))

    if metric == 'euclidean':
        vector_norm = distances.euclidean( vector1, vector2 )
    elif metric == 'mahalanobis':
        vi = numpy.linalg.inv( numpy.cov(
            numpy.concatenate((vector1, vector2)).T))
        vector_norm = distances.mahalanobis( vector1, vector2, vi )
    elif metric == 'seuclidean':
        vector_norm = distances.seuclidean( vector1, vector2 )
    elif metric == 'cityblock':
        vector_norm = distances.cityblock( vector1, vector2 )
    elif metric == 'hamming':
        vector_norm = distances.hamming( vector1, vector2 )
    else:
        print "Unknown metric"
        return None

    return vector_norm

def feature_normalization(trainset, testset, normalization, debug=False):
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
            new_trainset.append([trainset_id[i], trainset_wt[i],
                trainset_normfeat[i]])

        new_testset = []
        for i in range(len(testset)):
            new_testset.append([testset_id[i], testset_wt[i],
                testset_normfeat[i]])

        return new_trainset, new_testset

    else:
        trainset_id = []
        trainset_wt = []
        trainset_feat = []

        for itm in trainset:
            trainset_id.append(itm[0])
            trainset_wt.append(itm[1])
            trainset_feat.append(itm[2])

        trainset_feat = numpy.array(trainset_feat)

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
            new_trainset.append([trainset_id[i], trainset_wt[i],
                trainset_normfeat[i]])

        new_testset = []
        for i in range(len(testset)):
            new_testset.append([testset_id[i], testset_wt[i],
                testset_normfeat[i]])

        return new_trainset, new_testset

def counter(filename, word):
    '''
    Helper function that counts the occurences of a word in a file
    '''

    count = 0
    try:
        textfile = open(filename, 'r')
    except:
        print "Unable to open file"
        return count

    for line in textfile:
        if word in line:
            count += 1

    textfile.close()
    return count
