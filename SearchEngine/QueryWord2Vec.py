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
from nltk import ngrams
import re
import string
import os

printable = set(string.printable)


api_key ='AIzaSyAXSTt536rRbl4dK4pzuPs-QfuGKTT-YBk'
type_data= ['Corporation','Organization','GovernmentOrganization','EducationalOrganization','LocalBusiness','SportsTeam']
remove_list = []
file_loc = '/Users/Dhanush/Desktop/Enron_Data/Search_engine_pickle/'
org_loc = file_loc +"/Orgs/"




# We are loading the support files for the search Engine here
model = gensim.models.Word2Vec.load(file_loc+'wordvecmodel')
nlp = spacy.load('en')




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
experts_dict        =joblib.load(file_loc+'experts.pkl')
org_enron_contact   =joblib.load(file_loc+'org_enron_contact.pkl') 
enron_table 		=joblib.load(file_loc+'enron_table.pkl') 
other_org_table		=joblib.load(file_loc+'other_org_table.pkl')
SearchEngineWordList=joblib.load(file_loc+'SearchEngineWordList.pkl')
SearchEngineWordList.pop('hughes')
SearchEngineWordList.pop('the')

#lets have a mapping of people to their expertise
people_expertise ={}
for entity in experts_dict:
	for item in experts_dict[entity]:
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



print ("Backend Loaded")








def google_KG_search(word,entity_list):

	service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
	params = {
	'query': word,
	'limit': 3,
	'indent': True,
	'key': api_key,
	}
	detailed_description = ""
	description =" "
	image =""
	url = service_url + '?' + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())
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
						image = element['result']['image']['contentUrl']
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
		return None

	if flag == 0:
		return None

	else:
		#Lets analyze the detailed_description
		text_to_analyze = detailed_description
		token_list = text_to_analyze.split()
		token_list=[x.lower() for x in token_list]
		flag = False
		for token in token_list:
			if token in entity_list:
				flag = True


		if flag:
			return [name,description,detailed_description,url,image]
		else:
			return None


#remove_list = ['Lg Electronics','Sony Interactive Entertainment','Acrobat','Midway Games','The Weather Channel','Frost &Amp; Sullivan','Retired Teachers Of Ontario','Sovereign Military Order Of Malta','Msc Cruises','Toronto Transit Commission','Retired Teachers Of Ontario','Nazi Germany','Downgrade Fitch','Positions Concurrent','Owner Newsreleases','Customerservice 2652935','Controllers Arnold','Ernest','Henry Safety','Carr Futures','Floating Price','Messaging Security','Arealist Tx3','Fte Newsletters','July Crude','Piranha Clinic','Newport News','Resources Human','Super League']




threshold = {'energy' : 0.55,'oil' : 0.75,'utility':0.65,'power' : 0.40,'law': 0.30}

def entity(word):
	vector = model.wv[word]
	list_words =  model.similar_by_vector(vector, topn=300, restrict_vocab=None)
	results = []
	score = 0.55
	if word in threshold:
		score = threshold[word]
	for item in list_words:
		try:

			if (str(item[0]) == word):
				continue
			if (str(item[0])) in exception:
				continue
			if (float(item[1]) > score) and (fetch_type(str(item[0])) == "TOPIC"):
				results.append([str(item[0]),"E"])
			if (float(item[1]) < score) and (fetch_type(str(item[0])) == "TOPIC"):
				results.append([str(item[0]),"I"])
		except UnicodeEncodeError:
			continue
	return results


			


def get_similiar_entity(word):
	vector = model.wv[word]
	list_words =  model.similar_by_vector(vector, topn=300, restrict_vocab=None)
	results = []
	score = 0.55
	if word in threshold:
		score = threshold[word]
	for item in list_words:

		try:
			if (str(item[0]))in exception:
				continue

			if (str(item[0]) == word):
				continue
			if (float(item[1]) > score) and (fetch_type(str(item[0])) == "PERSON"):
				name =str(item[0]).replace(" ", "")
				results.append([str(item[0]), "Expert",fetch_type(str(item[0]))])

			elif (float(item[1]) < score) and (fetch_type(str(item[0])) == "PERSON"):
				name =str(item[0]).replace(" ", "")
				results.append([str(item[0]), " Interest " ,fetch_type(str(item[0]))])

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



