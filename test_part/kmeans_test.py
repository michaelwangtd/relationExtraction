#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

if __name__ == '__main__':

    ## 构造数据
    n_samples = 1500
    random_state = 170
    n_features = 3
    x,y = make_blobs(n_samples=100,cluster_std=[1.0,2,0.5],random_state=random_state)
    # print x
    # print y
    # print type(x),x.shape
    # print type(y),y.shape

    y_pred = KMeans(n_clusters=3,random_state=random_state).fit_predict(x)
    print type(y_pred),y_pred.shape
    print y_pred    #输出的y_pred表示某个样本属于哪一类
    plt.figure('white')
    plt.scatter(x[:,0],x[:,1],c=y_pred)
    plt.show()