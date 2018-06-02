# -*- coding: utf-8 -*-
# Author : tyty
# Date   : 2018-5-25
# Env    : python2.6

from __future__ import division
import DecisionPlot as DP
import tools as tl
import pydotplus

class DecisionTree:
    def __init__(self, value=None, trueBranch=None, falseBranch=None, results=None, col=-1, summary=None, data=None):
        self.value = value               #Record the value in TreeNode
        self.trueBranch = trueBranch     #True  branch in TreeNode
        self.falseBranch = falseBranch   #False branch in TreeNode
        self.results = results           #LeafNode results  - feature nums 
        self.col = col                   #Record the feature columns
        self.summary = summary           #Every Node's summary info
        self.data = data                 #LeafNode data

def buildDecisionTree(rows, evaluationFunc = None):
    currentGain = evaluationFunc(rows)
    rows_length = len(rows)
    #print rows_length
    best_gain = 0.0
    best_value = None
    best_set = None

    #choose the best gain for the former 4 feature
    for col in range(len(rows[0]) - 1):
        col_value_set = set([x[col] for x in rows])
        #print col_value_set
        for value in col_value_set:
            list1, list2 = tl.splitDataSet(rows, value, col)
            p = float(len(list1)) / rows_length
            gain = currentGain - p * evaluationFunc(list1) - (1-p) * evaluationFunc(list2)
            #print gain
            if gain > best_gain:
                best_gain = gain
                best_value = (col, value)
                best_set = (list1, list2)
    dcY = {'impurity' : '%.4f' %currentGain, 'samples': '%d' % rows_length}
    #stop or not stop
    if best_gain > 0:
        trueBranch = buildDecisionTree(best_set[0], evaluationFunc)
        falseBranch = buildDecisionTree(best_set[1], evaluationFunc)
        return DecisionTree(col=best_value[0], value=best_value[1], \
         trueBranch=trueBranch, falseBranch=falseBranch, summary=dcY)
    else:
        return DecisionTree(results=tl.calculateDiffCount(rows), \
            summary=dcY, data=rows)

def pruneTree(tree, minGain, evaluationFunc=None):
    """Prunes the obtained tree according to the minimal gain (entropy or gini )"""
    if (tree.trueBranch.results == None):
        pruneTree(tree.trueBranch, minGain, evaluationFunc)
    if (tree.falseBranch.results == None):
        pruneTree(tree.falseBranch, minGain, evaluationFunc)
    
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
            tree.trueBranch, tree.falseBranch = None, None
            tree.results = tl.calculateDiffCount(tB + fB)

#def classify(testSet, tree):
#    if tree.results != None: #LeafNode
#        return tree.results
#    else: 
#        v = testSet[tree.col]
#        branch = None
#        if isinstance(v, float) or isinstance(v, int):
#            if v >= tree.value: 
#                branch = tree.trueBranch
#            else:
#                branch = tree.falseBranch
#        else:
#            if v == tree.value:
#                branch = tree.trueBranch
#            else:
#                branch = tree.falseBranch
#    return classify(testSet, branch)


trainSet, labels, testSet, testLabels = DP.createDataSet()
tl.maxminScalar(trainSet)
tl.maxminScalar(testSet)

Tree = buildDecisionTree(trainSet, evaluationFunc=tl.gini)
pruneTree(Tree, 0.4, evaluationFunc=tl.gini)

#res = DP.plot(Tree)
#dot_data = DP.dotgraph(Tree)
#graph = pydotplus.graph_from_dot_data(dot_data)
#graph.write_png("fruit.png")

#test Step
accu = tl.accuracy(testSet, testLabels, Tree)
rec  = tl.recall(testSet, testLabels, Tree, len(trainSet) + len(testSet))
F    = tl.fValue(testSet, testLabels, Tree, len(trainSet) + len(testSet))
# print (trainSet[52][:-1])

# print (classify(trainSet[53][:-1], Tree))

