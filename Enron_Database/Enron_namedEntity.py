#import mysql.connector
import sqlite3
#from datetime import datetime
#import tldextract
import re
#from sklearn.externals import joblib
#import cs
#import cStringIO
import sqlite3
import json
import sys
import requests
from bs4 import BeautifulSoup
import json
import urllib2
from HTMLParser import HTMLParser
import sqlite3
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.tag import pos_tag
from nltk.tokenize import *
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.tokenize import *
from nltk.tag import pos_tag
from collections import Counter
from spacy.en import English
import os
import sys
import urllib
import urlparse
#from urllib3 import HTTPError
#from urllib3 import URLError
import json
import time
import wordcloud
# Plotting
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_style('whitegrid')

from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS


def generate_wordcloud(text,type1):


    wc = wordcloud.WordCloud(width=1600,
                             height=800,
                             max_words=200).generate(text)
    plt.figure(figsize=(20, 10))
    plt.imshow(wc)
    plt.axis("off")
    name = type1 + '.png' 
    plt.savefig(name, dpi=1000)
    plt.show()


nlp = spacy.load('en')
parser = English()
temp_org =[]
temp_person = []
temp_place = []
temp_others = []
temp_product = []
proper_nouns =[]
all_nouns =[]
corrected_text ={}
all_words = []

known_entity = ['Viagra']

dir1 ='/Users/Dhanush/Desktop/EnronDataSetAnalysis/Enron_Database/Grammar_clean'
A = time.time()
# load the text into file
temp_list = []
counter = 0
for file in os.listdir(dir1):
    if file.endswith(".txt"):
        file_to_read = dir1 + '/' + file 
        f = open(file_to_read,'r')
        data = str(f.readline())
        temp= data.split('\n')[0]
        if len(temp) < 1:
            continue
        temp = int(temp)
        corrected_text[temp] = {}
        corrected_text[temp]['mail'] = f.read()
        counter+=1
        temp = str(file)
        temp_list.append(int(temp.split('.')[0]))
temp_list.sort()

keys = corrected_text.keys()

# Check based on file name

email_entity_dict = {}

for key in keys:
    email_entity_dict[key] = {}
    email_entity_dict[key]['Names'] = []
    email_entity_dict[key]['Places'] = []
    email_entity_dict[key]['Org'] = []
    email_entity_dict[key]['Entities'] = []
    email_entity_dict[key]['tokens'] = []

# Create a dictionary to store all recognized Entities mapped to each Email.

count = 0

for key in keys:

    count+=1
    print "Processing Email: " +str(count)
    fixed_body=map(unicode,corrected_text[key]['mail'])
    fixed_body = "".join(fixed_body)

    if len(fixed_body) < 5:
        continue

    doc = nlp(fixed_body)
    current_noun = []
    for sentence in nltk.sent_tokenize(fixed_body) :
        parsed = parser(sentence)
        for token in parsed :
            if token.text.isalpha():
                if (token.tag_ == "NNP") or (token.tag_ == "NNPS"):
                    all_nouns.append(token.text)
                    current_noun.append(token.text)
                    email_entity_dict[int(key)]['tokens'].append(token.text)

    for ent in doc.ents:

        if ent.text not in current_noun:
            continue

    	if  (ent.label_ =='ORG'):
            if ent.text.isalpha():
                temp_org.append(ent.text)
                email_entity_dict[int(key)]['Org'].append(ent.text)

    	if  (ent.label_ == 'PERSON'):
            if ent.text.isalpha():
    	       temp_person.append(ent.text)
               email_entity_dict[int(key)]['Names'].append(ent.text)

    	if  (ent.label_ == 'GPE'):
            if ent.text.isalpha():
                temp_place.append(ent.text)
                email_entity_dict[int(key)]['Places'].append(ent.text)



    if count >5000:
        break

B = time.time()

# Create word clouds for body.


print("Names")
People = [x.lower() for x in temp_person]
People = ' '.join(People)
generate_wordcloud(People,"People")


print("Org")
org = [x.lower() for x in temp_org]
org = ' '.join(org)
generate_wordcloud(org,"org")

print("Place")
place = [x.lower() for x in temp_place]
place = ' '.join(place)
generate_wordcloud(place,"place")

print("All")
all1 = [x.lower() for x in all_nouns]
all1 = ' '.join(all1)
generate_wordcloud(all1,"All")


print ("Time taken for processing " + str (B-A) + " secs.")





                    