import sqlite3
from data.paths import DATABASE_DIR

con = sqlite3.connect(DATABASE_DIR / "mandarin.db")
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")

# WORDS TABLE
cur.execute("""CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY,
    hanzi TEXT,
    pinyin TEXT,
    word TEXT NOT NULL UNIQUE,
    lemma TEXT NOT NULL,
    frequency_score INTEGER DEFAULT 0,
    specificity_score INTEGER DEFAULT 0,
    total_count INTEGER DEFAULT 0
)""")

# SENTENCES TABLE
cur.execute("""CREATE TABLE IF NOT EXISTS sentences (
    id INTEGER PRIMARY KEY,
    hanzi TEXT,
    pinyin TEXT,
    sentence TEXT NOT NULL,
    token_count INTEGER DEFAULT 0
)""")

# WORDS_SENTENCES_LINKS TABLE
cur.execute("""CREATE TABLE IF NOT EXISTS words_sentences_links (
    word_id INTEGER NOT NULL,
    sentence_id INTEGER NOT NULL,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (sentence_id) REFERENCES sentences(id),
    PRIMARY KEY (word_id, sentence_id)
)""")

# TABLE VIEWS
# table view for id, word and scores only
cur.execute("""CREATE VIEW IF NOT EXISTS essentials AS
            SELECT id, word FROM words""")

con.commit()


# INSERT FUNCTIONS
class InsertFunction:
    def __init__(
        self,
        word=None,
        lemma=None,
        sentence=None,
        token_count=None,
        word_id=None,
        sentence_id=None,
        hanzi=None,
        pinyin=None,
    ):
        self.word = word
        self.lemma = lemma
        self.sentence = sentence
        self.token_count = token_count
        self.word_id = word_id
        self.sentence_id = sentence_id
        self.hanzi = hanzi
        self.pinyin = pinyin
        
    def inserts(self):
        return
        
    def insert_word(self):
        cur.execute(
            "INSERT INTO words (word, lemma, total_count) VALUES (?, ?, 1) ON CONFLICT(word) DO UPDATE SET total_count = total_count + 1 RETURNING id",
            (self.word, self.lemma),
        )

        # return the word id
        return cur.fetchone()[0]

    def insert_sentence(self):
        print(type(self.sentence))
        cur.execute(
            "INSERT INTO sentences (sentence, token_count) VALUES (?, ?)",
            (self.sentence, self.token_count),
        )

        # return the inserted sentence
        return cur.lastrowid
    
    def word_sentence_link(self):
        cur.execute(
            "INSERT OR IGNORE INTO words_sentences_links (word_id, sentence_id) VALUES (?, ?)",
            (self.word_id, self.sentence_id),
        )

        con.commit()
        return 0
    
    def insert_word_hanzi(self):
        cur.execute(
            "UPDATE words SET hanzi = ? WHERE word = ?", (self.hanzi, self.word)
        )  # TODO: fishy

        con.commit()
        return 0

    def insert_sentence_hanzi(self):
        cur.execute(
            "UPDATE sentences SET hanzi = ? WHERE sentence = ?", (self.hanzi, self.sentence)
        )  # TODO: fishy

        con.commit()
        return 0

    def insert_word_pinyin(self):
        cur.execute("UPDATE words SET pinyin = ? WHERE word = ?", (self.pinyin, self.word))

        con.commit()
        return 0

    def insert_sentence_pinyin(self):
        cur.execute(
            "UPDATE sentences SET pinyin = ? WHERE sentence = ?", (self.pinyin, self.sentence)
        )

        con.commit()
        return 0

# Scoring functions
# TODO: there has to be a way to fetch the specficic score from one function
class FetchFromDB:
    def __init__(self, id):
        self.id = id

    def frequency_score(self):
        cur.execute("SELECT frequency_score FROM words WHERE id = ?", (self.id,))

        return cur.fetchone()[0]

    def specificity_score(self):
        cur.execute("SELECT specificity_score FROM words WHERE id = ?", (self.id,))

        return cur.fetchone()[0]

    def word(self):
        cur.execute("SELECT word FROM words WHERE id = ?", (self.id,))

        return cur.fetchone()[0]

    def sentence(self):
        cur.execute("SELECT sentence FROM sentences WHERE id = ?", (self.id,))

        return cur.fetchone()[0]


def push_statistical_score(
    word_id, frequency_score, specificity_score
):  # TODO: add specificity too
    cur.execute(
        "UPDATE words SET frequency_score = ?, specificity_score = ? WHERE id = ?",
        (frequency_score, specificity_score, word_id),
    )

    return 0


# TODO: fix, make it faster
def save_and_fetch(record):
    # insert the sentence and get its id
    sentence_id = InsertFunction(
        sentence=record["sentence"], token_count=record["token_count"]
    ).insert_sentence()
    sentence_insert = dict(
        cur.execute("SELECT id, sentence FROM sentences WHERE id = ?", (sentence_id,)).fetchone()
    )

    # token label
    tokens = record["tokens"]
    # recent inserts list
    recent_inserts = []

    for token in tokens:
        # get word id with word and lemma with insert_word function
        word_id = InsertFunction(word=token["text"], lemma=token["lemma"]).insert_word()

        # link the word and sentence
        InsertFunction(word_id, sentence_id).word_sentence_link()
        # select the current token's word and id
        current_token = dict(
            cur.execute("SELECT * FROM words WHERE id = ?", (word_id,)).fetchone()
        ) | dict(
            cur.execute("SELECT token_count FROM sentences WHERE id = ?", (sentence_id,)).fetchone()
        )

        # insert current token into recent inserts list
        recent_inserts.append(dict(current_token))

    counted_inserts = {}

    for item in recent_inserts:
        word_id = item["id"]

        if word_id not in counted_inserts:
            counted_inserts[word_id] = item.copy()
            counted_inserts[word_id]["session_count"] = 1

        else:
            counted_inserts[word_id]["session_count"] += 1

    word_inserts = list(counted_inserts.values())

    con.commit()

    return sentence_insert, word_inserts  # returns a list of dictionaries
