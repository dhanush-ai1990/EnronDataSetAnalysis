# -*- coding: utf-8 -*-
#This Program loads a random email and tests if its positive or negative.
from __future__ import unicode_literals
import numpy as np
from sklearn.externals import joblib
from math import *
from sklearn.externals import joblib
from ExtractFeature import *
import spacy
import nltk
import sys
import csv
import re
import nltk.tokenize
import os

#Formal = 0 and informal = 1
# Load the emails as text from the folder.
print "Loading emails for test"
email_articles =[]
email_articles_label=[]
email_loc = '/Users/Dhanush/Desktop/EnronDataSetAnalysis/Formal-Informal/Test_samples'
for file in os.listdir(email_loc):
    if file.endswith(".csv")or file.endswith(".txt"):
        file_to_read = email_loc + '/' + file 
    	f1 = open(file_to_read,'r')
    	email_articles_label.append(int(f1.readline()))
    	data = f1.read()
    	email_articles.append(data)
#print len(email_articles)
email_articles=map(unicode,email_articles)
print "Raw email text loaded"
print ("processing data using Spacy")
# Load spacy 
test_data = []
nlp = spacy.load('en')   
for email in email_articles:
	doc = nlp(email)
	temp =[]
	for np in doc:
		temp.append(np.text)
	str1 = ' '.join(temp)
	test_data.append(str1)
email_articles = test_data	


print "data processed using spacy"

#print len(email_articles)
#Extract the features as per the lingusitic papers.
FeatureExtractor = ExtractFeature('/Users/Dhanush/Desktop/EnronDataSetAnalysis/Formal-Informal/ClassificationFeatures/')
feature_matrix = []
for email in email_articles:
	feature_matrix.append(FeatureExtractor.process_create_feature(email))
#print (len(feature_matrix))
print "Feature matrix created for test"
print len(feature_matrix)
#print feature_matrix
print email_articles_label
#Load the Classifier using joblib.
clf = joblib.load('randomforests.pkl') 
print ("classifier loaded")


#predict using the loaded data.
X = feature_matrix#.toarray()
out =clf.predict(X)
probablity = clf.predict_proba(X)
print out
print probablity