def fetch_person_details(person,expert_flag,entity_list):
	person = person.lower()
	type1='PERSON'
	name =person.title()
	organization =""
	email = ""
	if person in enron_table:
		email = enron_table[person][1]
		test =email.split('@')
		test = test[1]
		test = test.split('.')
		if test[0].lower() != 'enron':
			organization = test[0].title()
		else:
			organization = 'Enron Corporation'
		if email == "":
			email_name = person.replace(" ", "")
			email = email_name + '@enron.com'


	elif person in other_org_table:
		organization = other_org_table[person][0].title()
		email = other_org_table[person][1]
	else:
		organization = ''
		email_name = person.replace(" ", "")
		email = ""

	if (expert_flag =='Y') and (organization != 'Enron Corporation'):
		return []
		

	results = entity(person)
	interests =[]
	expertise = []
	if expert_flag =='Y':
		expertise.append(entity_list[0].title())
	for result in results:
		if result[1] == "E":
			if len(expertise) < 3:
				expertise.append(result[0].title())
		if result[1] == "I":
			if len(interests) < 3:
				interests.append(result[0].title())
	if len(interests) == 0:
		if person in people_interest:
			interests = people_interest[person]
		temp =[]
		for interest in interests:
			if interest[0] == 'fraud' or interest[0] == 'internet' or interest[0] == 'commission' or  interest[0] == "frauds":
				continue
			else:
				temp.append(interest[0])
		if len(interests) >3:
			interests = temp[0:3]
		else:
			interests=temp

	temp =[]
	for expert in expertise:
		if expert == 'fraud' or expert == 'internet' or expert == 'commission' or expert == 'frauds':
			continue
		else:
			temp.append(expert)

	expertise = list(set(expertise))
	interests=list(set(interests))
	name = re.sub(' +',' ',name)
	email = email.replace(" ", "")
	return [type1,name,organization,email,expertise,interests]

def fetch_org_details(org,entity):
	
	out = google_KG_search(org,entity)
	url =  ""
	image =""
	name = None
	type1 = None
	description =""
	interests = []
	interests.append(entity[0])
	if out is not None:
		name = out[0]
		type1 = out[1]
		description = out[2]
		url = out[3]
		image = out[4]
		if org in org_interest:
			add =  org_interest[org]
			interests = interests + add
			if len(interests) <2:
				add = find_interest(org)
				if add != None:
					interests = interests + add
		else:
			add = find_interest(org)
			if add != None:
				interests = interests + add


		if name is None:
			Name = org

		if type1 ==None:
			type1 = entity[0] + " Company"

		#Lets write to temp directory so its easier to read the file rather than querying GK again.
		file_name = org_loc + name +".txt"
		os.remove(file_name)
		F = open(file_name,"w") 
		F.write(org+"\n")
		F.write(name+"\n")
		F.write(type1+"\n")
		description = description.encode('utf-8')
		description=filter(lambda x: x in printable, description)
		F.write(description+"\n")
		F.write(url+"\n")
		F.write(" ".join(interests)+"\n")
		F.write(image+"\n")
		F.close()
		return [name,type1,description,url,image,interests]
	else:
		return []




def find_org_entity(entity):
	try:
		results_org=get_similiar_entity(entity.lower())
	except:
		return []
	temp =[]
	for result in results_org:
		if result[2] == 'ORG':
			if result[0] not in exception:
				temp.append(result[0].title())
	return temp	


