from translation.google_translate import translate
from data.db import insert_sentence_translation, insert_word_translation
# TODO ^^^ TURN TO CLASS

def translate_record(record):
    
    translated_sentence = translate(record["sentence"])
    
    for token in record["tokens"]:
        translate(token["text"])
        
        
    insert_sentence_translation(record["sentence"], translated_sentence)
    insert_word_translation(record["tokens"], translated_sentence)
    
    print(f"Translated sentence: {translated_sentence}")
    print(f"Translated tokens: {[translate(token['text']) for token in record['tokens']]}")
        
    