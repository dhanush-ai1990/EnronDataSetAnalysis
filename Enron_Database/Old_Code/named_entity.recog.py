#from __future__ import print_function  # In python 2.
#This program is mainly aimed at doing named entity recognition.


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

import sys
import urllib
import urlparse
#from urllib3 import HTTPError
#from urllib3 import URLError
import json


org_coded_list = ['Citibank']
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

def chunks(s, n):
    """Produce `n`-character chunks from `s`."""
    for start in range(0, len(s), n):
        yield s[start:start+n]
class ColoredText:
    """Colored text class"""
    colors = ['black', 'red', 'green', 'orange', 'blue', 'magenta', 'cyan', 'white']
    color_dict = {}
    for i, c in enumerate(colors):
        color_dict[c] = (i + 30, i + 40)

    @classmethod
    def colorize(cls, text, color=None, bgcolor=None):
        """Colorize text
        @param cls Class
        @param text Text
        @param color Text color
        @param bgcolor Background color
        """
        c = None
        bg = None
        gap = 0
        if color is not None:
            try:
                c = cls.color_dict[color][0]
            except KeyError:
                print("Invalid text color:", color)
                return(text, gap)

        if bgcolor is not None:
            try:
                bg = cls.color_dict[bgcolor][1]
            except KeyError:
                print("Invalid background color:", bgcolor)
                return(text, gap)

        s_open, s_close = '', ''
        if c is not None:
            s_open = '\033[%dm' % c
            gap = len(s_open)
        if bg is not None:
            s_open += '\033[%dm' % bg
            gap = len(s_open)
        if not c is None or bg is None:
            s_close = '\033[0m'
            gap += len(s_close)
        return('%s%s%s' % (s_open, text, s_close), gap)
def get_ginger_url(text):
    """Get URL for checking grammar using Ginger.
    @param text English text
    @return URL
    """
    API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"

    scheme = "http"
    netloc = "services.gingersoftware.com"
    path = "/Ginger/correct/json/GingerTheText"
    params = ""
    query = urllib.urlencode([
        ("lang", "US"),
        ("clientVersion", "2.0"),
        ("apiKey", API_KEY),
        ("text", text)])
    fragment = ""

    return(urlparse.urlunparse((scheme, netloc, path, params, query, fragment)))


def get_ginger_result(text):
    """Get a result of checking grammar.
    @param text English text
    @return result of grammar check by Ginger
    """
    url = get_ginger_url(text)

    try:
        response = urllib.urlopen(url)
    except urllib.HTTPError as e:
            print("HTTP Error:", e.code)
            results = text
    except urllib.error.HTTPError as e:
            print("URL Error:", e.reason)
            results = text
    except IOError, (errno, strerror):
        print("I/O error (%s): %s" % (errno, strerror))

    try:
        result = json.loads(response.read().decode('utf-8'))
    except ValueError:
        print("Value Error: Invalid server response.")

    return(result)

def clean(text):

	text = text.replace('--','')
	text = text.replace('\\t',' ')
	text = text.replace('=','') 
	text = text.replace('(','') 
	text = text.replace(')','') 
	text = text.replace('<','') 
	text = text.replace('>','')
	text = text.replace('thankskh','')
	text = re.sub(r'[^a-zA-Z0-9,?!./\']', ' ', text)
	return text

nlp = spacy.load('en')

file_out = '/Users/Dhanush/desktop/EnronDataSetAnalysis/Enron_Database/Enron_Text/'
Database = sqlite3.connect('Enron_database.db')
c = Database.cursor()

SQL = "select distinct(msgid), raw_body,subject from `Enron Prime`"
#SQL = "select msgid, raw_body, subject from 'Enron Prime' where msgid = 1335"

