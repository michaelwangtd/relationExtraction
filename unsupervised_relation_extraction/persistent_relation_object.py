#!/usr/bin/env python
# -*- coding:utf-8 -*-

from utils import inout
from utils.inout import printEscapeStr

"""
    将对称、非对称关系文本持久化为字典对象
    方便后续环节直接加载使用
"""


# if __name__ == '__main__':        ##  因为感觉加载速度不慢，所以没有持久化，后续如果速度慢，可以进行持久化工作
def getRelationShipDic():
    asymmetricInFilePath = inout.getResourcePath('asymmetricRelationShip.txt')
    symmetricInFilePath = inout.getResourcePath('symmetricRelationShip.txt')

    infoList = inout.readListFromTxt(asymmetricInFilePath)
    infoList.extend(inout.readListFromTxt(symmetricInFilePath))
    print len(infoList)

    # 初始化持久化对象字典
    initDic = dict()

    for lineItem in infoList:
        lineList = lineItem.strip().split('\t')
        key = lineList[0].strip()
        valueList = lineList[-1].strip()[1:-1].replace(' ','').split(',')
        ## 这是处理的第一种方法
        initDic[key] = valueList
        ## 还可以有第二中方法

    return initDic


