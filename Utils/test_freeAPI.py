#from __future__ import print_function  # In python 2.
import sys
import requests
from bs4 import BeautifulSoup
import json
import urllib2
from HTMLParser import HTMLParser
import sqlite3


def check_for_babelnet_entry(word):
	URL = 'http://live.babelnet.org/search?word='+word+'&lang=EN'
	URL ='http://babelnet.org/search?word='+word+'&lang=EN'
	session = requests.session()
	login_response = session.get(URL)
	soup = BeautifulSoup(login_response.text, "html.parser")
	for i in soup.find_all('div'):
		if i['class'] ==
		print i
	#text = str(soup)
	#print text
	soup=soup.getText()

	if 'No result found' in soup:
		return 'Not found'
	elif ('Verb' in soup) or ('Adverb' in soup) :
		return 'not noun'
	elif ('Named Entity' in soup):
		return 'named entity'
	else:
		return 'other'

print check_for_babelnet_entry('Jumping')



