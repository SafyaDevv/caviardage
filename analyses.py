import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

#function to get word frequency for all text
#stopword parameters, bool to decide whether stop words are wanted or not
#default is false
def word_frequency(poem, keep_stopwords = False):
    doc = nlp(poem)

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
