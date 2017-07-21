#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
from utils.inout import printEscapeStr
from utils import inout
from collections import OrderedDict
import time
from utils import systm
import uuid
import hashlib
import operator
import jieba
from tqdm import tqdm






# testStr = """
# 千年前两晋时期温婉现世，穿越南宋风雅，燃起窑焰竟日夜的传奇，自明代后逐渐淡出视野；1957年，龙泉青瓷于历史中蒙尘数\
# 百年后，在周总理的指示下恢复生产，并于2009年，入选联合国教科文组织所设《人类非物质文化遗产代表作名录》，成为唯一入选的陶瓷类项目。"""
#
# testStr = """哈佛大学研究表明，左撇子的女性患多发性硬化的风险要比习惯用右手者高62%"""
#
# re = ' '.join(jieba.cut(testStr))
# print re





endNum = 700000
initDic = dict()
findList = []
for i in tqdm(range(endNum)):
    initDic[i] = [i]
    findList.append(i)


startTime = time.time()

# findNum = 400000
# for item in findList:
for i in tqdm(range(len(findList))):
    item = findList[i]
    if item in initDic.keys():
        # print initDic[item][0]
        pass

endTime = time.time()

print endTime-startTime







# dic = dict()
# dic['宋喆'] = 5
# dic['马蓉'] = 9
# dic['王宝庆'] = 2
#
# orderedItemsList = sorted(dic.items(),key=lambda item:item[1],reverse=True)
# print type(orderedItemsList),orderedItemsList





# name1 = '李自成'
# name2 = '魏藻德'



# re1 = hashlib.md5(name1).hexdigest()
# print type(re1),re1
# re2 = hashlib.sha1(name2).hexdigest()
# print type(re2),re2



# re1 = uuid.uuid3(uuid.NAMESPACE_DNS,name1)
# print type(re1),re1
# re2 = uuid.uuid3(uuid.NAMESPACE_DNS,name2)
# print type(re2),re2
#
# re = str(re1) + str(re2)
# print type(re),re






# test = '\xe8\x89\xbe\xe5\x8a\x9b\xc2\xb7\xe4\xbe\x9d\xe6\x98\x8e'
# print test.decode('utf-8')






#
# def getTimeStampFromTimeStr(timeStr):
#     '''
#
#     '''
#     return time.mktime(time.strptime(timeStr,'%Y-%m-%d %H:%M:%S'))
#
#
#
#
# print getTimeStampFromTimeStr('2016-12-30 12:00:00')




# print systm.getTimeStampFromTimeStr('2017-1-1 12:00:00')

# timeStr = '2017-1-12 23:59:00'
# re = systm.getTimeStampFromTimeStr(timeStr)
# print type(re),re






# startTime = time.time()
# print startTime
# print type(startTime)
# for i in range(10000000):
#     j = i+1
#
# endTime = time.time()
# print endTime
# print 'end-start:'
# print endTime-startTime



# print time.time()


# test = '某'
# print len(test)

# item = """[[('\xe9\x83\xad\xe5\x8f\xb0\xe9\x93\xad', 'S-Nh'), ('\xe9\xa9\xac\xe4\xba\x91', 'S-Nh')], ['\xe9\x80\x8f\xe9\x9c\xb2', '\xef\xbc\x8c', '\xe6\x9e\x97\xe6\x96\x87\xe4\xbc\xaf', '\xe8\xae\xa4\xe4\xb8\xba', '\xef\xbc\x8c', '\xe7\xb4\xab\xe5\x85\x89', '\xe5\x85\xa5\xe8\x82\xa1', '\xe7\x9f\xbd\xe5\x93\x81', '\xef\xbc\x8c', '\xe5\xb0\xb1', '\xe5\x83\x8f', '\xe4\xbe\x9d\xe7\x84\xb6', '\xe5\x8f\xaf\xe4\xbb\xa5', '\xe6\x8e\x8c\xe6\x8e\xa7', '\xe9\x98\xbf\xe9\x87\x8c\xe5\xb7\xb4\xe5\xb7\xb4', '(', 'BABA-US', ')', '\xe7\x9a\x84', '\xe4\xb8\xbb\xe5\xaf\xbc\xe6\x9d\x83', '\xe4\xb8\x80\xe6\xa0\xb7', '\xef\xbc\x8c', '\xe5\x8f\xaa\xe8\xa6\x81', '\xe7\x9f\xbd\xe5\x93\x81', '\xe7\xbb\x8f\xe8\x90\xa5', '\xe5\x9b\xa2\xe9\x98\x9f', '\xe5\x8f\xaf\xe4\xbb\xa5', '\xe6\x8e\x8c\xe6\x8e\xa7', '\xe4\xb8\xbb\xe5\xaf\xbc\xe6\x9d\x83', '\xef\xbc\x8c', '\xe9\x82\xa3', '\xe7\x9f\xbd\xe5\x93\x81', '\xe8\xb7\x9f', '\xe7\xb4\xab\xe5\x85\x89', '\xe5\x9c\xa8', '\xe4\xb8\xad\xe5\x9b\xbd', '\xe5\x90\x88\xe8\xb5\x84', '\xe6\x88\x90\xe7\xab\x8b', '\xe4\xbb\x8d', '\xe5\x85\xb7\xe6\x9c\x89', '\xe4\xb8\xbb\xe5\xaf\xbc\xe6\x9d\x83', '\xe7\x9a\x84', '\xe5\xb0\x81\xe8\xa3\x85\xe5\x8e\x82', '\xef\xbc\x8c', '\xe9\x82\xa3', '\xe5\xba\x94\xe8\xaf\xa5', '\xe6\xb2\xa1\xe6\x9c\x89', '\xe5\xa4\xaa', '\xe5\xa4\xa7', '\xe7\x9a\x84', '\xe9\x97\xae\xe9\xa2\x98', '\xe3\x80\x82']]"""
# item = eval(item)
#
# firstPart = ' '.join(zip(*item[0])[0])
# sencondPart = '_'.join(item[1])
#
# print firstPart
# print sencondPart


