import spacy
from data_cleaning import clean_df, blackout_df

nlp = spacy.load("en_core_web_sm")

#function to find poems marked as having good grammar in Blackout dataset
#meaning grammar-check column is True
def get_grammar_check(df):
    df = df[df["grammar-check"]]
    return df["poem"]


   

# *** LOOKING AT GRAMMAR CHECKS ***
#goodGrammar = cleanDf[cleanDf["grammar-check"] == True]
#print(len(goodGrammar)) #NO POEMS IN CLEANED DATASET ARE MARKED AS HAVING GOOD GRAMMAR

#Storing Poems marked as having "good grammar" in the original dataset


