#This program is used to capture the interest and expertise of everyone. We load the mapped Dictionary as input.
# We also use the word to vec model to determine peoples interest and expertise.


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




model = gensim.models.Word2Vec.load('wordvecmodel')
mapping_to_type_dict= joblib.load('mapping_to_type_dict.pkl')

"""
	mapping_to_type_dict[people] ='PERSON'
	mapping_to_type_dict[place] = 'PLACE'
	mapping_to_type_dict[org] = 'ORG'
	mapping_to_type_dict[topic] ='TOPIC'
"""


orgs =[]
topics =[]
peoples = []
for entity in mapping_to_type_dict:
	if mapping_to_type_dict[entity] =='ORG':
		orgs.append(entity)
	if mapping_to_type_dict[entity] =='TOPIC':
		topics.append(entity)
	if mapping_to_type_dict[entity] =='PERSON':
		peoples.append(entity)

org_interest ={}

for org in orgs:
	interest =[]
	count = 0
	for entity in topics:
		if count >8:
			continue
		try:
			score =model.similarity(org, entity)
		except KeyError:
			continue
		if score < 0:
			continue
		count +=1
		interest.append([entity,score])
	interest=sorted(interest,key=lambda l:l[1], reverse=True)
	org_interest[org] = interest
joblib.dump(org_interest,'org_interest.pkl')	

people_interest ={}

for people in peoples:
	interest =[]
	count = 0

	for entity in topics:
		if count >8:
			continue
		try:
			score =model.similarity(people, entity)
		except KeyError:
			continue
		if score < 0:
			continue
		count +=1
		interest.append([entity,score])
	interest=sorted(interest,key=lambda l:l[1], reverse=True)
	people_interest[people] = interest
joblib.dump(people_interest,'people_interest.pkl')		

entity_experts ={}

for entity in topics:
	interest =[]
	count = 0
	for people in peoples:
		if count >6:
			continue
		try:
			score =model.similarity(entity, people)
		except KeyError:
			continue
		if score < 0.45:
			continue
		interest.append([people,score])
		count +=1
	interest=sorted(interest,key=lambda l:l[1], reverse=True)
	entity_experts[entity] = interest

joblib.dump(entity_experts,'experts.pkl')











