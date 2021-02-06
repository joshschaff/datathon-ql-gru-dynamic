#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 10:14:01 2021

@author: Student
"""

import numpy as np 
import bisect
import collections

# % difference between previous time periods and predicted time period 
# kinda like the momentum trading code but for increase between prev and predicted

def max_profit(prices): 
    
    profit = 0
    tups = []
    j = 0
    
    for i in range(1, len(prices)): 
        if prices[i - 1] > prices[i]: 
            j = i
    
        if prices[i - 1] <= prices[i] and (
                i + 1 == len(prices) or prices[i] > prices[i + 1]):
            tups.append((j + 1, i + 1, (prices[i] - prices[j]) * 0.9982))
            
    return tups

# once you run this you'll get coin: tuples 
# aggregate into dictionary 
# input dictionary values into schedule_weighted_intervals 
# find key for each path 


# aggregate and sort coin data (maybe in a mapping with the coin names)
agg_prices = [] #max_profit(prices) <- an aggregated versin of this 
agg_tups = sorted(agg_prices, key=lambda tup: tup[1])

 
def compute_previous_intervals(agg_tuples):
    # extract start and finish times
    start = [i[0] for i in agg_tuples]
    finish = [i[1] for i in agg_tuples]

    p = []
    for j in range(len(agg_tuples)):
        # rightmost interval f_i <= s_j
        i = bisect.bisect_right(finish, start[j]) - 1
        p.append(i)

    return p
    
def schedule_weighted_intervals(agg_tuples):

    agg_tuples.sort(key=lambda x: x[1])
    p = compute_previous_intervals(agg_tuples)

    # compute OPTs iteratively in O(n), here we use DP
    OPT = collections.defaultdict(int)
    OPT[-1] = 0
    OPT[0] = 0
    for j in range(1, len(agg_tuples)):
        OPT[j] = max(agg_tuples[j][2] + OPT[p[j]], OPT[j - 1])

    O = []

    def compute_solution(j):
        if j >= 0:  # will halt on OPT[-1]
            if agg_tuples[j][2] + OPT[p[j]] > OPT[j - 1]:
                O.append(agg_tuples[j])
                compute_solution(p[j])
            else:
                compute_solution(j - 1)
    compute_solution(len(agg_tuples) - 1)

    return sorted(O, key=lambda x: x[1])

#G = [(43,70,27),(3,18,24),(65,99,45),(20,39,26),(45,74,26),(10,28,20),(78,97,23),(0,9,22)]
#print(schedule_weighted_intervals(G))


