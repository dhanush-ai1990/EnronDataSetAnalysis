#from __future__ import print_function  # In python 2.
import sys
import requests
from bs4 import BeautifulSoup
import json
import urllib2
from HTMLParser import HTMLParser
import sqlite3
import json


def check_for_babelnet_entry(word):
	URL = 'http://live.babelnet.org/search?word='+word+'&lang=EN'
	URL ='http://babelnet.org/search?word='+word+'&lang=EN'
	URL = 'https://babelnet.io/v4/getSenses?word='+word+'&lang=EN&source=WIKI&key=eeb2340a-5060-4770-8a80-cc306222ab31'
	session = requests.session()
	login_response = session.get(URL)
	soup = BeautifulSoup(login_response.text, "html.parser")
	Output=json.loads(str(soup))
	if len(Output) <1:
		return "Not Found"
	else:
		return "Found"

print check_for_babelnet_entry('Eenehjjd')



