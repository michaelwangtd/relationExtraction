#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from utils import inout,systm
import index

if __name__ == '__main__':

    testStr = '今年2月份，刘翔的教练孙海平曾公开告诉媒体，冬天的时候可能跟腱会更脆弱，他们计划等到四五月份天气变暖，再看看情况。'

    ##1 分句
    # re = SentenceSplitter.split(testStr)
    # print type(re)
    # print re
    # print '\n'.join(re)

    ##2 分词
    segmentor = Segmentor()
    segmentorPath = inout.getLTPPath(index.CWS)
    segmentor.load(segmentorPath)
    words = segmentor.segment(testStr)
    segmentor.release()
    # print type(words)
    # print words
    result = '__'.join(words)
    # print type(result)
    print result
    # wordList = list(words)
    # for item in wordList:
    #     print type(item)
    #     item = item.decode('utf-8')
    #     print type(item)
    #     print item

    ##3 词性标注
    postagger = Postagger()
    postagger.load(inout.getLTPPath(index.POS))
    postags = postagger.postag(words)
    postagger.release()
    # print type(postags)
    # print postags
    print '\t'.join(postags)
    # for word,tag in zip(words,postags):
    #     print word + '\t' + tag

    ##4 命名实体识别
    recognizer = NamedEntityRecognizer()
    recognizer.load(inout.getLTPPath(index.NER))
    netags = recognizer.recognize(words,postags)
    recognizer.release()
    print type(netags)
    print netags
    for word,netag in zip(words,netags):
        print word + '\t' + netag





