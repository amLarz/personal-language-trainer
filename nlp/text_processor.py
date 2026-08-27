import csv

import spacy

# load the English NLP model
nlp = spacy.load("en_core_web_sm")

# recursive function to filter out stop words and return the lemmas of the remaining words
def is_stop_filter(token):
    # if the token is a stop word, move on.
    if token.is_stop:
        return True

    return False


def is_orphaned_filter(token):

    # orphan dependencies that are not useful for our purposes
    ORPHAN_DEPS = {
        "punct",
        "det",
        "expl",
        "discourse",
        "intj",
    }

    dep = token.dep_

    # if there are any orphan dependencies, move on.
    if dep in ORPHAN_DEPS:
        return True

    return False


def classify_words(token):

    tier1_content = (token.pos_ in ["NOUN", "VERB", "ADJ", "ADV", "PROPN", "NUM"]) or (
        token.dep_ in ["ROOT", "xcomp", "ccomp", "csubj"] and token.pos_ != "AUX"
    )

    if tier1_content:
        return True

    return None


def process_token(token):
    # layer 1: filter out stop words
    

    if is_stop == True:
        is_orphaned = True
    else:
        # layer 2: filter out orphan dependencies
        is_orphaned = is_orphaned_filter(token)

    if not is_stop and not is_orphaned:
        # layer 3: classify words
        return classify_words(token)

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
