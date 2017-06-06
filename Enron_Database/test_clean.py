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
import string

from nltk.tokenize.regexp import RegexpTokenizer

from subprocess import check_output

from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.lda import LDA
from sklearn.decomposition import LatentDirichletAllocation

import gensim
from gensim import corpora
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
from nltk.stem.porter import PorterStemmer
nlp = spacy.load('en')


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
	#stop = set(stopwords.words('english'))
	#stop=stop.update(("to","cc","subject","http","from","sent","aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",".thankskh"))
	#exclude = set(string.punctuation)
	#lemma = WordNetLemmatizer()
	#porter= PorterStemmer()
	#text=text.rstrip()



	#text = re.sub(r'[^a-zA-Z]', ' ', text)
	#stop_free = " ".join([i for i in text.lower().split() if((i not in stop) and (not i.isdigit()))])
	#punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
	#normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
	#stem = " ".join(porter.stem(token) for token in normalized.split())
	#return punc_free
	#return normalized
	return text
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
count = 0
for data in c:
	count+=1
	#file_to_write = file_out + str(file_number) + '.txt'
	#output = open(file_to_write, "w")
	msgid = str(data[0])
	print "**************************************************"
	print "before cleaning "
	print " "
	print data[1]
	print "After cleaning "
	print " "

	print clean(data[1])

	if count > 50:
		break


