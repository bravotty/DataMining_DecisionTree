# -*- coding: utf-8 -*-
# Author : tyty
# Date   : 2018-6-1
# Based on GraphViz : http://www.graphviz.org/
# Windows      : pip install pydotplus
# Linux & Mac  : pip install pydotplus +  install graphViz

import numpy as np
import pandas as pd

def createDataSet():
    fruit = pd.read_table('./fruit.txt')
    #convert pd.DataFrame -> ndarray -> list 
    fruit.head()
    #print fruit.shape
    labelsDict = {}
    labels = ['mass', 'width', 'height', 'color_score', 'fruit_label']
    for i in range(len(labels)):
        colKey = 'Column %d' % i
        labelsDict[colKey] = labels[i]
    train_data = fruit[labels]
    numpy_train_data = np.array(train_data)
    dataSet = numpy_train_data.tolist()
    return dataSet, labelsDict

def plot(tree):
	def toString(tree, indent=''):
		if tree.results != None: #LeafNode
			return str(tree.results)
		else:
			colKey = 'Column %s' % tree.col
			if colKey in labels:
				colKey = labels[colKey]
			if isinstance(tree.value, int) or isinstance(tree.value, float):
				decisionT = '%s >= %s?' % (colKey, tree.value)
			else:
				decisionT = '%s == %s?' % (colKey, tree.value)
			tB = indent + 'True ->' + toString(tree.trueBranch, indent + '\t')
			fB = indent + 'False->' + toString(tree.falseBranch, indent + '\t')
			return (decisionT + '\n' + tB + '\n' + fB)

	print(toString(tree))

def dotgraph(tree):
	global labels
	DNode = defaultdict(list)
	


dataSet, labels = createDataSet()