import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pickle

def inputData(file):
  print("Processing data file.")
  with open(file) as f:
    raw_text = f.readlines()
    f.close()

  raw_string = " ".join(raw_text)

  #go through the raw_text list and create word tokens from each entry
  wordTokens = word_tokenize(raw_string)

  #lower the tokens, then only take tokens that are alpha, not stopwords, and 6 characters or more
  lowerWordTokens = [t.lower() for t in wordTokens]
  processedTokens = [t for t in lowerWordTokens if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]

  #lemmatize the tokens
  wnl = WordNetLemmatizer()
  lemmas = [wnl.lemmatize(t) for t in processedTokens]

  #make unique
  lemmas_unique = list(set(lemmas))

  #POS tag uniques
  tags = nltk.pos_tag(lemmas_unique)
  print("Unique Lemma POS Tags:")
  print(tags[:20])

  #Only Nouns
  nouns = [t for t in tags if t[1][0] == "N"]

  #Printing
  print("Number of Processed Tokens: ", len(processedTokens))
  print("Number of Nouns: ", len(nouns))

  return processedTokens, nouns

def dictMaker(data):
  print("Print noun words with counts: ")
  nounsNoTags = [n[0] for n in data[1]]
  uniqueNouns = set(nounsNoTags)
  allTokens = data[0]

  pos_dict = {}
  for n in uniqueNouns:
    pos_dict[n] = allTokens.count(n)

  for pos in sorted(pos_dict, key=pos_dict.get, reverse=True):
    print(pos, ':', pos_dict[pos])

  return [pos for pos in sorted(pos_dict, key=pos_dict.get, reverse=True)]

def wordGuesser(words):
  score = 5
  
  

if __name__ == '__main__':
  # if len(sys.argv) < 2:
  #     sys.exit("Exiting Pogram: Please enter a file name as a system arg.")
  # else:
  #     file = sys.argv[1]
  #     dataInput(file)
  file = 'Homework2/anat19.txt'

  data = inputData(file)
  words = dictMaker(data)
  wordGuesser(words)