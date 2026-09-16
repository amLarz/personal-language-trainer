from translation.google_translate import translate
from data.db import insert_sentence_translation, insert_word_translation, FetchFromDB
# TODO ^^^ TURN TO CLASS

def translate_record(sentence, words):
    
    if FetchFromDB(sentence["id"]).sentence() == sentence["sentence"]:
        pass
    else:
        translated_sentence = translate(sentence["sentence"])
        insert_sentence_translation(sentence["sentence"], translated_sentence)
        print(f"Translated sentence: {translated_sentence}") # DELETE THIS
        
    for word in words:
        if FetchFromDB(word["id"]).word() == word["word"]:
            pass
        else:
            translated_word = translate(word["word"])
            insert_word_translation(word["word"], translated_word)
    
    print(f"Translated words: {[translate(word['word']) for word in words]}") # DELETE THIS
        
    