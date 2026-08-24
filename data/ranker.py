from db import fetch_words

def filter_top_words():
    get_top_words = fetch_words()
    
    filtered_ranked_words = []
    for index, word in enumerate(get_top_words):
        filtered_ranked_words.append({"rank": index + 1, "word": word[1]})

    return filtered_ranked_words
