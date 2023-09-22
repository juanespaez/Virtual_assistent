import nltk
from nltk.stem.porter import PorterStemmer
import json

nltk.download("punkt")
stemmer = PorterStemmer()


class NLP:

    def __init__(self, sentece, word):
        self.sentence = sentece
        self.word = word
        
    def tokenize(self):
        return nltk.word_tokenize(self.sentence)

    def stem(self):
        return stemmer.stem(self.word.lower())

    def bag_of_words(self, tokenize_sentence, all_words):
        pass  # aqui iran los modelos de compresion de vocabulario

