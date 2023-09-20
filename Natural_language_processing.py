import nltk
from nltk.stem.porter import PorterStemmer
import json

nltk.download("punkt")
stemmer = PorterStemmer()

def tokenize(setence):
    return nltk.word_tokenize(setence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(tokenize_sentence, all_words):
    pass# aqui iran los modelos de compresion de vocabulario
