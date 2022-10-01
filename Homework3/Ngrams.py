import sys
import nltk
from nltk import word_tokenize
from nltk.util import ngrams

def inputData(file):

  print("Processing data file: ", file)
  with open(file) as f:
    raw_text = f.readlines()
    f.close()

  raw_string = " ".join(raw_text)
  unigrams = word_tokenize(raw_string)
  bigrams = list(ngrams(unigrams,2))

  unigram_dict = {t:unigrams.count(t) for t in set(unigrams)}
  bigram_dict = {b:bigrams.count(b) for b in set(bigrams)}

if __name__ == '__main__':
  # for x in range(3):
  #   file = input("Please Input a File Name: ")
  #   data = inputData(file)

  file = "Homework3/" + input("Please Input a File Name: ")
  data = inputData(file)
