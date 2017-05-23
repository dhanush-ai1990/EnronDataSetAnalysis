# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.datasets import fetch_20newsgroups
import logging
import sys
from time import time
from math import *

import spacy
import nltk
import sys
import csv
import re
from nltk.corpus import stopwords
from nltk.tokenize import *
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.tag import pos_tag
import string as st
from ExtractFeature import *
import timeit
import os
import tldextract
import numpy as np
import re
import nltk
import nltk.tokenize
from scipy.sparse import coo_matrix
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from nltk.tokenize import TreebankWordTokenizer
from sklearn.model_selection import cross_val_score
from sklearn.cross_validation import ShuffleSplit
# from sklearn.grid_search import GridSearchCV
from sklearn.learning_curve import learning_curve
from sklearn.model_selection import GridSearchCV
from matplotlib import pyplot as pl
from matplotlib.backends.backend_pdf import PdfPages
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_blobs
import gc
from sklearn import svm
from sklearn.datasets import fetch_20newsgroups
from sklearn.externals import joblib

def MyRandomForest(X_train, y_train):
	clf = RandomForestClassifier()
	#param_grid = {'n_estimators': [10,20,30,50,70,100,200,500,1000,2000,2500]}
	param_grid = {'n_estimators': [75]}
	classifier= GridSearchCV(estimator=clf, cv=3 ,param_grid=param_grid)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def MyDecisionTree(X_train, y_train):
	clf = DecisionTreeClassifier(min_samples_split=2,random_state=0)
	param_grid = {'max_depth': [1,5,10,25,50,75,100,500]}
	classifier= GridSearchCV(estimator=clf, cv=3 ,param_grid=param_grid)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def MyExtraTreeClassifier(X_train, y_train):
	clf = ExtraTreesClassifier(min_samples_split=2, random_state=0,max_depth = 10)
	param_grid = {'n_estimators': [10,20,30,50]}
	#param_grid = {'max_depth': [1,5,10,25,50,75,100,500,1000,2000]}
	classifier= GridSearchCV(estimator=clf, cv=3 ,param_grid=param_grid)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def MyMultiNomialNB(X_train, y_train):
	clf = MultinomialNB()
	param_grid = {'alpha': [0.000000001,0.00000001,0.0000001,0.0000001] }
	#param_grid = {'alpha': [0.000001] }
	# Ten fold Cross Validation
	classifier= GridSearchCV(estimator=clf, cv=10 ,param_grid=param_grid)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def Mylinear_svm(X_train, y_train):
	linear_svc = svm.SVC(kernel='linear')#,decision_function_shape ='ovo'/'ovr'
	param_grid = {'C': np.logspace(-3, 2, 6)}
	#param_grid = {'C': [ 0.1]}
	classifier= GridSearchCV(estimator=linear_svc, cv=3 ,param_grid=param_grid)
	y_train= np.array(y_train)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def rbf_svm(X_train, y_train):
	rbf_svc = svm.SVC(kernel='rbf')#,max_iter = 10000,cache_size =1024,decision_function_shape ='ovo'/'ovo'
	param_grid = {'C': np.logspace(-3, 2, 6), 'gamma': np.logspace(-3, 2, 6)}
	classifier= GridSearchCV(estimator=rbf_svc, cv=10 ,param_grid=param_grid)
	y_train= np.array(y_train)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_


def convert_html_entities(s):
    matches = re.findall("&#\d+;", s)
    flag = 'n'
    if len(matches) > 0:
        hits = set(matches)
        for hit in hits:
            name = hit[2:-1]
            try:
                entnum = int(name)
                s = s.replace(hit, unichr(entnum))
                flag = 'y'
            except ValueError:
                pass

    matches = re.findall("&#[xX][0-9a-fA-F]+;", s)
    if len(matches) > 0:
        hits = set(matches)
        for hit in hits:
            hex = hit[3:-1]
            try:
            	flag = 'y'
                entnum = int(hex, 16)
                s = s.replace(hit, unichr(entnum))
            except ValueError:
                pass

    matches = re.findall("&\w+;", s)
    hits = set(matches)
    amp = "&amp;"
    if amp in hits:
        hits.remove(amp)
    for hit in hits:
        name = hit[1:-1]
        if htmlentitydefs.name2codepoint.has_key(name):
            s = s.replace(hit, unichr(htmlentitydefs.name2codepoint[name]))
    try:        
    	s = s.replace(amp, "&")
    except:
    	flag = 'y'

    if flag=='y':
    	s = '99999999999'
    return s 

