import nltk
import sys
import csv
import re
from nltk.corpus import stopwords
from nltk.tokenize import *
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tag import pos_tag
import string as st
import pandas as pd
import gzip
from bs4 import BeautifulSoup
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import time
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
from collections import Counter
from spacy.en import English


#list_entity = ['NORP','PERSON','GPE','ORG','FACILITY','LOC','PRODUCT','EVENT','WORK_OF_ART','LANGUAGE']
nlp = spacy.load('en')
parser = English()

def cleaninputusingspacy(inputs):
	output = []
	count = 0
	for data in inputs:
		temp_data = []
		for sentence in nltk.sent_tokenize(data) :
			parsed = parser(sentence)
			for token in parsed :
				if (token.tag_ == "NNP") or (token.tag_ == "NNPS")or (token.tag_ == "NN"):
					donothing =0
				else:
					temp_data.append(token.text)
		output.append(" ".join(temp_data))
	return output

cv=joblib.load('exp_int_vectorizer.pkl')
clf =joblib.load('exp_int_classifier.pkl')

test = [u'Ada the best one to contact for machine learning. She knows  to do the AI shit.']
#test =[u'Are you there yet ?']

test = cleaninputusingspacy(test)
X = cv.transform(test).toarray()

print X


#question is 0
#answer is 1
print clf.predict(X)