def fetch_topic_details(entity):
	name = entity.title()
	experts = experts_dict[entity.lower()]
	temp =[]
	temp1 =[]
	for expert in experts:
		if expert[0] in exception:
			continue
		if expert[0] in enron_table:
			temp.append(expert[0].title())
		else:
			temp1.append(expert[0].title())

	experts = temp
	if len(experts) > 6:
		experts = experts[0:5]
	interests= entity_interests[entity.lower()]
	interests = temp1 + interests
	temp = []
	for interest in interests:
		if interest[0] in exception:
			continue
		temp.append(interest[0].title())
	interest = temp

	if len(interests) > 6:
		interests = interests[0:5]
	organization_interested = find_org_entity(entity)
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
	found_org ='N'

	for ent in doc.ents:
		entity_unknown.append(ent.text)



		word = ent.text

		if  (ent.label_ == 'GPE'):
			word = ent.text
			if word in mapping_to_type_dict:
				entity_list.append(word.title())


		if  (ent.label_ == 'ORG'):
			word = ent.text
			if word in mapping_to_type_dict:
				if	mapping_to_type_dict[word.lower()] =='ORG':
					entity_list.append(word.title())
					found_org ='Y'


	if len(entity_list) == 0:

		bigrams = ngrams(text.split(), 2)
		for grams in bigrams:
				word=" ".join(grams)
				if word.lower() in SearchEngineWordList:
					
					if mapping_to_type_dict[word.lower()] =='PERSON':
						entity_searched_type.append("PERSON")
						entity_list.append(word.lower())

					if mapping_to_type_dict[word.lower()] =='ORG':
						entity_searched_type.append("ORG")
						entity_list.append(word.lower())
						found_org ='Y'
					break

	if len(entity_list) == 0:
		bigrams = ngrams(text.split(), 1)
		for grams in bigrams:
				word=" ".join(grams)
				if word.lower() in SearchEngineWordList:

					if mapping_to_type_dict[word.lower()] =='ORG':
						entity_searched_type.append("ORG")
						entity_list.append(word.lower())
						found_org ='Y'
					break


	if len(entity_list) == 0:
		bigrams = ngrams(text.split(), 3)
		for grams in bigrams:
				word=" ".join(grams)
				if word.lower() in SearchEngineWordList:

					if mapping_to_type_dict[word.lower()] =='ORG':
						entity_searched_type.append("ORG")
						entity_list.append(word.lower())
						found_org ='Y'
					break

	if len(entity_list) == 0:
		bigrams = ngrams(text.split(), 4)
		for grams in bigrams:
				word=" ".join(grams)
				if word.lower() in SearchEngineWordList:

					if mapping_to_type_dict[word.lower()] =='ORG':
						entity_searched_type.append("ORG")
						entity_list.append(word.lower())
						found_org ='Y'
					break

	if len(entity_list) == 0:
		bigrams = ngrams(text.split(), 5)
		for grams in bigrams:
				word=" ".join(grams)
				if word.lower() in SearchEngineWordList:

					if mapping_to_type_dict[word.lower()] =='ORG':
						entity_searched_type.append("ORG")
						entity_list.append(word.lower())
						found_org ='Y'
					break




		#Now lets look for the Topic
	if len(entity_list) == 0:
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
	#Now lets do the Word2Vec Queries.
	#double check to see if its a single search

	people_flag = 'N'
	org_flag ='N'
	expert_flag = 'N'
	place_flag = 'N'
	result_topics ='N'
	people_overide =False
	client_override = False
	token_list = query.split()
	token_list=[x.lower() for x in token_list]
	for token in token_list:
		if (token== 'who'):
			people_overide =True
		if (token == 'interest') or  (token == 'interested') or (token=='deals') or (token =='deal')or (token =='interests'):
			people_flag = 'Y'
		if (token =='expert') or (token =='expertise') or (token =='experts'):
			expert_flag = 'Y'
		if (token =='place') or (token =='places') or (token =='location') or (token =='locations'):
			place_flag = 'Y'
		if (token == 'org') or (token =='organization') or (token =='organizations') or (token =='company') or (token =='companies'):
			org_flag ='Y'
		if (token =='topic') or (token =='topics'):
			result_topics ='Y'
		if (token=='from'):
			client_override = True

	if len(restrict) == 0:
		restrict = []
		if len(entity_searched_type) >0:
			if not people_overide:
					if (entity_searched_type[0]== "PERSON") and (people_flag =='Y'):
						restrict.append('TOPIC')
						people_flag='N'

					if (entity_searched_type[0]== "PERSON") and (expert_flag=='Y'):
						restrict.append('TOPIC')
						expert_flag ='N'
					if (entity_searched_type[0]== "ORG") and (people_flag =='Y'):
						restrict.append('TOPIC')
						people_flag='N'

					if (entity_searched_type[0]== "ORG") and (expert_flag=='Y'):
						restrict.append('TOPIC')
						expert_flag ='N'


		if org_flag == 'Y':
			restrict.append('ORG')


		if place_flag =='Y':
			restrict.append('PLACE')


		if people_flag == 'Y':
			restrict.append('PERSON')


	#Write an override for organizations:
	print "ORG_FLAG: " + org_flag
	if org_flag =='Y':
		restrict = ['ORG']

	if len(restrict) == 0:
		restrict =['PERSON','ORG']

	results_query = []
	for items in entity_list:
		if items in SearchEngineWordList:
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
	print "flag is " + expert_flag
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
	if len(filter_result) >20:
			filter_result = filter_result[0:19]


	#Now we fetch more details about our entities and return them.
	More_details =[]

		#Lets issue an over ride if we are looking for people who deals with an organizations.
	#here we are only looking for people from Enron dealing with an organization.
	if len(entity_searched_type) >0:
		if (entity_searched_type[0]== "ORG") and people_flag =='Y':
			temp =[]
			for result in filter_result:
				name = result[0].lower()
				if name in enron_table:
					temp.append(result)

			filter_result = temp
			if len(filter_result) ==0:
				temp =[]
				if entity_list[0] in org_enron_contact:
					temp1 = org_enron_contact[entity_list[0].lower()]
					for item in temp1:
						a= item[0]
						if a in exception:
							continue
						b ='PERSON'
						temp.append([a,b])
					filter_result = temp



	for result in filter_result:
		if result[1] == 'PERSON':
			More_details.append(fetch_person_details(result[0].lower(),expert_flag,entity_list))
		if result[1] == 'ORG':
			More_details.append(fetch_org_details(result[0],entity_list))

		if result[1] == 'TOPIC':
			More_details.append(fetch_topic_details(result[0]))

		if result[1] == 'PLACE':
			More_details.append(fetch_place_details(result[0]))

	if expert_flag =='Y' and len(More_details) == 0:
		results = experts_dict[entity_list[0]]
		for result in results:
			More_details.append(fetch_person_details(result[0],expert_flag,entity_list))
	
	if expert_flag =='N' and len(More_details) == 0 and restrict[0] =='TOPIC':
		results = people_interest[entity_list[0]]
		for result in results:
			if result[0] == 'fraud' or result[0] == 'internet' or result[0] == 'commission' or  result[0] == "frauds":
				continue
			More_details.append(fetch_topic_details(result[0]))

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

