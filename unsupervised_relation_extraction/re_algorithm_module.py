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
from unsupervised_relation_extraction import persistent_relation_object

"""
   这里作为独立的算法模块
   程序入口参数为:sentenceList、sentenceFeatureList对象
        sentenceList:
        sentenceFeatureList:[[(ne1-type)],[other word list]]
"""


def namedEntityRecognize(sentence):
    '''
        使用pyltp模块进行命名实体识别
        返回：1）命名实体和类别元组列表、2）实体类别列表
    '''
    namedEntityTagTupleList = []

    segmentor = Segmentor()
    # segmentor.load(inout.getLTPPath(index.CWS))
    segmentor.load_with_lexicon(inout.getLTPPath(index.CWS),inout.getResourcePath('userDic.txt'))
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
    ## !!! 这里增加合并同一命名实体的功能
    namedEntityList = mergeNamedEntity(namedEntityList)

    # printEscapeStr(namedEntityList)
    # printEscapeStr(otherWordList)
    return namedEntityList,otherWordList

def mergeNamedEntity(namedEntityList):
    '''

    '''
    unzipList = zip(*namedEntityList)
    neWordList = unzipList[0]
    indexList = unzipList[1]
    finalNamedEntityList = []
    for i in range(len(indexList)):
        if 'B' in indexList[i]:
            if i + 1 < len(indexList):
                if 'I' in indexList[i + 1]:
                    if i + 2 < len(indexList):
                        if 'E' in indexList[i + 2]:
                            ne = neWordList[i] + neWordList[i + 1] + neWordList[i + 2]
                            # print ne
                            type = 'S' + '-' +indexList[i].split('-')[-1]
                            finalNamedEntityList.append((ne,type))
            if i + 1 < len(indexList):
                if 'E' in indexList[i + 1]:
                    ne = neWordList[i] + neWordList[i + 1]
                    # print ne
                    type = 'S' + '-' + indexList[i].split('-')[-1]
                    finalNamedEntityList.append((ne,type))
        if 'S' in indexList[i]:
            ne = neWordList[i]
            # print ne
            finalNamedEntityList.append((ne,indexList[i]))
    return finalNamedEntityList


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


def updateNeTypeDic(namedEntityAndTagList,featureWordList,originSentenceI,neTypeDic):
    '''

    '''
    namedEntityList = []
    typeTag = []
    for namedEntity in namedEntityAndTagList:
        namedEntityList.append(namedEntity[0])
        typeTag.append(namedEntity[1][-2:])
    typeTagKey = '_'.join(typeTag)
    if typeTagKey in neTypeDic.keys():
        neTypeDic[typeTagKey].append([originSentenceI,namedEntityList,featureWordList])


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
        resultList.extend(set(itemList[2]))
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
    # printEscapeStr(documentFrequencyStatisticList)
    # 3 获取特征值向量模板列表
    featureValueTemplateList = getFeatureValueTemplateList(documentFrequencyStatisticList)
    # printEscapeStr(featureValueTemplateList)
    ## 计算特征值
    for i in range(len(fieldClassifiedList)):
        # 初始化特征值数组
        featureValueVector = np.zeros((len(featureValueTemplateList)))
        contextWordList = fieldClassifiedList[i][2]
        for j in range(len(featureValueTemplateList)):
            if featureValueTemplateList[j] in contextWordList:
                # printEscapeStr(featureValueTemplateList[j])
                # 计算tf-idf值
                candidateWord = featureValueTemplateList[j]
                featureValue = (1 + np.log(contextWordList.count(candidateWord))) * np.log(documentNum / documentFrequencyStatisticList.count(candidateWord))
                featureValueVector[j] = featureValue
        # 组装领域特征值列表
        fieldFeatureValueList.append([fieldClassifiedList[i][1],featureValueVector])
        # 组装特征值索引映射字典
        featureValueIndexMapDic[str(list(featureValueVector))] = i

    return fieldFeatureValueList,featureValueIndexMapDic,featureValueTemplateList


def extractClusterData(fieldFeatureValueList):
    '''
        组装成数组形式
    '''
    trainData = []
    for item in fieldFeatureValueList:
        trainData.append(item[1])
    trainData = np.array(trainData)
    # print type(trainData)
    # print trainData.shape
    # print trainData
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
        nePairNameList.append('_'.join(item[1]) + '|' + str(item[0]))
        tempList.append(item[2])
    nePairNameList = list(set(nePairNameList))
    nePairNameStr = '    '.join(nePairNameList)
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
        # printEscapeStr(clusterDic)
        for clusterNum,clusterList in clusterDic.items():
            # 这里的clusterList是聚类的结果
            # 要加入判断去除命名实体对重复的逻辑
            # namedEntityPairClassifySetList = getNamedEntityPairClassifySetList(clusterList)

            namedEntityPairSetList = getNameEntityPairClusterSetList(clusterList)
            # print '------------------'
            # printEscapeStr(namedEntityPairSetList)
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
    countFik = relatedList[1].count(featureWord)
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
            if featureWord in relatedList[1]:
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
            for featureWord in relatedList[1]:
                tempWCik = getWCik(featureWord,relatedList)
                # 计算最终权重
                Wik = getWik(tempWCik,featureWordCCiWeightMap[featureWord])
                if (featureWord,Wik) not in featureWordWeightList:
                    featureWordWeightList.append((featureWord,Wik))
            # printEscapeStr(featureWordWeightList)
            featureWordWeightList = sorted(featureWordWeightList,key=lambda item:item[-1],reverse=True)
            dic[nePair] = featureWordWeightList
    return dic


