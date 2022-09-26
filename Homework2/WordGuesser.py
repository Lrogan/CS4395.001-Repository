import sys
import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from random import seed
from random import randint

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
  #parse data into easier to use variables
  nounsNoTags = [n[0] for n in data[1]]
  uniqueNouns = set(nounsNoTags)
  allTokens = data[0]

  #create dict
  pos_dict = {}
  for n in uniqueNouns:
    pos_dict[n] = allTokens.count(n)

  #print the top 50 in dict with correct format
  for pos in sorted(pos_dict, key=pos_dict.get, reverse=True)[:50]:
    print(pos, ':', pos_dict[pos])

  #Uses list comprehension to create a list of the dict in order from most common to least then truncate to first 50
  return [pos for pos in sorted(pos_dict, key=pos_dict.get, reverse=True)][:50]

def playRound(answer, currentGuess):
  print(*currentGuess)
  letterGuess = input("Guess a letter:")

  if letterGuess in answer:
    # add the letter guess to current guess
    count = 0
    for c in answer:
      if c == letterGuess:
        currentGuess[count] = c
      count += 1

    print("Correct!")
    return 1
  elif letterGuess == "!":
    print("Goodbye, Hope you play again soon!")
    return -400
  else:
    print("Sorry, guess again.")
    return -1

def wordGuesser(words):
  #init all the vars to play the game
  score = 5
  seed(50123)
  
    #fix answer format to list
  answerSelected = words[randint(0, len(words)-1)]
  answer = [c for c in answerSelected]
  currentGuess = ["_" for c in answer]

  #start the game
  print("Let's Play A Guessing Game!")

  #play rounds while the score is positive and the answer has not been guessed
  while score >= 0 and not currentGuess == answer:
    score += playRound(answer, currentGuess)
    print("Current Score: ", score)

  if score < 0:
    print("Game Over, better luck next time!")
  else:
    print("You solved it!")
  

if __name__ == '__main__':
  if len(sys.argv) < 2:
      sys.exit("Exiting Pogram: Please enter a file name as a system arg.")
  else:
      file = sys.argv[1]
      data = inputData(file)

  words = dictMaker(data)
  wordGuesser(words)