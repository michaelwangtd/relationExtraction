#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
from utils import inout
from utils.inout import printEscapeStr
import persistent_relation_object
from collections import OrderedDict


def removeStopWord(otherWordList,stopWordList):
    '''
        去掉无意义词和标点符号
    '''
    featureWordList = []
    if otherWordList:
        for item in otherWordList:
            if item not in stopWordList:
                featureWordList.append(item)
    return featureWordList


def removeOneLengthWord(featureWordList):
    '''
        特征词进行筛选，去除一个字的词
    '''
    resultList = []
    for item in featureWordList:
        item = item.decode('utf-8')
        # print type(item)
        # print len(item)
        if len(item) > 1:
            if not item.isdigit():
                item = item.encode('utf-8')
                resultList.append(item)
    return resultList


def getMappedWord(featureWord,relationDic):
    '''

    '''
    mappedWord = ''
    for mappedWordKey,mappingWordListValue in relationDic.items():
        if featureWord in mappingWordListValue:
            mappedWord = mappedWordKey
            break
    return mappedWord


def getRelationWordList(featureWordList,relationDic,i):
    '''
        :i sentenceFeatureList 的索引
    '''
    relationWordList = []
    for featureWord in featureWordList:
        mappedWord = getMappedWord(featureWord,relationDic)
        if mappedWord:
            relationWordList.append((mappedWord,i))
    return relationWordList


def getNamedEntityPairStr(namedEntityAndTagList):
    '''
        :input [('张杨', 'S-Nh'), ('郭亮', 'S-Nh')]
        :return xxx_xxx
    '''
    namedEntityPairStr = ''
    if namedEntityAndTagList:
        unzipList = zip(*namedEntityAndTagList)
        namedEntityPairStr = ' '.join(unzipList[0])
    return namedEntityPairStr


def getExchangedNamedEntityPairStr(namedEntityPairStr):
    '''

    '''
    resultList = []
    for i in range(len(namedEntityPairStr.split(' '))-1,-1,-1):
        resultList.append(namedEntityPairStr.split(' ')[i])
    return ' '.join(resultList)


def getWordFrequenceDic(relationWordList):
    '''

    '''
    dic = dict()
    for item in relationWordList:
        if item not in dic.keys():
            dic[item] = 0
        dic[item] = dic[item] + 1
    return dic


def getWordFrequenceList(wordFrequenceDic):
    '''

    '''
    resultList = []
    for k,v in wordFrequenceDic.items():
        resultList.append((k,v))
    return resultList



def getRelationWordSortedList(relationWordList):
    '''

    '''
    resultTupleList = []
    if relationWordList:
        if len(relationWordList) == 1:
            resultTupleList.append((relationWordList[0],1))
        elif len(relationWordList) >=1:
            wordFrequenceDic = getWordFrequenceDic(relationWordList)
            wordFrequenceList = getWordFrequenceList(wordFrequenceDic)
            wordFrequenceSortedList = sorted(wordFrequenceList,key=lambda item:item[1],reverse=True)
            resultTupleList.extend(wordFrequenceSortedList)
    return resultTupleList


def getOutputRelationWordSortedList(relationWordSortedList):
    '''

    '''
    outputStr = '['
    for tupleItem in relationWordSortedList:
        outItem = '(' + tupleItem[0] + ',' + str(tupleItem[1]) + ')'
        outputStr = outputStr + outItem
    outputStr = outputStr + ']'
    return outputStr




def getCandidateRelationStr(relationWordSortedList):
    '''

    '''
    resultList = []
    highScore = relationWordSortedList[0][1]
    for tupleItem in relationWordSortedList:
        if tupleItem[1] == highScore:
            resultList.append(tupleItem[0])
        else:
            break
    return ' '.join(resultList)


def getSentenceOutputStr(sentenceIndexList,sentenceList):
    '''

    '''
    resultStr = ''
    for index in sentenceIndexList:
        resultStr = resultStr + sentenceList[index] + '\n'
    return resultStr


def isSameNamedEntity(namedEntityAndTagList):
    '''

    '''
    if len(namedEntityAndTagList) == 2:
        if namedEntityAndTagList[0] == namedEntityAndTagList[1]:
            return True
    return False


def distinct(sentenceList,sentenceFeatureList):
    '''
        列表元素去除重复
    '''
    resultSenList = []
    resultSenFeaList = []
    for i in range(len(sentenceList)):
        if not sentenceList[i] in resultSenList:
            resultSenList.append(sentenceList[i])
        if not sentenceFeatureList[i] in resultSenFeaList:
            resultSenFeaList.append(sentenceFeatureList[i])
    return resultSenList,resultSenFeaList


def listlist2list(listlist):
    '''
        [[a,b],[c],[d]] ----> [a,b,c,d]
    '''
    resultList = []
    for itemList in listlist:
        resultList.extend(itemList)
    return resultList


