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
from collections import Count

model = gensim.models.Word2Vec.load('model_final')
nlp = spacy.load('en')
parser = English()

print "Word2Vec and Entity mapping Loaded"
mapping_to_type_dict = {}

def load_mapping():

	global mapping_to_type_dict
	people_dict= joblib.load('/Users/Dhanush/Desktop/Enron_Data/Outputs/Dictionary_Final/People_dictionary.pkl')
	place_dict =joblib.load('/Users/Dhanush/Desktop/Enron_Data/Outputs/Entity/Places_datatag.pkl')
	org_dict =joblib.load('/Users/Dhanush/Desktop/Enron_Data/Outputs/Entity/ORG_datatag.pkl')
	#Load the selected interest and expertise.
	interest_expertise = []
	in_file = open ('/Users/Dhanush/Desktop/Enron_Data/Outputs/selected_entity.txt','r')
	for line in in_file:
		line = line.replace('\n','')
		interest_expertise.append(line)
		mapping_to_type_dict[line] = 'TOPIC'


	for people in people_dict:
		mapping_to_type_dict[people] ='PERSON'

	for place in place_dict:
		mapping_to_type_dict[place_dict[place]] = 'PLACE'

	for org in org_dict:
		mapping_to_type_dict[org_dict[org]] = 'ORG'
	
load_mapping()


def get_similiar_entity(word):
	vector = model.wv[word]
	list_words =  model.similar_by_vector(vector, topn=50, restrict_vocab=None)
	results = []
	for item in list_words:
		if (str(item[0]) == word):
			continue
		try:
			if (float(item[1]) > 0.6) and (fetch_type(str(item[0])) == "PERSON"):
				results.append([str(item[0]), " Expert " ,fetch_type(str(item[0]))])

			elif (float(item[1]) < 0.60) and (fetch_type(str(item[0])) == "PERSON"):
				results.append([str(item[0]), " Interest " ,fetch_type(str(item[0]))])

			else:
				results.append([str(item[0]), " " ,fetch_type(str(item[0]))])
		except UnicodeEncodeError:
			continue

	return results


def convert(word):

	if word=='1person':
		return "PERSON"

	if word == '2person':
		return "PERSON"

	if word == 'place':
		return "PLACE"

	if word == 'org':
		return "ORG"

	if word == 'topic':
		return "TOPIC"

	raise Exception("Invalid type found. Something wrong with code")


def fetch_type(word):
	global mapping_to_type_dict
	try:
		word = mapping_to_type_dict[word]
	except KeyError:
		return "PERSON"
	return word


def identify(query):
	text = unicode(query,'utf8')


print get_similiar_entity('equity')
