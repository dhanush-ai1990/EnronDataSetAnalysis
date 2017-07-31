from sklearn.externals import joblib
from gensim.models import Word2Vec
import gensim
from sklearn.externals import joblib
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
import urllib
import urllib2
import json


api_key ='AIzaSyAXSTt536rRbl4dK4pzuPs-QfuGKTT-YBk'
#dict1 = joblib.load('/Users/Dhanush/Desktop/Enron_Data/pickle/Org.pkl')
type_data= ['Corporation','Organization','GovernmentOrganization','EducationalOrganization','LocalBusiness','SportsTeam']
#print dict1



def google_KG_search(word):

	service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
	params = {
	'query': word,
	'limit': 3,
	'indent': True,
	'key': api_key,
	}
	detailed_description = ""
	description =" "
	url = service_url + '?' + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())

	print response
	flag = 0
	u = 'University'
	try:
		for element in response['itemListElement']:


			description1 = element['result']['@type'] #list
			for e in description1:
				#if e in type_data:
				if True:
					try:
						name = element['result']['name']
						temp = name.split(" ")
						if temp[0] == 'University':
							name = word.title()


					except KeyError:
						name = ""
					try:
						description = element['result']['description']
					except KeyError:
						description =""
				
					try:
						detailed_description = element['result']['detailedDescription']['articleBody']
					except KeyError:
						detailed_description = ""

					try:
						url = element['result']['url']
					except KeyError:
						url =""




					flag = 1
			if flag ==1:
				break
	except KeyError:
		return []

	if flag == 0:
		return None

	else:
		return [name,description,detailed_description,url]

print google_KG_search("rbc capital markets")

