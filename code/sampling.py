#采样产生小型测试集
import os
import csv
import random

train_dir = os.listdir('../nju-introdm20/train/train/')

fname_list = []
for dir_name in train_dir:
	file_list = os.listdir('../nju-introdm20/train/train/' + dir_name)
	random.shuffle(file_list)
	for i in range(10):
		fname_list.append(file_list[i][ : -4])

file_pair = []
#415
for i in range(83):
	for j in range(5):
		file_pair.append([fname_list[10 * i + 2 * j] + '_' + \
				   fname_list[10 * i + 2 * j + 1], '1', str(i), str(i)])

# a = 830 - 10 * i, i = 1, 2, 3, ..., n
# S = 820 * n - 5 * n * (n - 1) = -5 * (n^2) + 825 * n
# target = 415 * 19 = 7885, S_10 = 8250 - 5000 = 7750
for i in range(10):
	for j in range(82 - i):
		for k in range(10):
			file_pair.append([fname_list[10 * j + k] + '_' + \
					fname_list[10 * (j + i + 1) + k], '0', str(j), \
					str(j + i + 1)])

random.shuffle(file_pair)

with open('fpair_list.csv', 'w', newline = '') as f:
	f_csv = csv.writer(f)
	f_csv.writerows(file_pair)
