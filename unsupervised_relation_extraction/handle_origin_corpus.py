#!/usr/bin/env python
# -*- coding:utf-8 -*-

from utils import inout
from utils.inout import printEscapeStr

"""
    筛选规则：
    1）字符串分割成列表形式；
    2）列表中提取“_”符号前后都有内容的元素组成新列表；
"""

def getNewLineList(lineList):
    '''

    '''
    resultList = []
    for item in lineList:
        if '_' in item:
            if item.split('_'):
                splitList = item.split('_')
                if len(splitList) == 2:
                    if splitList[0] != '' and splitList[1] != '':
                        resultList.append(item)
    return resultList



if __name__ == '__main__':
    # origin_corpus = inout.getDataOriginPath('origin_corpus.txt')
    origin_corpus = inout.getDataTestPath('origin_corpus_test.txt')

    infoList = inout.readListFromTxt(origin_corpus)

    for i in range(len(infoList)):
        line = infoList[i].strip()
        if line:
            if line != '_w  _w':
                lineList = line.split(' ')

                lineList = getNewLineList(lineList)
                printEscapeStr(lineList)
