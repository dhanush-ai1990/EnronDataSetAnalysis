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
file_loc = '/Users/Dhanush/Desktop/Enron_Data/Search_engine_pickle/'
mapping_to_type_dict=joblib.load(file_loc+'mapping_to_type_dict.pkl')

SearchEngineWordList=joblib.load(file_loc+'SearchEngineWordList.pkl')
print 'organization of the petroleum exporting countries' in SearchEngineWordList
print 'organization of the petroleum exporting countries' in mapping_to_type_dict
print len(mapping_to_type_dict)

def fetch_type(word):
	global mapping_to_type_dict
	try:
		word = mapping_to_type_dict[word]
	except KeyError:
		return "PERSON"
	return word


print fetch_type('organization of the petroleum exporting countries')