##this utility script contains functions relating to sentiment tagging

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

#adding texblob extension to spacy nlp pipeline
nlp = spacy.load("en_core_web_sm") 
nlp.add_pipe('spacytextblob')

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
