# -*- coding: utf-8 -*-

import jieba
import codecs
import jieba.posseg as pseg

#这个文件是参考了网上的示例，可以导出图像数据的，当然要用三方软件才可以打开相应的文件
#官网https://gephi.org/
#安装后，依次文件-导入表格数据-node.csv 和 edge.csv，最后都要选 导入到当前已存在的项目里
#有可能还需要在图像下方选 显示标签，修改标签字体和颜色，否则看不见标签内容

novel_file = '平凡的世界.txt'
family_names_file = '百家姓.txt'
names = {}			# 姓名字典
relationships = {}	# 关系字典
lineNames = []		# 每段内人物关系

# count names
# jieba.load_userdict("dict.txt")		# 加载字典
with codecs.open(novel_file, "r", "utf-8") as f:
	for line in f.readlines():
		poss = pseg.cut(line)		# 分词并返回该词词性
		lineNames.append([])		# 为新读入的一段添加人物名称列表
		for w in poss:
			if w.flag != "nr" or len(w.word) < 2:
				continue			# 当分词长度小于2或该词词性不为nr时认为该词不为人名
			lineNames[-1].append(w.word)		# 为当前段的环境增加一个人物
			if names.get(w.word) is None:
				names[w.word] = 0
				relationships[w.word] = {}
			names[w.word] += 1					# 该人物出现次数加 1

# explore relationships
for line in lineNames:					# 对于每一段
	for name1 in line:
		for name2 in line:				# 每段中的任意两个人
			if name1 == name2:
				continue
			if relationships[name1].get(name2) is None:		# 若两人尚未同时出现则新建项
				relationships[name1][name2]= 1
			else:
				relationships[name1][name2] = relationships[name1][name2]+ 1		# 两人共同出现次数加 1

# output
with codecs.open("node.csv", "w", "utf-8") as f:
	f.write("Id Label Weight\r\n")
	for name, times in names.items():
		if times > 20: #数字越大，导出的节点越少
			f.write(name + " " + name + " " + str(times) + "\r\n")

with codecs.open("edge.csv", "w", "utf-8") as f:
	f.write("Source Target Weight\r\n")
	for name, edges in relationships.items():
		for v, w in edges.items():
			if w > 50: #数字越大，导出的边越少
				f.write(name + " " + v + " " + str(w) + "\r\n")