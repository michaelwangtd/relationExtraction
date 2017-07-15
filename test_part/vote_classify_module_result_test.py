# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
from utils import inout
from utils.inout import printEscapeStr
from collections import OrderedDict
import time
import codecs

if __name__ == '__main__':

    filePath = inout.getDataAnalysisPath('test.txt')

    fr = codecs.open(filePath,'rb')

    while True:
        line = fr.readline()
        if line:
            reTuple = eval(line.split('DIV')[1].split('INNER')[1])
            print type(reTuple),reTuple,len(reTuple)
            if len(reTuple)==1:
                print reTuple[0]
        else:
            break











