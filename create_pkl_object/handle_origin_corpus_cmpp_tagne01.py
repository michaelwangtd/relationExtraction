#!/usr/bin/env python
# -*- coding:utf-8 -*-

from utils import inout
from utils.inout import printEscapeStr
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
import index


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


def restoreSentence(sentenceWordList):
    '''
        恢复原始的句子
    '''
    resultList = []
    for item in sentenceWordList:
        resultList.append(item.strip().split('_')[0])
    return ''.join(resultList)


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

    inputFileName = ''

    origin_corpus = inout.getDataOriginPath(inputFileName)
    # origin_corpus = inout.getDataTestPath('origin_corpus_test.txt')

    infoList = inout.readListFromTxt(origin_corpus)

    print '加载数据完毕...'

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

                if lineList:

                    ## 将列表中的多句话分开
                    sentenceSplitList = splitSentenceInLineList(lineList)
                    # for item in sentenceList:
                    #     printEscapeStr(item)

                    # 对每一个句子进行筛选
                    for sentenceWordList in sentenceSplitList:

                        ## 将带词性标注的词列表还原成原始的句子
                        sentence = restoreSentence(sentenceWordList)

                        namedEntityTagTupleList, neTagList = namedEntityRecognize(sentence)

                        namedEntityAndTagList, otherWordList = divideEntityAndOtherWord(namedEntityTagTupleList)

                        if len(namedEntityAndTagList) == 2:

                            sentenceFeatureList.append([namedEntityAndTagList, otherWordList])
                            sentenceList.append(sentence)

                            j = j + 1


    sentencePath = inout.getDataPklPath('sentence_list_corpus_test.pkl')
    sentenceFeaturePath = inout.getDataPklPath('sentence_feature_list_corpus_test.pkl')

    inout.writePersistObject(sentencePath, sentenceList)
    inout.writePersistObject(sentenceFeaturePath, sentenceFeatureList)
    print '持久化完成...'
    print '筛选的句子数量： ', i













