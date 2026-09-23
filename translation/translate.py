from translation.google_translate import translate
from data.db import InsertFunction, FetchFromDB
from pypinyin import pinyin as get_pinyin, lazy_pinyin, Style

PY_PINYIN_DEFAULT_STYLE = Style.TONE  # TODO: HARDCODE


# TODO: fix pinyin function
def translate_record(sentence, words):
    hanzi_translation = translate(sentence["sentence"])
    InsertFunction(sentence=sentence["sentence"], hanzi=hanzi_translation).insert_sentence_hanzi()

    get_sentence_pinyin = " ".join(
        lazy_pinyin(
            hanzi_translation,
            style=PY_PINYIN_DEFAULT_STYLE,
        )
    )

    print(get_sentence_pinyin)  # DELETE THIS
    InsertFunction(
        sentence=sentence["sentence"], pinyin=get_sentence_pinyin
    ).insert_sentence_pinyin()

    for word in words:
        hanzi_translation = translate(word["word"])
        InsertFunction(word=word["word"], hanzi=hanzi_translation).insert_word_hanzi()

        get_word_pinyin = " ".join(
            lazy_pinyin(
                hanzi_translation,
                style=PY_PINYIN_DEFAULT_STYLE,
            )
        )
        InsertFunction(word=word["word"], pinyin=get_word_pinyin).insert_word_pinyin()
        print(get_word_pinyin)  # DELETE THIS

    print(f"sentence translation inserted: {translate(sentence['sentence'])}")  # DELETE THIS
    print(f"Translated words: {[translate(word['word']) for word in words]}")  # DELETE THIS
