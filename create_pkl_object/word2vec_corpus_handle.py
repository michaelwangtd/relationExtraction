#!/usr/bin/env python
# -*- coding:utf-8 -*-

# import index
from utils import inout
# from utils.inout import printEscapeStr
import codecs
import os


def readListFromTxt(filePath):
    infoList = []
    if os.path.exists(filePath):
        f = codecs.open(filePath,'rb')
        while True:
            line = f.readline()
            if line:
                temp = line.strip()
                infoList.append(temp)
            else:
                break
        f.close()
    return infoList


def stopWordFilter(otherWordList,stopWordList):
    resultList = []

    for item in otherWordList:
        if item not in stopWordList:
            resultList.append(item)
    return resultList



if __name__ == '__main__':
    
    """
        处理sentence_and_feature_150-700_fnlp.txt中的句子
        每一句去除标点符号
        用空格分割
        
        
    """

    inputFilePath = inout.getDataNEMeatPath('sentence_and_feature_150-700_fnlp.txt')
    # inputFilePath = ''

    stopWordFilePath = inout.getResourcePath('stopWordList.txt')
    # stopWordFilePath = ''

    outputFilePath = 'D:\\word2vec_corpus_handled_150-700_cmpp.txt'
    # outputFilePath = ''


    stopWordList = readListFromTxt(stopWordFilePath)

    fw = codecs.open(outputFilePath,'wb')

    fr = codecs.open(inputFilePath,'rb')
    while True:
        line = fr.readline()
        if line:
            lineList = line.strip().split('||')

            if len(lineList) == 3:
                resultList = []
                namedEntityList = lineList[0].split('\t')
                otherWordList = lineList[1].split('_')

                # 停用词过滤
                stopedOtherWordList = stopWordFilter(otherWordList,stopWordList)

                resultList.extend(namedEntityList)
                resultList.extend(stopedOtherWordList)
                # print inout.printEscapeStr(resultList)
                # print resultList
                fw.write(' '.join(resultList) + '\n')
        else:
            break
    fr.close()
    fw.close()