#!/usr/bin/env python
# -*- coding:utf-8 -*-

from utils import inout
from pyltp import SentenceSplitter
from utils.inout import printList
from utils.inout import printEscapeStr
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
import index
from collections import OrderedDict


def namedEntityRecognize(sentence):
    '''
        返回
    '''
    namedEntityTagTupleList = []

    segmentor = Segmentor()
    segmentor.load(inout.getLTPPath(index.CWS))
    words = segmentor.segment(sentence)
    segmentor.release()
    postagger = Postagger()
    postagger.load(inout.getLTPPath(index.POS))
    postags = postagger.postag(words)
    postagger.release()
    recognizer = NamedEntityRecognizer()
    recognizer.load(inout.getLTPPath(index.NER))
    netags = recognizer.recognize(words,postags)
    recognizer.release()

    # 封装成元组形式
    for word,netag in zip(words,netags):
        namedEntityTagTupleList.append((word,netag))

    neTagList = '\t'.join(netags).split('\t')

    return namedEntityTagTupleList,neTagList

def getNamedEntityTypeDic():
    neList = ['Nh','Ni','Ns']
    dic = dict()
    for i in range(len(neList)):
        for j in range(len(neList)):
            key = neList[i] + '_' + neList[j]
            dic[key] = []
    return dic


if __name__ == '__main__':
    corpusPath = inout.getDataOriginPath('special_corpus.txt')
    corpus = inout.onlyReadLine(corpusPath)

    ## 1 对于复杂的文本数据要进行清洗
    sentences = SentenceSplitter.split(corpus)
    sentences = '\t'.join(sentences)#.decode('utf-8')
    sentenceList = sentences.split('\t')
    printList(sentenceList)

    neTypeDic = getNamedEntityTypeDic()

    ## 2 提取命名实体
    for sentence in sentenceList:
        namedEntityTagTupleList,neTagList = namedEntityRecognize(sentence)
        printEscapeStr(namedEntityTagTupleList)
        printEscapeStr(neTagList)
        ## 3 这里应该判断命名实体标签列表neTagList
        ## 4 将同一类别的命名实体对划分为一类

        # break

