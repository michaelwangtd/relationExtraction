#!/usr/bin/env python
# -*- coding:utf-8 -*-

from utils import inout
from utils.inout import printEscapeStr
import jieba
import codecs


if __name__ == '__main__':

    inFilePath = inout.getDataOriginPath('snow_white_origin.txt')
    outFilePath = inout.getDataOriginPath('snow_white_clean.txt')

    infoList = inout.readListFromTxt(inFilePath)

    outputStr = ''

    for item in infoList:
        sentence = item.replace('\t','').replace('\n','').replace('\r','').strip()
        sentenceSplitList = jieba.cut(sentence)
        outputStr = outputStr + ' '.join(sentenceSplitList) + ' '

    outputStr = outputStr + '\n'
    fw = codecs.open(outFilePath,'w','utf-8')
    fw.write(outputStr)
    fw.close()