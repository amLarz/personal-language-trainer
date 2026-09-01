from nltk.corpus import wordnet as wn
from nltk.wsd import lesk

sent = ["I", "joined", "a", "hackathon", "to", "continue", "my", "coding", "career"]
print(lesk(sent, "coding", "n"))

print(wn.synsets("coding"))
