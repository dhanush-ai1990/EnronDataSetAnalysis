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


#Lets load the selected entities
people_dict= joblib.load('/Users/Dhanush/Desktop/Enron_Data/Outputs/Entity/People_dictionary.pkl')
place_dict =joblib.load('/Users/Dhanush/Desktop/Enron_Data/Outputs/Entity/Places_datatag.pkl')
org_dict =joblib.load('/Users/Dhanush/Desktop/Enron_Data/Outputs/Entity/ORG_datatag.pkl')

#Load the selected interest and expertise.

interest_expertise = []


in_file = open ('/Users/Dhanush/Desktop/Enron_Data/Outputs/selected_entity.txt','r')
for line in in_file:
	line = line.replace('\n','')
	interest_expertise.append(line)

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


corrected_text ={}


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
tag_temp = {}

email_vs_entity_alone = {}
for key in keys:
    email_vs_entity_alone[key] = []
    email_entity_dict[key] = {}
    email_entity_dict[key]['Names'] = []
    email_entity_dict[key]['Places'] = []
    email_entity_dict[key]['Org'] = []
    email_entity_dict[key]['Entities'] = []
    email_entity_dict[key]['tokens'] = []
    email_entity_dict[key]['sender_email'] = []
    email_entity_dict[key]['receiver_email'] =[]
    email_entity_dict[key]['receiver_name'] =[]

#Query the main database and get the 
Database = sqlite3.connect('Enron_database.db')
c = Database.cursor()

SQL = "select msgid, sender_email, receiver_email, sender_first_name,sender_last_name,sender_full_name, receiver_first_name, receiver_last_name,receiver_full_name from `Enron Prime`"
c.execute(SQL)

hold = None
flag = False

"Processing database"

#load the mapped Employee dictionary
email_dict= joblib.load('/Users/Dhanush/Desktop/Enron_Data/Outputs/employee_dict_email.pkl')
for record in c:
    temp_org =[]
    MSGID = int(record[0])

    if MSGID not in keys:
        print ("skipping record")
        continue

    if hold == MSGID:
        flag = False

    else:
        flag = True
        hold = MSGID


    email_entity_dict[MSGID]['sender_email'] = record[1]

    if record[3] == '**' or record[4] == "**":
        placeholder =0
    else:
        email_entity_dict[MSGID]['sender_Name'] = record[5]

        if flag == True:
            email_vs_entity_alone[MSGID].append(record[5])
            try:
                email_vs_entity_alone[MSGID].append(email_dict[record[1]]['org'])
                email_entity_dict[MSGID]['Org'].append(email_dict[record[1]]['org'])
            except KeyError:
                blah=0

    if record[6] == '**' or record[7] == "**":
    		placeholder =0
    else:
    	email_entity_dict[MSGID]['receiver_name'].append(record[8])
        email_vs_entity_alone[MSGID].append(record[8])
        

    email_entity_dict[MSGID]['receiver_email'].append(record[2])
    try:
        email_vs_entity_alone[MSGID].append(email_dict[record[2]]['org'])
        email_entity_dict[MSGID]['Org'].append(email_dict[record[2]]['org'])
    except KeyError:
        continue


   
print "Processing the entity now"

mandatory =['rbcds.com','rbc.com','rbcinvestments.com','rbcdain.com','rbc confirm','rbc capital partners telecom fund','rbc capital markets','rbc capital markets vice']
temp_mapped ={'rbcds.com':'RBC Dominion Securities','rbc.com':'Royal Bank of Canada','rbcinvestments.com':'Royal Bank of Canada','rbcdain.com':'Royal Bank of Canada','rbc confirm':'Royal Bank of Canada','rbc capital partners telecom fund':'RBC CAPITAL MARKETS','rbc capital markets':'RBC CAPITAL MARKETS','rbc capital markets vice':'RBC CAPITAL MARKETS'}
count = 0
for key in keys:

    #print ("===================================================================")
    #print "Processing Email: " +str(count)
    text = unicode(corrected_text[key]['mail'],'utf8')
    
    if len(text) < 5:
        count+=1
        continue
    doc = nlp(text)
    for ent in doc.ents:

        if  (ent.label_ == 'PERSON'):
            word = ent.text
            word = word.strip()
            word = word.strip()
            word = re.sub("[^a-zA-Z]+"," ", word)
            if check_for_name_length(word):
                word=word.lower()
                if word in people_dict:
                    email_entity_dict[int(key)]['Names'].append(word)
                    email_vs_entity_alone[int(key)].append(word)
                if word == 'mark easterbrook':
                    email_entity_dict[int(key)]['Names'].append('mark easterbrook')
                    email_vs_entity_alone[int(key)].append('mark easterbrook')
                    print word

        if  (ent.label_ == 'GPE'):
            word = ent.text
            word = word.strip()
            word = word.strip()
            word = re.sub("[^a-zA-Z]+"," ", word)
            if check_noise(word):
                word = word.lower()
            	if word in place_dict:
                    email_entity_dict[int(key)]['Places'].append(place_dict[word])
                    email_vs_entity_alone[key].append(place_dict[word])


    
        if  (ent.label_ =='ORG'):
            word = ent.text
            word = word.strip()
            word = word.strip()
            word = re.sub("[^a-zA-Z]+"," ", word)
            if check_noise(word):
                word=word.lower()
                if word in org_dict:
                    email_entity_dict[int(key)]['Org'].append(org_dict[word])
                    email_vs_entity_alone[key].append(org_dict[word])
                elif word in mandatory:
                    email_entity_dict[int(key)]['Org'].append(temp_mapped[word])
                    email_vs_entity_alone[key].append(temp_mapped[word])
                    print word
                else:
                    continue





    for sentence in nltk.sent_tokenize(text) :
        parsed = parser(sentence)
        for token in parsed :
            if token.text.isalpha():
                if (token.tag_ == "NNP") or (token.tag_ == "NNPS")or (token.tag_ == "NN"):
                    word = token.text.lower()
                    if word in interest_expertise:
                        #Fraud and Banruptcy are of interests to Enron
                    	email_entity_dict[int(key)]['Entities'].append(word)
                        email_vs_entity_alone[key].append(word)


    count +=1



#print ("============================================")
B = time.time()

print ("Time taken for processing " + str (B-A) + " secs.")


#Dump the pickle objects

dump ='/Users/Dhanush/Desktop/Enron_Data/pickle/'

print ("Initializing the Data dumps")
joblib.dump(email_entity_dict, dump+'Email_Entity_Mapping.pkl')
joblib.dump(email_vs_entity_alone, dump+'email_vs_entity_alone.pkl')
print ("")
