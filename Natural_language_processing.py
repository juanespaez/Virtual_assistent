import nltk
from nltk.stem.porter import PorterStemmer
import numpy as np

nltk.download("punkt")
stemmer = PorterStemmer()


class NLP:

    def __init__(self, sentece=" ", word=" "):
        self.sentence = sentece
        self.word = word

    def tokenize(self):
        return nltk.word_tokenize(self.sentence)

    def stem(self):
        return stemmer.stem(self.word.lower())

    def bag_of_words(self, tokenize_sentence, all_words):
        tokenize_sentence = [NLP.stem(w) for w in tokenize_sentence]
        bag = np.zeros(len(all_words), dtype=np.float32)
        for idx, w in enumerate(all_words):
            if w in tokenize_sentence:
                bag[idx] = 1.0
        return bag

