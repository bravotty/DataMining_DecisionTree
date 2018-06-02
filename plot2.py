# -*- coding: utf-8 -*-
# Author : tyty
# Date   : 2018-6-1
# Env    : python2.6
# test file
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
    #
    trainSet = trainSet.tolist()
    testSet  = testSet.tolist()
    return trainSet, testSet, labelsDict

def trainTestSplit(X,test_size=0.3):
    X_num=X.shape[0]
    train_index=range(X_num)
    test_index=[]
    test_num=int(X_num*test_size)
    for i in range(test_num):
    
        randomIndex=int(np.random.uniform(0,len(train_index)))
        print randomIndex
        print len(train_index)
        test_index.append(train_index[randomIndex])
    
        del train_index[randomIndex] 
        print test_index

    print 'line'
    #train,test的index是抽取的数据集X的序号
    train=X[train_index] 
    test=X[test_index]
    return train,test

def plot(decisionTree):
    """Plots the obtained decision tree. """
    def toString(decisionTree, indent=''):
        if decisionTree.results != None:  # leaf node
            return str(decisionTree.results)
        else:
            szCol = 'Column %s' % decisionTree.col
            if szCol in labels:
                szCol = labels[szCol]
            if isinstance(decisionTree.value, int) or isinstance(decisionTree.value, float):
                decision = '%s >= %s?' % (szCol, decisionTree.value)
            else:
                decision = '%s == %s?' % (szCol, decisionTree.value)
            trueBranch = indent + 'yes -> ' + toString(decisionTree.trueBranch, indent + '\t\t')
            falseBranch = indent + 'no  -> ' + toString(decisionTree.falseBranch, indent + '\t\t')
            return (decision + '\n' + trueBranch + '\n' + falseBranch)

    print(toString(decisionTree))


def dotgraph(decisionTree):
    global labels
    dcNodes = defaultdict(list)
    """Plots the obtained decision tree. """
    def toString(iSplit, decisionTree, bBranch, szParent = "null", indent=''):
        if decisionTree.results != None:  # leaf node
            lsY = []
            for szX, n in decisionTree.results.items():
                    lsY.append('%s:%d' % (szX, n))
            dcY = {"name": "%s" % ', '.join(lsY), "parent" : szParent}
            dcSummary = decisionTree.summary
            dcNodes[iSplit].append(['leaf', dcY['name'], szParent, bBranch, dcSummary['impurity'],
                                    dcSummary['samples']])
            return dcY
        else:
            szCol = 'Column %s' % decisionTree.col
            if szCol in labels:
                    szCol = labels[szCol]
            if isinstance(decisionTree.value, int) or isinstance(decisionTree.value, float):
                    decision = '%s >= %s' % (szCol, decisionTree.value)
            else:
                    decision = '%s == %s' % (szCol, decisionTree.value)
            trueBranch = toString(iSplit+1, decisionTree.trueBranch, True, decision, indent + '\t\t')
            falseBranch = toString(iSplit+1, decisionTree.falseBranch, False, decision, indent + '\t\t')
            dcSummary = decisionTree.summary
            dcNodes[iSplit].append([iSplit+1, decision, szParent, bBranch, dcSummary['impurity'],
                                    dcSummary['samples']])
            return

    toString(0, decisionTree, None)
    lsDot = ['digraph Tree {',
                'node [shape=box, style="filled, rounded", color="black", fontname=helvetica] ;',
                'edge [fontname=helvetica] ;'
    ]
    i_node = 0
    dcParent = {}
    for nSplit, lsY in dcNodes.items():
        for lsX in lsY:
            iSplit, decision, szParent, bBranch, szImpurity, szSamples =lsX
            if type(iSplit) == int:
                szSplit = '%d-%s' % (iSplit, decision)
                dcParent[szSplit] = i_node
                lsDot.append('%d [label=<%s<br/>impurity %s<br/>samples %s>, fillcolor="#e5813900"] ;' % (i_node,
                                        decision.replace('>=', '&ge;').replace('?', ''),
                                        szImpurity,
                                        szSamples))
            else:
                lsDot.append('%d [label=<impurity %s<br/>samples %s<br/>class %s>, fillcolor="#e5813900"] ;' % (i_node,
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
                    lsDot.append('%d -> %d [labeldistance=2.5, labelangle=%s, headlabel="%s"] ;' % (p_node,
                                                        i_node, szAngle, szHeadLabel))
                else:
                    lsDot.append('%d -> %d ;' % (p_node, i_node))
            i_node += 1
    lsDot.append('}')
    dot_data = '\n'.join(lsDot)
    return dot_data

trainSet, testSet, labels = createDataSet()
# d, t = trainTestSplit(dataSet)









