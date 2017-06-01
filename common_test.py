#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
from utils.inout import printEscapeStr


testt = '_w   _w 组建_v 省_k 港口_x 集团_n  _w '
testList = testt.strip().split('  ')
printEscapeStr(testList)


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