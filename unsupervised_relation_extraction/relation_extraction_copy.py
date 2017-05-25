#!/usr/bin/env python
# -*- coding:utf-8 -*-

from utils import inout
from pyltp import SentenceSplitter
from utils.inout import printList
from utils.inout import printEscapeStr
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
import index
from collections import OrderedDict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

"""
    对实验版本的备份：
    实现关系抽取的一个小例子
"""


def namedEntityRecognize(sentence):
    '''
        使用pyltp模块进行命名实体识别
        返回：1）命名实体和类别元组列表、2）实体类别列表
    '''
    namedEntityTagTupleList = []

    segmentor = Segmentor()
    segmentor.load(inout.getLTPPath(index.CWS))
    words = segmentor.segment(sentence)
    segmentor.release()
    postagger = Postagger()
    postagger.load(inout.getLTPPath(index.POS))
    postags = postagger.postag(words)
    postagger.release()
    recognizer = NamedEntityRecognizer()
    recognizer.load(inout.getLTPPath(index.NER))
    netags = recognizer.recognize(words,postags)
    recognizer.release()

    # 封装成元组形式
    for word,netag in zip(words,netags):
        namedEntityTagTupleList.append((word,netag))

    neTagList = '\t'.join(netags).split('\t')

    return namedEntityTagTupleList,neTagList


def getNamedEntityTypeDic():
    '''
        获取命名实体类别字典
    '''
    neList = ['Nh','Ni','Ns']
    dic = dict()
    for i in range(len(neList)):
        for j in range(len(neList)):
            key = neList[i] + '_' + neList[j]
            dic[key] = []
    return dic


def divideEntityAndOtherWord(namedEntityTagTupleList):
    '''
        将列表中的命名实体和其他词分开
    '''
    namedEntityList = []
    otherWordList = []
    for tupleItem in namedEntityTagTupleList:
        if tupleItem[1] in ['O']:
            otherWordList.append(tupleItem[0])
        elif tupleItem[1] not in ['O']:
            namedEntityList.append(tupleItem)
    return namedEntityList,otherWordList


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


def updateNeTypeDic(namedEntityAndTagList,featureWordList,neTypeDic):
    '''

    '''
    namedEntityList = []
    typeTag = []
    for namedEntity in namedEntityAndTagList:
        namedEntityList.append(namedEntity[0])
        typeTag.append(namedEntity[1][-2:])
    typeTagKey = '_'.join(typeTag)
    if typeTagKey in neTypeDic.keys():
        neTypeDic[typeTagKey].append([namedEntityList,featureWordList])


def getFieldFeatureWordList(fieldClassifiedList):
    '''
        获取分类的领域内所有实体对的上下文的特征词集合
    '''
    fieldFeatureWordList = []
    for item in fieldClassifiedList:
        fieldFeatureWordList.extend(item[1])
    return fieldFeatureWordList


def getWordDocumentFrequencyStatisticList(fieldClassifiedList):
    '''

    '''
    resultList = []
    for itemList in fieldClassifiedList:
        resultList.extend(set(itemList[1]))
    return resultList


def getFeatureValueTemplateList(documentFrequencyStatisticList):
    '''
        去重
    '''
    return list(set(documentFrequencyStatisticList))


def createFieldFeatureValueList(fieldClassifiedList):
    '''
        将分类的领域列表中的特征词列表转换成数值特征向量的形式；
        特征词转换为数值特征向量;
        TFITF计算
    :param fieldClassifiedList: [[['马季', '侯宝林'], ['著名', '相声', '家', '师傅']], [['马季', '侯宝林'], ['师傅', '我国', '相声界', '鼻祖']], [['王祖蓝', '王茂'], ['二十', '年', '前', '小名']], [['王祖蓝', '王茂'], ['小名', '变']]]
    :return:
    '''

    # 初始化领域特征值列表
    fieldFeatureValueList = []

    # 初始化特征值索引映射字典
    featureValueIndexMapDic = dict()

    # 1 获取总的上下文列表数documentNum
    documentNum = len(fieldClassifiedList)

    # 2 获取词文档频率统计列表documentFrequencyStatisticList
    documentFrequencyStatisticList = getWordDocumentFrequencyStatisticList(fieldClassifiedList)
    printEscapeStr(documentFrequencyStatisticList)

    # 3 获取特征值向量模板列表
    featureValueTemplateList = getFeatureValueTemplateList(documentFrequencyStatisticList)
    printEscapeStr(featureValueTemplateList)

    ## 计算特征值
    for i in range(len(fieldClassifiedList)):
        # 初始化特征值数组
        featureValueVector = np.zeros((len(featureValueTemplateList)))
        contextWordList = fieldClassifiedList[i][1]
        printEscapeStr(contextWordList)

        for j in range(len(featureValueTemplateList)):
            if featureValueTemplateList[j] in contextWordList:
                # 计算tf-idf值
                candidateWord = featureValueTemplateList[j]
                featureValue = (1 + np.log(contextWordList.count(candidateWord))) * np.log(documentNum / documentFrequencyStatisticList.count(candidateWord))
                featureValueVector[j] = featureValue

        # 组装领域特征值列表
        fieldFeatureValueList.append([fieldClassifiedList[i][0],featureValueVector])
        # 组装特征值索引映射字典
        featureValueIndexMapDic[str(list(featureValueVector))] = i

    return fieldFeatureValueList,featureValueIndexMapDic


