# -*- coding: utf-8 -*-
# Author : tyty
# Date   : 2018-6-1
# Env    : python2.6
# Based on GraphViz : http://www.graphviz.org/
# Windows      : 
# Method1: pip install pydotplus + download graphviz
#   	   GraphViz Download WebSite : https://graphviz.gitlab.io/_pages/Download/Download_windows.html
# Method2: activate YOUR-ENV + conda install graphviz + pip install graphviz
# Linux & Mac  : pip install pydotplus +  apt-get / brew install graphViz

import numpy as np
import pandas as pd
from collections import defaultdict

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

	def toString(split, tree, branch, parent='null', indent=''):
		if (tree.results != None):
			temp = []
			for i, j in tree.results.items():
				temp.append('%s:%d' % (i, j))
			dcY = {'name' : '%s' % ','.join(temp), 'parent':parent}
			dcSummary = tree.summary
			DNode[split].append(['leaf', dcY['name'], parent, branch, 
				dcSummary['impurity'], dcSummary['samples']])
			return dcY
		else:
			colKey = 'Column %s' % tree.col
			if colKey in labels:
				colKey = labels[colKey]
			if isinstance(tree.value, int) or isinstance(tree.value, float):
				decisionT = '%s >= %s' % (colKey, tree.value)
			else:
				decisionT = '%s == %s' % (colKey, tree.value)
			tB = toString(split + 1, tree.trueBranch, True, decisionT, indent + '\t\t')
			fB = toString(split + 1, tree.falseBranch, False, decisionT, indent + '\t\t')
			dcSummary = tree.summary
			DNode[split].append([split + 1, decisionT, parent, branch, dcSummary['impurity'], dcSummary['samples']])
			return 
	toString(0, tree, None)
<<<<<<< HEAD
	DOT = ['disgraph Tree {',
=======
	DOT = ['digraph Tree {',
>>>>>>> 3bf0cb1812f8a5f13149a0279364a7f154a05a8b
	'node [shape=box, style="filled, rounded", color = "black", fontname=helvetica] ;',
	'edge [fontname=helvetica];']
	initialNode = 0
	DCparent = {}
	for i, j in DNode.items():
		for m in j:
			split, decisionT, parent, branch, impurity, samples = m
			if type(split) == int:
				ZZsplit = '%d-%s' % (split, decisionT)
				DCparent[ZZsplit] = initialNode
				DOT.append('%d [label=<%s<br/>impurity %s<br/>samples %s>, fillcolor="#e5813900"] ;' % \
					(initialNode, decisionT.replace('>=', '&ge;').replace('?', ''),
					impurity, samples))

			else:
				DOT.append('%d [label=<impurity %s<br/>samples %s<br/>class %s>, fillcolor="#e5813900"] ;' % \
					(initialNode, impurity, samples, decisionT))
			if parent != 'null':
				if branch:
					Sangle = '45'
					Slabel = 'True'
				else:
					Sangle = '-45'
					Slabel = 'False'
				ZZsplit = '%d-%s' % (i, parent)
				pNode = DCparent[ZZsplit]
				if i == 1:
					DOT.append('%d -> %d [labeldistance=2.5, labelangle=%s, headlabel="%s"] ;' % (pNode,
                            initialNode, Sangle, Slabel))
				else:
					DOT.append('%d -> %d ;' % (pNode, initialNode))
			initialNode += 1
	DOT.append('}')
	dot_data = '\n'.join(DOT)
	return dot_data

dataSet, labels = createDataSet()










