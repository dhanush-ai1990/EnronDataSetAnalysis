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
file_loc = '/Users/Dhanush/Desktop/Enron_Data/Search_engine_pickle/'
def google_KG_search(word):

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

	print response
	flag = 0
	u = 'University'
	try:
		for element in response['itemListElement']:


			description1 = element['result']['@type'] #list
			for e in description1:
				#if e in type_data:
				if True:
					try:
						name = element['result']['name']
						temp = name.split(" ")
						if temp[0] == 'University':
							name = word.title()


					except KeyError:
						name = ""
					try:
						description = element['result']['description']
					except KeyError:
						description =""
				
					try:
						detailed_description = element['result']['detailedDescription']['articleBody']
					except KeyError:
						detailed_description = ""

					try:
						url = element['result']['url']
					except KeyError:
						url =""




					flag = 1
			if flag ==1:
				break
	except KeyError:
		return []

	if flag == 0:
		return None

	else:
		return [name,description,detailed_description,url]


#remove_list = ['Lg Electronics','Sony Interactive Entertainment','Acrobat','Midway Games','The Weather Channel','Frost &Amp; Sullivan','Retired Teachers Of Ontario','Sovereign Military Order Of Malta','Msc Cruises','Toronto Transit Commission','Retired Teachers Of Ontario','Nazi Germany','Downgrade Fitch','Positions Concurrent','Owner Newsreleases','Customerservice 2652935','Controllers Arnold','Ernest','Henry Safety','Carr Futures','Floating Price','Messaging Security','Arealist Tx3','Fte Newsletters','July Crude','Piranha Clinic','Newport News','Resources Human','Super League']

model = gensim.models.Word2Vec.load(file_loc+'wordvecmodel')
nlp = spacy.load('en')


print ("Word2Vec and Entity mapping Loaded")


#Load the file of exception

exception =[]
exception_file = open (file_loc+'exception.txt','r')
for line in exception_file:
    line = line.replace('\n','')
    exception.append(line)
exception = list(set(exception)) + ['ECT','Enron']
exception =[element.lower() for element in exception]
#print exception
#print len(exception)

#Lets load the pickles


mapping_to_type_dict=joblib.load(file_loc+'mapping_to_type_dict.pkl')
people_interest     =joblib.load(file_loc+'people_interest.pkl')
org_interest        =joblib.load(file_loc+'org_interest.pkl')
experts             =joblib.load(file_loc+'experts.pkl')
org_enron_contact   =joblib.load(file_loc+'org_enron_contact.pkl') 
enron_table 		=joblib.load(file_loc+'enron_table.pkl') 
other_org_table		=joblib.load(file_loc+'other_org_table.pkl')
SearchEngineWordList=joblib.load(file_loc+'SearchEngineWordList.pkl')

#lets have a mapping of people to their expertise
people_expertise ={}
for entity in experts:
	for item in experts[entity]:
		if item[0] not in people_expertise:
			people_expertise[item[0]] =[]
			people_expertise[item[0]].append(entity)
		else:
			people_expertise[item[0]].append(entity)

entity_interests ={}

for people in people_interest:
	for item in people_interest[people]:
		if item[0] not in entity_interests:
			entity_interests[item[0]] =[]
			entity_interests[item[0]].append(people)
		else:
			entity_interests[item[0]].append(people)

entity_org ={}
for org in org_interest:
	for item in org_interest[org]:
		if item[0] not in entity_org:
			entity_org[item[0]] =[]
			entity_org[item[0]].append(org)
		else:
			entity_org[item[0]].append(org)









print ("All pickle Loaded")

def get_similiar_entity(word):
	vector = model.wv[word]
	list_words =  model.similar_by_vector(vector, topn=300, restrict_vocab=None)
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


def fetch_type(word):
	global mapping_to_type_dict
	try:
		word = mapping_to_type_dict[word]
	except KeyError:
		return "PERSON"
	return word


def find_org(person):
	try:
		results_org=get_similiar_entity(person)
	except:
		return "Unknown"
	for result in results_org:
		if result[2] == 'ORG':
			return result[0].title()
	return "Unknown"

def find_interest(org):
	try:
		results_org=get_similiar_entity(org)
	except:
		return None
	interest = []
	for result in results_org:
		if result[2] == 'TOPIC':
			interest.append(result[0].title())
	return interest



def fetch_person_details(person):
	person = person.lower()
	type1='PERSON'
	pic_url ='http://1.bp.blogspot.com/-vcxXefp0Yto/Uxi1V1NJKJI/AAAAAAAAAPo/EZcRSGFp52A/s1600/face.jpeg'
	name =person.title()
	organization =""
	email = ""
	if person in enron_table:
		organization = 'Enron Corporation'
		email = enron_table[person][1]

	elif person in other_org_table:
		organization = other_org_table[person].title()
		email = other_org_table[person][1]
	else:
		organization = find_org(person)
		split = organization.split(" ")
		if len(split) < 2:
			email_name = person.replace(" ", "")
			email = email_name +'@'+organization.lower()+'.com'

		else:
			#We create the abbreviation for the email.
			agg =[]
			for word in split:
				agg.append(word[0])
			agg ="".join(agg)
			email_name = person.replace(" ", "")
			email = email_name +'@'+agg.lower()+'.com'



	expertise =[]
	if person in people_expertise:
		expertise = people_expertise[person]
	expertise =[element.title() for element in expertise]
	interests = []
	if person in people_interest:
		interests = people_interest[person]
	temp =[]
	for element in interests:
		temp.append(element[0])

	interests =[element.title() for element in temp]

	return [type1,name,organization,email,expertise,interests,pic_url]

