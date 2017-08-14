# -*- coding:utf-8 -*-

from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from utils import inout
import index

if __name__ == '__main__':

    segmentor = Segmentor()
    segmentor.load_with_lexicon(inout.getLTPPath(index.CWS), inout.getResourcePath('userDic.txt'))
    postagger = Postagger()
    postagger.load(inout.getLTPPath(index.POS))

    infoList = inout.readListFromTxt('./dn_test.txt')

    for sentence in infoList:

        # segmentor.load(inout.getLTPPath(index.CWS))
        words = segmentor.segment(sentence)
        postags = postagger.postag(words)
        # result = zip(words,postags)
        # inout.printEscapeStr(result)


    segmentor.release()
    postagger.release()

    # recognizer = NamedEntityRecognizer()
    # recognizer.load(inout.getLTPPath(index.NER))
    # netags = recognizer.recognize(words, postags)
    # recognizer.release()

    # result = zip(words,postags)
    # inout.printEscapeStr(result)














