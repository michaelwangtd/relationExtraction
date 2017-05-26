#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from utils import inout
import index
from utils.inout import printEscapeStr


"""
    检测程序
    检测ltp是否识别出命名实体
"""

if __name__ == '__main__':

    # testLine = '著名相声家成龙的师傅是马季。'

    while True:
        testLine = raw_input('请输入字符串：（-1退出）')


        namedEntityTagTupleList = []

        segmentor = Segmentor()
        # segmentor.load(inout.getLTPPath(index.CWS))
        segmentor.load_with_lexicon(inout.getLTPPath(index.CWS), inout.getResourcePath('userDic.txt'))
        words = segmentor.segment(testLine)
        segmentor.release()
        postagger = Postagger()
        postagger.load(inout.getLTPPath(index.POS))
        postags = postagger.postag(words)
        postagger.release()
        recognizer = NamedEntityRecognizer()
        recognizer.load(inout.getLTPPath(index.NER))
        netags = recognizer.recognize(words,postags)
        recognizer.release()

        for word,netag in zip(words,netags):
            namedEntityTagTupleList.append((word,netag))

        neTagList = '\t'.join(netags).split('\t')

        printEscapeStr(namedEntityTagTupleList)
        printEscapeStr(neTagList)