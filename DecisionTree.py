# -*- coding: utf-8 -*-
# Author : tyty
# Date   : 2018-5-25
# Env    : python2.6

from __future__ import division
import DecisionPlot as dp
import tools as tl
import pydotplus
import cv2

class DecisionTree(object):
    def __init__(self, value=None, trueBranch=None, falseBranch=None, results=None, col=-1, summary=None):
        self.value = value               #Record the value in TreeNode
        self.trueBranch = trueBranch     #True  branch in TreeNode
        self.falseBranch = falseBranch   #False branch in TreeNode
        self.results = results           #feature num - Dictionary  
        self.col = col                   #Record the feature columns
        self.summary = summary           #Every Node's summary info for graph


#建树函数
def buildDecisionTree(dataSet, evaluationFunc = None):
    currentGain = evaluationFunc(dataSet)
    dataSet_length = len(dataSet)
    #print dataSet_length
    best_gain = 0.0
    best_value = None
    best_set = None
    #choose the best gain for the former 4 feature
    for col in range(len(dataSet[0]) - 1):
        col_value_set = set([x[col] for x in dataSet])
        #print col_value_set
        for value in col_value_set:
            list1, list2 = tl.splitDataSet(dataSet, value, col)
            p = float(len(list1)) / dataSet_length
            #feature gain
            gain = currentGain - p * evaluationFunc(list1) - (1-p) * evaluationFunc(list2)
            #print gain
            if gain > best_gain and len(list1) > 1 and len(list2) > 1:
                best_gain = gain
                best_value = (col, value)
                best_set = (list1, list2)
    dcY = {'impurity' : '%.2f' %currentGain, 'samples': '%d' % dataSet_length}
    #stop or not stop
    if best_gain > 0:
        #set[0] .. [1] : feature col

        trueBranch = buildDecisionTree(best_set[0], evaluationFunc)
        falseBranch = buildDecisionTree(best_set[1], evaluationFunc)
        return DecisionTree(col=best_value[0], value=best_value[1], \
         trueBranch=trueBranch, falseBranch=falseBranch, summary=dcY)
    else:
        #results {1:23} final classification
        return DecisionTree(results=tl.calculateDiffCount(dataSet), \
            summary=dcY)


def DecisionTreeModelMain():
    #根据fruit.txt抽取训练集、测试集、训练集标签、测试集标签
    trainSet, labels, testSet, testLabels = dp.createDataSet()
    #最大最小规约
    #tl.maxminScalar(trainSet)
    #tl.maxminScalar(testSet)

    #以Gini函数建树并剪枝
    Tree = buildDecisionTree(trainSet, evaluationFunc=tl.gini)
    tl.pruneTree(Tree, 0.3, evaluationFunc=tl.gini)


    #绘制决策树图像，并保存为fruit.png
    res = dp.plot(Tree)
    dot_data = dp.dotgraph(Tree)
    graph = pydotplus.graph_from_dot_data(dot_data)
    #报错提示没有graphViz模块，可以选择./DecisionTreeResultPng/中png图像进行显示
    if graph == None or dot_data == None :
        fruitPngBackup = cv2.imread("./DecisionTreeResultPng/fruit7.png")
        cv2.imshow("fruitPngBackup.png", fruitPngBackup)
        cv2.waitKey(4000)
    graph.write_png("fruit.png")

    #读取fruit.png
    #显示fruit.png,设置窗口时间为5秒自动关闭
    fruitPng = cv2.imread("./fruit.png")
    cv2.imshow('fruitPng.png', fruitPng)
    cv2.waitKey(4000)

    #测试 Step
    accu = tl.accuracy(testSet, testLabels, Tree)
    rec  = tl.recall(testSet, testLabels, Tree, len(trainSet) + len(testSet))
    F    = tl.fValue(testSet, testLabels, Tree, len(trainSet) + len(testSet))
    
    #print the acc, rec and F
    print 'DecisionTree Accuracy : ' + str(accu)
    print 'DecisionTree Recall   : ' + str(rec)
    print 'DecisionTree F-value  : ' + str(F)

if __name__ == '__main__':
    #main func start
    DecisionTreeModelMain()
