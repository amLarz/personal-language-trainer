import csv

import spacy

# load the English NLP model
nlp = spacy.load("en_core_web_sm")

def filter_token(text):
    
    ORPHAN_DEPS = {
        "punct",
        "det",
        "expl",
        "int"
    }
    
    FILTERED_POS = {
        "PUNCT",
        "X",
        "SPACE"
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

    for sent in sents:
        classification = {"content": []}
        for token in sent:
            classified_token = process_token(token)
            if classified_token:
                classification["content"].append(token.lemma_)
        results.append({"text": sent.text, "classification": classification})

    return results