c.execute(SQL)
file_number = 0
count = 0
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
for data in c:

    if count >100:
        break
    print "Processing Email: " +str(count)
    count+=1
	#file_to_write = file_out + str(file_number) + '.txt'
	#output = open(file_to_write, "w")

    msgid = str(data[0])
    corrected_text[msgid] = []
	#print msgid
	#print data[1]
	#print "*********************************"
	#print msgid
    subject = re.sub("[^a-zA-Z]", "", data[2]) 
	#body =re.sub("[^a-zA-Z]", " ", data[1])
    #print "*********************************"
    data1= data[1].split('-----Original Message-----')[0]
    body = clean(data1)
    fixed =[]
    for original_text in chunks(body, 550):
    	fixed_text = original_text
    	results = get_ginger_result(original_text)

    	
    	if(not results["LightGingerTheTextResult"]):
            filler =0
    		#print("Good English :)")
    	color_gap, fixed_gap = 0, 0
    	for result in results["LightGingerTheTextResult"]:
    		if(result["Suggestions"]):
    			from_index = result["From"] + color_gap
    			to_index = result["To"] + 1 + color_gap
    			suggest = result["Suggestions"][0]["Text"]

    			colored_incorrect = ColoredText.colorize(original_text[from_index:to_index], 'red')[0]
    			colored_suggest, gap = ColoredText.colorize(suggest, 'green')

    			original_text = original_text[:from_index] + colored_incorrect + original_text[to_index:]
    			fixed_text = fixed_text[:from_index-fixed_gap] + colored_suggest + fixed_text[to_index-fixed_gap:]

    			color_gap += gap
    			fixed_gap += to_index-from_index-len(suggest)
    	fixed.append(fixed_text)
    fixed_body=map(unicode,fixed)
    fixed_body= " ".join(fixed_body)
    corrected_text[msgid].append(fixed_body)
    # Saved the corrected Text.

    if len(fixed_body) < 2:
        continue
    doc = nlp(fixed_body)

    for ent in doc.ents:
    	if  (ent.label_ =='ORG'):
            if ent.text.isalpha():
                temp_org.append(ent.text)

    	if  (ent.label_ == 'PERSON'):
            if ent.text.isalpha():
    	       temp_person.append(ent.text)

    	if  (ent.label_ == 'GPE'):
            if ent.text.isalpha():
                temp_place.append(ent.text)

        if ent.text in org_coded_list:
            if ent.text.isalpha():
                temp_org.append(ent.text)



    for sentence in nltk.sent_tokenize(fixed_body) :
    	parsed = parser(sentence)
        for token in parsed :
            if token.text.isalpha():
                if (token.tag_ == "NNP") or (token.tag_ == "NNPS"):
                    all_nouns.append(token.text)
    	#print np.text
    
print "Post analysis to Sharpen the data source"
# The people are better understood by Spacy, so we leave this alone
temp_person= list(set(temp_person) & set(all_nouns))

# We have fixed people and kept other entities. These should include all other named entities.
# We will check if these are actual Entities if found in Babel
all_nouns =set(all_nouns)
all_nouns.difference_update(temp_person)

nouns_without_person = all_nouns
all_valid_entities = []

print len(list(nouns_without_person))
for word in list(nouns_without_person):
    if check_for_babelnet_entry(word) == 'found':
        all_valid_entities.append(word)

print len(all_valid_entities)

temp_place= list(set(temp_place) & set(all_valid_entities))
temp_org= list(set(temp_org) & set(all_valid_entities))

# We need to use API to get detailed information on all_valid_entities, but we will save it as script for Now
name_place_org = set(temp_person + temp_place + temp_org)

Interest_expertise = set(all_valid_entities)

Interest_expertise.difference_update(name_place_org)


print "Organizations"
print temp_org   # Needs to be Validated Using BabeL
print "Places"
print temp_place # Needs to be Validated Using BabeL
print "People"
print temp_person
print "Interest and Expertise"
print Interest_expertise  # Needs to be Validated Using BabeL


print len(list(Interest_expertise))
print len(corrected_text.keys())


print " "
