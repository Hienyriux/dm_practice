#决策树预测正式测试集
import csv
import numpy as np
from sklearn.externals import joblib

fname_list = []
with open('sample_submission.csv', 'r') as f:
	f_csv = csv.reader(f)
	for row in f_csv:
		fname_list.append(row[0].split('_'))
fname_list = fname_list[1 :]

fname_dict = dict()
with open('statistic_formaltest.csv', 'r') as f:
	f_csv = csv.reader(f)
	test_data = [row for row in f_csv]

test_data = test_data[1 : ]
for i in range(len(test_data)):	
	fname_dict[test_data[i][0]] = i
	test_data[i] = list(map(float, test_data[i][1 : ]))
test_data = np.asarray(test_data)

mytree = joblib.load('tree.model')
cidx = mytree.predict(test_data)

out_file = open('result_decision_tree.csv', 'w', newline = '')
f_csv = csv.writer(out_file)
f_csv.writerow(['id1_id2', 'predictions'])

for i in range(len(fname_list)):
	fname1 = fname_list[i][0]
	fname2 = fname_list[i][1]
	idx1 = fname_dict[fname1]
	idx2 = fname_dict[fname2]
	if cidx[idx1] == cidx[idx2]:
		f_csv.writerow([fname1 + '_' + fname2, '1'])
	else:
		f_csv.writerow([fname1 + '_' + fname2, '0'])

out_file.close()