### this utility script contains functions for pos tagging 
### and handling grammar check & POS-related tasks

import spacy
#from data_pipeline import blackout_df

nlp = spacy.load("en_core_web_sm")

# **** TOKENISATION AND PART-OF-SPEECH TAGGING ****

#function to apply POS tagging to each poem
def apply_pos(poem):
    doc = nlp(poem)
    pos_tags = [token.pos_ for token in doc]
    return pos_tags

#return True if any unknown POS tags (X) are found in the list of tags
#used in generate_dataset.py to filter out poems with unrecognised words
def has_unknown_pos(tags):
    return any(t == "X" for t in tags)

#function to find poems marked as having good grammar in Blackout dataset
#meaning grammar-check column is True
# /!\ WILL USE LATER FOR ANALYSIS LATER, why are those marked as true?/!\
def get_grammar_check(df):
    df = df[df["grammar-check"]]
    return df["poem"]

#NOTE: THE GOAL HEAR WAS TO CHECK THE POS OF POEMS MARKED AS GOOD GRAMMAR
#BUT IT's NOT TOO IMPORTANT SO I'M LEAVING IT FOR NOW !!!!
# good_grammar_poems = blackout_df[get_grammar_check(blackout_df)]
# tags = good_grammar_poems["poem"].apply(apply_pos)
# print(tags)
