import math
import wordfreq
from data.db import fetch_frequency_score, fetch_specificity_score, push_statistical_score, fetch_word


# frequency function for stat scoring, parameters of unpacked words table
def freq_score(word_id, count):
    current_db_score = fetch_frequency_score(word_id)

    token_frequency_score = math.log10(count + 1)  # Use log to scale the frequency score
    print("OLD:", token_frequency_score)  # DELETE THIS

    if current_db_score is None:
        return token_frequency_score

    frequency_score = (0.5 * token_frequency_score) + (0.2 * current_db_score)
    print("NEW", frequency_score)  # DELETE THIS

    return frequency_score

def spec_score(word_id, count, token_count): # TODO: fix the math for averaging or smoothing
    
    current_db_score = fetch_specificity_score(word_id)
    reference_zipf = wordfreq.zipf_frequency(fetch_word(word_id), 'en')
    word_zipf = math.log10((count / token_count) * 1e9)
    
    specificity_score = word_zipf - reference_zipf
    
    if current_db_score is None:
        return specificity_score
    
    specificity_score = (0.5 * specificity_score) + (0.2 * current_db_score)
    
    print("SPECIFICITY SCORE:", specificity_score)  # DELETE THIS
    
    return specificity_score

# main function for stat scoring, parameters of packed words table
def stat_scoring(table):
    token_count = table[0]["token_count"] # TODO: fix this because this does not look good
    
    for row in table[1:]: # TODO: REMOVE THE SLICE OMD FIX THIS
        
        word_id = row["id"]
        count = row["_count"]
        
        # calculate frequency score
        frequency_score = freq_score(word_id, count)

        # calculate specificity score
        specificity_score = spec_score(word_id, count, token_count)
        
        push_statistical_score(word_id, frequency_score, specificity_score)
    return 0
