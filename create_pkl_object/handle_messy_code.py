# -*- coding:utf-8 -*-

from utils import inout
import codecs
import re

def handleSentenceOne(sentenceOne):
    if sentenceOne!='':
        resultStr = ''
        splitList = sentenceOne.split('\t')
        if len(splitList) == 4:
            cakeStr = splitList[2]
            target = cakeStr.replace('候选关系：【','').replace('】','').strip()
            target = eval(target)[0]

            resultStr = splitList[0] + ' ' + splitList[1] + '\t' + \
                '候选关系【' + target + '】\t' + \
                splitList[3]
            # print resultStr
        return resultStr


def handleSentenceTwo(sentenceTwo):
    print sentenceTwo
    sortedRelationList = eval(sentenceTwo)
    print type(sortedRelationList)
    print sortedRelationList
    exit(0)


if __name__ == '__main__':

    inFilePath = inout.getDataAnalysisPath('vote_relation_ordered_result_fnlp_150w-2000w.txt')

    outFilePath = inout.getDataAnalysisPath('vote_relation_ordered_result_fnlp_150w-2000w_handled.txt')

    infoList = inout.readListFromTxt(inFilePath)

    print 'info list len:',len(infoList)

    allSentenceList = []
    itemSentenceList = []
    for item in infoList:
        item = item.strip()
        if item!='':
            # print item
            itemSentenceList.append(item)
        else:
            # print '|' + item + '|'
            allSentenceList.append(itemSentenceList)
            itemSentenceList = []

    fw = codecs.open(outFilePath,'wb')

    for innerSentenceList in allSentenceList:
        # inout.printEscapeStr(innerSentenceList)
        sentenceOne = ''
        sentenceTwo = ''
        if '候选关系' in innerSentenceList[0]:
            sentenceOne = innerSentenceList[0]
        if '[' in innerSentenceList[1] or ']' in innerSentenceList[1]:
            sentenceTwo = innerSentenceList[1]
        otherSentenceList = innerSentenceList[2:]

        # print sentenceOne
        # print sentenceTwo
        # exit(0)
        sentenceOneStr = handleSentenceOne(sentenceOne)

        sentenceTwoStr = handleSentenceTwo(sentenceTwo)




    fw.close()
