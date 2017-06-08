#!/usr/bin/env python
# -*- coding:utf-8 -*-

import index
from utils import inout
from utils.inout import printEscapeStr


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


def restoreSentence(sentenceWordList):
    '''
        恢复原始的句子
    '''
    resultList = []
    for item in sentenceWordList:
        resultList.append(item.strip().split('_')[0])
    return ''.join(resultList)


if __name__ == '__main__':




    """
        1 如果从cmpp里获取文章的时候，出现断断续续的情况
          在这里将几个部分的文件合并形成一个完整的origin_corpus文件
    """
    # rootPath = 'D:\\data_relation_extraction\\resource\\cmpp'
    #
    # inpPath_01 = rootPath + '\\origin_corpus_1000000_1250000.txt'
    # inpPath_02 = rootPath + '\\origin_corpus_1250000_1500000.txt'
    #
    # outpPath = inout.getDataOriginPath('origin_corpus_100w-150w.txt')
    #
    # infoList1 = inout.readListFromTxt(inpPath_01)
    # print len(infoList1)
    # # exit(0)
    #
    # infoList2 = inout.readListFromTxt(inpPath_02)
    # print len(infoList2)
    #
    # infoList1.extend(infoList2)
    #
    # inout.writeList2Txt(outpPath,infoList1)
    # print '生成新文件完成...'





    """
        2 
        筛选、过滤
        从原始语料中提取出完整的句子
        将句子保存到文本中
        
        组合成原始的完整句子
        这一部分已经在java上实现了
    """
    # origin_corpus = inout.getDataOriginPath('origin_corpus_100w-150w.txt')
    #
    # outPath = inout.getDataSentencePath('sentence_100w-150w.txt')
    #
    # infoList = inout.readListFromTxt(origin_corpus)
    #
    # print '加载数据完毕...'
    #
    # sentenceList = []
    #
    # door = 3 * 7
    #
    # for i in range(len(infoList)):
    #     line = infoList[i].strip()
    #     if line:
    #         if line != '_w  _w':
    #             if 'http://' not in line:
    #                 lineList = line.split(' ')
    #
    #                 ## 提取有效的词性标注元素
    #                 lineList = getNewLineList(lineList)
    #                 # printEscapeStr(lineList)
    #
    #                 if lineList:
    #                     ## 将列表中的多句话分开
    #                     sentenceSplitList = splitSentenceInLineList(lineList)
    #
    #                     # 对每一个句子进行筛选
    #                     for sentenceWordList in sentenceSplitList:
    #
    #                         ## 将带词性标注的词列表还原成原始的句子
    #                         sentence = restoreSentence(sentenceWordList)
    #
    #                         if len(sentence) > door:
    #
    #                             ## 这里主要进行筛选工作
    #                             sentence = sentence.replace('&quot;','').replace('&nbsp;','').replace('8&middot','')\
    #                                 .replace('&middot;','')
    #
    #                             sentence.replace('【推荐阅读】','').replace('推特原文：','').replace('人民日报：','')
    #
    #                             if sentence:
    #
    #                                 sentenceList.append(sentence.strip())
    #
    # print 'sentence list length：' ,len(sentenceList)
    #
    # inout.writeList2Txt(outPath,sentenceList)
    #
    # print '写入完成...'





    """
        3 提取命名实体
          这里因为要分布式的跑，所以要写几个文件
          这里写一个模板文件
          基本就是：读一条；处理一条；写一条
          
          在进行命名实体识别之前对数据进行分组分批处理
    """
    ## 这部分将50w为单位的数据分割成5个10w的句子，存储在文本中

    originFilePath = inout.getDataSentencePath('sentence_0-50w.txt')

    infoList = inout.readListFromTxt(originFilePath)

    print len(infoList)

    candy_01 = infoList[:100000]
    candy_02 = infoList[100000:200000]
    candy_03 = infoList[200000:300000]
    candy_04 = infoList[300000:400000]
    candy_05 = infoList[400000:500000]

    outPath_01 = inout.getDataNECandyPath('sentence_0w-10w.txt')
    outPath_02 = inout.getDataNECandyPath('sentence_10w-20w.txt')
    outPath_03 = inout.getDataNECandyPath('sentence_20w-30w.txt')
    outPath_04 = inout.getDataNECandyPath('sentence_30w-40w.txt')
    outPath_05 = inout.getDataNECandyPath('sentence_40w-50w.txt')

    inout.writeList2Txt(outPath_01,candy_01)
    print '01 写入完成...'
    inout.writeList2Txt(outPath_02,candy_02)
    print '02 写入完成...'
    inout.writeList2Txt(outPath_03,candy_03)
    print '03 写入完成...'
    inout.writeList2Txt(outPath_04,candy_04)
    print '04 写入完成...'
    inout.writeList2Txt(outPath_05,candy_05)
    print '05 写入完成...'









