#!/usr/bin/env python
# -*- coding:utf-8 -*-

from unsupervised_relation_extraction import persistent_relation_object,relation_extraction
from utils.inout import printEscapeStr

if __name__ == '__main__':

    testList = ['我','太公','前岳母']
    testList = ['岳云鹏','你','师父','郭德纲','喊','你','说','相声']

    relationDic = persistent_relation_object.getRelationShipDic()
    result = relation_extraction.candidateRelationWordMapping(testList,relationDic)
    printEscapeStr(result)