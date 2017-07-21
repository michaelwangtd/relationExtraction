# -*- coding:utf-8 -*-

from tqdm import tqdm
import os
from utils import inout
import codecs
from collections import OrderedDict


def getSentenceStrList(sentenceIndexList,sentenceList):
    '''

    '''
    outputStr = ''
    for index in sentenceIndexList:
        outputStr = outputStr + sentenceList[int(index)].strip() + '\n'
    return outputStr


if __name__ == '__main__':

    # inFilePath = inout.getDataAnalysisPath('vote_relation_weight_result_fnlp_150w-2000w.txt')
    inFilePath = inout.getDataAnalysisPath('test.txt')
    infoList = inout.readListFromTxt(inFilePath)
    print '关系权重列表长度:', len(infoList)

    outFilePath = inout.getDataAnalysisPath('map_vote_relation_ordered_result_fnlp_150w-2000w.txt')

    sentenceFilePath = inout.getDataAnalysisPath('sentenceList.txt')
    sentenceList = inout.readListFromTxt(sentenceFilePath)
    print '句子列表长度:', len(sentenceList)

    # 初始化字典
    classifyDic = dict()

    print '归类：'
    for i in tqdm(range(len(infoList))):
        divSplitList = infoList[i].split('DIV')
        if len(divSplitList) == 2:

            neStr = divSplitList[0]
            neList = neStr.split('\t')
            neReversedStr = ''
            if len(neList) == 2:
                neReversedStr = neList[1] + '\t' + neList[0]

            otherStr = divSplitList[1]

            if neStr!='' and neReversedStr!='':
                if neStr not in classifyDic.keys() and neReversedStr not in classifyDic.keys():
                    classifyDic[neStr] = [dict(),[]]

                innerSplitList = otherStr.split('INNER')
                if len(innerSplitList) == 3:
                    relationStr = innerSplitList[0]
                    weightStr = innerSplitList[1]
                    sentenceIndexStr = innerSplitList[2]

                    relationList = relationStr.split(' ')

                    # for relationItem in relationList:
                    #     # print relationItem
                    #     # print classifyDic[neStr][0].keys()
                    #     # exit(0)
                    #     if neStr in classifyDic.keys():
                    #         if relationItem not in classifyDic[neStr][0].keys():
                    #             classifyDic[neStr][0][relationItem] = 0.0
                    #
                    #         classifyDic[neStr][0][relationItem] = classifyDic[neStr][0][relationItem] + float(weightStr)
                    #     elif neReversedStr in classifyDic.keys():
                    #         if relationItem not in classifyDic[neReversedStr][0].keys():
                    #             classifyDic[neReversedStr][0][relationItem] = 0.0
                    #
                    #         classifyDic[neReversedStr][0][relationItem] = classifyDic[neReversedStr][0][relationItem] + float(weightStr)
                    #
                    #
                    # if neStr in classifyDic.keys():
                    #     classifyDic[neStr][1].append(sentenceIndexStr)
                    # elif neReversedStr in classifyDic.keys():
                    #     classifyDic[neReversedStr][1].append(sentenceIndexStr)

                    if neStr in classifyDic.keys():
                        for relationItem in relationList:
                            if relationItem not in classifyDic[neStr][0].keys():
                                classifyDic[neStr][0][relationItem] = 0.0

                            classifyDic[neStr][0][relationItem] = classifyDic[neStr][0][relationItem] + float(weightStr)

                        classifyDic[neStr][1].append(sentenceIndexStr)
                    elif neReversedStr in classifyDic.keys():
                        for relationItem in relationList:
                            if relationItem not in classifyDic[neReversedStr][0].keys():
                                classifyDic[neReversedStr][0][relationItem] = 0.0

                            classifyDic[neReversedStr][0][relationItem] = classifyDic[neReversedStr][0][relationItem] + float(weightStr)

                        classifyDic[neReversedStr][1].append(sentenceIndexStr)

    # 生成排序字典
    orderedDic = OrderedDict()

    print '排序：'
    transMiddleList = []
    classifyDicKeyList = classifyDic.keys()
    for i in range(len(classifyDicKeyList)):
        transMiddleList.append((i,len(list(set(classifyDic[classifyDicKeyList[i]][1])))))

    transMiddleList = sorted(transMiddleList,key=lambda item:item[1],reverse=True)

    for tupleItem in transMiddleList:
        idx = tupleItem[0]
        orderedDic[classifyDicKeyList[idx]] = classifyDic[classifyDicKeyList[idx]]


    print '输出：'
    # outputList = []
    fw = codecs.open(outFilePath,'wb')

    orderedDicKeyList = orderedDic.keys()
    # for neKey, relationDicValue in classifyDic.items():
    for i in tqdm(range(len(orderedDicKeyList))):
        neKey = orderedDicKeyList[i]
        relationDicValue = orderedDic[neKey]

        candidateList = []
        for relationKey, weightValue in relationDicValue[0].items():
            candidateList.append((relationKey, weightValue))

        orderedList = sorted(candidateList, key=lambda item: item[1], reverse=True)

        candidateRelation = orderedList[0][0]

        orderedOutputLine = ''
        for relationWeightItem in orderedList:
            if len(relationWeightItem) == 2:
                orderedOutputLine = orderedOutputLine + '(' + relationWeightItem[0] + ',' + str(relationWeightItem[1]) + ')' + ' '
        orderedOutputLine = orderedOutputLine.strip()

        sentenceIndexSetList = list(set(relationDicValue[1]))
        sentenceLen = str(len(relationDicValue[1]))

        sentenceStrList = getSentenceStrList(sentenceIndexSetList, sentenceList)

        outputLine = neKey + '\t候选关系：【' + candidateRelation + '】\t句子个数：' + sentenceLen + '\n'\
                 + orderedOutputLine + '\n' +\
                 sentenceStrList

        fw.write(outputLine + '\n')

    fw.close()

    # print '输出：'
    # inout.writeList2Txt(outFilePath, outputList)