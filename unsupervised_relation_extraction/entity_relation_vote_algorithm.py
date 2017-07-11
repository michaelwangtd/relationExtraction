#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
from utils import inout
from utils.inout import printEscapeStr
import persistent_relation_object
from collections import OrderedDict
import time


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
        适用于文本数量较少，大规模的数据量使用该函数会很慢
    '''
    resultSenList = []
    resultSenFeaList = []
    for i in range(len(sentenceList)):
        if not sentenceList[i] in resultSenList:
            resultSenList.append(sentenceList[i])
        if not sentenceFeatureList[i] in resultSenFeaList:
            resultSenFeaList.append(sentenceFeatureList[i])
    return resultSenList,resultSenFeaList


def dictDistinct(sentenceList,sentenceFeatureList):
    '''
        利用python dict结果进行过滤
    '''

    indexDic = dict()

    resultSentenceList = []
    resultSentenceFeatureList = []

    for i in range(len(sentenceList)):
        indexDic[str(sentenceList[i])] = i

    indexList = []
    for k,v in indexDic.items():
        indexList.append(v)
    indexList = list(set(indexList))

    for idx in indexList:
        resultSentenceList.append(sentenceList[idx])
        resultSentenceFeatureList.append(sentenceFeatureList[idx])

    return resultSentenceList,resultSentenceFeatureList




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


def convertDataFormat(infoList):
    '''
        input:姚景远	孙彩艳||文章_对_、_进行_了_猛烈_的_人身_抨击_。||文章对姚景远、孙彩艳进行了猛烈的人身抨击。
        output:
                [[(姚景远,S-Nh),(孙彩艳,S-Nh)],['生于', '加州', '一个', '中产', '家庭', '，', '意大利', '裔', '父亲']]
                文章对姚景远、孙彩艳进行了猛烈的人身抨击。
    '''
    sentenceList = []
    sentenceFeatureList = []

    for line in infoList:
        if len(line.strip().split('||')) == 3:
            lineList = line.strip().split('||')

            # 处理命名实体对
            nePairList = []
            neStrTemp = lineList[0]
            if len(neStrTemp.split('\t')) == 2:
                neStrTempList = neStrTemp.split('\t')

                ## 对命名实体进行筛选
                if '某' not in neStrTempList[0].strip() and '某' not in neStrTempList[1].strip():

                    if len(neStrTempList[0].strip()) > 3 and len(neStrTempList[1].strip()) > 3:

                        if neStrTempList[0].strip() != neStrTempList[1]:

                            nePairList.append((neStrTempList[0].strip(),'S-Nh'))
                            nePairList.append((neStrTempList[1].strip(),'S-Nh'))

            # 处理otherWordList
            otherWordStr = lineList[1]
            otherWordList = otherWordStr.split('_')

            # 处理句子
            sentenceStr = lineList[2]

            if nePairList:
                sentenceFeatureList.append([nePairList,otherWordList])
                sentenceList.append(sentenceStr)
    return sentenceList,sentenceFeatureList


def convertNewDataFormat(infoList):
    '''

    '''
    sentenceList = []
    sentenceFeatureList = []

    for line in infoList:
        if len(line.strip().split('#OUTER#'))==4:
            lineList = line.strip().split('#OUTER#')

            # 处理命名实体对
            nePairList = []
            if 'entityPair' in lineList[0]:

                neStrTemp = lineList[0].split('#INNER#')[1]
                if len(neStrTemp.split('\t')) == 2:
                    neStrTempList = neStrTemp.split('\t')

                    if '某' not in neStrTempList[0].strip() and '某' not in neStrTempList[1].strip():

                        if len(neStrTempList[0].strip()) > 3 and len(neStrTempList[1].strip()) > 3:

                            if neStrTempList[0].strip() != neStrTempList[1]:

                                nePairList.append((neStrTempList[0].strip(), 'S-Nh'))
                                nePairList.append((neStrTempList[1].strip(), 'S-Nh'))

            # 处理otherWordList
            otherWordList = []
            if 'wordList' in lineList[1]:
                otherWordStr = lineList[1].split('#INNER#')[1]
                otherWordList = otherWordStr.split('_')

            sentenceStr = ''
            # 处理句子
            if 'sentence' in lineList[2]:
                sentenceStr = lineList[2].split('#INNER#')[1]

            time = ''
            if 'time' in lineList[3]:
                if len(lineList[3].split('#INNER#'))==2:
                    if lineList[3].split('#INNER#')[1]!='':
                        time = lineList[3].split('#INNER#')[1]
            comSentence = time + '#INNER#' + sentenceStr

            if nePairList:
                sentenceFeatureList.append([nePairList,otherWordList])
                sentenceList.append(comSentence)
    return sentenceList, sentenceFeatureList



if __name__ == '__main__':

    # 输出路径
    outputPath = inout.getDataAnalysisPath('analysis_vote_sentence_fnlp_150w-2100w.txt')
    # outputPath = inout.getDataAnalysisPath('analysis_vote_sentence_0615.txt')
    # outputPath = inout.getDataAnalysisPath('analysis_test.txt')

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

    """
            这里加载数据的处理策略：
            1）从pkl对象直接加载
            2）从文本文件读取数据形成列表
            最后的数据都以列表形式合并成一个总的列表
    """
    sentenceList = []
    sentenceFeatureList = []


    ## 1 加载pkl对象
    # sentencePklPath = inout.getDataPklPath('sentence_list_corpus_complete_sentence.pkl')
    # sentenceFeaturePklPath = inout.getDataPklPath('sentence_feature_list_corpus_complete_sentence.pkl')

    # sentencePath = inout.getDataPklPath('sentence_list_corpus_test.pkl')
    # sentenceFeaturePath = inout.getDataPklPath('sentence_feature_list_corpus_test.pkl')

    # sentencePklList, slType = inout.readPersistObject(sentencePklPath)
    # sentenceFeaturePklList, sflType = inout.readPersistObject(sentenceFeaturePklPath)

    ## 2 加载pyltp 命名实体识别数据
    # infoListPartPath = inout.getDataNEMeatPath('sentence_and_feature_max_w.txt')
    #
    # infoListPart = inout.readListFromTxt(infoListPartPath)
    #
    # sentenceListTxt,sentenceFeatureListTxt = convertDataFormat(infoListPart)

    ## 3 加载 fnlp 命名实体识别数据 旧版数据
    # fnlpListPath = inout.getDataNEMeatPath('sentence_and_feature_150w-900w_fnlp_old.txt')
    fnlpListPath = inout.getDataTestPath('sentence_and_feature_test.txt')

    fnlpOldDataList = inout.readListFromTxt(fnlpListPath)
    print'原始-数据-旧 len:', len(fnlpOldDataList)

    fnlpSentenceList_old,fnlpSentenceFeatureList_old = convertDataFormat(fnlpOldDataList)
    print'处理-数据-旧 len:', len(fnlpSentenceList_old)

    sentenceList.extend(fnlpSentenceList_old)
    sentenceFeatureList.extend(fnlpSentenceFeatureList_old)

    ## 4 加载 fnlp 命名实体识别数据 数据新接口

    # fnlpNewDataListPath = inout.getDataNEMeatPath('sentence_and_feature_900w-2100w_fnlp_new.txt')
    fnlpNewDataListPath = inout.getDataTestPath('sentence_and_feature_test_new.txt')

    fnlpNewDataList = inout.readListFromTxt(fnlpNewDataListPath)
    print'原始-数据-新 len:', len(fnlpNewDataList)

    fnlpSentenceList_new,fnlpSentenceFeatureList_new = convertNewDataFormat(fnlpNewDataList)
    print'处理-数据-新 len:', len(fnlpSentenceList_new)

    sentenceList.extend(fnlpSentenceList_new)
    sentenceFeatureList.extend(fnlpSentenceFeatureList_new)



    # for i in range(5):
    #     printEscapeStr(fnlpSentenceFeatureList_new[i])
    #     print fnlpSentenceList_new[i]

    # print 'fnlp list len:',len(fnlpSentenceList)

    # exit(0)


    ## 合并所有的数据
    # sentenceList.extend(sentencePklList)
    # sentenceFeatureList.extend(sentenceFeaturePklList)
    #
    # sentenceList.extend(sentenceListTxt)
    # sentenceFeatureList.extend(sentenceFeatureListTxt)


    print 'sentenceList len: ',len(sentenceList)
    print 'sentenceFeatureList len: ',len(sentenceFeatureList)
    print '数据加载完毕...'

    # inout.writeList2Txt(inout.getDataTestPath('sentence.txt'),sentenceList)
    # inout.writeFnlpSentenceFeature2Txt(inout.getDataTestPath('sentenceFeature.txt'),sentenceFeatureList)
    exit(0)



    ## 加入去重逻辑
    # sentenceList,sentenceFeatureList = distinct(sentenceList,sentenceFeatureList)
    ## 利用python的dict结构去重
    sentenceList,sentenceFeatureList = dictDistinct(sentenceList,sentenceFeatureList)
    print len(sentenceList)
    print '句子去重复完成...'

    # inout.writeList2Txt(inout.getDataTestPath('fnlp_sentence.txt'),sentenceList)
    # inout.writeFnlpSentenceFeature2Txt(inout.getDataTestPath('fnlp_sentenceFeature.txt'),sentenceFeatureList)



    # exit(0)


    # for i in range(len(sentenceFeatureList)):
    #     printEscapeStr(sentenceFeatureList[i][0])
    #     if i==5:
    #         break
    # exit(0)

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
    print '开始处理...'
    startTime = time.time()
    print startTime

    for i in range(len(sentenceFeatureList)):

        if isinstance(sentenceFeatureList[i],str):
            sentenceFeature = eval(sentenceFeatureList[i])
        sentenceFeature = sentenceFeatureList[i]

        namedEntityAndTagList = sentenceFeature[0]
        otherWordList = sentenceFeature[1]

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

            outputLine = '人物实体：【' + neStr + '】 ' + '\t' + '候选关系： 【' + candidateRelationStr + '】' +\
                '\t' + '句子个数： ' + str(len(sentenceIndexList)) + '\n' + outputRelationWordSortedList + '\n' +\
                sentenceOutputStr

            fw.write(outputLine + '\n')
            # print i
            i = i + 1

    print 'i:'
    print i

    endTime = time.time()
    print endTime
    print 'end-start:'
    print endTime-startTime

    fw.close()









