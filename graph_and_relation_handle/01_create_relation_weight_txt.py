# -*- coding:utf-8 -*-

from utils import inout
import os
from tqdm import tqdm

def getSumWeight(weightList):
    result = 0.0
    for item in weightList:
        result = result + float(item)
    return result


def calculateCandidateRelationWeight(relationLine):
    '''

    '''
    relationAndWeightList = relationLine.replace('{','').replace('}','').strip().split(',')
    # inout.printEscapeStr(relationAndWeightList)

    relationList = []
    weightList = []
    for relAndWht in relationAndWeightList:
        relAndWht = relAndWht.strip()
        relationList.append(relAndWht.split('=')[0])
        weightList.append(relAndWht.split('=')[1])

    # inout.printEscapeStr(relationList)
    # inout.printEscapeStr(weightList)

    candidateRelation = relationList[0]
    candidateWeight = float(weightList[0])

    # print candidateRelation
    # print candidateWeight,type(candidateWeight)

    sumWeight = getSumWeight(weightList)

    candidateWeight = candidateWeight / sumWeight

    candidateWeight = round(candidateWeight * 100,2)
    # print candidateWeight

    # exit(0)
    return candidateWeight


if __name__ == '__main__':

    rootDir = 'D:/michaelD/kg/'

    infoList = inout.readListFromTxt(rootDir + 'rEOrigin_sen_20.txt')

    outputFilePath = rootDir + 'entity_relation_weight.txt'

    groupList = []
    tupleList = []
    for line in infoList:
        line = line.strip()
        if '候选关系：【' in line:
            if tupleList:
                groupList.append(tupleList)
                tupleList = []
        tupleList.append(line)

    outputList = []
    for tupleItemList in groupList:
        candidateLine = tupleItemList[0]
        relationLine = tupleItemList[1]

        percentageNum = calculateCandidateRelationWeight(relationLine)

        candidateList = candidateLine.split('\t')

        relation = candidateList[2].replace('【','').replace('】','').split('：')[1]

        outputLine = candidateList[0] + ' ' + candidateList[1] + '\t' + \
                     relation + '\t' + str(percentageNum)

        outputList.append(outputLine)
        print outputLine

    inout.writeList2Txt(outputFilePath,outputList)


        # inout.printEscapeStr(candidateList)
        # inout.printEscapeStr(candidateLine.split('\t'))

        # break




