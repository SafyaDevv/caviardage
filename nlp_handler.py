'''
This script contains functions for natural language processing tasks such as
part-of-speech tagging, word frequency analysis, and sentiment analysis.    
'''

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from collections import Counter

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe('spacytextblob') #will be used for sentiment analysis


def generate_doc(poem):
    doc = nlp(poem)
    return doc

## PART-OF-SPEECH TAGGING ##
#function to get sequence of POS tags for a poem
def apply_pos(doc):
    pos_tags = [token.pos_ for token in doc]
    return pos_tags

#return True if any unknown POS tags (X) are found in the list of tags
#used in generate_dataset.py to filter out poems with unrecognised words
def has_unknown_pos(tags):
    return any(t == "X" for t in tags)

## WORD FREQUENCY ##

#function to get word frequency for all text
#stopword parameters, bool to decide whether stop words are wanted or not
#default is false
def word_frequency(doc, keep_stopwords = False):

    if(keep_stopwords):
        tokens = [token.text
                for token in doc
                if not token.is_space
                if not token.is_punct]
    else:
        tokens = [token.text
                for token in doc 
                if not token.is_stop
                if not token.is_space
                if not token.is_punct]    

    words_frequency = Counter(tokens)
    return words_frequency

## SENTIMENT ANALYSIS ##

#compute sentiment analysis on poem and return polarity score
# number between -1 and 1, -1 = negative, 0 = neutral, 1 = positive
def get_polarity(poem):
       doc = nlp(poem)
       return doc._.blob.sentiment.polarity

#compute sentiment analysis on poem and return sbjectivity score, 
#number between 0.0 and 1, 1 = subjective, 0 = objective
def get_subjectivity(poem):
        doc = nlp(poem)
        return doc._.blob.sentiment.subjectivity

