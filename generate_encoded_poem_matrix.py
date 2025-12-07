import re
import numpy
import spacy
import pandas
from data_pipeline import clean_df_v2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize

nlp = spacy.load("en_core_web_lg")

### EMBEDDING AND ENCODING FEATURES ###

def get_vector(poem):
    doc = nlp(poem)
    vector = doc.vector
    return vector

#embedding poems into vectors and putting them in a numpy nd array
poem_matrix = numpy.vstack(clean_df_v2["poem"].apply(get_vector)) #vstack allows to keep each poem vector as a row in the matrix

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
poem_matrix = normalize(poem_matrix, axis=1) #normalising each row

## STORING IN DF THEN CSV ##

poem_matrix_df = pandas.DataFrame(poem_matrix, index=clean_df_v2.index) #turning into dataframe to store as csv, using original dataframe index to be able to link back to poems later

poem_matrix_df.to_csv("files/poem_matrix.csv", index=False)