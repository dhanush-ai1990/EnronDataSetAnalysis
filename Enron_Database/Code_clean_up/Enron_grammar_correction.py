from __future__ import print_function  # In python 2.
#This program is mainly aimed at doing named entity recognition.



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


import os
import sys
import urllib
import urlparse
#from urllib3 import HTTPError
#from urllib3 import URLError
import json



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
        c = None
        bg = None
        if c is not None:
            s_open = '\033[%dm' % c
            gap = len(s_open)
        if bg is not None:
            s_open += '\033[%dm' % bg
            gap = len(s_open)
        #if not c is None or bg is None:
        #    s_close = '\033[0m'
        #   gap += len(s_close)
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
    text = text.replace('Re:','')
    text = text.replace('RE:','')
    text = text.replace('re:','')
    text = text.replace('Fw:','')
    text = text.replace('FW:','')
    text = text.replace('fw:','')
    #text = re.sub(r'[^\'a-zA-Z0-9,?!./\']', ' ', text)

    return text


file_out = '/Users/Dhanush/Desktop/EnronDataSetAnalysis/Enron_Database/Grammar_clean/'
Database = sqlite3.connect('Enron_database.db')
c = Database.cursor()

SQL = "select distinct(msgid), raw_body,subject from `Enron Prime`"
#SQL = "select msgid, raw_body, subject from 'Enron Prime' where msgid = 1335"

c.execute(SQL)
file_number = 0
count = 0
temp_org =[]
temp_person = []
temp_place = []
temp_others = []
temp_product = []
proper_nouns =[]
all_nouns =[]
corrected_text ={}
all_words = []


dir1 ='/Users/Dhanush/Desktop/EnronDataSetAnalysis/Enron_Database/Grammar_clean'
# load the text into file

temp_list = []
counter = 0
for file in os.listdir(dir1):
    if file.endswith(".txt"):
        file_to_read = dir1 + '/' + file 
        f = open(file_to_read,'r')
        data = str(f.readline())
        temp= data.split('\n')[0]
        corrected_text[temp] = {}
        corrected_text[temp]['mail'] = f.read()
        counter+=1
        temp = str(file)
        temp_list.append(int(temp.split('.')[0]))
temp_list.sort()


count = 0
processed = 0
left =[]
for i in range(177000):
    if i not in temp_list:
        print (i)

        left.append(i)

print (len(left))
for data in c:
    if count not in left:
        count+=1
        continue

    count +=1
    processed +=1
    print ('Currently processing the email number: ' + str(count))
    file_to_write = file_out + str(count) + '.txt'
    output = open(file_to_write, "w")
    msgid = str(data[0])
    output.write(msgid)
	#print msgid
	#print data[1]
	#print "*********************************"
	#print msgid
    #subject = re.sub("[^a-zA-Z]", "", data[2]) 
	#body =re.sub("[^a-zA-Z]", " ", data[1])
    #print "*********************************"
    data1= data[1].split('-----Original Message-----')[0]
    body = clean(data1)
    fixed =[]
    for original_text in chunks(body, 550):
    	fixed_text = original_text
    	results = get_ginger_result(original_text)

    	color_gap, fixed_gap = 0, 0
        try:
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
        except TypeError:
            print ("Error for Grammar CHeck for Email :" + str(count))
            fixed.append(original_text)
    #fixed_body=map(unicode,fixed)
    fixed_body= " ".join(fixed)
    output.write("\n")
    output.write(fixed_body)
    #print (body)
    #print ("=============")
    #print (str(fixed_body))
    output.close()


print (" ")
