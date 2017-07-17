# -*- coding:utf-8 -*-

from utils import inout
from tqdm import tqdm
import codecs
from collections import OrderedDict


def getRelationWeightList(tupleList):
    '''

    '''
    relationList = []
    for tupleItem in tupleList:
        relationList.append(tupleItem[0])
    relationList = list(set(relationList))

    weightDic = dict()
    for keyItem in relationList:
        weightDic[keyItem] = 0.0

    for tupleItem in tupleList:
        relationKey = tupleItem[0]
        weightDic[relationKey] = weightDic[relationKey] + tupleItem[1]

    resultTupleList = []
    for k,v in weightDic.items():
        resultTupleList.append((k,v))

    return resultTupleList


def getSortedRelationWeightStr(tupleList):
    '''

    '''
    outputStr = '['
    for item in tupleList:
        outputStr = outputStr + '(' + item[0] + ',' + str(item[1]) + ')'
        outputStr = outputStr + ']'
    return outputStr


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
    print '关系权重列表长度:',len(infoList)

    outFilePath = inout.getDataAnalysisPath('vote_relation_ordered_result_fnlp_150w-2000w.txt')

    sentenceFilePath = inout.getDataAnalysisPath('sentenceList.txt')
    sentenceList = inout.readListFromTxt(sentenceFilePath)
    print '句子列表长度:',len(sentenceList)


    # 获取不重复的命名实体列表
    print '获取字典key值列表:'
    neSetList = []
    for i in tqdm(range(len(infoList))):
        divSplitList = infoList[i].split('DIV')
        if len(divSplitList) == 2:
            neStr = divSplitList[0]
            neList = neStr.split('\t')
            if len(neList) == 2:
                neStrReverse = neList[1] + '\t' + neList[0]
                # print type(neStr),neStr,'|',type(neStrReverse),neStrReverse
                if neStr not in neSetList and neStrReverse not in neSetList:
                    neSetList.append(neStr)

    print '字典key值长度:',len(neSetList)


    # 生成归类字典框架 key:[(relation1,w1),()][index1,]
    classifyDic = dict()
    sentenceLenDic = dict()
    print '初始化归类字典：'
    for i in tqdm(range(len(neSetList))):
        nePairStr = neSetList[i]
        # print nePairStr
        classifyDic[nePairStr] = [list(),list()]
        sentenceLenDic[nePairStr] = 0

    # print len(dic.keys())
    # exit(0)

    print '归类处理：'
    for i in tqdm(range(len(infoList))):
        divSplitList = infoList[i].split('DIV')
        if len(divSplitList) == 2:
            neStr = divSplitList[0]
            neList = neStr.split('\t')
            if len(neList) == 2:
                neStrReverse = neList[1] + '\t' + neList[0]

                innerSplitList = divSplitList[1].split('INNER')
                if len(innerSplitList) == 3:
                    relationStr = innerSplitList[0]
                    weightStr = innerSplitList[1]
                    sentenceIndex = innerSplitList[2]

                    #
                    relationAndWeightTupleList = []
                    relationList = relationStr.split(' ')
                    relationList = list(set(relationList))
                    for relation in relationList:
                        relationAndWeightTupleList.append((relation,float(weightStr)))

                    if neStr in classifyDic.keys():
                        classifyDic[neStr][0].extend(relationAndWeightTupleList)
                        classifyDic[neStr][1].append(sentenceIndex)
                    if neStrReverse in classifyDic.keys():
                        classifyDic[neStrReverse][0].extend(relationAndWeightTupleList)
                        classifyDic[neStrReverse][1].append(sentenceIndex)

    for k,v in classifyDic.items():
        sentenceLenDic[k] = len(v[1])

    sentenceLenItemsOrderedList = sorted(sentenceLenDic.items(),key=lambda item:item[1],reverse=True)


    # 生成outputDic
    outputDic =OrderedDict()
    for tupleItem in sentenceLenItemsOrderedList:
        outputDic[tupleItem[0]] = classifyDic[tupleItem[0]]



    print '输出：'
    fw = codecs.open(outFilePath,'wb')

    keyList = outputDic.keys()
    for i in tqdm(range(len(keyList))):
        key = keyList[i]
        relationAndWeightTempList = outputDic[key][0]
        sentenceIndexList = outputDic[key][1]
        sentenceIndexList = list(set(sentenceIndexList))

        relationWeightList = getRelationWeightList(relationAndWeightTempList)
        sortedRelationWeightList = sorted(relationWeightList,key = lambda item : item[1],reverse=True)
        # inout.printEscapeStr(sortedRelationWeightList)

        candidateRelation = sortedRelationWeightList[0][0]

        relationWeightStr = getSortedRelationWeightStr(sortedRelationWeightList)

        sentenceStrList = getSentenceStrList(sentenceIndexList,sentenceList)

        outputLine = '【' + key + '】\t候选关系：【' + candidateRelation + '】\t句子个数:' + str(len(sentenceIndexList)) + '\n' \
                     + relationWeightStr + '\n' + sentenceStrList

        fw.write(outputLine + '\n')

    fw.close()













    """
    因字典扩展问题，导致在大任务量时执行速度特别慢
    
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
    """









