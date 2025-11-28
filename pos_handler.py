import spacy
from data_cleaning import clean_df, blackout_df

nlp = spacy.load("en_core_web_sm")

#print(clean_df["poem"].to_string)


# **** TOKENISATION AND PART-OF-SPEECH TAGGING ****

doc = nlp(clean_df["poem"].to_string())

#function to apply POS tagging to each poem
def apply_pos(poem):
    doc = nlp(poem)
    pos_tags = [token.pos_ for token in doc]
    
    return pos_tags

clean_df["part-of-speech"] = clean_df["poem"].apply(apply_pos)

print(clean_df[["poem", "part-of-speech"]].head())





    


#function to find poems marked as having good grammar in Blackout dataset
#meaning grammar-check column is True
# /!\ WILL USE LATER FOR ANALYSIS LATER, why are those marked as true?/!\
def get_grammar_check(df):
    df = df[df["grammar-check"]]
    return df["poem"]




