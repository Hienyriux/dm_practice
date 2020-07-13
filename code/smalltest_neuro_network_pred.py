#神经网络预测小型测试集
import csv
import tensorflow as tf
import numpy as np

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

x = tf.placeholder("float", [None, 22])
W = tf.Variable(tf.zeros([22, 83]), name = 'W')
b = tf.Variable(tf.zeros([83]), name = 'b')
y = tf.nn.softmax(tf.matmul(x, W) + b)
y_ = tf.placeholder("float", [None, 83])

saver = tf.train.Saver()
sess = tf.Session()
saver.restore(sess, 'mymodel/mymodel.ckpt')

res = sess.run(y, feed_dict = {x: test_data})

raw_res = []
for i in range(len(fname_list)):
	fname1 = fname_list[i][0]
	fname2 = fname_list[i][1]
	idx1 = fname_dict[fname1]
	idx2 = fname_dict[fname2]
	mse = sum([(res[idx1][j] - res[idx2][j]) ** 2 for j in range(83)])	
	raw_res.append([i, fname1 + '_' + fname2, mse])

#0: no, 1: src, 2: mse
raw_res.sort(key = lambda x : (x[2]))
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
