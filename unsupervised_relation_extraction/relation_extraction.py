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
    # printEscapeStr(namedEntityList)
    # printEscapeStr(otherWordList)
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
    fieldFeatureWordList = []
    for item in fieldClassifiedList:
        fieldFeatureWordList.extend(item[1])
    return fieldFeatureWordList



if __name__ == '__main__':

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

    neTypeDic = getNamedEntityTypeDic()

    for sentence in sentenceList:
        ## 2 提取命名实体
        namedEntityTagTupleList,neTagList = namedEntityRecognize(sentence)
        # printEscapeStr(namedEntityTagTupleList)
        # printEscapeStr(neTagList)
        ## 3 分割实体和其他词
        namedEntityAndTagList,otherWordList = divideEntityAndOtherWord(namedEntityTagTupleList)
        # printEscapeStr(namedEntityList)
        ## 4 其他词去掉停用词
        featureWordList = removeStopWord(otherWordList,stopWordList)
        # printEscapeStr(featureWordList)
        ## 5 将实体对和特征词添加进实体类型列表
        updateNeTypeDic(namedEntityAndTagList,featureWordList,neTypeDic)

    ## 6 分领域分不同的实体标签类别处理数据
    for tagTypeKey,fieldClassifiedList in neTypeDic.items():
        if fieldClassifiedList:
            ## 7 获取域类别下所有的特征词
            fieldFeatureWordBagList = getFieldFeatureWordList(fieldClassifiedList)
            printEscapeStr(fieldFeatureWordBagList)
            ## 计算特征向量

