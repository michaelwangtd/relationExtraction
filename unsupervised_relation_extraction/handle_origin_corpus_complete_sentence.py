#!/usr/bin/env python
# -*- coding:utf-8 -*-

from utils import inout
from utils.inout import printEscapeStr
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
import index



def getSentenceList(infoList):
    '''
        从文本中筛选出句子
    '''
    resultList = []
    for line in infoList:
        if line.strip():
            if 'originText' in line:
                lineList = line.split('Text:')
                sentence = lineList[1].strip()
                resultList.append(sentence)
    return resultList


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


def divideEntityAndOtherWord(namedEntityTagTupleList):
    '''
        将列表中的命名实体和其他词分开
    '''
    personEntityTypeList = ['S-Nh','B-Nh','I-Nh','E-Nh']

    namedEntityList = []
    otherWordList = []
    for tupleItem in namedEntityTagTupleList:

        ''' 
        要修改这段逻辑
        if tupleItem[1] in ['O']:
            otherWordList.append(tupleItem[0])
        elif tupleItem[1] not in ['O']:
            namedEntityList.append(tupleItem)
        '''
        # 这里的逻辑被修改为：只提取人物命名实体
        if tupleItem[1] in personEntityTypeList:
            namedEntityList.append(tupleItem)
        else:
            otherWordList.append(tupleItem[0])
    ## !!! 这里增加合并同一命名实体的功能
    if namedEntityList:
        # printEscapeStr(namedEntityList)
        namedEntityList = mergeNamedEntity(namedEntityList)

    # printEscapeStr(namedEntityList)
    # printEscapeStr(otherWordList)
    return namedEntityList,otherWordList


def mergeNamedEntity(namedEntityList):
    '''
        合并同一命名实体
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



if __name__ == '__main__':

    origin_corpus = inout.getDataOriginPath('origin_corpus_test.txt')

    infoList = inout.readListFromTxt(origin_corpus)

    # 加入从文本中过滤句子的逻辑
    infoList = getSentenceList(infoList)
    print '原始总的句子个数： ',len(infoList)
    # exit(0)

    # 初始化两个同步的列表
    sentenceList = []
    sentenceFeatureList = []

    i = 0
    ## 命名实体识别
    for sentence in infoList:

        namedEntityTagTupleList, neTagList = namedEntityRecognize(sentence)

        namedEntityAndTagList, otherWordList = divideEntityAndOtherWord(namedEntityTagTupleList)

        # printEscapeStr(namedEntityAndTagList)
        # printEscapeStr(otherWordList)

        if len(namedEntityAndTagList) == 2:
            i = i + 1
            sentenceFeatureList.append([namedEntityAndTagList,otherWordList])
            sentenceList.append(sentence)
            printEscapeStr(namedEntityAndTagList)

    # 这里要持久化两个对象：sentenceList、sentenceFeatureList
    # sentencePath = inout.getDataPklPath('sentence_list_corpus_complete_sentence.pkl')
    # sentenceFeaturePath = inout.getDataPklPath('sentence_feature_list_corpus_complete_sentence.pkl')

    sentencePath = inout.getDataPklPath('sentence_list_corpus_test.pkl')
    sentenceFeaturePath = inout.getDataPklPath('sentence_feature_list_corpus_test.pkl')

    inout.writePersistObject(sentencePath, sentenceList)
    inout.writePersistObject(sentenceFeaturePath, sentenceFeatureList)
    print '持久化完成...'
    print '筛选的句子数量： ',i





