import math
import wordfreq
from data.db import FetchFromDB, push_statistical_score


# frequency function for stat scoring, parameters of unpacked words table
def freq_score(word_id, count):
    frequency_score = math.log10(count + 1)  # Use log to scale the frequency score

    print("NEW", frequency_score)  # DELETE THIS

    return frequency_score


def spec_score(word_id, count, token_count):  # TODO: fix the math for averaging or smoothing
    reference_zipf = wordfreq.zipf_frequency(FetchFromDB(word_id).word(), "en")
    word_zipf = math.log10((count / token_count) * 1e9)

    specificity_score = word_zipf - reference_zipf

    print("SPECIFICITY SCORE:", specificity_score)  # DELETE THIS

    return specificity_score


# main function for stat scoring, parameters of packed words table
def stat_scoring(table):

    for row in table:
        word_id = row["id"]
        session_count = row["session_count"]
        count = row["total_count"]
        token_count = row["token_count"]

        # calculate frequency score
        frequency_score = freq_score(word_id, count)

        # calculate specificity score
        specificity_score = spec_score(word_id, session_count, token_count)

        push_statistical_score(word_id, frequency_score, specificity_score)
    return 0
