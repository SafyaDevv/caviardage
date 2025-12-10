import re
import numpy
import pandas
import scipy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import OneHotEncoder

from data_pipeline import clean_df_v2

### EMBEDDING AND ENCODING FEATURES ###

model = SentenceTransformer('all-MiniLM-L6-v2')

#embedding poem into vectors using sentence_transformers, return an nd array
poem_embeddings = model.encode(clean_df_v2["poem"].tolist(), convert_to_numpy=True) 

#returns normalised poem embeddings for use in clustering.py
def get_normalised_poem_embeddings():
    return normalize(poem_embeddings, axis=1)

poem_embeddings_normalised = normalize(poem_embeddings, axis=1)

#encoding sequence of pos tags using TfidfVectorizer and adding them to matrix that will be use for cosine similarity
pos_strings = clean_df_v2["poem-pos"].apply(
    lambda pos_string: 
    re.sub(r"[\[\],']", "", pos_string)) #turn stringified list into space-separated pos tags for TfidfVectorizer

vectorizer = TfidfVectorizer(ngram_range=(1,3), token_pattern=r"\S+") # using ngrams of size 1 to 3, token pattern = tags separated by whitespace
pos_vectors = vectorizer.fit_transform(pos_strings)

pos_vectors_scaled = StandardScaler(with_mean=False).fit_transform(pos_vectors) #scaling sparse matrix

#hot encoding poem-cluster-id
ohe = OneHotEncoder(sparse_output=False)
poem_cluster_ids = clean_df_v2[["poem-cluster-id"]]
ids_encoded = ohe.fit_transform(poem_cluster_ids)

#building the matrix used for cosine similarity
ppl_gpt2 = numpy.log1p(clean_df_v2["ppl-gpt2"]) #starting by logscaling perplexity scores to reduce right skewness

num_features = numpy.column_stack((ppl_gpt2, clean_df_v2["poem-polarity"], clean_df_v2["poem-subjectivity"], 
                  clean_df_v2["poem-word-count"])) #stacking numeric features as columns in a "temporary" matrix

num_features_scaled = StandardScaler().fit_transform(num_features)

ids_encoded_scaled = StandardScaler().fit_transform(ids_encoded) 

#concatening the features into matrix
poem_matrix = scipy.sparse.hstack((pos_vectors_scaled, num_features_scaled, ids_encoded_scaled)) 

#returning poem matrix function before normalisation
def get_poem_matrix():
    return poem_matrix

poem_matrix_normalized = normalize(poem_matrix, axis=1) #normalising each row

def get_poem_matrix_normalized():
    return poem_matrix_normalized