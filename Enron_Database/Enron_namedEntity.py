#import mysql.connector
import sqlite3
#from datetime import datetime
#import tldextract
import re
from bs4 import BeautifulSoup
import json
import urllib2
#from sklearn.externals import joblib
#import cs
#import cStringIO
from sklearn.externals import joblib
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


stop_list = '/Users/Dhanush/Desktop/Enron_Data/stop_words_people.txt'
stop_file= open(stop_list,'r')
stop_list= []
for line in stop_file:
    line = line.replace('\n','')
    stop_list.append(line)
stop_list = list(set(stop_list)) + ['ECT','Enron','com']
stop_list =[element.lower() for element in stop_list]

# Stop words for Places and Org

place_stop_list =[]
place_file = open ('/Users/Dhanush/Desktop/Enron_Data/list_Places.txt','r')
for line in place_file:
    line = line.replace('\n','')
    place_stop_list.append(line)
place_stop_list = list(set(place_stop_list)) + ['ECT','Enron']
place_stop_list =[element.lower() for element in place_stop_list]

def check_for_babelnet_entry(word):
    #URL = 'http://live.babelnet.org/search?word='+word+'&lang=EN'
    #URL ='http://babelnet.org/search?word='+word+'&lang=EN'
    URL = 'https://babelnet.io/v4/getSenses?word='+word+'&lang=EN&source=WIKI&key=eeb2340a-5060-4770-8a80-cc306222ab31'
    session = requests.session()
    login_response = session.get(URL)
    soup = BeautifulSoup(login_response.text, "html.parser")
    Output=json.loads(str(soup))
    if len(Output) <1:
        return "Not Found"
    else:
        return "found"
def check_for_name_length(word):
    caps = sum(1 for c in word if c.isupper())
    if caps > 3:
        return False

    if (sum(1 for c in word)) < 7:
        return False

    word_list = word.split(" ")

    if (len(word_list)) == 1:
        return False

    if (len(word_list)) > 2:
        return False

    #Only one capital letter allowed per word
    if caps > len(word_list):
        return False
    count = 0
    for word in word_list:

        if (count ==0):
            if len(word) < 3:
                return False

        if (count==1)  or (count ==2):
            if word.isalpha():

                if  (word[0].islower()):
                    return False

        if (len(word) >1):
            if (word[0].isupper()) and (word[1].isupper()):
                return False

        
        word = word.lower()
        if word in stop_list:
            return False 
        count+=1
    return True

def check_noise(word):
    caps = sum(1 for c in word if c.isupper())
    word_list = word.split(" ")
    for word in word_list:
        word = word.lower()
        if word in place_stop_list:
            return False 
    return True

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

    #print ("===================================================================")
    #print "Processing Email: " +str(count)
    text = unicode(corrected_text[key]['mail'],'utf8')
    
    if len(text) < 5:
        count+=1
        #print ("Error: " + str(count))
        continue

    
    count+=1

    #print (fixed_body)
    doc = nlp(text)
    for ent in doc.ents:

        if  (ent.label_ == 'PERSON'):
            word = ent.text
            word = word.strip()
            word = word.strip()
            word = re.sub("[^a-zA-Z]+"," ", word)
            if check_for_name_length(word):
                temp_person.append(word)
                email_entity_dict[int(key)]['Names'].append(word)

        if  (ent.label_ == 'GPE'):
            word = ent.text
            word = word.strip()
            word = word.strip()
            word = re.sub("[^a-zA-Z]+"," ", word)
            if check_noise(word):
                temp_place.append(word)
                email_entity_dict[int(key)]['Places'].append(word)

    
        if  (ent.label_ =='ORG'):
            word = ent.text
            word = word.strip()
            word = word.strip()
            word = re.sub("[^a-zA-Z]+"," ", word)
            if check_noise(word):
                temp_org.append(word)
                email_entity_dict[int(key)]['Org'].append(word)



    for sentence in nltk.sent_tokenize(text) :
        parsed = parser(sentence)
        for token in parsed :
            if token.text.isalpha():
                if (token.tag_ == "NNP") or (token.tag_ == "NNPS")or (token.tag_ == "NN"):
                    all_nouns.append(token.text)
                    email_entity_dict[int(key)]['tokens'].append(token.text)

    print ("Processed " + str(count))


#print ("============================================")
B = time.time()

# Create word clouds for body.
"""
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
"""

print ("Time taken for processing " + str (B-A) + " secs.")
print (len(all_nouns))
print (len(temp_place))
print (len(temp_org))
print (len(temp_person))

#Dump the pickle objects

dump ='/Users/Dhanush/Desktop/Enron_Data/pickle/'

print ("Initializing the Data dumps")
joblib.dump(email_entity_dict, dump+'Email_Entity_Mapping.pkl')
joblib.dump(all_nouns, dump+'All_Entity.pkl')
joblib.dump(temp_person, dump+'People.pkl')
joblib.dump(temp_org, dump+'Org.pkl')
joblib.dump(temp_place, dump+'Place.pkl')



print ("")