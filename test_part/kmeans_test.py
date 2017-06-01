#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

if __name__ == '__main__':
    pd.set_option('display.width', 300)
    np.set_printoptions(linewidth=300, suppress=True)

    ## 构造数据
    n_samples = 1500
    random_state = 100
    n_features = 3
    x,y = make_blobs(n_samples=50,cluster_std=[1.0,2,0.5],random_state=random_state)
    # print x
    # print y
    # print type(x),x.shape
    # print type(y),y.shape

    ## 改进的方法：
    model = KMeans(n_clusters=3)
    clustered = model.fit(x)
    # print type(model)
    # print model

    print '聚类中心：',len(clustered.cluster_centers_)
    print clustered.cluster_centers_
    print '聚类结果：',type(clustered.labels_),clustered.labels_
    print '样本点到所属簇中心距离之和：',clustered.inertia_
    y_hat = model.predict(x)
    print type(y_hat)
    print y_hat


    ## 之前有的方法：
    # y_pred = KMeans(n_clusters=3,random_state=random_state).fit_predict(x)
    # print type(y_pred),y_pred.shape
    # print y_pred    #输出的y_pred表示某个样本属于哪一类
    # plt.figure('white')
    # plt.scatter(x[:,0],x[:,1],c=y_pred)
    # plt.show()