A1 = timeit.default_timer()
#Load the news data from twenty news group
categories = ['alt.atheism',

 'comp.graphics',
 'comp.os.ms-windows.misc',
 'comp.sys.ibm.pc.hardware',
 'comp.sys.mac.hardware',
 'comp.windows.x',
 'misc.forsale',
 'rec.autos',
 'rec.motorcycles',
 'rec.sport.baseball',
 'rec.sport.hockey',
 'sci.crypt',
 'sci.electronics',
 'sci.med',
 'sci.space',
 'soc.religion.christian',
 'talk.politics.guns',
 'talk.politics.mideast',
 'talk.politics.misc',
 'talk.religion.misc']
remove = ('headers', 'footers', 'quotes')

data_train = fetch_20newsgroups(subset='train', categories=categories,
                                shuffle=True, random_state=42,
                                remove=remove)

data_test = fetch_20newsgroups(subset='test', categories=categories,
                               shuffle=True, random_state=42,
                               remove=remove)

print('data loaded')

twenty_y_train, y_test = data_train.target, data_test.target
twenty_X_train =data_train.data
twenty_X_train=map(unicode,twenty_X_train)
#print (len(twenty_X_train))

print ("processing news")
# Load spacy 
train_data_formal = []
nlp = spacy.load('en')   
for news in twenty_X_train:
	doc = nlp(news)
	temp =[]
	for np in doc:
		temp.append(np.text)
	str1 = ' '.join(temp)
	train_data_formal.append(str1)

#print train_data_formal[0]


# Load the Tweets !
print ("Procesing Tweets")
twitter_dataset = '/Users/Dhanush/Desktop/EnronDataSetAnalysis/Datasets/tweets.txt'
train_data_informal = []
f = open(twitter_dataset,'r')
lines = f.read().splitlines()

temp_lines =[]

for line in lines:
	
	string1 = convert_html_entities(line)
	if (string1 == '99999999999'):
		continue
	temp_lines.append(string1)
lines = temp_lines

lines=map(unicode,lines)
line_reduced = lines[0:10000] + lines[-10000:]
lines = line_reduced
for line in lines:
	doc = nlp(line)
	temp =[]
	for np in doc:
		temp.append(np.text)
	str1 = ' '.join(temp)	
	train_data_informal.append(str1)

#print (train_data_informal[3])

#Create the label matrix

formal_data_label_list =[]  #Formal = 0
informal_data_label_list =[] #Informal = 1

for i in range(len(train_data_formal)):
	formal_data_label_list.append(0)

for i in range(len(train_data_informal)):
	informal_data_label_list.append(1)
# combine and create a common training set. We will use CV and split into train and test later.
print "Formal dataset " +str(len(train_data_formal))
print "Informal dataset " +str(len(train_data_informal))
Combined_training_data = train_data_formal + train_data_informal
Combined_training_label = formal_data_label_list +informal_data_label_list

print ("Total training data samples " + str(len(Combined_training_data)))
print ("Total training data labels " + str(len(Combined_training_label)))

"""
cv = TfidfVectorizer(input ='Combined_training_data',lowercase=True,analyzer ='word',binary =False,min_df = 0.3,max_features =5000)#,non_negative=True)#,)

X = cv.fit_transform(Combined_training_data).toarray()

vocab = np.array(cv.get_feature_names())
y = (np.array(Combined_training_label))
X_train, X_test, y_train, y_test = train_test_split(X,y ,test_size=0.2, random_state=5677)
results_DTC = MyRandomForest(X_train,y_train)
print "Maximum Train accuracy: " 
print results_DTC['mean_train_score']

print "Maximum Test accuracy: " 
print results_DTC['mean_test_score']

"""
A2 = timeit.default_timer()
load_time = A2 - A1
print ('---------------------------------------------------')
print ("It took " + str(load_time) + ' seconds to load the data. Now extracting features')
print ('---------------------------------------------------')
#Call ExtractFeature to get the feature matrix.

FeatureExtractor = ExtractFeature('/Users/Dhanush/Desktop/EnronDataSetAnalysis/Formal-Informal/ClassificationFeatures/')

feature_matrix = []
count = 0
A3 = timeit.default_timer()
for data in Combined_training_data:
	if (count %500 ==0):
		A4 = timeit.default_timer()
		temp_time = A4 - A3
		print ("processed " + str(count) +" tweets in " + str(temp_time))

	count +=1
	feature_matrix.append(FeatureExtractor.process_create_feature(data))
print (len(feature_matrix))
dataset = (feature_matrix,Combined_training_label)
joblib.dump(dataset, 'feature_matrix.pkl')