# This routine handles the backend for People result page
def PeopleSearch(word):
	pass


"""
# The below routine handles the backend for Organization result page
This returns the Organization results from before, with colloborators from enron and from the organization. Along with interests of Org

"""
def OrgSearch(word):
	file_name = org_loc + word +".txt"
	F = open(file_name, "r").readlines()
	original_name=F[0].split("\n")[0]
	print original_name
	name =F[1].split("\n")[0]
	print name
	type1 =F[2].split("\n")[0]
	print type1
	description=F[3].split("\n")[0]
	print description
	link = F[4].split("\n")[0]
	print link
	interest = F[5].split("\n")[0]
	interest = interest.split(" ")
	interest_orginal = interest
	image = F[6].split("\n")[0]
	print image


	searchword= original_name.lower()
	#We need to get the People from this Organization.
	employees =[]
	find_employees = 'N'
	if searchword in other_org_table:
		employees = other_org_table[searchword]
		if len(employees) == 0:
			find_employees = 'Y'
	else:
		find_employees = 'Y'


	print employees
	
	contact_enron =[]
	find_contact_enron ='N'
	#We need to get the colloborators of this organization from Enron
	if searchword in org_enron_contact:
		contact_enron = org_enron_contact[searchword]
		if len(contact_enron) ==0:
			find_contact_enron ='Y'
	else:
		find_contact_enron ='Y'



	print contact_enron

	additional_interest=[]
	#We need to get more interests of this organizations
	if searchword in org_interest:
		additional_interest = org_interest[searchword]
		results =[]
		if len(additional_interest) !=0:
			
			for entity in additional_interest:
				if entity[0] in exception:
					continue
				else:
					results.append(entity[0])
			if len(results) >3:
				results = results[0:2]
	interest = interest + results


	print interest


	#We need to get the entity cluster map for the organization
	#Lets get the Top interests of the organizations first.
	# We can use direct word2Vec to get this. We are isolating and repeating code not to disturb the existing functionalities
	vector = model.wv[searchword]
	list_words =  model.similar_by_vector(vector, topn=1000, restrict_vocab=None)
	#Lets accumulate people, places and interests of this organization
	accum_employee=[]
	accum_enron_employee =[]
	accum_interests =[]
	accum_places =[]


	for item in list_words:

		try:
			if (str(item[0]))in exception:
				continue

			if (str(item[0]) == word):
				continue

			if (fetch_type(str(item[0])) == "TOPIC"):
				accum_interests.append([item[0].title(),item[1]])

			if (fetch_type(str(item[0])) == "PLACE"):
				accum_places.append([item[0].title(),item[1]])

			if (fetch_type(str(item[0])) == "PERSON"):
				if item[0] == 'hugo chavez':
					continue

				if item[0] in enron_table:
					accum_enron_employee.append([item[0].title(),item[1]])
				else:
					accum_employee.append([item[0].title(),item[1]])
	
		except UnicodeEncodeError:
			continue


	if len(accum_interests) > 3:
		accum_interests = accum_interests[0:3]
	if len(accum_employee) > 5:
		accum_employee = accum_employee[0:4]
	if len(accum_enron_employee) > 5:
		accum_enron_employee = accum_enron_employee[0:4]
	if len(accum_places) > 5:
		accum_places = accum_places[0:4]

	if len(accum_interests) !=0:
		temp_interest = []
		for item in accum_interests:
			temp_interest.append(item[0].title())
		if interest_orginal[0].title() in temp_interest:
			donothing =0
		else:
			temp_interest.insert(0, interest[0])
			accum_interests.insert(0,[interest[0],0.95])
		interest = temp_interest

	if len(accum_employee) !=0:
		temp_employee = []
		for item in accum_employee:
			temp_employee.append(item[0].title())

		employees = temp_employee

	if len(accum_enron_employee) !=0:

		temp_enron_employee =[]
		for item in accum_enron_employee:
			temp_enron_employee.append(item[0].title())

		contact_enron = temp_enron_employee

	places = []
	if len(accum_places) !=0:
		for item in accum_places:
			places.append(item[0].title())
		
	"""
	print "Name of Org"
	print name
	print "type of Org"
	print type1
	print "description of the org"
	print description
	print "Website"
	print link
	print "image Url"
	print image
	print "interests"
	print interest
	print "Employee from the org"
	print employees
	print "Enron colloborators"
	print contact_enron
	print "Places of Interests"
	print places
	"""

	#Lets make the JSON for the Organization cluster Map
	#===================================================
	json = {'name' : name,'employees' :accum_employee, 'colloborators' : accum_enron_employee, 'interests' :accum_interests ,'places': accum_places }


	return [name,type1,description,link,image,interest,employees,contact_enron,places],json



