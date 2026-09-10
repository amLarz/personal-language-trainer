import sqlite3
from data.paths import DATABASE_DIR
from collections import Counter

con = sqlite3.connect(DATABASE_DIR / "mandarin.db")
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")

# WORDS TABLE
cur.execute("""CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY,
    word TEXT NOT NULL UNIQUE,
    lemma TEXT NOT NULL,
    frequency_score INTEGER DEFAULT 0,
    specificity_score INTEGER DEFAULT 0,
    count INTEGER DEFAULT 0
)""")

# SENTENCES TABLE
cur.execute("""CREATE TABLE IF NOT EXISTS sentences (
    id INTEGER PRIMARY KEY,
    sentence TEXT NOT NULL,
    token_count INTEGER DEFAULT 0
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
def insert_word(word, lemma):
    cur.execute("INSERT OR IGNORE INTO words (word, lemma) VALUES (?, ?)", (word, lemma))

    cur.execute("UPDATE words SET count = count + 1 WHERE word = ?", (word,))

    # return the word id
    return cur.execute("SELECT id FROM words WHERE word = ?", (word,)).fetchone()[0]

def insert_sentence(sentence, token_count):
    cur.execute("INSERT INTO sentences (sentence, token_count) VALUES (?, ?)", (sentence, token_count))

    # return the last sentence id
    return cur.lastrowid


def word_sentence_link(word_id, sentence_id):
    cur.execute(
        "INSERT OR IGNORE INTO words_sentences_links (word_id, sentence_id) VALUES (?, ?)",
        (word_id, sentence_id),
    )

    return 0


# Scoring functions
# TODO: there has to be a way to fetch the specficic score from one function
def fetch_frequency_score(word_id):
    cur.execute("SELECT frequency_score FROM words WHERE id = ?", (word_id,))

    return cur.fetchone()[0]

def fetch_specificity_score(word_id):
    cur.execute("SELECT specificity_score FROM words WHERE id = ?", (word_id,))

    return cur.fetchone()[0]

def fetch_word(id):
    cur.execute("SELECT word FROM words WHERE id = ?", (id,))

    return cur.fetchone()[0]


def push_statistical_score(word_id, frequency_score, specificity_score):  # TODO: add specificity too
    cur.execute("UPDATE words SET frequency_score = ?, specificity_score = ? WHERE id = ?", (frequency_score, specificity_score, word_id))

    return 0

# TODO: fix, make it faster
def save_and_fetch(processed_text):
    for record in processed_text:
        # insert the sentence and get its id
        sentence_id = insert_sentence(record["sentence"], record["token_count"])

        # token label
        tokens = record["tokens"]
        # recent inserts list
        recent_inserts = []

        for token in tokens:
            word_id = insert_word(token["text"], token["lemma"])

            # link the word and sentence
            word_sentence_link(word_id, sentence_id)
            # select the current token's word and id
            current_token = cur.execute("SELECT * FROM words WHERE id = ?", (word_id,)).fetchone()
            # insert current token into recent inserts list
            recent_inserts.append(dict(current_token))

    # TODO: find a way to connect token count to word table return
    counted_inserts = {}

    for item in recent_inserts:
        word_id = item["id"]
        
        if word_id not in counted_inserts:
            counted_inserts[word_id] = item.copy()
            counted_inserts[word_id]["_count"] = 1
            
        else:
            counted_inserts[word_id]["_count"] += 1
    
    final_inserts = list(counted_inserts.values())
    final_inserts.insert(0, {"token_count": record["token_count"]})  # TODO: fix this because this does not look good
    
    print(final_inserts)  # DELETE THIS
    con.commit()

    return final_inserts # returns a list of dictionaries 
