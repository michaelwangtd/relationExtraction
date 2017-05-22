#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from utils import inout,systm
import index

if __name__ == '__main__':

    testStr = '一直在躲雨，雨会不会很难过。早上坐公交车上班？注意到身边一名男子！他穿着干净、得体。。脸庞留下少许岁月的痕迹。'
    testStr = '李晨喜欢我。我喜欢看书。书是书他妈生的。'
    testStr = '杨润楷在中国北京的中国科学院计算机研究所学习。'
    testStr = '中国的首都是北京'

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
    # result = '__'.join(words)
    # print type(result)
    # print result
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
    # print '\t'.join(postags)
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