"""
 This routine handles the backend for Topics result page
 returns Topic Name, Similiar Topics List , Organizations dealing with this Topic,people from the organizations interested in that topic
 if any and people in enron dealing with this topics.
 Another Major output is the organizations and those people as a json file along with distance, entities similiar with distance normalized.


"""


def KG_search_for_topic_page(word):
	service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
	params = {
	'query': word,
	'limit': 3,
	'indent': True,
	'key': api_key,
	}
	detailed_description = ""
	description =" "
	image =""
	url = service_url + '?' + urllib.urlencode(params)
	response = json.loads(urllib.urlopen(url).read())
	flag = 0
	name = None
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

						flag = 1

					except KeyError:
						name = None

			if flag ==1:
				break
					

	except KeyError:
		name= None

	return name

def TopicSearch(word):
	searchword = word.lower()
	vector = model.wv[searchword]
	list_words =  model.similar_by_vector(vector, topn=1000, restrict_vocab=None)
	accum_employee=[]
	accum_enron_employee =[]
	accum_interests =[]
	accum_places =[]
	accum_org = []


	for item in list_words:

		try:
			if (str(item[0]))in exception:
				continue

			if (str(item[0]) == word):
				continue

			if (fetch_type(str(item[0])) == "TOPIC"):
				accum_interests.append([item[0].title(),item[1]])

			if (fetch_type(str(item[0])) == "PLACE"):
				accum_places.append([item[0].title(),item[1]])

			if (fetch_type(str(item[0])) == "ORG"):
				accum_org.append([item[0].title(),item[1]]))

			if (fetch_type(str(item[0])) == "PERSON"):

				if item[0] in enron_table:
					accum_enron_employee.append([item[0].title(),item[1]])
				else:
					accum_employee.append([item[0].title(),item[1]])
	
		except UnicodeEncodeError:
			continue


	if len(accum_interests) > 3:
		accum_interests = accum_interests[0:3]
	if len(accum_employee) > 15:
		accum_employee = accum_employee[0:14]
	if len(accum_enron_employee) > 15:
		accum_enron_employee = accum_enron_employee[0:14]
	if len(accum_places) > 10:
		accum_places = accum_places[0:9]

	if len(accum_org) > 5:
		accum_org = accum_org[0:4]

	enron_name = []
	other_name = []
	orgs = []
	places =[]
	similiar_entity = []

	if len(accum_interests) !=0:
		for item in accum_interests:
			similiar_entity.append(item[0].title())

	if len(accum_employee) !=0:
		for item in accum_employee:
			other_name.append(item[0].title())

	if len(accum_enron_employee) !=0:
		for item in accum_enron_employee:
			enron_name.append(item[0].title())

	if len(accum_places) !=0:
		for item in accum_places:
			places.append(item[0].title())



	#We need to leverage the Google Knowledge Graph now to get better results for the Organizations

	output_array = [word.title(),similiar_entity,enron_name,other_name,places,orgs]
	json = {'name' : word.title(),'employees' :accum_employee, 'colloborators' : accum_enron_employee, 'similiarinterests' :accum_interests ,'places': accum_places,'orgs':accum_org}

	return output_array,json

