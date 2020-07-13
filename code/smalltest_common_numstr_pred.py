#公共数字/字符串法预测小型测试集
import csv

fname_list = []
label = []
with open('fpair_list.csv', 'r') as f:
	f_csv = csv.reader(f)
	for row in f_csv:
		fname_list.append(row[0].split('_'))
		label.append(row[1])

with open('mytest.txt', 'r') as f:
	mydata = f.read().split('\1')

mydata = mydata[1 : ]
fname_dict = dict()
for i in range(len(mydata)):
	enter_pos = mydata[i].find('\n', 1)
	fname_dict[mydata[i][1 : enter_pos]] = i 

raw_res = []
for i in range(len(fname_list)):
	#fname1 = 'mytest/' + fname_list[i][0] + '.txt'
	#fname2 = 'mytest/' + fname_list[i][1] + '.txt'
	fname1 = fname_list[i][0] + '.txt'
	fname2 = fname_list[i][1] + '.txt'
	myset1 = set()
	myset2 = set()
	
	idx1 = fname_dict.get(fname1)
	idx2 = fname_dict.get(fname2)
	sections1 = mydata[idx1].split('\n')
	for j in range(2, len(sections1) - 1):
		myset1.add(sections1[j])
	sections2 = mydata[idx2].split('\n')
	for j in range(2, len(sections2) - 1):
		myset2.add(sections2[j])
	
	'''
	with open(fname1, 'r') as f:
		mylines1 = f.readlines()
	for word in mylines1:
		myset1.add(word[ : -1])
	
	with open(fname2, 'r') as f:
		mylines2 = f.readlines()
	for word in mylines2:
		myset2.add(word[:-1])
	'''
	myset3 = myset1.intersection(myset2)
	mylen1 = len(myset1)
	mylen2 = len(myset2)
	mylen3 = len(myset3)
	
	myhit1 = 0
	if mylen1 != 0:
		myhit1 = mylen3 / mylen1
	myhit2 = 0
	if mylen2 != 0:
		myhit2 = mylen3 / mylen2
	min_hit = min(myhit1, myhit2)
	max_hit = max(myhit1, myhit2)
	
	
	last_slash = fname1.rfind('/')
	fname1 = fname1[last_slash + 1 : -4]
	last_slash = fname2.rfind('/')
	fname2 = fname2[last_slash + 1 : -4]
	
	raw_res.append([i, fname1 + '_' + fname2, \
				 mylen1, mylen2, mylen3, min_hit, max_hit])


#0: no, 1: src, 2: len1, 3: len2, 4: len3, 5: min_hit, 6: max_hit
raw_res.sort(key = lambda x : (-x[5], -x[6], -x[4]))
#若要使用max_hit为首要关键字, 取消下行注释
#raw_res.sort(key = lambda x : (-x[6], -x[5], -x[4]))
res = [cur[ : 3] for cur in raw_res]
for i in range(415):
	res[i][2] = 1
for i in range(415, len(res)):
	res[i][2] = 0
res.sort(key = lambda x : (x[0]))
res = [cur[1 : 3] for cur in res]

tp = 0
fp = 0
tn = 0
fn = 0

for i in range(len(res)):
	if res[i][1] == 1 and label[i] == '1':
		tp += 1
	elif res[i][1] == 1 and label[i] == '0':
		fp += 1
	elif res[i][1] == 0 and label[i] == '1':
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
