from data.db import fetch_words
import math

# frequency function for stat scoring, parameters of unpacked words table
def freq_score(id, word, frequency_score, count):
    token_frequency_score = math.log10(count + 1)  # calculate frequency score

    
    
# main function for stat scoring, parameters of packed words table
def stat_scoring(table):
    for row in table:
        # calculate frequency score
        freq_score(*row)  