#print GeneralSearch("who is interested in power",[])
#print GeneralSearch("who has expertise in law",[]) # Works and gives good results
#print GeneralSearch("who has interest in utility related topics",[])
#print GeneralSearch("who has expertise in utility related topics",[])
#print GeneralSearch("who is an expert in power",[])
#print GeneralSearch("who has expertise in energy",[])
#print GeneralSearch("what expertise does chakib khelil have",[])
#print GeneralSearch("what expertise does Matt Hughes have",[])
#print GeneralSearch("what are the interests of Steve Bunkin ?",[])
#print GeneralSearch("what are the organizations interested in oil ?",[]) # Works and gives good results
#print GeneralSearch("what does Jeana Mac deals with ?",[]) #Works and good results
#print GeneralSearch("What are the interests of Statoil",[])
#print GeneralSearch("What are the interests of Energy Future Holdings",[])
#print GeneralSearch("What are the interests of Scotiabank",[])
#print GeneralSearch("What are the interests of rbc capital markets",[])
#print GeneralSearch("who are the people who deals with RBC Capital Markets",[])
#print GeneralSearch("who are the people who deals with Statoil",[])
#print GeneralSearch("What are the interests of Jeana Mac",[])
#print GeneralSearch("who are the people Jeana Mac deals with ?",[])
#print GeneralSearch("who are the people from RBC Capital Markets ?",[]) # Need not work, lets not make it too detail.


#Search Result Pages Search
#print OrgSearch("Royal Dutch Shell")





