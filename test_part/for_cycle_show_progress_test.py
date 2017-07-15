# -*- coding:utf-8 -*-

import time
import progressbar
from time import sleep
from tqdm import tqdm

"""
    测试python显示进度条的程序
"""
if __name__ == '__main__':

    for i in tqdm(range(1000)):
        sleep(0.01)




    # p = progressbar.ProgressBar()
    # N = 1000
    # p.start(N)
    # for i in range(N):
    #     time.sleep(0.01)
    #     p.update(i+1)
    # p.finish()



    # p = progressbar.ProgressBar()
    # N = 1000
    # for i in p(range(N)):
    #     time.sleep(0.01)
