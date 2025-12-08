''' Some of the code adapted from following sources:
https://www.datacamp.com/tutorial/introduction-t-sne
https://medium.com/@RobuRishabh/clustering-text-data-with-k-means-and-visualizing-with-t-sne-9bc1fe7d8fed
https://codesignal.com/learn/courses/introduction-to-tf-idf-vectorization-in-python/lessons/navigating-the-weights-of-words-analyzing-tf-idf-scores-in-nlp
'''

import plotly.express as px
import umap.umap_ as umap
import numpy as np
import pandas
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from generate_poem_matrix import get_poem_embeddings
from data_pipeline import clean_df_v2

from sklearn.feature_extraction.text import TfidfVectorizer

# Function to run kmeans clustering on poem embeddings
# called in get_poem_clusters()
def run_kmeans(n_clusters):
    poems = get_poem_embeddings() #get scaled poem embeddings

    # reducing dimensionality using PCA first then UMAP
    pca = PCA(n_components=50, random_state=42)
    poems_pca = pca.fit_transform(poems)

    reducer = umap.UMAP(n_neighbors=15, n_components=15, metric='cosine', random_state=42, low_memory=False)
    reduced_poems = reducer.fit_transform(poems_pca)

    # clustering
    n_clusters = 10
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(reduced_poems)
    print("Cluster labels:", labels)
    
    return reduced_poems, labels, n_clusters

poems, labels, n_clusters = run_kmeans(n_clusters=10)

## START HERE 
# FUNCTION THAT RETURNS POEM INDICES WITH CLUSTER IDS AND LABELS ##
#...by executing other functions in this script
# returns either visualisation figure and poem clusters df,
# or just poem clusters df depending on parameter
def clustering(visualisation=False):
    poems, labels, n_clusters = run_kmeans(n_clusters=10)

    poem_with_clusters = clean_df_v2["poem"].to_frame()
    poem_with_clusters['cluster_id'] = labels

    labels_names = labels.tolist()

    #create dictionary of cluster ids to names
    cluster_id_to_name = {
        0: "Familial",
        1: "Animalistic",
        2: "Cosmic",
        3: "Instrumental",
        4: "Existential",
        5: "Maritime",
        6: "Emotional",
        7: "Appearance",
        8: "Botanical",
        9: "Spiritual" }

    #naming clusters
    for i in range(len(labels_names)):
        if labels_names[i] in cluster_id_to_name:
            labels_names[i] = cluster_id_to_name[labels_names[i]]
        else:
            raise ValueError("Cluster id not in range")
    
    poem_with_clusters['theme'] = labels_names

    vis_fig = get_clustering_vis(poems, labels, poem_with_clusters)

    if visualisation:
        return poem_with_clusters, vis_fig
    else:
        return poem_with_clusters


# Function to visualise the clusters
# get_poem_clusters() needs to be run first to get reduced poems, cluster ids (labels),
# and label names
def get_clustering_vis(poems, labels, poem_df_with_clusters):
    #further reducing dimensionality to 3D for visualisation
    reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, n_components=3)
    reduced_poems = reducer.fit_transform(poems)

#creating df for visualisation
    visualisation_df = pandas.DataFrame({
        'x': poems[:, 0],
        'y': poems[:, 1],
        'z': poems[:, 2],
        'poem': poem_df_with_clusters['poem'],
        'cluster_id': labels,
        'theme': poem_df_with_clusters['theme'],
        'index': poem_df_with_clusters.index
        })

    fig = px.scatter_3d(
        visualisation_df, x='x', y='y', z='z', color='cluster_id', 
        hover_data=['index', 'poem', 'theme'])
    fig.update_layout(
        title="3D Visualisation of poem clusters")
        
    return fig

## TESTING ZONE ##

clustering(visualisation=True)
poem_clusters_df, vis_fig = clustering(visualisation=True)
print(poem_clusters_df.head())
print(poem_clusters_df.columns.values)
vis_fig.show()











### LABELLING CLUSTERS ###

## NOTE: The following code was used during development
## but is not called anywhere in the project 

# giving each cluster a label based on common themes in poems
def get_top_terms(cluster_id): 
    poem_texts = clean_df_v2['poem'].tolist()
    indices = np.where(labels == cluster_id)[0] #get indices of poems in that cluster
    cluster_poems = [poem_texts[i] for i in indices] #create list of poems in that cluster
    #find top terms using TFIDF
    vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(cluster_poems)
    feature_names = np.array(vectorizer.get_feature_names_out())
    mean_tfidf = tfidf_matrix.mean(axis=0).A1 #average tfidf score for each term in cluster 
                                             # (how important is that term in that cluster), 
                                             # then flatten it
    top_indices = mean_tfidf.argsort()[::-1][:10] #slice through array of indices 
                                            #sorted by descending tfidf score to get top 10 terms
    top_terms = feature_names[top_indices]
    
    
    return top_terms

def print_top_terms():
    #iterate through each cluster and print top terms for each cluster
    for cluster_id in range(n_clusters):
        print(f"\n[Cluster {cluster_id}] Top terms:")
        top_terms = get_top_terms(cluster_id)
        print(", ".join(top_terms))
      
# function to show example poems from each cluster
# def show_examples(cluster_id, n=5):
#     index = np.where(labels == cluster_id)[0][:n]
#     for i in index:
#         print(f"\n[poem {i}] (cluster {cluster_id})")
#         print(clean_df_v2.loc[i, "poem"])

# show_examples(cluster_id=7, n=10)
