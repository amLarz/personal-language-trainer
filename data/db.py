import sqlite3
from data.paths import DATABASE_DIR
from collections import Counter

con = sqlite3.connect(DATABASE_DIR / "mandarin.db")
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")

# WORDS TABLE
cur.execute("""CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY,
    word TEXT NOT NULL UNIQUE,
    lemma TEXT NOT NULL UNIQUE,
    frequency_score INTEGER DEFAULT 0,
    specificity_score INTEGER DEFAULT 0,
    count INTEGER DEFAULT 0
)""")

# SENTENCES TABLE
cur.execute("""CREATE TABLE IF NOT EXISTS sentences (
    id INTEGER PRIMARY KEY,
    sentence TEXT NOT NULL
)""")

# WORDS_SENTENCES_LINKS TABLE
cur.execute("""CREATE TABLE IF NOT EXISTS words_sentences_links (
    word_id INTEGER NOT NULL,
    sentence_id INTEGER NOT NULL,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (sentence_id) REFERENCES sentences(id)
    PRIMARY KEY (word_id, sentence_id)
)""")

# TABLE VIEWS
# table view for id, word and scores only
cur.execute("""CREATE VIEW IF NOT EXISTS essentials AS
            SELECT id, word FROM words""")

con.commit()


# INSERT FUNCTIONS
def insert_word(word):
    cur.execute("INSERT OR IGNORE INTO words (word) VALUES (?)", (word,))
    cur.execute("UPDATE words SET count = count + 1 WHERE word = ?", (word,))

    # return the word id
    return cur.execute("SELECT id FROM words WHERE word = ?", (word,)).fetchone()[0]


def insert_sentence(sentence):
    cur.execute("INSERT INTO sentences (sentence) VALUES (?)", (sentence,))

    # return the last sentence id
    return cur.lastrowid


def word_sentence_link(word_id, sentence_id):
    cur.execute(
        "INSERT OR IGNORE INTO words_sentences_links (word_id, sentence_id) VALUES (?, ?)",
        (word_id, sentence_id),
    )

    return 0


# TODO: fix, make it faster
def save_and_fetch(processed_text):
    for item in processed_text:
        # insert the sentence and get its id
        sentence_id = insert_sentence(item["sentence"])

        # token label
        tokens = item["tokens"]
        # recent inserts list
        recent_inserts = []

        for token in tokens:
            word_id = insert_word(token["lemma"])

            # link the word and sentence
            word_sentence_link(word_id, sentence_id)
            # select the current token's word and id
            current_token = cur.execute(
                "SELECT id, word FROM words WHERE id = ?", (word_id,)
            )
            # insert current token into recent inserts list
            recent_inserts.append(current_token.fetchone())
            
        recent_inserts = Counter(recent_inserts)

    con.commit()

    return recent_inserts
