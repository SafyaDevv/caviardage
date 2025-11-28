### This script generates an updated dataset with part-of-speech tagging applied to each poem
## and exports it as a new CSV file
## so it can be used by data_pipeline.py and streamlit_app.py
## to avoid re-computing POS tagging each time those scripts are run

import pandas
from pos_handler import apply_pos, has_unknown_pos
from data_pipeline import clean_df

df = clean_df.drop(columns=["grammar-check"]) #Dropping grammar-check column as all values are false & copying to new df
poem_index = df.columns.get_loc("poem")

pos_tags = df["poem"].apply(apply_pos) #generating POS tags for each poem

df.insert(poem_index + 1, "part-of-speech", pos_tags) #inserting new column with POS tags next to poem column

#removing poems with gibberish / unrecognised words
mask = df["part-of-speech"].apply(has_unknown_pos) #takes each element in series and pass it to function
df = df[~mask] #update df to only keep rows where mask is false

df.to_csv("files/better_blackout.csv", index=False)