from data.db import fetch_words


def frequency():
    words = fetch_words()
    print(words)
    
    
frequency()