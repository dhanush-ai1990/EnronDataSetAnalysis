import json
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



def Convert2Dict(list1):
	result = {}
	for item in list1:
		result[item[0]] = item[1]

	return result

file_loc = '/Users/Dhanush/Desktop/Enron_Data/Search_engine_pickle/'
org_loc = file_loc +"/Orgs/"

SearchEngineWordList=joblib.load(file_loc+'SearchEngineWordList.pkl')
SearchEngineWordList.pop('hughes')
SearchEngineWordList.pop('the')

mapping_to_type_dict=joblib.load(file_loc+'mapping_to_type_dict.pkl')

exception =[]
exception_file = open (file_loc+'exception.txt','r')
for line in exception_file:
    line = line.replace('\n','')
    exception.append(line)
exception = list(set(exception)) + ['ECT','Enron']
exception =[element.lower() for element in exception]

Database = sqlite3.connect('/Users/Dhanush/Desktop/Enron_Data/Enron_database.db')
c = Database.cursor()

SQL = "select `EMAIL ID`, FIRST, LAST, `FULL NAME`, ORGANIZATION from `EMPLOYEE`"
c.execute(SQL)
enron_table = {}
other_org_table ={}
for record in c:
	org = record[4].lower()
	if org == 'enron':
		enron_table[record[0].lower()] =[]
		enron_table[record[0].lower()].append(record[3])
	else:
		other_org_table[record[0].lower()] =[]
		other_org_table[record[0].lower()].append(record[3])


with open('/Users/Dhanush/Desktop/temp.json') as json_data:
    d = json.load(json_data)
    nodes =d['nodes']
    edges =d['edges']



count =0
node_list =[]
person_list =[]
for node in nodes:
	if node['caption'] in enron_table:
		word = enron_table[node['caption']][0]
		node_list.append([word.lower(),node['id']])
		person_list.append([node['id'],word.lower()])
		count+=1
	elif node['caption'] in other_org_table:
		word = other_org_table[node['caption']][0]
		node_list.append([word.lower(),node['id']])
		person_list.append([node['id'],word.lower()])
		count+=1
	else:
		continue

node_list = Convert2Dict(node_list)
person_list = Convert2Dict(person_list)
joblib.dump(node_list,'person_node_mapping.pkl')
joblib.dump(person_list,'Node_person_mapping.pkl')







