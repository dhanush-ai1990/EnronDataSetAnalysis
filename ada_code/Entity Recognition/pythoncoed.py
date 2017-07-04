#This program is mainly aimed at doing named entity recognition.


#import mysql.connector
import sqlite3
#from datetime import datetime
#import tldextract
import re
#from sklearn.externals import joblib
#import cs
#import cStringIO
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
    except IOError as e:
            print("HTTP Error:", e.code)
            quit()
    except IOError as e:
            print("URL Error:", e.reason)
            quit()
    except IOError, (errno, strerror):
        print("I/O error (%s): %s" % (errno, strerror))
        quit

    try:
        result = json.loads(response.read().decode('utf-8'))
    except ValueError:
        print("Value Error: Invalid server response.")
        quit()

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
	text = re.sub(r'[^a-zA-Z0-9,?!./]', ' ', text)
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
for data in c:
	#file_to_write = file_out + str(file_number) + '.txt'
	#output = open(file_to_write, "w")
	msgid = str(data[0])
	#print msgid
	#print data[1]
	#print "*********************************"
	#print msgid
	subject = re.sub("[^a-zA-Z]", "", data[2]) 
	#body =re.sub("[^a-zA-Z]", " ", data[1])
	body = clean(data[1])
	original_text = body
	fixed_text = original_text
	results = get_ginger_result(original_text)

	print "-------------------------------------------"
	print results
	if(not results["LightGingerTheTextResult"]):
		print("Good English :)")
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
	print fixed_text
	doc = nlp(fixed_text)



	for ent in doc.ents:
		if  (ent.label_ =='ORG'):
			#print(ent.label_, ent.text)
			temp_org.append(ent.text)
		if  (ent.label_ == 'PERSON'):
			temp_person.append(ent.text)

		if  (ent.label_ == 'GPE'):
			temp_place.append(ent.text)


	for sentence in nltk.sent_tokenize(clean(data[1])) :
		parsed = parser(sentence)

		for token in parsed :
			if (token.tag_ == "NNP") or (token.tag_ == "NNPS") :
				all_nouns.append(token.text)
	
		#print np.text
					
	#output.write(msgid+'\n')
	#output.write(subject+'\n')
	#output.write(body+'\n')
	#file_number +=1
	count+=1


	
	if count >10:
		break
print temp_place
temp_place= list(set(temp_place) & set(all_nouns))
temp_org= list(set(temp_org) & set(all_nouns))
temp_person= list(set(temp_person) & set(all_nouns))

#=================================================		

words_to_count = (word for word in temp_place if word[:1].isupper())
c = Counter(words_to_count)
places= c.most_common(500)
print places
print "***********************************"


words_to_count = (word for word in temp_org if word[:1].isupper())
c = Counter(words_to_count)
org= c.most_common(500)
print org
print "***********************************"

words_to_count = (word for word in temp_person if word[:1].isupper())
c = Counter(words_to_count)
person= c.most_common(500)
print person
print "***********************************"


#print c.most_common(500)

#Now since we have all emails as text, its easier to load them and process using Spacy.

# We will do a word cloud or dictionary first and save that as pickled object.

#trying a new NLTK Entity recognizer.
