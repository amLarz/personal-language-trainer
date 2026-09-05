import math
from data.db import fetch_frequency_score, push_statistical_score


# frequency function for stat scoring, parameters of unpacked words table
def freq_score(word_id, count):
    current_db_score = fetch_frequency_score(word_id)

    token_frequency_score = math.log10(count + 1)  # Use log to scale the frequency score
    print("OLD:", token_frequency_score)  # DELETE THIS

    if current_db_score is None:
        return token_frequency_score

    new_frequency_score = (0.5 * token_frequency_score) + ((1 - 0.8) * current_db_score)
    print("NEW", new_frequency_score)  # DELETE THIS

    return new_frequency_score

def spec_score(word_id, count):
    pass

# main function for stat scoring, parameters of packed words table
def stat_scoring(table):
    for row in table:
        # TODO: lowk fix this because it looks messy ash
        word_id, word, lemma, frequency_score, specificity_score, count = row  # Unpack the row

        # calculate frequency score
        frequency_score = freq_score(word_id, count)

        # calculate specificity score
        specificity_score = spec_score(word_id, count)
        
        push_statistical_score(word_id, frequency_score)

    return 0
