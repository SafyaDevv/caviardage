'''
This script generates an updated dataset with new features such as part-of-speech tagging 
and sentiment applied to each poem and exports it as a new CSV file
Using NLP functions from nlp_handler.py
so it can be used by data_pipeline.py and streamlit_app.py
to avoid re-computing everything each time those scripts are run.
'''

import clustering as themes
import plotly.io as pio

import nlp_handler as nlp
from data_pipeline import clean_df

## SETUP ##

df = clean_df.copy() #copying to new df
doc_poem = clean_df["poem"].apply(nlp.generate_doc) #getting tokenised poems
doc_pass = clean_df["passage"].apply(nlp.generate_doc) #getting tokenised passages

## PART-OF-SPEECH TAGGING ##

pos_tags = doc_poem.apply(nlp.apply_pos) #generating POS TAGS for each poem 
df.insert(df.columns.get_loc("poem") + 1, "poem-pos", pos_tags) #inserting new column with POS tags next to poem column

passage_pos_tags = doc_pass.apply(nlp.apply_pos) #same for passages
df.insert(df.columns.get_loc("passage") + 1, "passage-pos", passage_pos_tags)

#removing rows that has poems gibberish / unrecognised words (meaning rows with any X POS tags)
mask = df["poem-pos"].apply(nlp.has_unknown_pos) 
df = df[~mask]

## SENTIMENT ANALYSIS ##
df["poem-polarity"] = doc_poem.apply(nlp.get_polarity)
df["poem-subjectivity"] = doc_poem.apply(nlp.get_subjectivity)

passage_polarity = doc_pass.apply(nlp.get_polarity)
passage_subjectivity = doc_pass.apply(nlp.get_subjectivity)

df.insert(df.columns.get_loc("passage") + 2, "passage-polarity", passage_polarity) #putting it after passage-pos tags
df.insert(df.columns.get_loc("passage-polarity") + 1, "passage-subjectivity", passage_subjectivity)

## WORD COUNT ##
word_count = doc_poem.apply(lambda poem: len(poem)) #counting tokens in each poem
df["poem-word-count"] = word_count

word_count_passage = doc_pass.apply(lambda passage: len(passage))
passage_wc = word_count_passage
df.insert(df.columns.get_loc("passage-subjectivity") + 1, "passage-word-count", passage_wc) #putting it after passage-subjectivity

## POEM LABELS ##
poem_clusters_df, vis_fig = themes.clustering(visualisation=True) #getting poem clusters with clusters ids and labels
df["poem-cluster-id"] = poem_clusters_df["cluster_id"]
df["poem-theme"] = poem_clusters_df["theme"]

## EXPORTING VISUALISATION AS JSON##
pio.write_json(vis_fig, "files/poem_clusters.json")

#csv generation
df.to_csv("files/caviardage_dataset.csv", index=False)