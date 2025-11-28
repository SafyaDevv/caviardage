import spacy

nlp = spacy.load("en_core_web_sm")

# **** TOKENISATION AND PART-OF-SPEECH TAGGING ****

#function to apply POS tagging to each poem
def apply_pos(poem):
    doc = nlp(poem)
    pos_tags = [token.pos_ for token in doc]
    
    return pos_tags

#function to find poems marked as having good grammar in Blackout dataset
#meaning grammar-check column is True
# /!\ WILL USE LATER FOR ANALYSIS LATER, why are those marked as true?/!\
def get_grammar_check(df):
    df = df[df["grammar-check"]]
    return df["poem"]




