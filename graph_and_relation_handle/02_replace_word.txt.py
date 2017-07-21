# -*- coding:utf-8 -*-

from utils import inout

if __name__ == '__main__':

    infoList = inout.readListFromTxt('D:/michaelD/kg/entity_relation_weight_origin.txt')
    # print len(infoList)
    # exit(0)

    outFilePath = 'D:/michaelD/kg/entity_relation_weight.txt'

    outputList = []
    for line in infoList:
        line = line.strip()

        # if '成员' in line:
        resultLine = line.replace('成员','朋友')
        resultLine = resultLine.replace('middot;','')
        resultLine = resultLine.replace('Paytm','')
        resultLine = resultLine.replace('，','')
        resultLine = resultLine.replace('&middot','')#&middot;

        outputList.append(resultLine)

    inout.writeList2Txt(outFilePath,outputList)

