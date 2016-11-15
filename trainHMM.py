# _*_ coding=utf-8  _*_

"""
authored by JingWei in 2016.11.14

利用
并将训练结果存放在trainedHMM.sqlite数据库中，提供给viterbi算法的同学调用
"""

import sqlite3
import math
import crash_on_ipython
from pypinyin import pinyin,NORMAL

# 定义一个迭代函数 从数据集中逐行地产生训练数据
def iter_dict():
    with open('dict.txt') as f:
        for line in f:
            word, freq, tag= line.split()
            yield word.decode('utf8'),int(freq)


database = 'trainedHMM.sqlite'
cnn = sqlite3.connect(database)
cursor = cnn.cursor()

# 训练转移矩阵transition
cursor.execute('create table transition(id,previous,behind,probability)')
transitionMap={}
for word, freq in iter_dict():
    for i in range(len(word)-1):
        if word[i] in transitionMap:
            # 如果在transitionMap中已经有了属于word[i]的字典
            transitionMap[word[i]][word[i+1]] = freq + transitionMap[word[i]].get(word[i+1],0)
        else:
            # 否则 在字典里新建一个字典
            transitionMap[word[i]]={word[i+1]: freq}
row = 0
for previous, map in transitionMap.iteritems():
    # 使用频数计算log频率并存入表transition中
    countSum = sum(map.values())
    for key, value in map.iteritems():
        value = math.log(float(value)/countSum)
        cursor.execute('insert into transition values(?,?,?,?)',(row,previous,key,value,))
        row+=1


# 训练发射矩阵emission
cursor.execute('create table emission(id,character,pinyin,probability)')
charPyMap = {}
for word, freq in iter_dict():
    pyOfWord = pinyin(word, style=NORMAL)
    for character,py in zip(word, pyOfWord):
        sumPinyin = len(py) # 每个字可能是个多音字 len(py)得到总的有多少个音
        if character not in charPyMap:
            # 如果在字典中还没有的话，直接初始化为这次的freq
            charPyMap[character] = {x: freq/sumPinyin for x in py}
        else:
            pyFreqMap = charPyMap[character]
            for x in py:
                pyFreqMap[x] = pyFreqMap.get(x,0)+freq/sumPinyin
row=0
for character,cpMap in charPyMap.iteritems():
    sumPyofChar = sum(cpMap.values())
    for key, value in cpMap.iteritems():
        value = math.log(float(value)/sumPyofChar)
        cursor.execute('insert into emission values(?,?,?,?)',(row,character,key,value))
        row += 1


# 训练初始矩阵starting
cursor.execute('create table starting(id,character,probability)') # (行数，汉字，在句首的概率）
freqMap = {}
count = 0
for word, freq in iter_dict():
    count += freq
    freqMap[word[0]] = freqMap.get(word[0],0) + freq
row = 0
for key, value in freqMap.iteritems():
    value = math.log(float(value)/count)
    cursor.execute('insert into starting values(?,?,?)',(row,key,value,))
    row+=1

#保存并关闭数据库
cursor.close()
cnn.commit()
cnn.close()