import spacy
from data_pipeline import normalised_df
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load("en_core_web_lg")

#embedding poems into vectors
def get_vector(poem):
    doc = nlp(poem)
    vector = doc.vector
    return vector

# #replacing poem by poem vectors in dataframe
# normalised_df["poem-vector"] = normalised_df["poem"].apply(
#     lambda poem: get_vector(poem))
# normalised_df.drop(columns=["poem"], inplace=True)

# #encoding sequence of pos tags using TfidfVectorizer and replacing poem-pos by poem-pos-vectors in dataframe
# normalised_df["poem-pos"] = normalised_df["poem-pos"].apply(
#     lambda pos_list: " ".join(pos_list))

# vectorizer = TfidfVectorizer(ngram_range=(3,5), token_pattern=r"\S+") #using non-whitespace characters as tokens, ngrams match lenght of each tag
# pos_vectors = vectorizer.fit_transform(normalised_df["poem-pos"])

# normalised_df["poem-pos-vector"] = list(pos_vectors.toarray())
# normalised_df.drop(columns=["poem-pos"], inplace=True)

# #storing in new csv
# normalised_df.to_csv("files/normalised_data.csv", index=False)