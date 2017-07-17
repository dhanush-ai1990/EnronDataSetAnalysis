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


model = gensim.models.Word2Vec.load('model')
nlp = spacy.load('en')


print ("Word2Vec and Entity mapping Loaded")
mapping_to_type_dict = {}
interest_expertise =[]

people_dict= joblib.load('/Users/Dhanush/Desktop/Enron_Data/Outputs/Dictionary_Final/People_dictionary.pkl')
place_dict =joblib.load('/Users/Dhanush/Desktop/Enron_Data/Outputs/Entity/Places_datatag.pkl')
org_dict =joblib.load('/Users/Dhanush/Desktop/Enron_Data/Outputs/Entity/ORG_datatag.pkl')

def load_mapping():

	global mapping_to_type_dict
	global interest_expertise
	global people_dict
	global place_dict
	global org_dict
	#Load the selected interest and expertise.

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
	list_words =  model.similar_by_vector(vector, topn=100, restrict_vocab=None)
	results = []
	for item in list_words:

		try:

			if (str(item[0]) == word):
				continue
			if (float(item[1]) > 0.55) and (fetch_type(str(item[0])) == "PERSON"):
				results.append([str(item[0]), " Expert " ,fetch_type(str(item[0]))])

			elif (float(item[1]) < 0.55) and (fetch_type(str(item[0])) == "PERSON"):
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


def identify(query,restrict):

	# In word2Vec model person and topics are lower but org and 


	if query[-1:] == '?':
		query = query[:-1] 

	temp = query.split()

	if len(temp) < 5:
		query = "what are the things in " + query

	query = query.title()





	#Now lets recognize the entities and add them to the list. Most ideal searches will have one entity
	#But multiple entities will results in a combined results. Maximum results cant be greater than 100.
	entity_list = []
	entity_searched_type = []
	text = unicode(query,'utf8')
	doc = nlp(text)
	for ent in doc.ents:

		print ent.text

		if  (ent.label_ == 'PERSON'):
			word = ent.text

			word=word.lower()
			
			entity_list.append(word)
			entity_searched_type.append("PERSON")

		word = ent.text
		if word in mapping_to_type_dict:
			entity_list.append(word.title())


		if  (ent.label_ == 'GPE'):
			word = ent.text
			if word in mapping_to_type_dict:
				entity_list.append(word.title())


		if  (ent.label_ == 'ORG'):
			word = ent.text
			if word in mapping_to_type_dict:
				entity_list.append(word.title())

		#Now lets look for the Topic
	count = 0

	token_list = query.split()
	token_list=[x.lower() for x in token_list]
	for token in token_list:
		if token in interest_expertise:
			entity_list.append(token)
			count +=1
	ENTITY ='YES'
	if count > 1:
		ENTITY='NO'

	#Now lets do the Word2Vec Queries.
	#double check to see if its a single search


	




	print entity_list
	results_query = []
	for items in entity_list:
		try:
			results_query+=(get_similiar_entity(items))
		except KeyError:
			continue


	if len(results_query) == 0:
		return None

	
	#----------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>
	Intermediate_result = results_query



	if len(restrict) ==0:
		return Intermediate_result

	final_result =[]
	for res in restrict:
		for result in Intermediate_result:
			if result[2] == res:
				final_result.append(result)

	return final_result

	


	#Case 2: Who ! return everyone in top 100.
	#Case 3: What + client ! return Topics of that org(if org) else return Topics of that client(person)
	#Case 4: type_of_query = 'C', just a entity ->If person or organization -> Just the person or org. else just an entity results + people + org interested in them.



#print identify("'Jeana Mac",['PLACE'])
print identify("Jeana Mac",['ORG'])

#print get_similiar_entity('tom talley')



