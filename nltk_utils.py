import nltk
import numpy as np
# Downloading tokenizer
#nltk.download('punkt')
#nltk.download('punkt_tab') IF PUNKT DOESN'T WORK USE PUNKT_TAB

# Importing the stemer from nltk
from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

# Tokenization function
def tokenize(sentence):
    return nltk.word_tokenize(sentence)


# Stem function
def stem(word):
    return stemmer.stem(word.lower())




def bag_of_words(tokenized_sentence, all_words):

    tokenized_sentence = [stem(w) for w in tokenized_sentence]

    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0

    return bag

# Bag of words example
""" sentence = ['hello', 'how', 'are', 'you']
words = ['hi', 'hello', 'I', 'you', 'bye', 'thanks', 'cool']
bag = bag_of_words(sentence, words)
print(bag) """