def extractClusterData(fieldFeatureValueList):
    '''
        组装成数组形式
    '''
    trainData = []
    for item in fieldFeatureValueList:
        trainData.append(item[1])
    trainData = np.array(trainData)
    return trainData


def getContextWordSetList(contextList):
    '''

    '''
    resultList = []
    for item in contextList:
        resultList.extend(list(set(item)))
    return resultList


def getNamedEntityPairClassifySetList(clusterList):
    '''
        将上下文聚类的结果集中不同的实体对分开
    '''
    resultList = []
    dic = dict()

    for item in clusterList:
        nePair = '_'.join(item[0])
        if nePair not in dic.keys():
            dic[nePair] = []
        dic[nePair].append(item[1])

    for nePair,contextList in dic.items():
        ## 这里可以对contextList进行筛选，暂时不进行筛选
        # 获取context word set list
        contextWordSetList = getContextWordSetList(contextList)
        resultList.append([nePair,len(contextList),contextWordSetList])
    return resultList

def getNameEntityPairClusterSetList(clusterList):
    '''

    '''
    resultList = []
    dic = dict()

    nePairNameList = []
    tempList = []
    for item in clusterList:
        nePairNameList.append('_'.join(item[0]))
        tempList.append(item[1])
    nePairNameStr = '-'.join(nePairNameList)
    dic[nePairNameStr] = tempList

    for nePair,contextList in dic.items():
        ## 这里可以对contextList进行筛选，暂时不进行筛选
        # 获取context word set list
        contextWordSetList = getContextWordSetList(contextList)
        resultList.append([nePair,len(contextList),contextWordSetList])
    return resultList



def createNEPairClassifyDic(clusterDic):
    '''
        将命名实体对作为key值
        同一命名实体对的上下文特征作为列表
        生成命名实体对不重复的字典
        字典形式： key : named entity pair(String)
                  value : [context list num(int) , feature word list(list)]
    '''

    clusteredAllFeatureWordList = []
    nePairClassifyDic = dict()
    if clusterDic:
        for clusterNum,clusterList in clusterDic.items():
            # 这里的clusterList是聚类的结果
            # 要加入判断去除命名实体对重复的逻辑
            # namedEntityPairClassifySetList = getNamedEntityPairClassifySetList(clusterList)

            namedEntityPairSetList = getNameEntityPairClusterSetList(clusterList)

            for item in namedEntityPairSetList:
                if item[0] not in nePairClassifyDic.keys():
                    nePairClassifyDic[item[0]] = [item[1],item[2]]
                    clusteredAllFeatureWordList.extend(item[2])
    clusteredAllFeatureWordSetList = list(set(clusteredAllFeatureWordList))
    return nePairClassifyDic,clusteredAllFeatureWordSetList


def getWCik(featureWord,relatedList):
    '''
        根据特征词featureWord，计算WCik的权重值
    '''
    countFik = relatedList[-1].count(featureWord)
    WCik = np.log2(countFik + 1) / np.log2(relatedList[0] + 1)
    return WCik


def getFeatureWordCCiWeightMap(nePairClassifyDic,clusteredAllFeatureWordSetList):
    '''
        这个接口应该是高扩展的
    '''
    CCiMapDic = dict()

    # 聚类总数
    clusterSumNum = len(nePairClassifyDic)

    for featureWord in clusteredAllFeatureWordSetList:
        # WCik权重的最大值
        maxWCik = 0.0
        # Sum WCik 权重的总数
        SumWCik = 0.0
        for nePair,relatedList in nePairClassifyDic.items():
            if featureWord in relatedList[-1]:
                # 获取WCik权重
                tempWCik = getWCik(featureWord,relatedList)
                if tempWCik > maxWCik:
                    maxWCik = tempWCik
                SumWCik = SumWCik + tempWCik
        # print 'maxWCik: ',maxWCik
        # print 'SumWCik: ',SumWCik
        # 计算CCi

        fWCCi = np.log((clusterSumNum * maxWCik) / SumWCik) * (1 / np.log(clusterSumNum))
        CCiMapDic[featureWord] = fWCCi
    return CCiMapDic


def getWik(WCik,CCi):
    '''
        根据WCik和CCi计算featureWord的最终权重
    '''
    Wik = (np.square(WCik) * np.square(CCi)) / (np.sqrt(np.square(WCik) + np.square(CCi)))
    return Wik


