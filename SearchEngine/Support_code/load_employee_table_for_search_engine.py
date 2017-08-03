#This program is used to capture the employee tables and colloborators. We load the mapped Dictionary as input.
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
import sqlite3
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
import clearbit

Database = sqlite3.connect('/Users/Dhanush/Desktop/Enron_Data/Enron_database.db')
c = Database.cursor()

SQL = "select `EMAIL ID`, FIRST, LAST, `FULL NAME`, ORGANIZATION from `EMPLOYEE`"
c.execute(SQL)
#/Users/Dhanush/desktop/


#model = gensim.models.Word2Vec.load('wordvecmodel')
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

enron_table = {}
other_org_table ={}
for record in c:
	if record[2] =='**':
		continue
	org = record[4].lower()
	print org
	if org == 'enron':
		enron_table[record[3].lower()] =[]
		enron_table[record[3].lower()].append('enron')
		enron_table[record[3].lower()].append(record[0])
	else:
		other_org_table[record[3].lower()] =[]
		other_org_table[record[3].lower()].append(record[4])
		other_org_table[record[3].lower()].append(record[0])

joblib.dump(enron_table,'enron_table.pkl')
joblib.dump(other_org_table,'other_org_table.pkl')
# We have built the initial tables. Now lets find the colloborators for that organization
"""
org_enron_contact ={}

for org in orgs:
	interest =[]
	count = 0

	for people in enron_table:
		if count >8:
			continue
		try:
			score =model.similarity(org, people)
		except KeyError:
			continue
		if score < 0.5:
			continue
		count +=1
		interest.append([people,score])
	interest=sorted(interest,key=lambda l:l[1], reverse=True)
	org_enron_contact[org] = interest

for org in org_enron_contact:
	print "@@@@@@@@@@@@@@@@@@@@@@"
	print org
	print "----------------------"
	for item in org_enron_contact[org]:
		print item[0]
joblib.dump(org_enron_contact,'org_enron_contact.pkl')
#lets find those people not in enron_table or other_org_table but from the list of all people 'peoples'
# We need to assign these people to organizations, create emails and other information.

"""
print ""




