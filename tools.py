# -*- coding: utf-8 -*-
# Author : tyty
# Date   : 2018-6-2
# Env    : python2.6

from __future__ import division
from math import log

#计算数据集中的最后一列类别个数
#return : {0:13, 1: 12, 2:3, 3:20}
def calculateDiffCount(dataSet):
    results = {}
    for data in dataSet:
        if data[-1] not in results:
            results[data[-1]] = 1
        else :
            results[data[-1]] += 1
    return results

#分割数据集
#return : set1=[value > given value] set2=[others]
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

#entropy function
def entropy(rows):
    results = calculateDiffCount(rows)
    entroP = 0.0
    for i in results:
        p = float(results[i]) / len(rows)
        entroP -= p * log(p, 2)
    return entroP

#gini function
def gini(rows):
    #cal the gini
    results = calculateDiffCount(rows)
    imp = 0.0
    for i in results:
        #需转Float类型
        imp += float(results[i]) / len(rows) * float(results[i]) / len(rows)
    return 1 - imp

#数据集最大最小规约
def maxminScalar(dataSet):
    for i in range(len(dataSet[0]) - 1):
        temp = [a[i] for a in dataSet]
        maxNumber = max(temp)
        minNumber = min(temp)
        #standardize the dataSet
        for j in range(len(dataSet)):
            denominator = maxNumber - minNumber
            dataSet[j][i] = (dataSet[j][i] - minNumber) / denominator

#决策树剪枝函数
def pruneTree(tree, minGain, evaluationFunc=None):
    #Not leafNode - 递归
    if (tree.trueBranch.results == None):
        pruneTree(tree.trueBranch, minGain, evaluationFunc)
    if (tree.falseBranch.results == None):
        pruneTree(tree.falseBranch, minGain, evaluationFunc)
    #merge the leafNode
    if tree.trueBranch.results != None and tree.falseBranch.results != None:
        tB = []
        fB = []
        for i, j in tree.trueBranch.results.items():
            tB = [[i]] * j
        for i, j in tree.falseBranch.results.items():
            fB = [[i]] * j
        #true branch P
        p = float(len(tB)) / len(tB + fB)
        #Gini gain or entropy gain
        delta = evaluationFunc(tB + fB) - p * evaluationFunc(tB) - (1 - p) * evaluationFunc(fB)
        if delta < minGain:
            #merge
            tree.trueBranch, tree.falseBranch = None, None
            tree.results = calculateDiffCount(tB + fB)

#测试集分类函数
def classify(testSet, tree):
    if tree.results != None: #LeafNode
        return tree.results
    else: 
        v = testSet[tree.col]
        branch = None
        #for int and float data
        if isinstance(v, float) or isinstance(v, int):
            if v >= tree.value: 
                branch = tree.trueBranch
            else:
                branch = tree.falseBranch
        #for the string type
        else:
            if v == tree.value:
                branch = tree.trueBranch
            else:
                branch = tree.falseBranch
    return classify(testSet, branch)

#计算准确率函数
def accuracy(testSet, testLabels, tree):
    cnt = 0
    for i in range(len(testSet)):
        res = classify(testSet[i], tree)
        if (res.keys()[0] == testLabels[i]):
            cnt += 1
    accu = cnt / len(testSet)
    return accu

#计算召回率函数
def recall(testSet, testLabels, tree, dataSetlength=59):
    cnt = 0
    for i in range(len(testSet)):
        res = classify(testSet[i], tree)
        if (res.keys()[0] == testLabels[i]):
            cnt += 1
    rec = cnt / dataSetlength
    return rec
#计算F值函数
def fValue(testSet, testLabels, tree, dataSetLength=59):
    accu = accuracy(testSet, testLabels, tree)
    rec  = recall(testSet, testLabels, tree, dataSetLength)
    if (accu + rec) == 0:
        print 'Bad DecisionTree Construction !'
        return 0 
    F    = (accu * rec * 2) / (accu + rec)
    return F


