# -*- coding: utf-8 -*-
# Author : tyty
# Date   : 2018-6-1
# Env    : python2.6

from __future__ import division
import numpy as np
import pandas as pd
from collections import defaultdict

def createDataSet(splitSize=0.2):
    fruit = pd.read_table('./fruit.txt')
    #convert pd.DataFrame -> ndarray -> list 
    fruit.head()
    #print fruit.shape
    labelsDict = {}
    labels = ['mass', 'width', 'height', 'color_score', 'fruit_label']
    #process the dataset to key : "Column 1:" value : "labels"
    for i in range(len(labels)):
        colKey = 'Column %d' % i
        labelsDict[colKey] = labels[i]
    trainData = fruit[labels]
    numpyTrainData = np.array(trainData)
    # dataSet = numpy_train_data.tolist()
    #list - dataSet
    recordNums = numpyTrainData.shape[0]
    trainDataIndex = range(recordNums)
    #train_data_index = [1, ..., 59]
    testDataIndex = []
    testNumber = int(recordNums * splitSize)
    for i in range(testNumber):
    	#choose test_number test e.g.s
    	randomNum = int(np.random.uniform(0, len(trainDataIndex)))
    	testDataIndex.append(trainDataIndex[randomNum])
    	del trainDataIndex[randomNum]
    trainSet = numpyTrainData[trainDataIndex]
    testSet  = numpyTrainData[testDataIndex]
    trainSet = trainSet.tolist()
    testSet  = testSet.tolist()

    testlabel = [a[-1] for a in testSet]
    testSet   = [a[:-1] for a in testSet]
    #print testSet
    #print testlabel
    return trainSet, labelsDict, testSet, testlabel

trainSet, labels, testSet, testlabels = createDataSet()

def plot(tree):
	#Nested
    def toString(tree, indent=''):
        if tree.results != None:  
        # leaf
            return str(tree.results)
        else:
            ColKey = 'Column %s' % tree.col
            if ColKey in labels:
                ColKey = labels[ColKey]
            #for nums >=
            if isinstance(tree.value, int) or isinstance(tree.value, float):
                decision = '%s >= %s?' % (ColKey, tree.value)
            else:
            #for string ==
                decision = '%s == %s?' % (ColKey, tree.value)
            #true branch choice    
            trueBranch = indent + 'yes -> ' + toString(tree.trueBranch, indent + '\t\t')
            falseBranch = indent + 'no -> ' + toString(tree.falseBranch, indent + '\t\t')
            return (decision + '\n' + trueBranch + '\n' + falseBranch)
    print(toString(tree))

def dotgraph(tree):
	#global defination of labels
    global labels
    dcNodes = defaultdict(list)

    def toString(split, tree, bBranch, szParent = "null", indent=''):
        if tree.results != None:  
        # leaf node
            lsY = []
            for szX, n in tree.results.items():
                    lsY.append('%s:%d' % (szX, n))
            dcY = {"name": "%s" % ', '.join(lsY), "parent" : szParent}
            dcSummary = tree.summary
            #leafNode
            dcNodes[split].append(['leaf', dcY['name'], szParent, bBranch, dcSummary['impurity'],
                                    dcSummary['samples']])
            return dcY
        else:
        	#for the node 
            szCol = 'Column %s' % tree.col
            if szCol in labels:
                    szCol = labels[szCol]
            if isinstance(tree.value, int) or isinstance(tree.value, float):
                    decision = '%s >= %s' % (szCol, tree.value)
            else:
                    decision = '%s == %s' % (szCol, tree.value)
            trueBranch = toString(split+1, tree.trueBranch, True, decision, indent + '\t')
            falseBranch = toString(split+1, tree.falseBranch, False, decision, indent + '\t')
            dcSummary = tree.summary
            dcNodes[split].append([split+1, decision, szParent, bBranch, dcSummary['impurity'],
                                    dcSummary['samples']])
            return
    #run
    toString(0, tree, None)
    #initial Graph list
    DOT_graph = ['digraph Tree {',
                'node [shape=box, style="filled, rounded", color="black", fontname=helvetica] ;',
                'edge [fontname=helvetica] ;'
    ]

    initialNode = 0
    dcParent = {}
    for nSplit, lsY in dcNodes.items():
        for lsX in lsY:
            split, decision, szParent, bBranch, szImpurity, szSamples =lsX
            if type(split) == int:
                szSplit = '%d-%s' % (split, decision)
                dcParent[szSplit] = initialNode
                DOT_graph.append('%d [label=<%s<br/>impurity %s<br/>samples %s>, fillcolor="#e5813900"] ;' % (initialNode,
                                        decision.replace('>=', '&ge;').replace('?', ''),
                                        szImpurity,
                                        szSamples))
            else:
                DOT_graph.append('%d [label=<impurity %s<br/>samples %s<br/>class %s>, fillcolor="#e5813900"] ;' % (initialNode,
                                        szImpurity,
                                        szSamples,
                                        decision))
                
            if szParent != 'null':
                if bBranch:
                    szAngle = '45'
                    szHeadLabel = 'True'
                else:
                    szAngle = '-45'
                    szHeadLabel = 'False'
                szSplit = '%d-%s' % (nSplit, szParent)
                p_node = dcParent[szSplit]
                if nSplit == 1:
                    DOT_graph.append('%d -> %d [labeldistance=2.5, labelangle=%s, headlabel="%s"] ;' % (p_node,
                                                        initialNode, szAngle, szHeadLabel))
                else:
                    DOT_graph.append('%d -> %d ;' % (p_node, initialNode))
            initialNode += 1
    DOT_graph.append('}')
    dot_data = '\n'.join(DOT_graph)
    return dot_data



