#coding=utf-8
import json
import sqlite3
#在sqlite中读取word在一个词语首部的概率
def getStartPro(word):
	return 1;
#在sqlite中读取word在对应pinYin的发射概率
def getEmission(word):
	return 1;
#在sqlite中读取nextWord在preWord之后的概率
def getTransition(preWord,nextWord):
	return 1;


#连接数据库
myConnect = sqlite3.connect("D:/src/test.db");
myCursor = myConnect.cursor();

#拼音汉字映射文件
covertPinFile = open('py2hz.json');
covertPin = json.load(covertPinFile);

while 1:
	#在pinYin中存输入拼音的list，wordLists对应拼音的汉字字符串
	#用户使用space来分割拼音输入
	pinYin = raw_input("type pinYin using space to separate = ");
	#将输入存为list
	pinYin = pinYin.split(" ");
	wordLists=[];
	index=[];
	probability=[];
	#拼音对应汉字的字符串
	for onePin in pinYin:
		wordLists.append(covertPin[onePin]);
	#对probability list做初始化
	oneList = wordLists[0];
	tmpPro = [];
	for i1 in range(0,len(oneList)):
		#概率的对数，使用加法
		tmpPro.append(getStartPro(oneList[i1]) + getEmission(oneList[i1]));
	probability.append(tmpPro);
	#对之后的节点做遍历
	for i1 in range(1,len(wordLists)):
		tmpIndex = [];
		tmpPro = [];
		oneList = wordLists[i1];
		preList = wordLists[i1-1];
		prePro = probability[i1-1];
		#print len(oneList)
		#对当前节点的每个汉字做遍历
		for i2 in range(0,len(oneList)):
			maxPro = 0;
			maxIndex = -1;
			#对前一个节点的每个汉字做概率的遍历
			for i3 in range(0,len(preList)):
				temp = getTransition(preList[i3],oneList[i2])+prePro[i3];
				if maxPro<temp:
					maxPro = temp;
					maxIndex = i3;
			#加上该字的发射概率对数得到该字的概率
			tmpIndex.append(maxIndex);
			tmpPro.append(maxPro+getEmission(oneList[i2]));
		index.append(tmpIndex);
		probability.append(tmpPro)
	
	#找最后一个节点的概率最大值，然后倒退
	length = len(wordLists)
	max = 0
	tmp5 = 0
	oneList = wordLists[length-1]
	#找最后一行的最大值
	for i1 in range(0,len(oneList)):
		tmp = probability[length-1][i1]
		if max<tmp:
			max = tmp
			tmp5 = i1

	result = [0]*length
	result[length-1] = wordLists[length-1][tmp5]

	for i1 in range(0,length-1):
		result[length-i1-2] = wordLists[length-i1-2][tmp5]
		tmp5 = index[length-i1-2][tmp5]
		
	for tmp in result:
		print tmp
