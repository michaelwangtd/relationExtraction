#!/usr/bin/env python
# -*- coding:utf-8 -*-

import index
from utils import inout
from utils.inout import printEscapeStr
import codecs


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
        1 合并文件
    """
    # # rootPath = 'D:\\data_relation_extraction\\resource\\cmpp'
    # rootPath = 'D:\\workstation\\repositories\\relationExtraction\\data\\sentence'
    #
    # inpPath_01 = rootPath + '\\sentence_1200w-12359300.txt'
    # inpPath_02 = rootPath + '\\sentence_12359300-1300w.txt'
    # # inpPath_03 = rootPath + '\\sentence_100w-150w.txt'
    #
    # outputPath = inout.getDataSentencePath('sentence_1200w-1300w.txt')
    # resultList = []
    #
    # infoList1 = inout.readListFromTxt(inpPath_01)
    # infoList2 = inout.readListFromTxt(inpPath_02)
    # # infoList3 = inout.readListFromTxt(inpPath_03)
    # # print len(infoList1)
    # # exit(0)
    #
    # resultList.extend(infoList1)
    # resultList.extend(infoList2)
    # # resultList.append(infoList3)
    #
    # inout.writeList2Txt(outputPath,resultList)
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
          
          这里实现的是：在进行命名实体识别之前对数据进行分组处理
                        将数据分开到不同的文件中
    """
    ## 这部分将50w为单位的数据分割成5个10w的句子，存储在文本中

    # originFilePath = inout.getDataSentencePath('sentence_500w-550w.txt')
    #
    # infoList = inout.readListFromTxt(originFilePath)
    #
    # print len(infoList)
    # # exit(0)
    #
    # # candy_01 = infoList[-500000:-400000]
    # # candy_02 = infoList[-400000:-300000]
    # # candy_03 = infoList[-300000:-200000]
    # # candy_04 = infoList[-200000:-100000]
    # # candy_05 = infoList[-100000:]
    #
    # post1 = int(len(infoList) /5 * 1)
    # post2 = int(len(infoList) /5 * 2)
    # post3 = int(len(infoList) /5 * 3)
    # post4 = int(len(infoList) /5 * 4)
    #
    # # print post1
    # # print post2
    # # print post3
    # # print post4
    # # exit(0)
    #
    # candy_01 = infoList[:post1]
    # candy_02 = infoList[post1:post2]
    # candy_03 = infoList[post2:post3]
    # candy_04 = infoList[post3:post4]
    # candy_05 = infoList[post4:len(infoList)]
    #
    # outPath_01 = inout.getDataNECandyPath('sentence_500w-510w.txt')
    # outPath_02 = inout.getDataNECandyPath('sentence_510w-520w.txt')
    # outPath_03 = inout.getDataNECandyPath('sentence_520w-530w.txt')
    # outPath_04 = inout.getDataNECandyPath('sentence_530w-540w.txt')
    # outPath_05 = inout.getDataNECandyPath('sentence_540w-550w.txt')
    #
    # inout.writeList2Txt(outPath_01,candy_01)
    # print '01 写入完成...'
    # inout.writeList2Txt(outPath_02,candy_02)
    # print '02 写入完成...'
    # inout.writeList2Txt(outPath_03,candy_03)
    # print '03 写入完成...'
    # inout.writeList2Txt(outPath_04,candy_04)
    # print '04 写入完成...'
    # inout.writeList2Txt(outPath_05,candy_05)
    # print '05 写入完成...'



    """
        4 将处理完的sentence,sentenceFeature分开的文本合并到一个总的文本中
        这个总的文本命名为：sentence_and_feature_max_w.txt
        放在/data/analysis/ne/meat/目录下
        之前被合并的各部分文件被合并之后放在/data/analysis/ne/meat/backup/目录下
        
        程序运行以追加的方式，将各部分文件内容追加到sentence_and_feature_max_w.txt文件中
    """
    # finalMaxFilePath = inout.getDataNEMeatPath('sentence_and_feature_900w-2100w_fnlp_new.txt')
    #
    # finalList = []
    #
    # inputPath_01 = inout.getDataNEMeatPath('sentence_and_feature_1900w-2000w.txt')
    # inputPath_02 = inout.getDataNEMeatPath('sentence_and_feature_2000w-2100w.txt')
    # # inputPath_03 = inout.getDataNEMeatPath('sentence_and_feature_1600w-1700w.txt')
    # # inputPath_04 = inout.getDataNEMeatPath('sentence_and_feature_1700w-1800w.txt')
    # # inputPath_05 = inout.getDataNEMeatPath('sentence_and_feature_1800w-1900w.txt')
    #
    # info_01 = inout.readListFromTxt(inputPath_01)
    # info_02 = inout.readListFromTxt(inputPath_02)
    # # info_03 = inout.readListFromTxt(inputPath_03)
    # # info_04 = inout.readListFromTxt(inputPath_04)
    # # info_05 = inout.readListFromTxt(inputPath_05)
    #
    # finalList.extend(info_01)
    # finalList.extend(info_02)
    # # finalList.extend(info_03)
    # # finalList.extend(info_04)
    # # finalList.extend(info_05)
    #
    # print len(finalList)
    #
    # # exit(0)
    #
    # # 覆盖写
    # # inout.writeList2Txt(finalMaxFilePath,finalList)
    #
    # # 追加写
    # inout.appendList2Txt(finalMaxFilePath,finalList)
    #
    # print '写入完成...'




    """
        5 从已抽取的关系文件中（analysis）选取符合条件的关系
    """
    # fr = codecs.open(inout.getDataAnalysisPath('analysis_vote_sentence_fnlp_150w-2100w.txt'),'rb')

    fr = codecs.open('D:/java_map_vote_relation_ordered_result_fnlp_150w-2000w.txt','rb')

    # fw = codecs.open(inout.getDataAnalysisPath('graph_candidate_entity_relation_150w-2100w.txt'),'wb')

    resultList = []

    i = 0
    # while i<200:
    while True:
        line = fr.readline()
        i += 1
        if line:
            if '候选关系：【' in line:

                # outputLine = line.strip()

                # fw.write(outputLine + '\n')

                resultList.append(line.strip())
                # i += 1
        print i

    # fw.close()
    fr.close()




    outFilePath = inout.getDataOriginPath('graph_candidate_entity_relation_150w-2100w.txt')
    inout.writeList2Txt(outFilePath,resultList)

    print '写入完成...'






    """
        test:
        测试了原来pkl对象内部的结构：
        [[('尼古拉斯', 'S-Nh'), ('奥古斯特·科波拉', 'S-Nh')], ['生于', '加州', '一个', '中产', '家庭', '，', '意大利', '裔', '父亲', '是', '文学', '教授', '，', '德国裔', '的', '母亲', 'Joy']]
    """
    # sentenceFeatureList,typeList = inout.readPersistObject(inout.getDataPklPath('sentence_feature_list_corpus_complete_sentence.pkl'))
    #
    # i = 1
    # for item in sentenceFeatureList:
    #     printEscapeStr(item)
    #     printEscapeStr(item[0])
    #     printEscapeStr(item[1])
    #
    #     i = i + 1
    #     if i==3:
    #         exit(0)


    """
        自己挖的坑，自己跳进去了，自己处理
    """
    # inFilePath = inout.getDataNECandyPath('sentence_150w-160w.txt')
    #
    # infoList = inout.readListFromTxt(inFilePath)
    #
    # print len(infoList)
    #
    # linshiInfo = infoList[:80000]
    # infoList[]











