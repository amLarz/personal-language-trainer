import math


# frequency function for stat scoring, parameters of unpacked words table
def freq_score(id, word, lemma, count):
    token_frequency_score = math.log10(count + 1)  # Use log to scale the frequency score
    
    return token_frequency_score


# main function for stat scoring, parameters of packed words table
def stat_scoring(table):
    for row in table:
        # calculate frequency score
        frequency_score = freq_score(*row, table.get(row))
