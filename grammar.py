import spacy

import data_cleaning as data

data = data.clean_df

nlp = spacy.load("en_core_web_sm")


def get_grammar_check(df):
    df = df[df["grammar-check"]]
    return df["poem"].tolist() 

   

# *** LOOKING AT GRAMMAR CHECKS ***
#goodGrammar = cleanDf[cleanDf["grammar-check"] == True]
#print(len(goodGrammar)) #NO POEMS IN CLEANED DATASET ARE MARKED AS HAVING GOOD GRAMMAR

#Storing Poems marked as having "good grammar" in the original dataset


