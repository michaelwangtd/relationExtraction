# -*- coding:utf-8 -*-

"""
    模块实现关系抽取的第二步：
    计算每一个句子抽取出来的关系相应的权重
    线性的方式处理
"""

from utils import inout
import codecs
import time
from utils import systm
from tqdm import tqdm

def convertDataFormat(infoList):
    '''
        input:姚景远	孙彩艳||文章_对_、_进行_了_猛烈_的_人身_抨击_。||文章对姚景远、孙彩艳进行了猛烈的人身抨击。
        output:
                [[(姚景远,S-Nh),(孙彩艳,S-Nh)],['生于', '加州', '一个', '中产', '家庭', '，', '意大利', '裔', '父亲']]
                文章对姚景远、孙彩艳进行了猛烈的人身抨击。
    '''
    sentenceList = []
    sentenceFeatureList = []

    for line in infoList:
        if len(line.strip().split('||')) == 3:
            lineList = line.strip().split('||')

            # 处理命名实体对
            nePairList = []
            neStrTemp = lineList[0]
            if len(neStrTemp.split('\t')) == 2:
                neStrTempList = neStrTemp.split('\t')

                ## 对命名实体进行筛选
                if '某' not in neStrTempList[0].strip() and '某' not in neStrTempList[1].strip():

                    if len(neStrTempList[0].strip()) > 3 and len(neStrTempList[1].strip()) > 3:

                        if neStrTempList[0].strip() != neStrTempList[1]:

                            nePairList.append((neStrTempList[0].strip(),'S-Nh'))
                            nePairList.append((neStrTempList[1].strip(),'S-Nh'))

            # 处理otherWordList
            otherWordStr = lineList[1]
            otherWordList = otherWordStr.split('_')

            # 处理句子
            sentenceStr = lineList[2]

            if nePairList:
                sentenceFeatureList.append([nePairList,otherWordList])
                sentenceList.append(sentenceStr)
    return sentenceList,sentenceFeatureList

def convertNewDataFormat(infoList):
    '''

    '''
    sentenceList = []
    sentenceFeatureList = []

    for line in infoList:
        if len(line.strip().split('#OUTER#'))==4:
            lineList = line.strip().split('#OUTER#')

            # 处理命名实体对
            nePairList = []
            if 'entityPair' in lineList[0]:

                neStrTemp = lineList[0].split('#INNER#')[1]
                if len(neStrTemp.split('\t')) == 2:
                    neStrTempList = neStrTemp.split('\t')

                    if '某' not in neStrTempList[0].strip() and '某' not in neStrTempList[1].strip():

                        if len(neStrTempList[0].strip()) > 3 and len(neStrTempList[1].strip()) > 3:

                            if neStrTempList[0].strip() != neStrTempList[1]:

                                nePairList.append((neStrTempList[0].strip(), 'S-Nh'))
                                nePairList.append((neStrTempList[1].strip(), 'S-Nh'))

            # 处理otherWordList
            otherWordList = []
            if 'wordList' in lineList[1]:
                otherWordStr = lineList[1].split('#INNER#')[1]
                otherWordList = otherWordStr.split('_')

            sentenceStr = ''
            # 处理句子
            if 'sentence' in lineList[2]:
                sentenceStr = lineList[2].split('#INNER#')[1]

            time = ''
            if 'time' in lineList[3]:
                if len(lineList[3].split('#INNER#'))==2:
                    if lineList[3].split('#INNER#')[1]!='':
                        time = lineList[3].split('#INNER#')[1]
            comSentence = time + '#INNER#' + sentenceStr

            if nePairList:
                sentenceFeatureList.append([nePairList,otherWordList])
                sentenceList.append(comSentence)
    return sentenceList, sentenceFeatureList

def dictDistinct(sentenceList,sentenceFeatureList):
    '''
        利用python dict结果进行过滤
    '''

    indexDic = dict()

    resultSentenceList = []
    resultSentenceFeatureList = []

    for i in range(len(sentenceList)):
        indexDic[str(sentenceList[i])] = i

    indexList = []
    for k,v in indexDic.items():
        indexList.append(v)
    indexList = list(set(indexList))

    for idx in indexList:
        resultSentenceList.append(sentenceList[idx])
        resultSentenceFeatureList.append(sentenceFeatureList[idx])

    return resultSentenceList,resultSentenceFeatureList


