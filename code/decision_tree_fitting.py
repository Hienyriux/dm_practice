#拟合决策树
from sklearn import tree
from sklearn.externals import joblib
import numpy as np
import csv

with open('statistic_train.csv', 'r') as f:
	f_csv = csv.reader(f)
	train_data = [cur[1 : ] for cur in f_csv]
	train_data = train_data[1 : ]
	train_label = [int(cur[-1]) for cur in train_data]
	train_data = [list(map(float, cur[ : -1])) for cur in train_data]
	train_data = np.asarray(train_data)

train_label = np.asarray(train_label)

mytree = tree.DecisionTreeClassifier()
mytree = mytree.fit(train_data, train_label)
joblib.dump(mytree, 'tree.model')