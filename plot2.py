# -*- coding: utf-8 -*-
# Author : tyty
# Date   : 2018-6-1
# Env    : python2.6
# test file
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
    #dataSet = numpy_train_data.tolist()
    return numpy_train_data, labelsDict

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

dataSet, labels = createDataSet()
d, t = trainTestSplit(dataSet)









