#utility script to generate csv with all frequencies
#so it doesn't have to be computed at runtime

from data_pipeline import clean_df_v2
import analyses
import pandas

#generating frequencies, then turning frequencies dict into dataframe then dataframe into csv
#for poem series
word_frequency_poems = analyses.word_frequency(clean_df_v2["poem"].to_string())

#turn dictionary into tuple, so it can be easily turned into a dataframe
poems_wf = pandas.DataFrame(word_frequency_poems.items(), columns=["word", "frequency"])

poems_wf.to_csv("files/poems_word_frequency.csv", index=False) 

#for passage series
word_frequency_passages = analyses.word_frequency(clean_df_v2["passage"].to_string())
passages_wf = pandas.DataFrame(word_frequency_passages.items(), columns=["word", "frequency"])
passages_wf.to_csv("files/passages_word_frequency.csv", index=False) 


