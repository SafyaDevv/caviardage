''' Some of the code adapted from following sources:
https://www.datacamp.com/tutorial/introduction-t-sne
https://medium.com/@RobuRishabh/clustering-text-data-with-k-means-and-visualizing-with-t-sne-9bc1fe7d8fed
https://codesignal.com/learn/courses/introduction-to-tf-idf-vectorization-in-python/lessons/navigating-the-weights-of-words-analyzing-tf-idf-scores-in-nlp
'''

## STEP 1: Using kmeans clustering to cluster poems, using poem embeddings only
import plotly.express as px
import matplotlib.pyplot as plot    
from sklearn.cluster import KMeans
import umap.umap_ as umap
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from generate_poem_matrix import get_poem_embeddings
import numpy as np
from data_pipeline import clean_df_v2
import nlp_handler as nlp
from sklearn.feature_extraction.text import TfidfVectorizer

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

# visualizing the clusters
fig = px.scatter(x=reduced_poems[:, 0], y=reduced_poems[:, 1], color=labels)
fig.update_layout(
    title="Visualisation of poem clusters",
)
fig.show()

# function to show example poems from each cluster
def show_examples(cluster_id, n=5):
    index = np.where(labels == cluster_id)[0][:n]
    for i in index:
        print(f"\n[poem {i}] (cluster {cluster_id})")
        print(clean_df_v2.loc[i, "poem"])

show_examples(cluster_id=7, n=10)

# giving each cluster a label based on common themes in poems

poem_texts = clean_df_v2['poem'].tolist()

def get_top_terms(cluster_id):
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

#iterate through each cluster and get top terms
for cluster_id in range(n_clusters):
     print(f"\n[Cluster {cluster_id}] Top terms:")
     top_terms = get_top_terms(cluster_id)
     print(", ".join(top_terms))
      