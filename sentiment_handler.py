##this utility script contains functions relating to sentiment tagging

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load("en_core_web_sm") #!!! WILL PROBABLY WANT TO DO THIS ONLY ONCE IN ONE FILE
nlp.add_pipe('spacytextblob')

def get_polarity(poem):
       doc = nlp(poem)
       return doc._.blob.sentiment.polarity

def get_subjectivity(poem):
        doc = nlp(poem)
        return doc._.blob.sentiment.subjectivity

# print(sentiment)
# if sentiment.polarity == 0:
#     print("Sentence is neutral")
# elif sentiment.polarity < 0:
#         print("Sentiment is negative")
# else:
#         print("Sentiment is positive")
