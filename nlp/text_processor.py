import csv

import spacy

# load the English NLP model
nlp = spacy.load("en_core_web_sm")


def filter_text(text):

    # orphan dependencies that are not useful for content classification
    ORPHAN_DEPS = {"punct", "expl", "intj", "discourse"}

    # filtered parts of speech that are not useful for content classification
    FILTERED_POS = {
        "PUNCT",
        "X",
        "SPACE",
    }

    # filter out expletives
    filtered_tokens = [
        token for token in text if token.dep_ not in ORPHAN_DEPS and token.pos_ not in FILTERED_POS
    ]

    return filtered_tokens


def classify_words(token):

    return {
        "text": token.text,
        "lemma": token.lemma_,
        "pos": token.pos_,
        "dep": token.dep_,
        "is_stop": token.is_stop,
    }


def process_text(text):

    # process the text using spaCy
    doc = nlp(text)
    sents = list(doc.sents)
    results = []
    sentences = []

    # goes through each sentence
    for sent in sents:
        # filter the text to remove unwanted tokens
        filtered_text = filter_text(doc)
        sentences.append(sent.text)

        # TODO: WORK ON THIS LOL
        # loops over filtered tokens and classifies them
        for token in filtered_text:
            classified_token = classify_words(token)
            results.append(classified_token)

    return results