def isHaveCandidateRelationWordMapping(featureWordList,relationDic):
    '''
        是否有候选关系映射判断
    '''
    for i in range(len(featureWordList)):
        for key,valueList in relationDic.items():
            if featureWordList[i] in valueList:
                return True
    return False


def candidateRelationWordMapping(featureWordList,relationDic):
    '''
        发现候选关系并进行关系映射，关系归一化处理
    '''

    for i in range(len(featureWordList)):
        for key,valueList in relationDic.items():
            if featureWordList[i] in valueList:
                featureWordList[i] = key
                break
    return featureWordList


def getLabelWeightOutputStr(labelWordWeightList):
    '''

    '''
    resultStr = ''
    for item in labelWordWeightList:
        resultStr = resultStr + '(' + str(item[0]) + ',' + str(item[1]) + ')' + ','
    return resultStr


if __name__ == '__main__':

    ## 输入参数
    n_cluster = 250

    corpusNum = 200

    analysisPath = inout.getDataAnalysisPath('analysis.txt')

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
    sentencePath = inout.getDataOriginPath('sentence_list_corpus.pkl')
    sentenceFeaturePath = inout.getDataOriginPath('sentence_feature_list_corpus.pkl')

    sentenceList,slType = inout.readPersistObject(sentencePath)
    sentenceFeatureList,sflType = inout.readPersistObject(sentenceFeaturePath)

    ## 这里对语料个数进行控制
    # sentenceList = sentenceList[:corpusNum]
    # sentenceFeatureList = sentenceFeatureList[:corpusNum]

    # exit(0)

    # 命名实体类别字典
    neTypeDic = getNamedEntityTypeDic()

    # 统计句子中有实体关系，且进行实体关系映射的数目
    # k = 0
    for originSentenceI in range(len(sentenceList)):

        namedEntityAndTagList = sentenceFeatureList[originSentenceI][0]
        otherWordList = sentenceFeatureList[originSentenceI][1]

        ##  其他词去掉停用词
        featureWordList = removeStopWord(otherWordList,stopWordList)
        # printEscapeStr(featureWordList)
        # exit(0)

        ##  去掉特征词中的一个字的词和数字
        featureWordList = removeOneLengthWord(featureWordList)
        # printEscapeStr(featureWordList)

        if featureWordList:

            ## 4.4 进行是否有候选关系映射的判断
            if isHaveCandidateRelationWordMapping(featureWordList,relationDic):

                ## 4.5 候选关系词进行映射
                featureWordList = candidateRelationWordMapping(featureWordList,relationDic)
                # printEscapeStr(featureWordList)

                ## 5 将实体对和特征词添加进实体类型列表
                updateNeTypeDic(namedEntityAndTagList,featureWordList,originSentenceI,neTypeDic)

                # k = k + 1

    print '人物实体类型句子总数： ',len(neTypeDic['Nh_Nh'])

    # print '筛选后句子数量： ',k

    # NhList = neTypeDic['Nh_Nh']
    # for item in NhList:
    #     printEscapeStr(item)
    # print len(NhList)
    # exit(0)

    # 聚类之后再分类的结果暂时存储在list中[dict1(),dict2()]
    clusterResultListAll = []

    ## 6 分领域分不同的实体标签类别处理数据
    # print len(neTypeDic)

    for tagTypeKey,fieldClassifiedList in neTypeDic.items():
        if fieldClassifiedList:

            print '当前只有这一个类别：',tagTypeKey,
            # printEscapeStr(fieldClassifiedList)
            # for item in fieldClassifiedList:
                # printEscapeStr(item)
            # exit(0)

            ## 7 生成域分类特征向量列表 和 特征值，索引映射字典
            fieldFeatureValueList, featureValueIndexMapDic,featureValueTemplateList = createFieldFeatureValueList(fieldClassifiedList)
            # printEscapeStr(fieldFeatureValueList)
            # printEscapeStr(featureValueIndexMapDic)
            # printEscapeStr(featureValueTemplateList)
            # exit(0)

            ## 聚类
            ## 8 准备聚类数据
            clusterTrainData = extractClusterData(fieldFeatureValueList)
            # print clusterTrainData
            # print clusterTrainData.shape

            # exit(0)
            ## 9 cluster
            random_state = 200

            # y_hat = KMeans(n_clusters=n_clusters,random_state=random_state).fit_predict(clusterTrainData)
            # print type(y_hat)
            # print y_hat.shape

            model = KMeans(n_clusters=n_cluster)
            clustered = model.fit(clusterTrainData)

            print '\n-----------------------'
            print '聚类中心个数：', len(clustered.cluster_centers_)
            # print clustered.cluster_centers_
            print '样本点到所属簇中心距离之和（数值越小越说明聚类中心点越准确）：', clustered.inertia_
            y_hat = clustered.labels_
            print '样本所属类标记：',len(y_hat),y_hat


            typeDic = dict()
            typeDic[tagTypeKey] = dict()
            ## 10 聚类结果进行分类
            for k in range(len(y_hat)):
                if y_hat[k] not in typeDic[tagTypeKey].keys():
                    typeDic[tagTypeKey][y_hat[k]] = []
                typeDic[tagTypeKey][y_hat[k]].append(fieldClassifiedList[k])

            clusterResultListAll.append(typeDic)
            # printEscapeStr(typeDic[tagTypeKey].keys())
            # for k,v in typeDic[tagTypeKey].items():
            #     print k
            #     print '下面是聚类结果：'
            #     printEscapeStr(v)
    # exit(0)

    fw = open(analysisPath, 'wb')

    ## 11 识别可鉴别词，对实体对标记关系，这里计算准则依据DCM方案（Discriminative Category Matching）
    # print 'clusterResultListAll len: ',len(clusterResultListAll)
    for typeDic in clusterResultListAll:

        # 命名实体对类别
        nePairType = typeDic.keys()[0]
        print '命名实体类别： ',nePairType
        clusterDic = typeDic[nePairType]    # [[['王祖蓝', '王茂'], ['二十', '年', '前', '小名']], [['王祖蓝', '王茂'], ['小名', '变']]]

        ## 这里因为数据量少，没有出现同一个已经聚类的类别中出现不同命名实体对的情况
        ## 后面更换数据后，可以在进行下面的数据整理操作时添加：将同一聚类类别中不同命名实体对分开的操作
        # print 'clusterDic:'
        # printEscapeStr(clusterDic)
        # exit(0)

        ## 12 整理clusterDic字典，将clusterDic转换为nePairClassifyDic命名实体对分类字典
        nePairClassifyDic,clusteredAllFeatureWordSetList = createNEPairClassifyDic(clusterDic)
        # printEscapeStr(nePairClassifyDic)
        # exit(0)

        # print len(nePairClassifyDic)
        # for k,v in nePairClassifyDic.items():
        #     print k
        #     printEscapeStr(v)
        # printEscapeStr(clusteredAllFeatureWordSetList)
        # print '-------------------'
        # exit(0)

        ## 13 计算同一实体对类别下命名实体对下所有特征词的类间特征权重（CCi权重）
        featureWordCCiWeightMap = getFeatureWordCCiWeightMap(nePairClassifyDic,clusteredAllFeatureWordSetList)

        ## 14 计算命名实体对分类字典中各个特征词的权重
        labelWordWeightDic = calculateFeatureWordWeight(nePairClassifyDic,featureWordCCiWeightMap)
        # printEscapeStr(labelWordWeightDic)


        relationList = relationDic.keys()
        for nePairStr,labelWordWeightList in labelWordWeightDic.items():
            outputLine = ''
            # 处理 key
            outputSentenceList = []
            nePairList = []
            nePairStrList = nePairStr.split('    ')
            for item in nePairStrList:
                outputSentenceList.append(sentenceList[int(item.split('|')[1])])
                if item.split('|')[0] not in nePairList:
                    nePairList.append(item.split('|')[0])
            # 处理 value
            targetLabelWordList = []
            for item in labelWordWeightList:
                if item[0] in relationList:
                   targetLabelWordList.append(item[0])

            if not targetLabelWordList:
                targetLabelWordStr = 'Null'
            else:
                targetLabelWordStr = ' >> '.join(targetLabelWordList)
            outputLine = '---------------\n' + '聚类内个数：' + str(len(outputSentenceList)) + '\n' + '\n'.join(outputSentenceList) +\
                         '\n' + '    '.join(nePairList) + '\n' + '候选关系：' + targetLabelWordStr

            # 处理labelWeightList
            labelWordWeightStr = getLabelWeightOutputStr(labelWordWeightList)

            # print outputLine
            # printEscapeStr(labelWordWeightList)

            outputLine = outputLine + '\n' + labelWordWeightStr

            fw.write(outputLine + '\n')

    fw.close()
    print '程序结束...'
























