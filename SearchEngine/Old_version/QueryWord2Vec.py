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


api_key ='AIzaSyAXSTt536rRbl4dK4pzuPs-QfuGKTT-YBk'
type_data= ['Corporation','Organization','GovernmentOrganization','EducationalOrganization','LocalBusiness','SportsTeam']
remove_list = []
def google_KG_search(word,type_data):

	service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
	params = {
	'query': word,
	'limit': 3,
	'indent': True,
	'key': api_key,
	}
	detailed_description = ""
	description =" "
	url = service_url + '?' + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())
	flag = 0
	u = 'University'
	try:
		for element in response['itemListElement']:


			description1 = element['result']['@type'] #list
			for e in description1:
				if e in type_data:
					try:
						name = element['result']['name']
						temp = name.split(" ")
						if temp[0] == 'University':
							name = word.title()


					except KeyError:
						return []
					try:
						description = element['result']['description']
					except KeyError:
						return []
					try:
						detailed_description = element['result']['detailedDescription']['articleBody']
					except KeyError:
						return []
					flag = 1
			if flag ==1:
				break
	except KeyError:
		return []

	if flag == 0:
		return None

	else:
		return [name,description,detailed_description]


remove_list = ['Lg Electronics','Sony Interactive Entertainment','Acrobat','Midway Games','The Weather Channel','Frost &Amp; Sullivan','Retired Teachers Of Ontario','Sovereign Military Order Of Malta','Msc Cruises','Toronto Transit Commission','Retired Teachers Of Ontario','Nazi Germany','Downgrade Fitch','Positions Concurrent','Owner Newsreleases','Customerservice 2652935','Controllers Arnold','Ernest','Henry Safety','Carr Futures','Floating Price','Messaging Security','Arealist Tx3','Fte Newsletters','July Crude','Piranha Clinic','Newport News','Resources Human','Super League']

model = gensim.models.Word2Vec.load('wordvecmodel')
nlp = spacy.load('en')


print ("Word2Vec and Entity mapping Loaded")
mapping_to_type_dict = {}
interest_expertise =[]

people_dict= joblib.load('People_dictionary.pkl')
place_dict =joblib.load('Places_datatag.pkl')
org_dict =joblib.load('ORG_datatag.pkl')

def load_mapping():

	global mapping_to_type_dict
	global interest_expertise
	global people_dict
	global place_dict
	global org_dict
	#Load the selected interest and expertise.

	in_file = open ('selected_entity.txt','r')
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
print len(mapping_to_type_dict)

def get_similiar_entity(word):
	vector = model.wv[word]
	list_words =  model.similar_by_vector(vector, topn=100, restrict_vocab=None)
	results = []
	for item in list_words:

		try:

			if (str(item[0]) == word):
				continue
			if (float(item[1]) > 0.55) and (fetch_type(str(item[0])) == "PERSON"):
				name =str(item[0]).replace(" ", "")
				results.append([str(item[0]), "Expert",fetch_type(str(item[0])),name+"@enron.com","Enron","Employee"])

			elif (float(item[1]) < 0.55) and (fetch_type(str(item[0])) == "PERSON"):
				name =str(item[0]).replace(" ", "")
				results.append([str(item[0]), " Interest " ,fetch_type(str(item[0])),name+"@enron.com","Enron","Employee"])

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


def GeneralSearch(query,restrict):

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
	entity_unknown=[]
	for ent in doc.ents:
		print "******************"
		print ent.text
		entity_unknown.append(ent.text)

		if  (ent.label_ == 'PERSON'):
			word = ent.text

			word=word.lower()
			
			entity_list.append(word)
			entity_searched_type.append("PERSON")
			print "1111here"

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

	


	if len(entity_list) ==0:
		for item in entity_unknown:
			print item
			out= google_KG_search(word,type_data)
			print out
			if out ==None:
				continue
			else:
				entity_list.append(out[0].title())
	token_list = query.split()
	token_list=[x.lower() for x in token_list]
	topics = 'N'
	for token in token_list:
		if token in interest_expertise:
			entity_list.append(token)
			count +=1
			topics = 'Y'
	ENTITY ='YES'
	if count > 1:
		ENTITY='NO'
	print "Identified"
	print entity_list
	#Now lets do the Word2Vec Queries.
	#double check to see if its a single search

	people_flag = 'N'
	org_flag ='N'
	expert_flag = 'N'
	place_flag = 'N'
	result_topics ='N'

	token_list = query.split()
	token_list=[x.lower() for x in token_list]
	for token in token_list:
		if (token == 'interest') or  (token == 'interested') or (token=='deals') or (token =='deal'):
			people_flag = 'Y'
		if (token =='expert') or (token =='expertise') or (token =='experts'):
			expert_flag = 'Y'
		print expert_flag
		if (token =='place') or (token =='places') or (token =='location') or (token =='locations'):
			place_flag = 'Y'
		if (token == 'org') or (token =='organization') or (token =='organizations') or (token =='company') or (token =='companies'):
			org_flag =='Y'
		if (token =='topic') or (token =='topics'):
			result_topics ='Y'

	if len(restrict) == 0:
		restrict = []
		if len(entity_searched_type) >0:
			if (entity_searched_type[0]== "PERSON") and (people_flag =='Y'):
				restrict.append('TOPIC')

			if (entity_searched_type[0]== "PERSON") and (expert_flag=='Y'):
				restrict.append('TOPIC')

		if org_flag == 'Y':
			restrict.append('ORG')
			print "a"

		if place_flag =='Y':
			restrict.append('PLACE')
			print "b"

		if people_flag == 'Y':
			restrict.append('PERSON')
			print "c"







	results_query = []
	for items in entity_list:
		try:
			results_query+=(get_similiar_entity(items))
		except KeyError:
			continue


	if len(results_query) == 0:
		return [],[]

	
	#----------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>
	Intermediate_result = results_query



	#Here we need to determine the query automatically if no check boxes are present.
	"""
	put the code here.
	"""

	if len(restrict) == 0:
		restrict.append('PERSON')

	
	if expert_flag =='Y':
		temp_result = []
		for result in Intermediate_result:
			if result[1] == 'Expert':
				temp_result.append(result)

		Intermediate_result = temp_result

	if len(restrict) > 1:
		restrict = [restrict[0]]
	if (restrict is not None) or (len(restrict) > 0):
		final_result =[]
		for res in restrict:
			for result in Intermediate_result:
				if result[2] == res:
					final_result.append(result)
	else:
		final_result = Intermediate_result



	filter_result = []

	if restrict[0]== 'PERSON':
		for result in final_result:
			name = result[0].title()
			if name in remove_list:
				continue
			filter_result.append([name,result[3],result[4],result[5],result[1]])
		header = ["Name", "Email-ID","Organization","Client","Level of Knowledge"]

		return filter_result,header

	if restrict[0]== 'PLACE':
		for result in final_result:
			name = result[0].title()
			if name in remove_list:
				continue
			filter_result.append([name])
		header = ["Place"]
		return filter_result,header

	if restrict[0]== 'ORG':
		for result in final_result:
			name = result[0].title()
			if name in remove_list:
				continue
			filter_result.append([name])
		header = ["Organization"]
		return filter_result,header

	if restrict[0]== 'TOPIC':
		for result in final_result:
			name = result[0].title()
			if name in remove_list:
				continue
			filter_result.append([name])
		header = ["Topic-Entity"]
		return filter_result,header

	










