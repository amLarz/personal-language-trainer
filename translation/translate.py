from translation.google_translate import translate
from data.db import InsertFunction, FetchFromDB
from pypinyin import pinyin as pinyin, Style

PY_PINYIN_DEFAULT_STYLE = Style.TONE  # TODO: HARDCODED CHANGE IN FUTURE
PY_PINYIN_DEFAULT_HETERONYM = False  # TODO: HARDCODED CHANGE IN FUTURE

#TODO: fix pinyin function
def translate_record(sentence, words):
    translation = translate(sentence["sentence"])
    InsertFunction(sentence["sentence"], sentence["token_count"]).insert_sentence_translation()

    for word in words:
        translation = translate(word["word"])
        InsertFunction(word["word"], translation).insert_word_translation()
        pinyin = pinyin(
            translation, style=PY_PINYIN_DEFAULT_STYLE, heteronym=PY_PINYIN_DEFAULT_HETERONYM
        )
        print(pinyin)  # DELETE THIS

    print(f"sentence translation inserted: {translate(sentence['sentence'])}")  # DELETE THIS
    print(f"Translated words: {[translate(word['word']) for word in words]}")  # DELETE THIS
