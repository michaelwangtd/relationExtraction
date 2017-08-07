# -*- coding:utf-8 -*-

from utils import inout


def isExist(sonWordArr,momWordList):
    for tupleItem in momWordList:
        if sonWordArr[0] in tupleItem and sonWordArr[1] in tupleItem:
            print 'momWordArr:',tupleItem[0],tupleItem[1]
            print 'sonWordArr:',sonWordArr[0],sonWordArr[1]
            return True
    return False


if __name__ == '__main__':

    """
        处理4500后的数据，取一个差集
    """

    blackWordList = ['利物浦','凤凰','CEO','AC米兰','阿森纳','尤文图斯','TD','欧战'\
                     'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',\
                     'Q','R','S','T','U','V','W','X','Y','Z'\
                     '欧洲杯','主任','沃尔沃','恒大','鲁能','胡润','周岁'\
                     '0','1','2','3','4','5','6','7','8','9'\
                     '双冰','詹皇','尤文','王总']


    momInfo = inout.readListFromTxt('D:/michaelD/kg/entity_relation_weight_4500.txt')
    sonInfo = inout.readListFromTxt('D:/michaelD/kg/4500_after_data.txt')
    outPath = 'D:/michaelD/kg/after_tp_1.txt'

    momWordList = []
    for momItem in momInfo:
        wordArr = momItem.split('\t')[0].split(' ')
        momWordList.append((wordArr[0],wordArr[1]))

    middleList = []
    for sonItem in sonInfo:
        sonWordArr = sonItem.split('\t')[0].split(' ')
        if isExist(sonWordArr,momWordList):
            continue
        middleList.append(sonItem)
    print 'middleList:',len(middleList)

    resultList = []
    for middItem in middleList:
        middWordArr = middItem.split('\t')[0].split(' ')
        if middWordArr[0] == middWordArr[1]:
            inout.printEscapeStr(middItem)
            continue

        flag = False
        for blackWord in blackWordList:
            if blackWord in middWordArr[0]:
                flag = True
                inout.printEscapeStr(middItem)
                break
            if blackWord in middWordArr[1]:
                flag = True
                inout.printEscapeStr(middItem)
                break

        if flag:
            continue

        resultList.append(middItem)
    print 'result len:',len(resultList)

    inout.writeList2Txt(outPath,resultList)

