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
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
import time
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
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
import sklearn
from sklearn import datasets, linear_model

#list_entity = ['NORP','PERSON','GPE','ORG','FACILITY','LOC','PRODUCT','EVENT','WORK_OF_ART','LANGUAGE']
nlp = spacy.load('en')
parser = English()
list1 = [u'?', u'where',u'whom',u'why',u'whose',u'when',u'how',u'who',u' ?',u'? ',u' ? ']
def cleaninputusingspacy(inputs,type1):
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
					if type1 == 'A':
						word = (token.text).lower()
						if word not in list1:
							temp_data.append(word)
					else:
						temp_data.append(token.text)
		output.append(" ".join(temp_data))
	return output

def parse(path):
  g = gzip.open("qa_Software.json.gz", 'rb')
  for l in g:
    yield eval(l)

  f = gzip.open("qa_Electronics.json.gz", 'rb')
  for r in f:
    yield eval(r)


def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')

#df_software = getDF('/Users/aditimiglani/Downloads/qa_Software.json.gz')
df_electronics = getDF('qa_Electronics.json.gz')
#print df

df_combined = df_electronics['answer']
#print df_combined

#label for answers = 1
X_input =[]
X_input1 =[]
X_input2 =[]
y_input =[]
feat =[]
count =0
for line in df_combined:
	try:
		text = unicode(line,'utf8')
		X_input1.append(text)
		y_input.append(1.0)
		count +=1
	except UnicodeDecodeError:

		continue

	if count >10000:
		break



f = open("train_2000.txt",'r')

#question = f.read()

#label for questions = 0
temp = []
for line in f:
	line = line.split('\n')[0]
	try:
		text = unicode(line,'utf8')
		X_input2.append(text)
		temp.append(text)
		y_input.append(0.0)
	except UnicodeDecodeError:
		continue


X_input1 = cleaninputusingspacy(X_input1,"A")
X_input2 = cleaninputusingspacy(X_input2,"Q")
X_input = X_input1 + X_input2


print "After cleaning"
print len(X_input)


#cv = CountVectorizer(input = 'feat')
#X = cv.fit_transform(feat).toarray()
#mapping = cv.get_feature_names()
mapping = list(set([u'?', u'where',u'whom',u'why',u'whose',u'when',u'how',u'who',u' ?',u'? ',u' ? ']))
print len(mapping)
mapping.sort()
print mapping


cv = CountVectorizer(input = 'X_input', lowercase=True,vocabulary=mapping,binary=True)
X = cv.fit_transform(X_input).toarray()
mapping = cv.get_feature_names()


joblib.dump(cv,'exp_int_vectorizer.pkl')
y = np.array(y_input)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=123)
print ("training classifiers")
a= time.time()
clf = sklearn.svm.LinearSVC()
clf.fit(X_train, y_train)

joblib.dump(clf,'exp_int_classifier.pkl')
b = time.time()

print ("Time taken to train in secs: " + str(b-a))
out =clf.predict(X_test)
print "Accuracy:" +str(accuracy_score(y_test,out))
print "F1 score: "+str(f1_score(y_test,out, average='macro'))
print "Percision: " + str(precision_score(y_test,out, average='macro'))
print "Recall: " +str(recall_score(y_test,out, average='macro')) 



#Aditi get the feature mapping from the classifier and find if ? are there as one of the features. 
# I think its coming as \t or \n. If so we need to remove all the new line and tab characters from our data.   


















