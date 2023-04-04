import numpy as np

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram
from sklearn.datasets import load_iris
from sklearn.cluster import AgglomerativeClustering


import plotly.figure_factory as ff
import scipy.cluster.hierarchy as sch
import numpy as np

X = np.matrix([[0,0,0,0],[13,0,0,0],[2,14,0,0],[17,1,18,0]])

names = "0123"
fig = ff.create_dendrogram(X,
                           orientation='left',
                           labels=names,
                           linkagefun=lambda x: sch.linkage(x, "average"),)
fig.update_layout(width=800, height=800)
fig.show()