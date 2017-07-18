# -*- coding:utf-8 -*-

import tqdm
import os
from utils import inout


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
                    classifyDic[neStr] = dict()

                innerSplitList = otherStr.split('INNER')
                if len(innerSplitList) == 3:
                    relationStr = innerSplitList[0]
                    weightStr = innerSplitList[1]
                    sentenceIndexStr = innerSplitList[2]

                    relationList = relationStr.split(' ')
                    for relationItem in relationList:
                        if relationItem not in classifyDic[neStr].keys():
                            classifyDic[neStr][relationItem] = 0.0

                        classifyDic[neStr][relationItem] = classifyDic[neStr][relationItem] + float(weightStr)

    print '排序：'
    outputList = []

    classifyDicKeyList = classifyDic.keys()
    # for neKey, relationDicValue in classifyDic.items():
    for i in tqdm(range(len(classifyDicKeyList))):
        neKey = classifyDicKeyList[i]
        relationDicValue = classifyDic[neKey]
        candidateList = []
        for relationKey, weightValue in relationDicValue.items():
            candidateList.append((relationKey, weightValue))

        orderedList = sorted(candidateList, key=lambda item: item[1], reverse=True)

        outputLine = ''
        for relationWeightItem in orderedList:
            if len(relationWeightItem) == 2:
                outputLine = outputLine + '(' + relationWeightItem[0] + ',' + relationWeightItem[1] + ')' + ' '
        outputLine = outputLine.strip()

        outputList.append(neKey + '\n' + outputLine + '\n')

    print '输出：'
    inout.writeList2Txt(outFilePath, outputList)