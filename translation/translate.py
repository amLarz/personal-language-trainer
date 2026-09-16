from translation.google_translate import translate
from data.db import insert_sentence_translation, insert_word_translation, FetchFromDB
# TODO ^^^ TURN TO CLASS

def translate_record(sentence, words):
    
    insert_sentence_translation(sentence["sentence"], translate(sentence["sentence"]))
    
    for word in words:
        insert_word_translation(word["word"], translate(word["word"]))
        
    print(f"sentence translation inserted: {translate(sentence['sentence'])}") # DELETE THIS
    print(f"Translated words: {[translate(word['word']) for word in words]}") # DELETE THIS
        
    