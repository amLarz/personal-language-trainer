from data.db import fetch_words


def extract_fetched():
    get_top_words = fetch_words()
    extracted_words = []
    for word in get_top_words:
        extracted_words.append(
            (word[0], word[1])
        )  # 0 contains the id and 1 contains the word itself

    return extracted_words


def filter_top_words(extracted_words):

    filtered_ranked_words = []
    for index, word in enumerate(extracted_words):
        filtered_ranked_words.append({"rank": index + 1, "word": word[1], "id": word[0]})

    return filtered_ranked_words
