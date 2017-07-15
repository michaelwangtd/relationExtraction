# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
from utils import inout
from utils.inout import printEscapeStr
import unsupervised_relation_extraction.persistent_relation_object
from collections import OrderedDict
import time
from tqdm import tqdm
import codecs

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


def isSameNamedEntity(namedEntityAndTagList):
    '''

    '''
    if len(namedEntityAndTagList) == 2:
        if namedEntityAndTagList[0] == namedEntityAndTagList[1]:
            return True
    return False


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


def getMappedWord(featureWord,relationDic):
    '''

    '''
    mappedWord = ''
    for mappedWordKey,mappingWordListValue in relationDic.items():
        if featureWord in mappingWordListValue:
            mappedWord = mappedWordKey
            break
    return mappedWord


def getNamedEntityPairStr(namedEntityAndTagList):
    '''
        :input [('张杨', 'S-Nh'), ('郭亮', 'S-Nh')]
        :return xxx_xxx
    '''
    namedEntityPairStr = ''
    if namedEntityAndTagList:
        unzipList = zip(*namedEntityAndTagList)
        namedEntityPairStr = '\t'.join(unzipList[0])
    return namedEntityPairStr


def transList2Str(relationWordAndSentenceIndexList):
    '''
    :param relationWordAndSentenceIndexList:
    :return:
    '''

    upzipList = zip(*relationWordAndSentenceIndexList)

    relationList = upzipList[0]
    sentenceIndexlist = upzipList[1]

    # indexStr = ''
    # for item in sentenceIndexlist:
    #     indexStr = indexStr +

    return '\t'.join(relationList) + 'INNER' + str(sentenceIndexlist)








if __name__ == '__main__':


    # 输出路径
    # outputPath = inout.getDataAnalysisPath('analysis_vote_sentence_fnlp_150w-2100w.txt')
    outputPath = inout.getDataAnalysisPath('test.txt')

    ## 加载停用词列表
    stopWordPath = inout.getResourcePath('stopWordList.txt')
    stopWordList = inout.readListFromTxt(stopWordPath)
    # 这地方加入临时逻辑，后面可以进行停用词合并
    stopWordList = list(set(stopWordList))

    ## 加载关系字典
    relationDic = unsupervised_relation_extraction.persistent_relation_object.getRelationShipDic()


    """
                这里加载数据的处理策略：
                1）从pkl对象直接加载
                2）从文本文件读取数据形成列表
                最后的数据都以列表形式合并成一个总的列表
        """
    sentenceList = []
    sentenceFeatureList = []


    ## 1
    # fnlpListPath = inout.getDataNEMeatPath('sentence_and_feature_150w-900w_fnlp_old.txt')
    fnlpListPath = inout.getDataTestPath('sentence_and_feature_test.txt')

    fnlpOldDataList = inout.readListFromTxt(fnlpListPath)
    print'原始-数据-旧 len:', len(fnlpOldDataList)

    fnlpSentenceList_old, fnlpSentenceFeatureList_old = convertDataFormat(fnlpOldDataList)
    print'处理-数据-旧 len:', len(fnlpSentenceList_old)

    sentenceList.extend(fnlpSentenceList_old)
    sentenceFeatureList.extend(fnlpSentenceFeatureList_old)


    ## 2
    # fnlpNewDataListPath = inout.getDataNEMeatPath('sentence_and_feature_900w-2100w_fnlp_new.txt')
    fnlpNewDataListPath = inout.getDataTestPath('sentence_and_feature_test_new.txt')

    fnlpNewDataList = inout.readListFromTxt(fnlpNewDataListPath)
    print'原始-数据-新 len:', len(fnlpNewDataList)

    fnlpSentenceList_new, fnlpSentenceFeatureList_new = convertNewDataFormat(fnlpNewDataList)
    print'处理-数据-新 len:', len(fnlpSentenceList_new)

    sentenceList.extend(fnlpSentenceList_new)
    sentenceFeatureList.extend(fnlpSentenceFeatureList_new)

    print 'sentenceList len: ', len(sentenceList)
    print 'sentenceFeatureList len: ', len(sentenceFeatureList)
    print '数据加载完毕...'


    sentenceList, sentenceFeatureList = dictDistinct(sentenceList, sentenceFeatureList)
    print len(sentenceList)
    print '句子去重复完成...'

    print '开始处理...'
    startTime = time.time()
    print startTime


    fw = codecs.open(outputPath,'wb')

    for i in tqdm(range(len(sentenceFeatureList))):

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
                relationWordAndSentenceIndexList = getRelationWordList(featureWordList,relationDic,i)

                if relationWordAndSentenceIndexList:
                    ## 归类到字典中

                    relationWordAndSentenceIndexStr = transList2Str(relationWordAndSentenceIndexList)

                    namedEntityPairStr = getNamedEntityPairStr(namedEntityAndTagList)

                    # print namedEntityPairStr
                    # printEscapeStr(relationWordAndSentenceIndexList)
                    # print sentenceList[i]
                    # print '------------------------'

                    outputLine = namedEntityPairStr + 'DIV' + relationWordAndSentenceIndexStr

                    # print outputLine
                    fw.write(outputLine + '\n')

    fw.close()