def convert2SortedDic(initDic):
    '''
        转换成排序字典
        按照字典value中列表的长度，重新排序字典，将列表长度长的放在最前面进行处理
        转换形式：
            value: [ [('xx',i),('aa',i)],[('bb',i)],[('dd',i)] ] ----> [ ('xx',i),('aa',i),('bb',i),('dd',i) ]
    '''
    dic = OrderedDict()
    ## 获取keyLsit
    keyList = initDic.keys()
    indexAndSentenceCountTupleList = []
    for i in range(len(keyList)):
        indexAndSentenceCountTupleList.append((i,len(initDic[keyList[i]])))
    ## 排序
    sortedIndexAndSentenceCountTupleList = sorted(indexAndSentenceCountTupleList,key=lambda item:item[1],reverse=True)

    for tupleItem in sortedIndexAndSentenceCountTupleList:
        idx = tupleItem[0]
        relationAndIndexTupeList = listlist2list(initDic[keyList[idx]])
        dic[keyList[idx]] = relationAndIndexTupeList
    return dic




if __name__ == '__main__':

    # outputPath = inout.getDataAnalysisPath('analysis_vote_sentence.txt')
    outputPath = inout.getDataAnalysisPath('analysis_test.txt')

    ## 配置
    pd.set_option('display.width', 300)
    np.set_printoptions(linewidth=300, suppress=True)

    ## 加载停用词列表
    stopWordPath = inout.getResourcePath('stopWordList.txt')
    stopWordList = inout.readListFromTxt(stopWordPath)
    # 这地方加入临时逻辑，后面可以进行停用词合并
    stopWordList = list(set(stopWordList))

    ## 加载关系字典
    relationDic = persistent_relation_object.getRelationShipDic()

    ## 作为模块的入口，加载对象
    # sentencePath = inout.getDataPklPath('sentence_list_corpus_complete_sentence.pkl')
    # sentenceFeaturePath = inout.getDataPklPath('sentence_feature_list_corpus_complete_sentence.pkl')

    sentencePath = inout.getDataPklPath('sentence_list_corpus_test.pkl')
    sentenceFeaturePath = inout.getDataPklPath('sentence_feature_list_corpus_test.pkl')

    ## 加载pkl对象
    sentenceList, slType = inout.readPersistObject(sentencePath)
    sentenceFeatureList, sflType = inout.readPersistObject(sentenceFeaturePath)

    ## 加入去重逻辑
    sentenceList,sentenceFeatureList = distinct(sentenceList,sentenceFeatureList)
    print '句子去重复完成...'

    # print len(sentenceList)
    # for i in range(len(sentenceList)):
    #     printEscapeStr(sentenceList[i])
    #     printEscapeStr(sentenceFeatureList[i])
    #     if i == 5:
    #         break
    # print len(sentenceList)
    # printEscapeStr(sentenceList)
    # print len(sentenceFeatureList)
    # printEscapeStr(sentenceFeatureList)
    # exit(0)

    ## 初始化归类字典
    initDic = dict()

    ## 开始处理
    for i in range(len(sentenceFeatureList)):
        namedEntityAndTagList = sentenceFeatureList[i][0]
        otherWordList = sentenceFeatureList[i][1]

        ## 判断两个命名实体是否相同
        if not isSameNamedEntity(namedEntityAndTagList):

            ##  其他词去掉停用词
            featureWordList = removeStopWord(otherWordList, stopWordList)

            ##  去掉特征词中的一个字的词和数字
            featureWordList = removeOneLengthWord(featureWordList)

            if featureWordList:

                ## 获取特征词中含有的命名实体关系词的列表
                relationWordAndIndexList = getRelationWordList(featureWordList,relationDic,i)

                if relationWordAndIndexList:
                    ## 归类到字典中

                    namedEntityPairStr = getNamedEntityPairStr(namedEntityAndTagList)
                    exchangedEntityPairStr = getExchangedNamedEntityPairStr(namedEntityPairStr)

                    if namedEntityPairStr not in initDic.keys() and exchangedEntityPairStr not in initDic.keys():
                        initDic[namedEntityPairStr] = []

                    ## 这里也可以用命名实体排序的方法
                    if namedEntityPairStr in initDic.keys():
                        ## !! 注意这里的append的修改
                        initDic[namedEntityPairStr].append(relationWordAndIndexList)
                    if exchangedEntityPairStr in initDic.keys():
                        initDic[exchangedEntityPairStr].append(relationWordAndIndexList)

    print '归类完成...'
    # exit(0)

    ## initDic按照相同实体对句子的多少重新排序字典
    initDic = convert2SortedDic(initDic)
    print '排序字典完成...'

    fw = open(outputPath,'wb')

    i = 1
    for neStr,relationAndIndexTupeList in initDic.items():
        if relationAndIndexTupeList:
            # printEscapeStr(relationAndIndexTupeList)
            unzipList = zip(*relationAndIndexTupeList)
            relationWordList = unzipList[0]
            sentenceIndexList = list(set(unzipList[1]))

            relationWordSortedList = getRelationWordSortedList(relationWordList)
            # printEscapeStr(relationWordSortedList)

            outputRelationWordSortedList = getOutputRelationWordSortedList(relationWordSortedList)

            candidateRelationStr = getCandidateRelationStr(relationWordSortedList)

            sentenceOutputStr = getSentenceOutputStr(sentenceIndexList,sentenceList)

            outputLine = '人物实体：【' + neStr + '】 ' + '\t\t' + '候选关系： 【' + candidateRelationStr + '】' +\
                '\n' + outputRelationWordSortedList + '\n' +\
                sentenceOutputStr

            fw.write(outputLine + '\n')
            print i
            i = i + 1

    fw.close()









