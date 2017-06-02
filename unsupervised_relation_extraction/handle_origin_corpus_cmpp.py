#!/usr/bin/env python
# -*- coding:utf-8 -*-

from utils import inout
from utils.inout import printEscapeStr

"""
    筛选规则：
    1）字符串分割成列表形式；
    2）列表中提取“_”符号前后都有内容的元素组成新列表；
    筛选结果：
    筛选的结果以对象的形式保存
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


def splitSentenceInLineList(lineList):
    '''

    '''
    resultList = []

    pointNum = 0
    for item in lineList:
        if '。' in item or '！' in item or '？' in item:
            pointNum = pointNum + 1
    if pointNum <= 1:
        resultList.append(lineList)
    elif pointNum >=2:
        resultList = splitSentenceList(lineList)
    return resultList


def splitSentenceList(lineList):
    '''
        将lineList中多个句子分开
    '''
    sentenceList = []

    startIdx = 0
    endIdx = 0
    for i in range(len(lineList)):
        if '。' in lineList[i] or '！' in lineList[i] or '？' in lineList[i]:
            startIdx = endIdx
            endIdx = i + 1
            sentenceList.append(lineList[startIdx:endIdx])
    return sentenceList


def divideNEPairAndOtherWord(sentenceWordList):
    '''
        提取、分割命名实体对和其他词，分别组成列表形式
    '''
    personEntityList = ['nr','nr1','nr2','nrf','nrj']

    nePairTagList = []
    otherWordList = []

    for item in sentenceWordList:
        itemList = item.split('_')
        if itemList[1].strip() in personEntityList:
            nePairTagList.append((itemList[0],'S-Nh'))
        else:
            otherWordList.append(itemList[0].strip())
    return nePairTagList,otherWordList


def packageWord2Sentence(sentenceWordList):
    '''
        将词列表形式转化为句子
    '''
    sentence = ''
    for item in sentenceWordList:
        sentence = sentence + item.split('_')[0].strip()
    return sentence





if __name__ == '__main__':
    origin_corpus = inout.getDataOriginPath('origin_corpus_cmpp.txt')
    # origin_corpus = inout.getDataTestPath('origin_corpus_test.txt')

    infoList = inout.readListFromTxt(origin_corpus)

    # 初始化两个同步的列表
    sentenceList = []
    sentenceFeatureList = []

    j = 0
    for i in range(len(infoList)):
        line = infoList[i].strip()
        if line:
            if line != '_w  _w':
                lineList = line.split(' ')

                ## 提取有效的词性标注元素
                lineList = getNewLineList(lineList)
                # printEscapeStr(lineList)

                ## 将列表中的多句话分开
                sentenceSplitList = splitSentenceInLineList(lineList)
                # for item in sentenceList:
                #     printEscapeStr(item)

                # 对每一个句子进行筛选
                for sentenceWordList in sentenceSplitList:
                    # printEscapeStr(sentenceWordList)
                    # 找出命名实体对，分离命名实体对和其他词
                    nePairTagList,otherWordList = divideNEPairAndOtherWord(sentenceWordList)
                    # 判断句子是否符合有两个命名实体的条件
                    if len(nePairTagList) == 2:     # 说明这一句子中有且仅有两个命名实体
                        sentenceFeatureList.append([nePairTagList,otherWordList])
                        # 组装句子
                        packagedSentence = packageWord2Sentence(sentenceWordList)
                        sentenceList.append(packagedSentence)

                        j = j + 1
                # if j > 5:
                #     break

    for i in range(len(sentenceList)):
        printEscapeStr(sentenceList[i])
        printEscapeStr(sentenceFeatureList[i])
    print '筛选的句子数量： ' + str(j)

    # 这里要持久化两个对象：sentenceList、sentenceFeatureList
    sentencePath = inout.getDataOriginPath('sentence_list_corpus.pkl')
    sentenceFeaturePath = inout.getDataOriginPath('sentence_feature_list_corpus.pkl')

    inout.writePersistObject(sentencePath,sentenceList)
    inout.writePersistObject(sentenceFeaturePath,sentenceFeatureList)
    print '持久化完成...'
















