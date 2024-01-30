# Copyright (C) 2014-2024 Ivan E. Cao-Berg
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
import logging
import pandas as pd

def query(good_set, candidates, alpha=-5, metric='euclidean', normalization='zscore', debug=False):
    '''
    Returns a ranked list

    :param alpha: alpha
    :type alpha: double
    :param candidates: DataFrame of image ids from candidates
    :type candidates: DataFrame
    :param good_set: DataFrame of image ids from members of the good set
    :type good_set: DataFrame
    :param metric: a valid metric
    :type metric: string
    :param normalization: normalization parameter. default value is 'zscore'
    :type normalization: string
    :rtype: DataFrame of ranked image
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

    for _, candidate in candidates.iterrows():
        iids.append(candidate[0])
        if debug:
            logging.debug("Analyzing candidate: " + candidate[0])

        candidate_distance = big_distance(alpha, candidate,
            good_set, metric=metric, debug=debug)
        if debug:
            logging.debug("Candidate distance: " + str(candidate_distance))

        if candidate_distance != 'NaN':
            ratings.append(candidate_distance)

    result = pd.DataFrame({'iids': iids, 'ratings': ratings})
    result.sort_values(by='ratings', inplace=True)

    return result

def big_distance(alpha, candidate, good_set, weighted=True,
        metric='euclidean', debug=True):
    '''
    Calculates the distance between a candidate and every member of the good set

    :param alpha: alpha
    :type alpha: double
    :param candidate: a feature vector
    :type candidates: Series
    :param good_set: a DataFrame of feature vectors
    :type good_set: DataFrame
    :param weight: weight
    :type weight: double
    :rtype: total_distance
    '''

    try:
        mp.dps = 50
        very_big = float(numpy.finfo(numpy.float32).max)/2

        total = mpf('0')

        #number of images
        counts = len(good_set)

        #pairwise distance
        weights = mpf('0')

        for _, good in good_set.iterrows():
            if weighted:
                weight = mpf(good[1])
            else:
                weight = mpf('1')

            weights = weights+weight
            score = distance(candidate[2],
                good[2], alpha=alpha, metric=metric )

            if alpha < 0 and score == 0:
                total_distance = 0
                return total_distance

            score = m