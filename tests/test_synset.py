from nltk.corpus import wordnet as wn
from nltk.wsd import lesk

sent = ["He", "began", "to", "bank", "the", "plane"]

print(lesk(sent, "bank", "n").definition())