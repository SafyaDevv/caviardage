### this utility script contains functions for pos tagging 
### and handling grammar check & POS-related tasks

import spacy

nlp = spacy.load("en_core_web_sm")

# **** TOKENISATION AND PART-OF-SPEECH TAGGING ****

#function to apply POS tagging to each poem
def apply_pos(poem):
    doc = nlp(poem)
    pos_tags = [token.pos_ for token in doc]
    
    return pos_tags

#return True if any unknown POS tags (X) are found in the list of tags
#used in generate_dataset.py to filter out poems with unrecognised words
def check_for_unknown_pos(tag):
    if any(t == "X" for t in tag):
        return True
    return False

#function to find poems marked as having good grammar in Blackout dataset
#meaning grammar-check column is True
# /!\ WILL USE LATER FOR ANALYSIS LATER, why are those marked as true?/!\
def get_grammar_check(df):
    df = df[df["grammar-check"]]
    return df["poem"]
