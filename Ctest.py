# -*- coding: utf-8 -*-
# Author : tyty
# Date   : 2018-6-1
import numpy as np
from collections import defaultdict
import pandas as pd

class DecisionTree:
    def __init__(self, value=None, trueBranch=None, falseBranch=None, results=None, col=-1, summary=None, data=None):
        self.value = value               #Record the value in TreeNode
        self.trueBranch = trueBranch     #True  branch in TreeNode
        self.falseBranch = falseBranch   #False branch in TreeNode
        self.results = results           #LeafNode results  - feature nums 
        self.col = col                   #Record the feature columns
        self.summary = summary           #Every node's summary info
        self.data = data                 #LeafNode data

def createDataSet():
    fruit = pd.read_table('./fruit.txt')
    fruit.head()
    #print fruit.shape
    labels = ['mass', 'width', 'height', 'color_score', 'fruit_label']
    train_data = fruit[labels]
    numpy_train_data = np.array(train_data)
    dataSet = numpy_train_data.tolist()
    return dataSet, labels

def maxminScalar(dataSet):
    for i in range(len(dataSet[0]) - 1):
        temp = [a[i] for a in dataSet]
        maxNumber = max(temp)
        minNumber = min(temp)
        #standardize the dataSet
        for j in range(len(dataSet)):
            denominator = maxNumber - minNumber
            dataSet[j][i] = (dataSet[j][i] - minNumber) / denominator

def calculateDiffCount(dataSet):
    results = {}
    for data in dataSet:
        if data[-1] not in results:
            results[data[-1]] = 1
        else :
            results[data[-1]] += 1
    return results

def gini(rows):
    results = calculateDiffCount(rows)
    imp = 0.0
    for i in results:
        imp += float(results[i]) / len(rows) * float(results[i]) / len(rows)
    return 1 - imp


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

def buildDecisionTree(rows, evaluationFunc = gini):
    currentGain = evaluationFunc(rows)
    rows_length = len(rows)
    #print rows_length
    best_gain = 0.0
    best_value = None
    best_set = None

    #choos the best gain for the former 4 feature
    for col in range(len(rows[0]) - 1):
        col_value_set = set([x[col] for x in rows])
        #print col_value_set
        for value in col_value_set:
            list1, list2 = splitDataSet(rows, value, col)
            p = float(len(list1)) / rows_length
            gain = currentGain - p * evaluationFunc(list1) - (1-p) * evaluationFunc(list2)
            #print gain
            if gain > best_gain:
                best_gain = gain
                best_value = (col, value)
                best_set = (list1, list2)
    dcY = {'impurity' : '%.3f' %currentGain, 'samples':'%d' % rows_length}

    #stop or not stop
    if best_gain > 0:
        trueBranch = buildDecisionTree(best_set[0], evaluationFunc)
        falseBranch = buildDecisionTree(best_set[1], evaluationFunc)
        return DecisionTree(col=best_value[0], value=best_value[1], trueBranch=trueBranch, falseBranch=falseBranch, summary=dcY)
    else:
        return DecisionTree(results=calculateDiffCount(rows), summary=dcY, data=rows)

def pruneTree(tree, minGain, evaluationFunc=gini, notify=False):
    """Prunes the obtained tree according to the minimal gain (entropy or gini )"""
    if (tree.trueBranch.results == None):
        pruneTree(tree.trueBranch, minGain, evaluationFunc, notify)
    if (tree.falseBranch.results == None):
        pruneTree(tree.falseBranch, minGain, evaluationFunc, notify)
    
    #merge leafNode
    if tree.trueBranch.results != None and tree.falseBranch.results != None:
        tB, fB = [], []
        for i, j in tree.trueBranch.results.items():

            tB = [[i]] * j
        for i, j in tree.falseBranch.results.items():

            fB = [[i]] * j
        p = float(len(tB)) / len(tB + fB)
        delta = evaluationFunc(tB + fB) - p * evaluationFunc(tB) - (1 - p) * evaluationFunc(fB)
        if delta < minGain:
            if notify:
                print 'A branch was pruned : gain = %f' % delta
            tree.trueBranch, tree.falseBranch = None, None
            tree.results = calculateDiffCount(tB + fB)


def classify(observations, tree):
    if tree.results != None: #LeafNode
        return tree.results
    else: 
        v = observations[tree.col]
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
    return classify(observations, branch)






dataSet, labels = createDataSet()
maxminScalar(dataSet)

Tree = buildDecisionTree(dataSet)

pruneTree(Tree, 0.4, notify=True)

print dataSet[52][:-1]

print (classify(dataSet[53][:-1], Tree))


