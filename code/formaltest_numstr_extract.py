#提取正式测试集数字/字符串
import os

#变量类型
var_types = ['long long', 'long', 'double', 'int', 'short', 'char', \
			 'unsigned', 'void']
var_types_set = {'long', 'double', 'int', 'short', 'char', 'unsigned', 'void'}
content = ''
extract_data = ''
test_dir = os.listdir('../nju-introdm20/test/test/')

for fname in test_dir:
	fpath = '../nju-introdm20/test/test/' + fname
	
	print(fpath)
	with open(fpath, 'r') as f:
		content = f.read()
	content_len = len(content)
	
	mystr_dict = dict()
	mynum_dict = dict()
	#立即字符串
	idx = 0
	while True:
		idx = content.find('\"', idx)
		if idx == -1:
			break
		#假设不会出现转义双引号
		right_idx = content.find('\"', idx + 1)
		cur_str = content[idx + 1 : right_idx]
		cur_str = cur_str.replace('\\n', '')
		cur_str = cur_str.replace('\\t', '')
		#cur_str = cur_str.replace(' ', '')
		#如果是0或1, 加入到数字字典中
		if cur_str == '0' or cur_str == '1':
			res = mynum_dict.get(cur_str)
			if res == None:
				mynum_dict[cur_str] = 1
			else:
				mynum_dict[cur_str] = res + 1
		#如果是其他数字, 放掉
		elif cur_str != '':
			j = 0
			while j < len(cur_str) and \
			(cur_str[j].isdigit() or cur_str[j] == '.'):
				j += 1
			if j != len(cur_str):
				res = mystr_dict.get(cur_str)
				if res == None:
					mystr_dict[cur_str] = 1
				else:
					mystr_dict[cur_str] = res + 1
		idx = right_idx + 1
	
	#立即字符
	idx = 0
	while True:
		idx = content.find('\'', idx)
		if idx == -1:
			break
		if content[idx + 1] == '\\':
			idx += 4
			continue
		cur_char = content[idx + 1]
		#cur_char = cur_char.replace(' ', '')
		#如果是0或1, 加入到数字字典中
		if cur_char == '0' or cur_char == '1':
			res = mynum_dict.get(cur_char)
			if res == None:
				mynum_dict[cur_char] = 1
			else:
				mynum_dict[cur_char] = res + 1
		elif cur_char != '' and not cur_char.isdigit():
			res = mystr_dict.get(cur_char)
			if res == None:
				mystr_dict[cur_char] = 1
			else:
				mystr_dict[cur_char] = res + 1
		idx += 3
	
	#除0和1外的立即数
	idx = 0
	while True:
		while idx < content_len and (not content[idx].isdigit()):
			idx += 1
		if idx == content_len:
			break
		if content[idx - 1].isalnum() or content[idx - 1] == '_':
			right_idx = idx + 1
			while content[right_idx].isdigit() or content[right_idx] == '.':
				right_idx += 1
			idx = right_idx + 1
			continue
		if (content[idx] == '0' or content[idx] == '1') and \
		(not (content[idx + 1].isdigit() or content[idx + 1] == '.')):
			idx += 2
			continue
		right_idx = idx + 1
		while content[right_idx].isdigit() or content[right_idx] == '.':
			right_idx += 1
		cur_num = content[idx : right_idx]
		res = mynum_dict.get(cur_num)
		if res == None:
			mynum_dict[cur_num] = 1
		else:
			mynum_dict[cur_num] = res + 1
		idx = right_idx + 1
	
	#变量
	myvar_set = set()
	myvar_list = []
	var_types_cnt = [0] * len(var_types)
	for j in range(len(var_types)):
		idx = 0
		type_len = len(var_types[j])
		while True:
			idx = content.find(var_types[j], idx)	
			if idx == -1:
				break
			if content[idx + type_len] != ' ':
				idx += type_len
				continue
			#找换行符
			nln_idx = content.find('\n', idx + type_len + 1)
			#按逗号分隔
			dec_parts = content[idx + type_len + 1 : nln_idx].split(',');
			#去除首尾空格和tab
			for k in range(len(dec_parts)):
				dec_parts[k] = dec_parts[k].strip()
			#滤去空串
			dec_parts = list(filter(None, dec_parts))
			#列表为空, 立刻转到下一行搜索
			if len(dec_parts) == 0:
				idx = nln_idx + 1
				continue
			#判断该行是否为函数声明, 检查最后一部分是否满足声明格式
			last_part = dec_parts[-1]
			#去除所有空格和tab
			last_part = last_part.replace(' ', '')
			last_part = last_part.replace('\t', '')
			last_len = len(last_part)
			is_dec = False
			#至少有一个字符, 否则上一步就被滤去
			if (last_part[-1] == ')') or (last_len > 1 and \
			last_part[-1] == '}' and last_part[-2] == ')'):
				dec_parts = dec_parts[0 : 1]	
				is_dec = True
			#替换掉空格和tab
			#提取第一个可视为变量的子串
			#如果该行是函数声明, 抛弃剩余部分
			for cur in dec_parts:
				if cur[0].isdigit():
					continue
				if cur[0] == '*':
					cur = cur[1 :]
				is_found = False
				for k in range(len(cur)):
					if not (cur[k].isalnum() or cur[k] == '_'):
						is_found = True
						break
				if not is_found:
					k += 1
				if k > 0:
					cur = cur[: k]
					if not (cur in var_types_set) and cur != 'main':
						var_types_cnt[j] += 1
						if not (cur + str(j) in myvar_set):
							myvar_set.add(cur + str(j))
							myvar_list.append([cur, j, 0])
			if is_dec:
				idx += type_len + 1
			else:
				idx = nln_idx + 1
	for j in range(len(myvar_list)):
		myvar_list[j][2] = content.count(myvar_list[j][0])
	
	extract_data += '\1\n' + fname + '\n'
	for k in mystr_dict.keys():
		extract_data += k + '\n'
	for k in mynum_dict.keys():
		extract_data += k + '\n'

with open('extract.txt', 'w') as f:
	f.write(extract_data)