def loadIndexSentenceList():
    '''
        加载包含索引信息的句子列表
    '''
    sentenceList = []
    sentenceFeatureList = []

    ## 1
    # fnlpListPath = inout.getDataNEMeatPath('sentence_and_feature_150w-900w_fnlp_old.txt')
    # fnlpListPath = inout.getDataTestPath('sentence_and_feature_test.txt')
    fnlpListPath = '/data/wangtd/workspace/re/data/sentence_and_feature_150w-900w_fnlp_old.txt'

    fnlpOldDataList = inout.readListFromTxt(fnlpListPath)
    print'原始-数据-旧 len:', len(fnlpOldDataList)

    fnlpSentenceList_old, fnlpSentenceFeatureList_old = convertDataFormat(fnlpOldDataList)
    print'处理-数据-旧 len:', len(fnlpSentenceList_old)

    sentenceList.extend(fnlpSentenceList_old)
    sentenceFeatureList.extend(fnlpSentenceFeatureList_old)

    ## 2
    # fnlpNewDataListPath = inout.getDataNEMeatPath('sentence_and_feature_900w-2100w_fnlp_new.txt')
    # fnlpNewDataListPath = inout.getDataTestPath('sentence_and_feature_test_new.txt')
    fnlpNewDataListPath = '/data/wangtd/workspace/re/data/sentence_and_feature_900w-2100w_fnlp_new.txt'

    fnlpNewDataList = inout.readListFromTxt(fnlpNewDataListPath)
    print'原始-数据-新 len:', len(fnlpNewDataList)

    fnlpSentenceList_new, fnlpSentenceFeatureList_new = convertNewDataFormat(fnlpNewDataList)
    print'处理-数据-新 len:', len(fnlpSentenceList_new)

    sentenceList.extend(fnlpSentenceList_new)
    sentenceFeatureList.extend(fnlpSentenceFeatureList_new)

    print 'sentenceList len: ', len(sentenceList)
    print 'sentenceFeatureList len: ', len(sentenceFeatureList)
    print '数据加载完毕...'

    sentenceList, sentenceFeatureList = dictDistinct(sentenceList, sentenceFeatureList)
    print '句子去重复完成...',len(sentenceList)

    return sentenceList,sentenceFeatureList

def getSetList(relationStr):

    return list(set(relationStr.split('\t')))


def getRelationWeight(sentence):

    systemTime = time.time()

    basicTime = systm.getTimeStampFromTimeStr('2016-12-30 12:00:00')

    coldTime = systm.getTimeStampFromTimeStr('2017-1-1 12:00:00')

    weight = 0.0

    if sentence:
        if 'INNER' in sentence:
            timeStr = sentence.split('#INNER#')[0].strip()
            # print timeStr
            articleTime = systm.getTimeStampFromTimeStr(timeStr)
        else:
            articleTime = coldTime

        weight = (articleTime - basicTime) / (systemTime - basicTime)
    return weight


if __name__ == '__main__':

    ## 加载包含索引信息的句子到内存
    # sentenceList,sentenceFeatureList = loadIndexSentenceList()

    sentenceFilePath = inout.getDataAnalysisPath('sentenceList.txt')
    sentenceList = inout.readListFromTxt(sentenceFilePath)

    # for item in sentenceList:
    #     print item
    # exit(0)

    inFilePath = inout.getDataAnalysisPath('vote_classify_module_result_fnlp_150w-2100w.txt')
    # inFilePath = '/data/wangtd/workspace/re/vote_classify_module_result_fnlp_150w-2100w.txt'

    outFilePath = inout.getDataAnalysisPath('vote_relation_weight_result_fnlp_150w-2000w.txt')
    # outFilePath = '/data/wangtd/workspace/re/vote_relation_weight_result_fnlp_150w-2000w.txt'

    infoList = inout.readListFromTxt(inFilePath)

    ## 开始处理
    fw = codecs.open(outFilePath,'wb')

    for i in tqdm(range(len(infoList))):
        line = infoList[i]
        if line:
            line = line.strip()
            entityPair = ''
            relationSetStr = ''
            weight = ''
            sentenceIndex = ''

            divSplitList = line.split('DIV')
            #
            entityPair = divSplitList[0]
            innerSplitList = divSplitList[1].split('INNER')
            #
            relationStr = innerSplitList[0]
            relationSetStr = str(getSetList(relationStr))
            #
            indexList = eval(innerSplitList[1])
            sentenceIndex = indexList[0]
            #
            weigth = getRelationWeight(sentenceList[sentenceIndex])

            outputLine = entityPair + 'DIV' + relationSetStr + 'INNER' + \
                str(weigth) + 'INNER' + str(sentenceIndex)

            fw.write(outputLine + '\n')


    fw.close()