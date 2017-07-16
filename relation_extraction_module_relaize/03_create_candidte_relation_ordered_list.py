# -*- coding:utf-8 -*-

from utils import inout
from tqdm import tqdm

if __name__ == '__main__':

    inFilePath = inout.getDataAnalysisPath('vote_relation_weight_result_fnlp_150w-2000w.txt')
    infoList = inout.readListFromTxt(inFilePath)

    outFilePath = inout.getDataAnalysisPath('vote_relation_ordered_result_fnlp_150w-2000w.txt')


    # neList = []
    # for i in tqdm(range(len(infoList))):
    #     divSplitList = infoList[i].split('DIV')
    #     if len(divSplitList) == 2:
    #         neStr = divSplitList[0]
    #         neList.append(neStr)
    # neList = list(set(neList))

    classifyDic = dict()

    print '归类：'
    for i in tqdm(range(len(infoList))):
        divSplitList = infoList[i].split('DIV')
        if len(divSplitList) == 2:
            neStr = divSplitList[0]
            otherStr = divSplitList[1]

            if neStr not in classifyDic.keys():
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
    for neKey,relationDicValue in classifyDic.items():
        candidateList = []
        for relationKey,weightValue in relationDicValue.items():
            candidateList.append((relationKey,weightValue))

        orderedList = sorted(candidateList,key=lambda item : item[1],reverse=True)

        outputLine = ''
        for relationWeightItem in orderedList:
            if len(relationWeightItem) == 2:
                outputLine = outputLine + '(' + relationWeightItem[0] + ',' + relationWeightItem[1] + ')' + ' '
        outputLine = outputLine.strip()

        outputList.append(neKey + '\n' + outputLine + '\n')

    print '输出：'
    inout.writeList2Txt(outFilePath,outputList)









