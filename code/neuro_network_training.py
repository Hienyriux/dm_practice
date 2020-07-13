#训练神经网络
import tensorflow as tf
import numpy as np
import csv

with open('statistic_train.csv', 'r') as f:
	f_csv = csv.reader(f)
	train_data = [cur[1 : ] for cur in f_csv]
	train_data = train_data[1 : ]
	train_label_raw = [cur[-1] for cur in train_data]
	train_data = [list(map(float, cur[ : -1])) for cur in train_data]
	train_data = np.asarray(train_data)

train_label = np.zeros((len(train_data), 83));
for i in range(len(train_data)):
	train_label[i][int(train_label_raw[i])] = 1

x = tf.placeholder("float", [None, 22])
W = tf.Variable(tf.zeros([22, 83]), name = 'W')
b = tf.Variable(tf.zeros([83]), name = 'b')
y = tf.nn.softmax(tf.matmul(x, W) + b)
y_ = tf.placeholder("float", [None, 83])

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels = y_, logits = y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

saver = tf.train.Saver()

#init = tf.global_variables_initializer()
sess = tf.Session()
#sess.run(init)

saver.restore(sess, 'mymodel/mymodel.ckpt')

#已训练20 * 2000 = 40000次
for i in range(2000):
	sess.run(train_step, feed_dict = {x: train_data, y_: train_label})
	if i % 50 == 0:
		print(sess.run(cross_entropy, feed_dict = {x: train_data, y_: train_label}))

saver.save(sess, 'mymodel/mymodel.ckpt')