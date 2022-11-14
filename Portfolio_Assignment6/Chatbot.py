import numpy as np
import random
import string
import warnings
import datetime as dt
import os
import random
import string # to process standard python strings
import nltk
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer

#warnings got annoying
import warnings
warnings.filterwarnings('ignore')



class User:
  def __init__(self, n): 
    self.name = n.lower()
    self.likes = []
    self.dislikes = []
    self.neutral = []
    self.lastContact = dt.datetime.now()

  def getName(self):
      return self.name

  def getLikes(self): # returns a random like, else none
    if len(self.likes) > 0:
      return random.choice(self.likes)
    else:
      return None

  def getDislikes(self): # returns a random dislike, else none
    if len(self.dislikes) > 0:
      return random.choice(self.dislikes)
    else:
      return None

  def getNeutral(self): # returns a random neutral, else none
    if len(self.neutral) > 0:
      return random.choice(self.neutral)
    else:
      return None

  def addPreference(self, sent): # Uses sentiment analysis to add a sentence to a user's like/dislike/or neutral
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(sent)
    if score['pos'] >= score['neu'] and score['pos'] >= score['neg']:
      self.likes.append(sent)
    elif score['neg'] >= score['neu'] and score['neg'] >= score['pos']:
      self.dislikes.append(sent)
    else:
      self.neutral.append(sent)

  def getDaysFromLastContact(self):
    return (dt.datetime.now() - self.lastContact).days

  def updateLastContact(self):
    self.lastContact = dt.datetime.now()

  def toString(self):
    print("User : " + self.name)
    print("\tLikes: " + str(self.likes))
    print("\tDislikes: " + str(self.dislikes))
    print("\tNeutrals: " + str(self.neutral))
    print("\tDays Since Last Chatted: ", self.getDaysFromLastContact())


users = {}
currentUser = ""
cwd = os.getcwd().replace("\\","/")

#manage Users
def createNewUser(name):
  global currentUser
  users[name] = User(name)
  currentUser = name

def addSentenceToUserPref(name, sent):
  users[name].addPreference(sent)

def closeUserSession(name):
  users[name].updateLastContact()
  saveUsers(users)

# Load or Create users dict
def loadUsers():
  # if users exist, load users. Otherwise create users (first use)
  userLoc = find("users.p", cwd) 
  if(find("users.p", cwd) == None):
    userLoc = cwd + "/users.p"

  if os.path.isfile(userLoc):
    users = unpickleUsers()
  else:
    users = {}
  return users

# Read in user objects
def unpickleUsers():
  with open(find("users.p", cwd), 'rb') as pf:
    print("STATUS: Loaded users.p")
    return pickle.load(pf)

# Save user objects
def saveUsers(users):
  userLoc = find("users.p", cwd)
  if(userLoc == None):
    userLoc = cwd + "/users.p"

  with open(userLoc, 'wb') as pf:
    print("STATUS: Saved users.p")
    pickle.dump(users, pf)

#find a file given the name and the starting point
def find(name, path):
  for root, dirs, files in os.walk(path):
    if name in files:
      return os.path.join(root, name)

#getting knowledge base chatbot.txt, must be in current working directory as chatbot.py
knowledgeBaseFile = find("chatbot.txt", cwd)
with open(knowledgeBaseFile,'r', encoding='utf8', errors ='ignore') as f:
  raw = f.read().lower()

#make da tokens
sentenceTokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

#clean it up
lemmer = WordNetLemmatizer()

def LemTokens(tokens):
  return [lemmer.lemmatize(token) for token in tokens]
removeDictPunctuation = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
  return LemTokens(nltk.word_tokenize(text.lower().translate(removeDictPunctuation)))

#detect greeting and respond
possibleGreetings = ("hello", "hi", "greetings", "sup", "what's up","hey",)
reponses = ["hi", "hey", "*nods*", "hi there", "hello", "Hello, thanks for talking with me"]

def greeting(sentence):
  for word in sentence.split():
    if word.lower() in possibleGreetings:
      return random.choice(reponses)

def tailoredOpener():
  global currentUser
  sentiment = random.choice(["pos", "neg", "neu"])
  if(sentiment == "pos" and users[currentUser].getLikes() != None):
      print("Bottington: I remember last time you expressed excitement when you said ", users[currentUser].getLikes())
  elif(sentiment == "neg" and users[currentUser].getDislikes() != None):
      print("Bottington: I remember last time you expressed disappointment when you said ", users[currentUser].getDislikes())
  else:
    if(users[currentUser].getNeutral() != None):
      print("Bottington: I remember last time you made a good point when you said ", users[currentUser].getNeutral())
  

#Create a response based on user input
def response(userInput):
  global currentUser
  botResponse = ''
  sentenceTokens.append(userInput)
  addSentenceToUserPref(currentUser, userInput)

  Vectorization = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
  sentenceData = Vectorization.fit_transform(sentenceTokens)

  vals = cosine_similarity(sentenceData[-1], sentenceData)
  idx = vals.argsort()[0][-2]
  flat = vals.flatten()
  flat.sort()
  sentenceData = flat[-2]

  if(sentenceData==0):
    botResponse = botResponse + "I am sorry! I don't understand you"
    return botResponse
  else:
    botResponse = botResponse + sentenceTokens[idx]
    return botResponse

#initialization
users = loadUsers()
skipped = False

def userExists(input):
  global currentUser
  for n in users.keys():
    if(n in input):
      currentUser = users[n].getName()
      return True
  return False

print("If you wish to exit, type bye")
print("Bottington: My name is Bottington. I will answer your queries about Microservices. Whats your name?")
userInput = input()
userInput = userInput.lower()
if(userInput != 'bye'):
  if (userExists(userInput)):
    print("Bottington: Nice to chat with you again " + currentUser)
  else:
    print("Bottington: Oh I haven't met you before do you mind saying just your name again? Nothing else just your name.")
    userInput = input()
    userInput = userInput.lower()
    createNewUser(userInput)
    print("Bottington: Nice to meet you " + currentUser)
else:
    print("Bottington: Cya!")  
    skipped = True


if(not skipped):
  #main loop
  Chatting=True
  while(Chatting):
    userInput = input()
    userInput = userInput.lower()
    if(userInput != 'bye'):
      if(userInput == 'thanks' or userInput == 'thank you' ):
        Chatting = False
        print("Bottington: No Problem!")
      else:
        if(greeting(userInput) != None):
          print("Bottington: " + greeting(userInput))
          tailoredOpener()
        else:
          print("Bottington: ", end = "")
          print(response(userInput))
          sentenceTokens.remove(userInput)
    else:
      Chatting = False
      print("Bottington: Cya!")  

  closeUserSession(currentUser)

userInput = input()
if(userInput == "print users"):
  for u in users.keys():
    users[u].toString()