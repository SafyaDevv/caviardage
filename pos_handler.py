### this utility script contains functions for pos tagging 
### and handling grammar check & POS-related tasks

import spacy

nlp = spacy.load("en_core_web_lg")

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
