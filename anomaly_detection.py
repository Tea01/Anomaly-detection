# -*- coding: utf-8 -*-
"""
Authors:

Jairo El Yazidi Ríos
Tea Shkurti

In data analysis, *anomaly detection* (also referred to as outlier detection and sometimes as novelty detection) is generally understood to be the identification of rare items, events or observations which deviate significantly from the majority of the data and do not conform to a well defined notion of normal behaviour.
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
# %matplotlib inline

import scipy as stats
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

X=np.load('data.npy')
X

"""Plot of the data with the center"""

plt.scatter(X[:,0], X[:,1])

"""Clustering the data"""

from sklearn.cluster import KMeans
k = 2
kmeans = KMeans(n_clusters = k, random_state = 1).fit(X)

plt.scatter(X[:,0], X[:,1], c=kmeans.labels_, cmap='brg', alpha=0.4)  # plot points with cluster dependent colors
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], c = 'black', s=100)
plt.show()

"""Lets print each of the clusters"""

for k in range(0,2):
    plt.scatter(X[kmeans.labels_==k,0], X[kmeans.labels_==k,1],color =(['blue','green'])[k])
    plt.show()

"""Detecting anomalies on the data finding points far from the centroids"""

eucledianDist = np.sqrt(np.sum((X - kmeans.cluster_centers_[kmeans.labels_])**2,axis=-1))
plt.scatter(X[:,0], X[:,1],c=(eucledianDist),cmap='Reds')

medians = np.r_[np.median(eucledianDist[kmeans.labels_==0]),np.median(eucledianDist[kmeans.labels_==1])]
eucledianMedians = np.abs(eucledianDist/medians[kmeans.labels_])
plt.scatter(X[:,0], X[:,1],c=(eucledianMedians),cmap='Reds')

"""Eucledian distance between the datapoints and the center"""

data = X[kmeans.labels_==0,:]
center = kmeans.cluster_centers_[0]

eucledianDist = np.sqrt(np.sum((data[:,0:2] - center)**2,axis=1))

plt.scatter(data[:,0], data[:,1],c=(eucledianDist),cmap='Blues')
plt.scatter(center[0], center[1], c = 'red', s=100)

"""Here, we consider anomaly datapoints that are distant for the center a threshhold. """

threshold = 10

plt.scatter(data[:,0], data[:,1],c=(eucledianDist>threshold))
plt.scatter(center[0], center[1], c = 'red', s=100)

"""The Eucledian distance does not seems the best one for this data set. Let's try the Mahalanobis distance."""

def calculateMahalanobis(data):
    y_mu = data - np.mean(data,axis=0)
    cov = np.cov(data.values.T)
    inv_covmat = np.linalg.inv(cov)
    left = np.dot(y_mu, inv_covmat)
    mahal = np.dot(left, y_mu.T)
    return mahal.diagonal()
  

mahalanobisDistance= calculateMahalanobis(pd.DataFrame(data, columns = ['x','y']))
plt.scatter(data[:,0], data[:,1],c=(mahalanobisDistance),cmap='Greens')
plt.scatter(center[0], center[1], c = 'red', s=100)

"""Detecting anomalies by considering the Mahalanobis distance."""

threshold = 2

plt.scatter(data[:,0], data[:,1],c=(mahalanobisDistance>threshold))
plt.scatter(center[0], center[1], c = 'red', s=100)

"""There is no correct way to determine the threshold. One way is to try different values and compute the percentage of anomalies each threshold detects. The number of anomalies should be very small, by defition (e.g., between 0-5%). """

for threshold in np.linspace(start=0.5, stop=10, num=20):
    print(f"{threshold} {(mahalanobisDistance>threshold).sum()/mahalanobisDistance.shape[0]}")

"""# Short competition

Our aim is to detect frauds in finantial transactions. The dataset consists of features related to financial transactions, some of which may involve fraudulent activity. The data has been normalized and dimentionality reduced to prevent the use of heuristics based on human knowledge. Your task is to identify anomalies in order to detect possible fraud. Frauds are frequently atypical transactions. It is worth noting that atypical transactions are not necessarily fraudulent.
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
# %matplotlib inline

import scipy as stats
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
data = np.load("anomalyDATA.npy")
data

"""The dataset comprises 5 columns, with the first 4 columns providing transaction features such as transaction value, time, and agent's salary. The fifth column contains three distinct values: 0, 1, and nan. The value 0 indicates that the transaction is not fraudulent, while 1 indicates that it is fraudulent. The "nan" value denotes instances where the financial institution is unsure whether the transaction is fraudulent or not."""

np.unique(data[:,4])

#Your code here
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV

train = data[np.isnan(data[:,4])==False]
test = data[np.isnan(data[:,4])]

kmeans = KMeans(n_init='auto', random_state = 1)
param = {'n_clusters':[2, 4, 6, 8, 10], 'algorithm':['lloyd', 'elkan']}
km_gs = GridSearchCV(kmeans, param, n_jobs=-1, cv=10)

km_gs.fit(train[:,:4])
test_pred = km_gs.predict(test[:,:4])

def calculateMahalanobis(data):
    y_mu = data - np.mean(data,axis=0)
    cov = np.cov(data.values.T)
    inv_covmat = np.linalg.inv(cov)
    left = np.dot(y_mu, inv_covmat)
    mahal = np.dot(left, y_mu.T)
    return mahal.diagonal()

mahalanobisDistances = []
k = km_gs.best_params_['n_clusters']
for i in range(0,k):
    clusterI = test[test_pred==i]
    mahalanobisDistances.append(calculateMahalanobis(pd.DataFrame(clusterI[:,:4], columns = ['w','x','y','z'])))

thresholds = []
for i in range(0,k):
    for threshold in np.linspace(start=0.5, stop=15, num=30):
        percent = (mahalanobisDistances[i]>threshold).sum()/mahalanobisDistances[i].shape[0]
        if percent < 0.05:
            thresholds.append(threshold)
            break

for i in range(0,k):
    test[test_pred==i, 4] = mahalanobisDistances[i] > thresholds[i]

print(np.count_nonzero(test[:,4])/test.shape[0])
