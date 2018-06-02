# -*- coding: utf-8 -*-
# Author : tyty
# Date   : 2018-6-2
# Env    : python2.6

from __future__ import division
from math import log



def calculateDiffCount(dataSet):
    results = {}
    for data in dataSet:
        if data[-1] not in results:
            results[data[-1]] = 1
        else :
            results[data[-1]] += 1
    return results

def splitDataSet(rows, value, column):
    set1 = []
    set2 = []
    #for int or float type
    if (isinstance(value, int) or isinstance(value, float)):
        for row in rows:
            if (row[column] >= value):
                set1.append(row)
            else:
                set2.append(row)
    #for string type
    else:
        for row in rows:
            if (row[column] == value):
                set1.append(row)
            else:
                set2.append(row)
    return set1, set2

def entropy(rows):
    results = calculateDiffCount(rows)
    entroP = 0.0
    for i in results:
        p = float(results[i]) / len(rows)
        entroP -= p * log(p, 2)
    return entroP

def gini(rows):
    #cal the gini
    results = calculateDiffCount(rows)
    imp = 0.0
    for i in results:
        imp += float(results[i]) / len(rows) * float(results[i]) / len(rows)
    return 1 - imp

def maxminScalar(dataSet):
    for i in range(len(dataSet[0]) - 1):
        temp = [a[i] for a in dataSet]
        maxNumber = max(temp)
        minNumber = min(temp)
        #standardize the dataSet
        for j in range(len(dataSet)):
            denominator = maxNumber - minNumber
            dataSet[j][i] = (dataSet[j][i] - minNumber) / denominator

def classify(testSet, tree):
    if tree.results != None: #LeafNode
        return tree.results
    else: 
        v = testSet[tree.col]
        branch = None
        if isinstance(v, float) or isinstance(v, int):
            if v >= tree.value: 
                branch = tree.trueBranch
            else:
                branch = tree.falseBranch
        else:
            if v == tree.value:
                branch = tree.trueBranch
            else:
                branch = tree.falseBranch
    return classify(testSet, branch)

def accuracy(testSet, testLabels, tree):
    cnt = 0
    for i in range(len(testSet)):
        res = classify(testSet[i], tree)
    # print testSet[i]
        print res.keys()[0]
        if (res.keys()[0] == testLabels[i]):
            cnt += 1
    accu = cnt / len(testSet)
    return accu

def recall(testSet, testLabels, tree, dataSetlength=59):
    cnt = 0
    for i in range(len(testSet)):
        res = classify(testSet[i], tree)
        if (res.keys()[0] == testLabels[i]):
            cnt += 1
    rec = cnt / dataSetlength
    return rec

def fValue(testSet, testLabels, tree, dataSetLength=59):
    accu = accuracy(testSet, testLabels, tree)
    rec  = recall(testSet, testLabels, tree, dataSetLength)
    if (accu + rec) == 0:
        print 'bad DC!'
        return 0 
    F    = (accu * rec * 2) / (accu + rec)
    return F


