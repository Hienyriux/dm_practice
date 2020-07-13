#决策树预测小型测试集
import csv
import numpy as np
from sklearn.externals import joblib

fname_list = []
label = []
with open('fpair_list.csv', 'r') as f:
	f_csv = csv.reader(f)
	for row in f_csv:
		fname_list.append(row[0].split('_'))
		label.append(row[1])

fname_dict = dict()
with open('statistic_smalltest.csv', 'r') as f:
	f_csv = csv.reader(f)
	test_data = [row for row in f_csv]

test_data = test_data[1 : ]
for i in range(len(test_data)):	
	fname_dict[test_data[i][0]] = i
	test_data[i] = list(map(float, test_data[i][1 : ]))
test_data = np.asarray(test_data)

mytree = joblib.load('tree.model')
cidx = mytree.predict(test_data)

tp = 0
fp = 0
tn = 0
fn = 0

for i in range(len(fname_list)):
	fname1 = fname_list[i][0]
	fname2 = fname_list[i][1]
	idx1 = fname_dict[fname1]
	idx2 = fname_dict[fname2]
	if cidx[idx1] == cidx[idx2]:
		if label[i] == '1':
			tp += 1
		else:
			fp += 1
	else:
		if label[i] == '1':
			fn += 1
		else:
			tn += 1

prec = tp / (tp + fp)
recall = tp / (tp + fn)
f1score = (2 * prec * recall) / (prec + recall)

acc = (tp + tn) / (tp + tn + fp + fn)

print('tp = ' + str(tp) + '\nfp = ' + str(fp) + \
	  '\ntn = ' + str(tn) + '\nfn = ' + str(fn) + \
	  '\nprec = ' + str(prec) + '\nrecall = ' + str(recall) + \
	  '\nf1-score = ' + str(f1score) + \
	  '\nacc = ' + str(acc))
