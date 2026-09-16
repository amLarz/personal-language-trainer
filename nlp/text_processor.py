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

    # fix contractions
    CONTRACTIONS = {
        "n't",
        "'s",
        "'re",
        "'ve",
        "'ll",
        "'d",
        "'m",
    }

    # filter out expletives
    filtered_tokens = []
    for token in text:
        if token.dep_ not in ORPHAN_DEPS and token.pos_ not in FILTERED_POS:
            word = (
                token.lemma_ if token.text in CONTRACTIONS else token.text
            )  # Turn to lemma if a contraction.

            filtered_tokens.append((token, word))

    return filtered_tokens


def classify_words(token, word):

    return {
        "text": word.lower() if token.pos_ != "PROPN" else word,
        "lemma": token.lemma_,
        "pos": token.pos_,
        "dep": token.dep_,
        "tag": token.tag_,
        "is_stop": token.is_stop,
    }


def process_text(text):

    # process the text using spaCy
    doc = nlp(text)
    sents = list(doc.sents)
    results = []
    # goes through each sentence
    for sent in sents:
        # filter the text to remove unwanted tokens
        filtered_text = filter_text(sent)

        # loops over filtered tokens and classifies them
        results.append(
            {
                "sentence": sent.text,
                "token_count": len(sent),
                "tokens": [classify_words(*token) for token in filtered_text],
            }
        )

    return results
