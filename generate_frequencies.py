#utility script to generate csv with all frequencies
#so it doesn't have to be computed at runtime

import pandas

import nlp_handler as nlp
from data_pipeline import clean_df_v2

#generating frequencies, then turning frequencies dict into dataframe then dataframe into csv
#for poem series
doc_poem = clean_df_v2["poem"].to_string().apply(nlp.generate_doc)
doc_passage = clean_df_v2["passage"].to_string().apply(nlp.generate_doc)
word_frequency_poems = nlp.get_word_frequency(doc_poem)

#turn dictionary into tuple, so it can be easily turned into a dataframe
poems_wf = pandas.DataFrame(word_frequency_poems.items(), columns=["word", "frequency"])

poems_wf.to_csv("files/poems_word_frequency.csv", index=False) 

#for passage series
word_frequency_passages = nlp.get_word_frequency(doc_passage)

passages_wf = pandas.DataFrame(word_frequency_passages.items(), columns=["word", "frequency"])
passages_wf.to_csv("files/passages_word_frequency.csv", index=False) 


