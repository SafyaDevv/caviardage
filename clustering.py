''' Following tutorial : https://towardsdev.com/mastering-data-clustering-with-embedding-models-87a228d67405
Some of the code is adapted from there
'''

## STEP 1: Using kmeans clustering to cluster poems, using poem embeddings only
import matplotlib.pyplot as plot
from sklearn.cluster import KMeans
from generate_poem_matrix import get_poem_embeddings
import umap.umap_ as umap

poems = get_poem_embeddings()

# reducing dimensions for visualisation
reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2)
reduced_embeddings = reducer.fit_transform(poems)

plot.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], cmap='viridis')
plot.colorbar()
plot.show()

# kmeans = KMeans(n_clusters=5, random_state=0)

# kmeans.fit(poems)

# cluster_labels = kmeans.labels_

# print("Cluster labels for each poem:")
# print(cluster_labels)