def fetch_org_details(org):
	out = google_KG_search(org,type_data)
	url =  ""
	name = None
	type1 = None
	description =""
	interests = []
	if out is not None:
		name = out[0]
		type1 = out[1]
		description = out[2]
		url = out[3]


	if org in org_interest:
		interests =  org_interest[org]
	else:
		interests = find_interest(org)

	if name is None:
		Name = org

	if type1 ==None:
		type1 = interests[0] + " Company"

	return [name,type1,description,url,interests]




		


def fetch_topic_details(entity):
	name = entity.title()
	experts = experts[entity]
	if len(experts) > 6:
		experts = experts[0:5]
	interests= entity_interests[entity]
	if len(interests) > 6:
		interests = interests[0:5]
	organization_interested = org_interest[entity]
	if len(organization_interested) > 6:
		organization_interested = organization_interested[0:5]
	return [name,experts,interests,organization_interested]

def fetch_place_details(place):
	return [place]

def GeneralSearch(query,restrict):

	# In word2Vec model person and topics are lower but org and 

	global exception
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
		entity_unknown.append(ent.text)

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
	topics = 'N'
	for token in token_list:
		if token in SearchEngineWordList:
			entity_list.append(token)
			count +=1
			topics = 'Y'

	ENTITY ='YES'
	if count > 1:
		ENTITY='NO'
	print "Identified"
	print entity_list

	#We have mostly identified our query by now. All below process includes back up routines to capture
	#the entity being searched

	if len(entity_list) ==0:
		print "Houston! We have a problem :("
		for item in entity_unknown:
			print item
			out= google_KG_search(word,type_data)
			print out
			if out ==None:
				continue
			else:
				entity_list.append(out[0].title())
	



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
				people_flag='N'

			if (entity_searched_type[0]== "PERSON") and (expert_flag=='Y'):
				restrict.append('TOPIC')
				expert_flag = 'N'

		if org_flag == 'Y':
			restrict.append('ORG')
			print "a"

		if place_flag =='Y':
			restrict.append('PLACE')
			print "b"

		if people_flag == 'Y':
			restrict.append('PERSON')
			print "c"



	if len(restrict) == 0:
		restrict =['PERSON','ORG']

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



	
	#Put the routine to call dictionary to get the experts in a Topic, below will be depreciated ! This is put on hold now
	#We can use the expert dictionary if needed.
	if expert_flag =='Y':
		temp_result = []

		for result in Intermediate_result:
			if result[1] == 'Expert':
				temp_result.append(result)

		Intermediate_result = temp_result


	if (restrict is not None) or (len(restrict) > 0):
		final_result =[]
		for res in restrict:
			for result in Intermediate_result:
				if result[2] == res:
					final_result.append(result)
	else:
		final_result = Intermediate_result



	filter_result = []

	for result in final_result:
			name = result[0].lower()
			if name in exception:
				continue
			name = result[0].title()

			filter_result.append([name,result[2]])

	#We need to send only first 50 results.
	if len(filter_result) >50:
			filter_result = filter_result[0:49]


	#Now we fetch more details about our entities and return them.
	More_details =[]
	for result in filter_result:
		if result[1] == 'PERSON':
			More_details.append(fetch_person_details(result[0]))
		if result[1] == 'ORG':
			More_details.append(fetch_org_details(result[0]))

		if result[1] == 'TOPIC':
			More_details.append(fetch_topic_details(result[0]))

		if result[1] == 'PLACE':
			More_details.append(fetch_place_details(result[0]))



	return More_details

	"""
	if restrict[0]== 'PERSON':
		for result in final_result:
			name = result[0].lower()
			if name in exception:
				continue
			name = result[0].title()

			filter_result.append([name,result[3],result[4],result[5],result[1]])
		if len(filter_result) >60:
			filter_result = filter_result[1:40]
		header = ["Name", "Email-ID","Organization","Client","Level of Knowledge"]

		return filter_result,header

	if restrict[0]== 'PLACE':
		for result in final_result:
			name = result[0].lower()
			if name in exception:
				continue
			name = result[0].title()

			filter_result.append([name])
		if len(filter_result) >20:
			filter_result = filter_result[1:20]
		header = ["Place"]
		return filter_result,header

	if restrict[0]== 'ORG':
		for result in final_result:
			name = result[0].lower()
			if name in exception:
				continue
			name = result[0].title()

			filter_result.append([name])
		if len(filter_result) >40:
			filter_result = filter_result[1:40]

		header = ["Organization"]
		return filter_result,header

	if restrict[0]== 'TOPIC':
		for result in final_result:
			name = result[0].lower()
			if name in exception:
				continue
			name = result[0].title()
			filter_result.append([name])
		if len(filter_result) >10:
			filter_result = filter_result[1:10]
		header = ["Topic-Entity"]
		return filter_result,header
	"""
	

print GeneralSearch("who is interested in oil",[])