# testDic = OrderedDict()
# testList = ['a','b','a','b']
# for i in range(len(testList)):
#     testDic[testList[i]] = i
#
# print testDic.keys()
# for k,v in testDic.items():
#     print k,v






# path = inout.getDataTestPath('origin_corpus_test.txt')
# infoList = inout.readListFromTxt(path)
# for item in infoList:
#     print item
#     print len(item)





# sentencePath = inout.getDataPklPath('sentence_list_corpus_complete_sentence.pkl')
#
# sentenceList, slType = inout.readPersistObject(sentencePath)
# print len(sentenceList)



# testList = [('刘霆', 'S-Nh'), ('刘霆', 'S-Nh')]
# if testList[0] == testList[1]:
#     print 'y'



# testList = ['a','b']
# for i in range(len(testList)-1,-1,-1):
#     print testList[i]


# testList = [('张杨', 'S-Nh'), ('郭亮', 'S-Nh')]
# re = zip(*testList)
# printEscapeStr(re)
# final = ' '.join(re[0])
# print final


# testList = []
# if testList:
#     print 'y'


# testWord = ''
# if testWord:
#     print 'y'



# testList = [('潘世明','S-Nh')]
#
# unzipList = zip(*testList)
# printEscapeStr(unzipList)
# neWordList = unzipList[0]
# indexList = unzipList[1]
#
# printEscapeStr(neWordList)
# printEscapeStr(indexList)


# sentencePath = inout.getDataOriginPath('sentence_list_corpus.pkl')
# sentenceFeaturePath = inout.getDataOriginPath('sentence_feature_list_corpus.pkl')
#
#
# sentenceList,senType = inout.readPersistObject(sentencePath)
# print len(sentenceList)
# for item in sentenceList:
#     print item

# sentenceFeatureList,sfType = inout.readPersistObject(sentenceFeaturePath)
# print len(sentenceFeatureList)
# print sfType
# for item in sentenceFeatureList:
#     printEscapeStr(item)



# testList = ['1','2','3']
# printEscapeStr(testList[0:1])


# path = inout.getDataTestPath('origin_corpus_test.txt')
# info = inout.readListFromTxt(path)
# for item in info:
#     lineList = item.strip().split(' ')
#     printEscapeStr(lineList)
#     for it in lineList:
#         if '_' in it:
#             if len(it.split('_')) == 2:
#                 splitList = it.split('_')
#                 print type(splitList[0])
#                 print splitList[0]
#                 if not splitList[0] == '':
#                     print 'yes'
#                 print '|||||'
#                 exit(0)









# if testList[0] != '' and testList[1] != '':
#     printEscapeStr(testList)


# testt = '_w   _w 组建_v 省_k 港口_x 集团_n  _w '
# testList = testt.strip().split('  ')
# printEscapeStr(testList)


# testList = [('王','B-Nh'),('宝强','E-Nh'),('马蓉','S-Nh')]
# result = zip(*testList)
# printEscapeStr(result)
# print type(result)
# neList = result[0]
# indexList = result[1]
# cIndexList = []
# namedEntityList = []
# for i in range(len(indexList)):
#     if 'B' in indexList[i]:
#         if i+1 < len(indexList):
#             if 'I' in indexList[i+1]:
#                 if i+2 < len(indexList):
#                     if 'E' in indexList[i+2]:
#                         ne = neList[i]+neList[i+1]+neList[i+2]
#                         print ne
#                         namedEntityList.append(ne)
#         if i+1 < len(indexList):
#             if 'E' in indexList[i+1]:
#                 ne = neList[i] + neList[i+1]
#                 print ne
#                 namedEntityList.append(ne)
#     if 'S' in indexList[i]:
#         ne = neList[i]
#         print ne
#         namedEntityList.append(ne)
# printEscapeStr(namedEntityList)




# print np.sqrt(9)
# print type(np.sqrt(9))


# print np.square(3)
# print type(np.square(3))

# print np.log2(8)
# print type(np.log2(8))


# dic = dict()
# dic['1'] = []
# dic['2'] = []
# dic['3'] = []
# print len(dic)



# testList = ['王祖蓝','王茂']
# re = '_'.join(testList)
# print re



# testList = ['a','d','g']
# vector = np.zeros((len(testList)))
# print vector


# np.array()

# testList = ['中国精神分裂剑法','价代发飞机阿发的']
# print type(testList)
# print type(str(testList))
# print str(testList)
# print str(testList).decode('string_escape')