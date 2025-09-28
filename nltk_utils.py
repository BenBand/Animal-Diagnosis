import nltk

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
    pass

