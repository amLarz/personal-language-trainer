import csv

import spacy

# load the English NLP model
nlp = spacy.load("en_core_web_sm")

def filter_text(text):
    
    # orphan dependencies that are not useful for content classification
    ORPHAN_DEPS = {
        "punct",
        "det",
        "expl",
        "intj",
        "discourse"
    }
    
    # filtered parts of speech that are not useful for content classification
    FILTERED_POS = {
        "PUNCT",
        "X",
        "SPACE",
        "DET"
    }
    
    # filter out expletives
    filtered_tokens = [token for token in text 
                       if token.dep_ not in ORPHAN_DEPS
                       and token.pos_ not in FILTERED_POS
                       ]
    
    return filtered_tokens
    
    

def classify_words(token):

    tier1_content = (token.pos_ in ["NOUN", "VERB", "ADJ", "ADV", "PROPN", "NUM"]) or (
        token.dep_ in ["ROOT", "xcomp", "ccomp", "csubj"] and token.pos_ != "AUX"
    )

    if tier1_content:
        return True

    return None

def process_token(token):
    # filtering 
    
    

    return None


def process_text(text):
    
    # process the text using spaCy
    doc = nlp(text)
    sents = list(doc.sents)
    results = []
    
    # goes through each sentence
    for sent in sents:
        # filter the text to remove unwanted tokens
        filtered_text = filter_text(doc)
        
        classification = {"content": []}
        
        # loops over filtered tokens and classifies them
        for token in filtered_text:
            classified_token = process_token(token)
            if classified_token:
                classification["content"].append(token.lemma_)
        results.append({"text": sent.text, "classification": classification})

    return results
