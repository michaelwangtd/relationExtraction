# !/usr/bin/env python
# -*- coding:utf-8 -*-

import xlrd
import os
import codecs
import xlwt
import json
import index
import pickle

"""
    获取路径相关
"""
def getDataPath(fileName):
    '''
         获取data目录文件路径
    '''
    return os.path.join(index.ROOTPATH,index.DATA,fileName)

def getLTPPath(modelName):
    '''

    '''
    return os.path.join(index.ROOTPATH,'ltkmodel','ltp_data',modelName+'.model')

def getDataOriginPath(fileName):
    '''
         获取data目录文件路径
    '''
    return os.path.join(index.ROOTPATH,index.DATA,index.ORIGIN,fileName)


def getDataPklPath(fileName):
    '''
         获取data目录文件路径
    '''
    return os.path.join(index.ROOTPATH,index.DATA,index.PKL,fileName)


def getDataSentencePath(fileName):
    '''
         获取data目录文件路径
    '''
    return os.path.join(index.ROOTPATH,index.DATA,index.SENTENCE,fileName)


def getDataNECandyPath(fileName):
    '''
         获取data目录文件路径
    '''
    return os.path.join(index.ROOTPATH,index.DATA,index.NE,index.CANDY,fileName)


def getDataNEMeatPath(fileName):
    '''
         获取data目录文件路径
    '''
    return os.path.join(index.ROOTPATH,index.DATA,index.NE,index.MEAT,fileName)


def getDataAnalysisPath(fileName):
    '''
         获取data目录文件路径
    '''
    return os.path.join(index.ROOTPATH,index.DATA,index.ANALYSIS,fileName)


def getDataTestPath(fileName):
    '''
         获取data目录文件路径
    '''
    return os.path.join(index.ROOTPATH,index.DATA,index.TEST,fileName)


def getResourcePath(fileName):
    '''
         获取data目录文件路径
    '''
    return os.path.join(index.ROOTPATH,index.RESOURCE,fileName)



"""
    文件输入/输出相关
"""

def writePersistObject(filePath,cake):
    '''
        写出持久化的对象
    '''
    fw = open(filePath,'wb')
    pickle.dump(cake,fw)
    fw.close()


def readPersistObject(filePath):
    '''
        读入持久化的对象
    '''
    fr = open(filePath,'rb')
    cake = pickle.load(fr)
    return cake,type(cake)



def writeContent2Excel(infoList,outputFilePath):
    """
        “覆盖”的方式写入数据
    """
    xls = xlwt.Workbook()
    sheet = xls.add_sheet('Sheet1')
    for i in range(len(infoList)):
        for j in range(len(infoList[i])):
            sheet.write(i,j,infoList[i][j])
        print('写入第【',str(i),'】条数据...')
    xls.save(outputFilePath)
    print('数据写入完成...')


def getListFromExcel(filePath):
    '''
        输入路径
        以列表形式返回单条列表数据
    '''
    tempList = []
    if os.path.exists(filePath):
        xls_r = xlrd.open_workbook(filePath)
        sheet_r = xls_r.sheet_by_index(0)
        rows = sheet_r.nrows
        for i in range(rows):
            oneRecord = sheet_r.row_values(i)
            tempList.append(oneRecord)
    return tempList


def loadData2Json(filePath):
    '''

    '''
    jsonList = []
    if os.path.exists(filePath):
        fr = codecs.open(filePath,'rb')
        i = 1
        while True:
            line = fr.readline()
            if line:
                try:
                    temp = line.strip()
                    lineJson = json.loads(temp)
                    # print(i,type(lineJson),str(lineJson))
                    i += 1
                    jsonList.append(lineJson)
                except Exception as ex:
                    print(ex)
            else:
                break
    return jsonList


def readListFromTxt(filePath):
    infoList = []
    if os.path.exists(filePath):
        f = codecs.open(filePath,'rb')
        while True:
            line = f.readline()
            if line:
                temp = line.strip()
                infoList.append(temp)
            else:
                break
        f.close()
    return infoList

def onlyReadLine(filePath):
    if os.path.exists(filePath):
        fr = codecs.open(filePath,'rb')
        line = fr.readline()
        if line:
            return line.strip()



def liststr2listlist(liststr):
    resultList = []
    for item in liststr:
        resultList.append(item.strip().split(','))
    return resultList


def writeList2Txt(filePath,infoList):
    if infoList:
        f = codecs.open(filePath,'wb')
        for i in range(len(infoList)):
            if isinstance(infoList[i],list):
                outputLine = ','.join(infoList[i]).strip()
            elif isinstance(infoList[i],str):
                outputLine = infoList[i].strip()
            f.write(outputLine + '\n')
        f.close()


"""
    控制台打印相关
"""
def printList(outList):
    '''

    '''
    if outList:
        for item in outList:
            print item
        print 'len: ',len(outList)


def printEscapeStr(object):
    '''

    '''
    if object:
        print str(object).decode('string_escape')