from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Load Data
data = load_digits().data
pca = PCA(2)

# Transform the data
df = pca.fit_transform(data)
df.shape
print(df)

# Initialize the class object
kmeans = KMeans()

# predict the labels of clusters.
label = kmeans.fit_predict(df)
print(kmeans)
print(label)

# Getting the Centroids
centroids = kmeans.cluster_centers_
u_labels = np.unique(label)
print(u_labels)
# plotting the results:
plt.figure(figsize=(10, 10))
for i in u_labels:
    plt.scatter(df[label == i, 0], df[label == i, 1], label=i)
plt.scatter(centroids[:, 0], centroids[:, 1], s=80, color='k')
plt.legend()
plt.savefig('out1.png', dpi=80)
