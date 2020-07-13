# dm_practice
Practice of Nanjing University's Introduction to Data Mining course in 2020 spring  
一个代码查重(代码克隆)识别程序, 用于判断一对代码是否属于同一类  
具体思路请看dm_report.pdf  
原始训练和测试数据在https://www.kaggle.com/c/nju-introdm20  
下面是运行说明:

### 预测sample_submission.csv, 请保证:  
+ sample_submission.csv与formaltest_common_numstr_pred.py在同一目录下
+ extract.txt与formaltest_common_numstr_pred.py在同一目录下
+ 运行formaltest_common_numstr_pred.py
+ 输出文件为result_common_numstr.csv


### 这里还提供了模型生成, 及小规模测试的相关代码:
| PART 1 | | 输入 | 输出 |
| ---- | ---- | ---- | ---- |
| sampling.py | 采样产生小型测试集 | nju-introdm20/train/train/ | fpair_list.csv |
| smalltest_numstr_extract.py | 提取小型测试集数字/字符串 | nju-introdm20/train/train/ | mytest.txt |
| smalltest_attr_extract.py | 提取小型测试集特征向量 | nju-introdm20/train/train/, fpair_list.csv | statistic_smalltest.csv |
| train_attr_extract.py | 提取训练集特征向量 | nju-introdm20/train/train/, fpair_list.csv | statistic_train.csv |

| PART 2 | | 输入 | 输出 |
| ---- | ---- | ---- | ---- |
| formaltest_numstr_extract.py | 提取正式测试集数字/字符串 | nju-introdm20/test/test/ | extract.txt |
| formaltest_attr_extract.py | 提取正式测试集特征向量 | nju-introdm20/test/test/ | statistic_formaltest.csv |

| PART 3 | | 输入 | 输出 |
| ---- | ---- | ---- | ---- |
| neuro_network_training.py | 训练神经网络 | statistic_train.csv, mymodel/ | mymodel/ |
| decision_tree_fitting.py | 拟合决策树 | statistic_train.csv | tree.model |

| PART 4 | | 输入 | 输出 |
| ---- | ---- | ---- | ---- |
| smalltest_common_numstr_pred.py | 公共数字/字符串法预测小型测试集 | fpair_list.csv, mytest.txt | Console输出表现指标 |
| smalltest_neuro_network_pred.py | 神经网络预测小型测试集 | sample_submission.csv, statistic_formaltest.csv, mymodel/ | Console输出表现指标 |
| smalltest_decision_tree_pred.py | 决策树预测小型测试集 | fpair_list.csv, statistic_smalltest.csv, tree.model | Console输出表现指标 |

| PART 5 | | 输入 | 输出 |
| ---- | ---- | ---- | ---- |
| formaltest_common_numstr_pred.py | 公共数字/字符串法预测正式测试集 | sample_submission.csv, extract.txt | result_common_numstr.csv |
| formaltest_neuro_network_pred.py | 神经网络预测正式测试集 | fpair_list.csv, statistic_smalltest.csv, mymodel/ | result_neuro_network.csv |
| formaltest_decision_tree_pred.py | 决策树预测正式测试集 | sample_submission.csv, statistic_formaltest.csv, tree.model | result_decision_tree.csv |

### 运行上述代码前请保证:
+ 你安装了tensorflow, scikit-learn
+ 如果要运行PART 1和PART 2中的代码, 请保证nju-introdm20/与这些代码的***父目录***在同一目录下, 因为代码中的路径是以"../nju-introdm20/"开头的

### 运行指南:
+ 在模型目录models/中我已经提供了必要的文件, 先将models/下所有的文件复制到代码目录下, 再运行PART 4中的代码, 即可观察三种方法在小型测试集上的表现
+ 如果想要观察三种方法在正式测试集上的运行结果, 请运行PART 5中的代码; 注意, 作为对照, 神经网络和决策树预测正式测试集的效果会非常差 
+ 如果想要重新生成模型目录中的文件, 请按顺序运行PART 1和PART 2中的代码; 至于PART 3中的代码, neuro_network_training.py需要读取mymodel/中的内容, 不能直接运行; 可以运行decision_tree_fitting.py重新拟合决策树
+ 由于小型测试集是从训练集中随机采样的, 每次采用的具体数据会有所差异