def calculateFeatureWordWeight(nePairClassifyDic,featureWordCCiWeightMap):
    '''
        根据CCi映射列表和WCik权重值，计算每个特征词的权重
    '''
    dic = dict()
    for nePair,relatedList in nePairClassifyDic.items():
        if nePair not in dic.keys():
            featureWordWeightList = []
            for featureWord in relatedList[-1]:
                tempWCik = getWCik(featureWord,relatedList)
                # 计算最终权重
                Wik = getWik(tempWCik,featureWordCCiWeightMap[featureWord])
                if (featureWord,Wik) not in featureWordWeightList:
                    featureWordWeightList.append((featureWord,Wik))
            # printEscapeStr(featureWordWeightList)
            featureWordWeightList = sorted(featureWordWeightList,key=lambda item:item[-1],reverse=True)
            dic[nePair] = featureWordWeightList
    return dic


if __name__ == '__main__':

    pd.set_option('display.width', 300)
    np.set_printoptions(linewidth=300, suppress=True)

    corpusPath = inout.getDataOriginPath('special_corpus.txt')
    corpus = inout.onlyReadLine(corpusPath)

    ## 加载停用词列表
    stopWordPath = inout.getResourcePath('stopWordList.txt')
    stopWordList = inout.readListFromTxt(stopWordPath)

    ## 1 对于复杂的文本数据要进行清洗
    sentences = SentenceSplitter.split(corpus)
    sentences = '\t'.join(sentences)#.decode('utf-8')
    sentenceList = sentences.split('\t')
    printList(sentenceList)

    # 命名实体类别字典
    neTypeDic = getNamedEntityTypeDic()

    for sentence in sentenceList:
        ## 2 提取命名实体
        namedEntityTagTupleList,neTagList = namedEntityRecognize(sentence)
        printEscapeStr(namedEntityTagTupleList)
        printEscapeStr(neTagList)
        ## 3 分割实体和其他词
        namedEntityAndTagList,otherWordList = divideEntityAndOtherWord(namedEntityTagTupleList)
        printEscapeStr(namedEntityAndTagList)
        printEscapeStr(otherWordList)
        ## 4 其他词去掉停用词
        featureWordList = removeStopWord(otherWordList,stopWordList)
        printEscapeStr(featureWordList)
        ## 5 将实体对和特征词添加进实体类型列表
        updateNeTypeDic(namedEntityAndTagList,featureWordList,neTypeDic)

    # 聚类之后再分类的结果暂时存储在list中[dict1(),dict2()]
    clusterResultListAll = []
    # exit(0)

    ## 6 分领域分不同的实体标签类别处理数据
    for tagTypeKey,fieldClassifiedList in neTypeDic.items():
        if fieldClassifiedList:
            printEscapeStr(fieldClassifiedList)

            ## 7 生成域分类特征向量列表 和 特征值，索引映射字典
            fieldFeatureValueList, featureValueIndexMapDic = createFieldFeatureValueList(fieldClassifiedList)
            printEscapeStr(fieldFeatureValueList)
            printEscapeStr(featureValueIndexMapDic)
            ## 聚类
            ## 8 准备聚类数据
            clusterTrainData = extractClusterData(fieldFeatureValueList)

            ## 9 cluster
            n_clusters = 2
            random_state = 170
            y_hat = KMeans(n_clusters=n_clusters,random_state=random_state).fit_predict(clusterTrainData)
            print y_hat
            typeDic = dict()
            typeDic[tagTypeKey] = dict()

            ## 10 聚类结果进行分类
            for k in range(len(y_hat)):
                if y_hat[k] not in typeDic[tagTypeKey].keys():
                    typeDic[tagTypeKey][y_hat[k]] = []
                typeDic[tagTypeKey][y_hat[k]].append(fieldClassifiedList[k])


            clusterResultListAll.append(typeDic)



    ## 11 识别可鉴别词，对实体对标记关系，这里计算准则依据DCM方案（Discriminative Category Matching）
    for typeDic in clusterResultListAll:

        # 命名实体对类别
        nePairType = typeDic.keys()[0]
        print '命名实体类别： ',nePairType
        clusterDic = typeDic[nePairType]    # [[['王祖蓝', '王茂'], ['二十', '年', '前', '小名']], [['王祖蓝', '王茂'], ['小名', '变']]]

        for k,v in clusterDic.items():
            printEscapeStr(k)
            printEscapeStr(v)

        ## 12 整理clusterDic字典，将clusterDic转换为nePairClassifyDic命名实体对分类字典
        nePairClassifyDic,clusteredAllFeatureWordSetList = createNEPairClassifyDic(clusterDic)
        printEscapeStr(nePairClassifyDic)
        printEscapeStr(clusteredAllFeatureWordSetList)
        # exit(0)


        ## 13 计算同一实体对类别下命名实体对下所有特征词的类间特征权重（CCi权重）
        featureWordCCiWeightMap = getFeatureWordCCiWeightMap(nePairClassifyDic,clusteredAllFeatureWordSetList)
        printEscapeStr(featureWordCCiWeightMap)
        ## 14 计算命名实体对分类字典中各个特征词的权重
        labelWordWeightDic = calculateFeatureWordWeight(nePairClassifyDic,featureWordCCiWeightMap)
        printEscapeStr(labelWordWeightDic)
        ## 结果输出
        print '--------------------'
        for k,v in labelWordWeightDic.items():
            print k
            printEscapeStr(v)
























