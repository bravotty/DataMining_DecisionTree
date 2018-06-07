# DataMining_DecisionTree

[![auc][aucsvg]][auc] [![License][licensesvg]][license]

[aucsvg]: https://img.shields.io/badge/tyty-DecisionTree-orange.svg
[auc]: https://github.com/bravotty/DataMining_DecisionTree

[licensesvg]: https://img.shields.io/badge/License-MIT-blue.svg
[license]: https://github.com/bravotty/DataMining_DecisionTree/blob/master/LICENSE

A python implementation of Decision Tree
Env       : Python 2.6

## Usage     : 

Windows     : 
```lisp
	1. Anaconda command  : activate "python2.x env"
	2.                     pip/conda install numpy, pydotplus, pandas
	3. Download GraphViz : https://graphviz.gitlab.io/_pages/Download/Download_windows.html
	4.                     add the GraphViz to your PATH env
```
Mac & Linux :
```lisp
	1.pip install numpy, pydotplus, pandas
	Linux 2.sudo apt-get install graphviz
	Mac   2.brew install graphviz
```
Run .py
```lisp
    python DecisionTree
```


## Defination :

DecisionTree Node
```lisp
class DecisionTree:
    def __init__(self, value=None, trueBranch=None, falseBranch=None, results=None, col=-1, summary=None, data=None):
        self.value = value               #Record the value in TreeNode
        self.trueBranch = trueBranch     #True  branch in TreeNode
        self.falseBranch = falseBranch   #False branch in TreeNode
        self.results = results           #LeafNode results  - feature nums 
        self.col = col                   #Record the feature columns
        self.summary = summary           #Every Node's summary info
        self.data = data                 #LeafNode data
```


## Code Flie  :
```lisp
tools.py 
	|--Evaluation Function
	|--
DecisionTree.py
DecisionPlot.py
```

## License

[The MIT License](https://github.com/bravotty/DataMining_DecisionTree/blob/master/LICENSE)
