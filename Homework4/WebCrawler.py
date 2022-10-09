from genericpath import isfile
import re
import requests
import urllib.request
from urllib.request import Request
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk import sent_tokenize
from nltk import word_tokenize
from pathlib import Path
import string
import os

#write urls to a file
def urlScraper(soup):
  counter = 0

  with open('Homework4/urls.txt', 'w') as f:
    for link in soup.find_all('a'):
      link_str = str(link.get('href'))
      print(link_str)
      if 'Microservices' in link_str or 'microservices' in link_str:
              if counter > 50:
                break
              if link_str.startswith('/url?q='):
                link_str = link_str[7:]
                print('MOD:', link_str)
              if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
              if link_str.startswith('http') and 'google' not in link_str:
                f.write(link_str + '\n')
                counter += 1
    f.close()

  print("URL's Scraped")

#determinse if an html element is visible
def visible(element):
  if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
      return False
  elif re.match('<!--.*-->', str(element.encode('utf-8'))):
      return False
  return True

#grab all the text of a given url then write it to a file with the format site[#]text.txt where # is the 0 based index of that files url in the urls.txt file
def textScraper(url, count):
  print(url)
  req = Request(
    url=url,
    headers={'User-Agent': 'Mozilla/5.0'}
  )
  html = urllib.request.urlopen(req).read()
  soup = BeautifulSoup(html, features = "lxml")
  data = soup.findAll(text=True)
  result = filter(visible, data)
  temp_list = list(result)      # list from filter
  temp_str = ' '.join(temp_list)
  #process string
  temp_str.strip('\n')
  temp_str.strip('\t')
  # print(temp_str)
  with open('Homework4/SiteTexts/site[' + str(count) + ']Text.txt', 'w', encoding="utf-8") as f:
    f.write(temp_str)
    f.close()

#root of all web crawling
def web_crawler(url):
  r = requests.get(url)

  data = r.text
  soup = BeautifulSoup(data, features = "lxml")

  #only run url scrapper if the urls txt does not exist
  path = Path('Homework4/urls.txt')
  if not path.exists():
    urlScraper(soup)
  
  with open('Homework4/urls.txt') as f:
    urls = f.readlines()
    f.close()
  
  count = 0
  
  for url in urls:
    textScraper(url, count)
    count += 1

#grabs the local file representing the site text
def getSiteText(filename):
  if filename.is_file():
    with open(filename.path, encoding="utf-8") as f:
      siteText = f.read()
      f.close()
    return siteText
  return ""

#does more text preprocessing and then sent_tokenizes the files and joins them back to put into a file
def sentancer():
  directory = 'Homework4/SiteTexts'

  count = 0

  for filename in os.scandir(directory):
    siteText = getSiteText(filename)
    with open('Homework4/SiteSents/site[' + str(count) + ']Sent.txt', 'w', encoding="utf-8") as f:
      noNewLine = siteText.replace('\n', " ")
      noTabs = noNewLine.replace('\t', " ")
      sentances = sent_tokenize(noTabs)
      f.write(" ".join(sentances))
      f.close()
    count += 1

def importantWords():
  sentancer()
  
  directory = 'Homework4/SiteSents'
  pos_dict = {}

  for filename in os.scandir(directory):
    print(filename.path)
    #remove punctuation from the site text
    siteText = getSiteText(filename).translate(str.maketrans('','', string.punctuation))
    
    #tokenize and process
    wordTokens = word_tokenize(siteText)
    #lowercase the tokens, and remove non alpha and english stopwords
    lowerWordTokens = [t.lower() for t in wordTokens]
    processedTokens = [t for t in lowerWordTokens if t.isalpha() and t not in stopwords.words('english') and len(t) > 6]

    #calculate term frequency
    for n in processedTokens:
      pos_dict[n] = processedTokens.count(n)
    
  for pos in sorted(pos_dict, key=pos_dict.get, reverse=True)[:40]:
    print(pos, ':', pos_dict[pos])

def buildKnowledgeBase():
  with open('Homework4/ManuallyImportantWords.txt') as f:
    words = f.readlines()

  for filename in os.scandir('Homework4/SiteSents'):
    siteText = getSiteText(filename)
      

if __name__ == '__main__':
  starter_url = "https://en.wikipedia.org/wiki/Microservices"
  # web_crawler(starter_url)
  importantWords()
  buildKnowledgeBase()
  