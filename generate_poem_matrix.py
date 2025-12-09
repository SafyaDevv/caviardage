import re
import numpy
import pandas
from data_pipeline import clean_df_v2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize
from sentence_transformers import SentenceTransformer


### EMBEDDING AND ENCODING FEATURES ###

model = SentenceTransformer('all-MiniLM-L6-v2')

#embedding poem into vectors using sentence_transformers, return an nd array
poem_embeddings = model.encode(clean_df_v2["poem"].tolist(), convert_to_numpy=True) 
poem_matrix = poem_embeddings

#returns scaled poem embeddings for use in clustering.py
def get_poem_embeddings():
    z_scaler = StandardScaler()
    return z_scaler.fit_transform(poem_embeddings)

def get_normalised_poem_embeddings():
    return normalize(poem_embeddings, axis=1)

#encoding sequence of pos tags using TfidfVectorizer and adding them to matrix that will be use for cosine similarity
pos_strings = clean_df_v2["poem-pos"].apply(
    lambda pos_string: 
    re.sub(r"[\[\],']", "", pos_string)) #turn stringified list into space-separated pos tags for TfidfVectorizer

vectorizer = TfidfVectorizer(ngram_range=(1,3), token_pattern=r"\S+") # using ngrams of size 1 to 3, token pattern = tags separated by whitespace
pos_vectors = vectorizer.fit_transform(pos_strings)

### SCALING AND NORMALISING FEATURES ###
z_scaler = StandardScaler()

ppl_gpt2 = numpy.log1p(clean_df_v2["ppl-gpt2"]) #starting by logscaling perplexity scores to reduce right skewness

num_features = numpy.column_stack((ppl_gpt2, clean_df_v2["poem-polarity"], clean_df_v2["poem-subjectivity"], 
                  clean_df_v2["poem-word-count"])) #stacking numeric features as columns in a "temporary" matrix

poem_matrix = numpy.hstack((poem_matrix, pos_vectors.toarray(), num_features)) #adding pos vectors and numeric features to poem matrix, concatening the features

poem_matrix = z_scaler.fit_transform(poem_matrix) #scaling all features 

#returning poem matrix function before normalisation
def get_poem_matrix():
    return poem_matrix

poem_matrix_normalized = normalize(poem_matrix, axis=1) #normalising each row

## STORING IN DF THEN CSV ##

poem_matrix_df = pandas.DataFrame(poem_matrix_normalized, index=clean_df_v2.index) #turning into dataframe to store as csv, using original dataframe index to be able to link back to poems later

poem_matrix_df.to_csv("files/poem_matrix.csv", index=True)
