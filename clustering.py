''' Some of the code adapted from following sources:
https://www.datacamp.com/tutorial/introduction-t-sne
https://medium.com/@RobuRishabh/clustering-text-data-with-k-means-and-visualizing-with-t-sne-9bc1fe7d8fed
https://codesignal.com/learn/courses/introduction-to-tf-idf-vectorization-in-python/lessons/navigating-the-weights-of-words-analyzing-tf-idf-scores-in-nlp
'''
import plotly.express as px
import umap.umap_ as umap
import numpy as np
import pandas
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
from sklearn.feature_extraction.text import TfidfVectorizer
from encoding_features import get_normalised_poem_embeddings

from data_pipeline import clean_df_v2

# Function to run kmeans clustering on poem embeddings
# called in get_poem_clusters()
def run_kmeans(n_clusters):
    print("Running Kmeans clustering...")
    poems = get_normalised_poem_embeddings()

    #DEBUG LINE
    print(f"Original poems shape: {poems.shape}")

    # reducing dimensionality using PCA first then UMAP
    pca = PCA(n_components=50, random_state=42)
    poems_pca = pca.fit_transform(poems)

    print(f"After PCA shape: {poems_pca.shape}")

    reducer = umap.UMAP(n_neighbors=15, n_jobs=1, n_components=15, metric='cosine', random_state=42, low_memory=False)    
    reduced_poems = reducer.fit_transform(poems_pca)
    print(f"After UMAP shape: {reduced_poems.shape}")

    # clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(reduced_poems)

    print(f"Labels shape: {labels.shape}")

    # Calculate Silhoutte Score
    score = silhouette_score(reduced_poems, labels, metric='cosine')
    print(f"Silhouette Score for {n_clusters} clusters: {score:.3f}")

    print("Finishing Kmeans clustering...")
    return reduced_poems, labels, n_clusters

if __name__ == "__main__":
    poems, labels, n_clusters = run_kmeans(n_clusters=12)
    print(f"clean_df_v2 shape: {len(clean_df_v2)}")

## START HERE 
# FUNCTION THAT RETURNS POEM INDICES WITH CLUSTER IDS AND LABELS ##
#...by executing other functions in this script
# returns either visualisation figure and poem clusters df,
# or just poem clusters df depending on parameter
def clustering(visualisation=False):
    poems, labels, n_clusters = run_kmeans(n_clusters=12)

    poem_with_clusters = clean_df_v2["poem"].to_frame()
    poem_with_clusters['cluster_id'] = labels

    labels_names = labels.tolist()

    #create dictionary of cluster ids to names
    cluster_id_to_name = {
        0: "History, thoughts, people and events",
        1: "Time and Seasons, ",
        2: "Water and its bodies",
        3: "Family, friends and people",
        4: "Feelings, love and pain",
        5: "Poetry itself",
        6: "Flowers and those who like them",
        7: "Looking and kissing",
        8: "Anatomy and Things",
        9: "Night and Day, Darkness and Light",
        10: "Forest and animals",
        11: "Spiritual"}

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
#creating df for visualisation

#further reducing dimensions to 3D for visualisation
    print("Starting vis...")
    reducer_3d = umap.UMAP(n_neighbors=15, n_jobs=1, n_components=3, metric='cosine', random_state=42, low_memory=False)
    poems = reducer_3d.fit_transform(poems)

    visualisation_df = pandas.DataFrame({
        'x': poems[:, 0],
        'y': poems[:, 1],
        'z': poems[:, 2],
        'poem': poem_df_with_clusters['poem'],
        'cluster_id': labels,
        'theme': poem_df_with_clusters['theme'],
        'index': poem_df_with_clusters.index
        })

    fig = px.scatter_3d(visualisation_df, x='x', y='y', z='z', color='theme', 
        custom_data=['index', 'poem', 'theme'], opacity=0.7)
    
    fig.update_layout(title="3D Visualisation of poem themes (clusters)",
        legend_title="Poem Themes",
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Century Gothic"),
        legend=dict(
        font=dict(size=18),
        title_font=dict(size=20),
        itemsizing='constant'))
    
    fig.update_traces(hovertemplate=(
            "Index: %{customdata[0]}<br>"
            "Poem: <b>%{customdata[1]}</b><br>"
            "Theme: %{customdata[2]}<br><extra></extra>"))
        
    return fig

## LABELLING CLUSTERS ###
# giving each cluster a label based on common themes in poems
def get_top_terms(labels, cluster_id, n_terms=10): 
    poem_texts = clean_df_v2['poem'].tolist()

    vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(poem_texts)
    feature_names = np.array(vectorizer.get_feature_names_out())

    #get indices of poems in that cluster
    indices = np.where(labels == cluster_id)[0] 

    #find top terms using TFIDF
    cluster_poems = tfidf_matrix[indices] 

    mean_tfidf = cluster_poems.mean(axis=0).A1 #average tfidf score for each term in cluster 
                                             # (how important is that term in that cluster), 
                                             # then flatten it
    top_indices = mean_tfidf.argsort()[::-1][:n_terms] #slice through array of indices 
                                            #sorted by descending tfidf score to get top 10 terms
    top_terms = feature_names[top_indices]
    
    return top_terms

def print_top_terms(labels, n_clusters):
    #iterate through each cluster and print top terms for each cluster
    for cluster_id in range(n_clusters):
        print(f"\n[Cluster {cluster_id}] Top terms:")
        top_terms = get_top_terms(labels, cluster_id)
        print(", ".join(top_terms))
  
# function to show example poems from each cluster
def show_examples(labels, cluster_id, n=5):
    index = np.where(labels == cluster_id)[0][:n]
    for i in index:
        print(f"\n[poem {i}] (cluster {cluster_id})")
        print(clean_df_v2.loc[i, "poem"])


# TESTING ZONE ##

if __name__ == "__main__":
    poem_clusters_df, vis_fig = clustering(visualisation=True)
    vis_fig.show()

    print(f"Labels shape in testing zone: {labels.shape}")
    poem_clusters_df["cluster_id"] = labels

    # print_top_terms(labels, n_clusters)

    # show_examples(labels, cluster_id=7, n=10)