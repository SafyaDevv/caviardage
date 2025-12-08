''' Following tutorial : https://towardsdev.com/mastering-data-clustering-with-embedding-models-87a228d67405
Some of the code is adapted from there
'''

## STEP 1: Using kmeans clustering to cluster poems, using poem embeddings only
import matplotlib.pyplot as plot
from sklearn.cluster import KMeans
from generate_poem_matrix import get_poem_embeddings
import umap.umap_ as umap
import numpy as np
from data_pipeline import clean_df_v2

poems = get_poem_embeddings() #get scaled poem embeddings

# reducing dimensions for visualisation
reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=2, random_state=0)
reduced_embeddings = reducer.fit_transform(poems)

# # plotting before clustering
# plot.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1])
# plot.title("Poem Embeddings visualisation (UMAP 2D projection)")
# plot.show()

#clustering
kmeans = KMeans(n_clusters=10, random_state=0)
labels = kmeans.fit_predict(poems)

def show_examples(cluster_id, n=5):
    idx = np.where(labels == cluster_id)[0][:n]
    for i in idx:
        print(f"\n[poem {i}] (cluster {cluster_id})")
        print(clean_df_v2.loc[i, "poem"])

show_examples(cluster_id=0, n=10)

show_examples(cluster_id=5, n=10)

# # plotting after clustering
# plot.figure(figsize=(10, 6))
# plot.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c=labels, cmap='tab10')
# plot.title("Poem Embeddings clustered using KMeans (UMAP 2D projection)")
# plot.show()