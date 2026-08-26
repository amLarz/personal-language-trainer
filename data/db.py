import sqlite3
from data.paths import DATABASE_DIR

con = sqlite3.connect(DATABASE_DIR / "mandarin.db")
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")

# WORDS TABLE
cur.execute("""CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY,
    word TEXT NOT NULL UNIQUE,
    frequency INTEGER NOT NULL DEFAULT 0
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

con.commit()


def insert_word(word):
    cur.execute("INSERT OR IGNORE INTO words (word) VALUES (?)", (word,))

    cur.execute("UPDATE words SET frequency = frequency + 1 WHERE word = ?", (word,))

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


def fetch_words():
    fetch_words = cur.execute("SELECT * FROM words ORDER BY frequency DESC LIMIT 50").fetchall()

    return fetch_words


def save_to_database(results):

    sentences_count = 0
    word_links_count = 0

    for record in results:
        sentence_id = insert_sentence(record["text"])
        sentences_count += 1
        for lemma in record["classification"]["content"]:
            word_id = insert_word(lemma)
            word_sentence_link(word_id, sentence_id)
            word_links_count += 1

    con.commit()

    return {
        "sentences_inserted": sentences_count,
        "word_links_inserted": word_links_count,
    }
