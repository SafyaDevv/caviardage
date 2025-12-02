### This script generates an updated dataset with part-of-speech tagging and sentiment applied to each poem
## as well as other features
## and exports it as a new CSV file
## so it can be used by data_pipeline.py and streamlit_app.py
## to avoid re-computing POS tagging each time those scripts are run

import pandas
from pos_handler import apply_pos, has_unknown_pos
from data_pipeline import clean_df
from sentiment_handler import get_subjectivity, get_polarity

df = clean_df.drop(columns=["grammar-check"]) #Dropping grammar-check column as all values are false & copying to new df


## part of speech section
pos_tags = df["poem"].apply(apply_pos) #generating POS tags for each poem

passage_pos_tags = df["passage"].apply(apply_pos) #generating POS tags for each passage

df.insert(df.columns.get_loc("poem") + 1, "part-of-speech", pos_tags) #inserting new column with POS tags next to poem column
df.insert(df.columns.get_loc("passage") + 1, "passage-part-of-speech", passage_pos_tags) #next to passage column


#removing poems with gibberish / unrecognised words
mask = df["part-of-speech"].apply(has_unknown_pos) #takes each element in series and pass it to function
df = df[~mask] #update df to only keep rows where mask is false

## sentiment analysis section

#for poems
df["sentiment_polarity"] = df["poem"].apply(get_polarity)
df["sentiment_subjectivity"] = df["poem"].apply(get_subjectivity)

#for passages
passage_polarity = df["passage"].apply(get_polarity)
passage_subjectivity = df["passage"].apply(get_subjectivity)

#placing it right after passage
df.insert(df.columns.get_loc("passage") + 2, "passage_sentiment_polarity", passage_polarity) 
df.insert(df.columns.get_loc("passage_sentiment_polarity") + 1, "passage_subjectivity", passage_subjectivity) 

# add word counts features
df["passage-word-count"] = df["passage"].apply(lambda passage: len(passage.split()))
df["poem-word-count"] = df["poem"].apply(lambda poem: len(poem.split()))


#csv generation
df.to_csv("files/better_blackout.csv", index=False)
