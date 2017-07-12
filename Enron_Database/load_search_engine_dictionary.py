#This program reads the dictionary of named entities and updated the final database of entities which will be used in our search Engine.

# The imports for the program

import random
from sklearn.externals import joblib

# Initial values

scores = [0.1,0.2,0.3,0.4, 0.8]

#Step 1 : Load the saved Pickle Object


path = '/Users/Dhanush/Desktop/Enron_Data/pickle/Email_Entity_Mapping.pkl'
email_entity_dict = joblib.load(path)


#Built the people vs Entity Table


#----- The data needs to be in Below format 

#FIELD 1 : Count       : KEY
#FIELD 2 : Person
#FIELD 3 : Organization
#FIELD 4 : Entity
#FIELD 5 : Interestorexpertise
#FIELD 6 : Type
# Lets built a 2d matrix to updated 

peoplevsentity = []


# We will need to query the employee table to get the org. If not found assign a random one from Org in the email.

keys = email_entity_dict.keys()


# Make an output Dictionary to map and remove duplicates and to aggregate scores,

person_dict = {}
for key in keys:
	people = email_entity_dict[key]['Names']  # List
	place = email_entity_dict[key]['Places']  # List
	org = email_entity_dict[key]['Org']  # List
	Interestorexpertise = email_entity_dict[key]['Entities']  # List
	receiver_name = email_entity_dict[key]['receiver_name']  # List
	interest_expertise_score = random.choice(scores)
	try:
		sender_name = email_entity_dict[key]['sender_Name']	#One entry
	except KeyError:
		continue

	if sender_name  not in person_dict:

		person_dict[sender_name] ={}
		person_dict[sender_name]['name'] = sender_name
		#person_dict[sender_name]['org'] = fetchorgfromtable(sender_name)
		person_dict[sender_name]['org'] = 'Enron'
		person_dict[sender_name]['Entity'] = []
		person_dict[sender_name]['Emailcount'] = 1
		person_dict[sender_name]['type'] = []
		person_dict[sender_name]['entityscore'] = []

		for ent in receiver_name:
			person_dict[sender_name]['Entity'].append(ent)
			person_dict[sender_name]['type'].append('1person')
			person_dict[sender_name]['entityscore'].append(interest_expertise_score)
		for ent in people:
			person_dict[sender_name]['Entity'].append(ent)
			person_dict[sender_name]['type'].append('2person')
			person_dict[sender_name]['entityscore'].append(interest_expertise_score)

		for ent in place:
			person_dict[sender_name]['Entity'].append(ent)
			person_dict[sender_name]['type'].append('place')
			person_dict[sender_name]['entityscore'].append(interest_expertise_score)

		for ent in org:
			person_dict[sender_name]['Entity'].append(ent)
			person_dict[sender_name]['type'].append('org')
			person_dict[sender_name]['entityscore'].append(interest_expertise_score)

		for ent in Interestorexpertise:
			person_dict[sender_name]['Entity'].append(ent)
			person_dict[sender_name]['type'].append('topic')
			person_dict[sender_name]['entityscore'].append(interest_expertise_score)

	else:
		person_dict[sender_name]['Emailcount'] +=1

		for ent in receiver_name:
			person_dict[sender_name]['Entity'].append(ent)
			person_dict[sender_name]['type'].append('1person')
			person_dict[sender_name]['entityscore'].append(interest_expertise_score)

		for ent in people:
			person_dict[sender_name]['Entity'].append(ent)
			person_dict[sender_name]['type'].append('2person')
			person_dict[sender_name]['entityscore'].append(interest_expertise_score)

		for ent in place:
			person_dict[sender_name]['Entity'].append(ent)
			person_dict[sender_name]['type'].append('place')
			person_dict[sender_name]['entityscore'].append(interest_expertise_score)

		for ent in org:
			person_dict[sender_name]['Entity'].append(ent)
			person_dict[sender_name]['type'].append('org')
			person_dict[sender_name]['entityscore'].append(interest_expertise_score)

		for ent in Interestorexpertise:
			person_dict[sender_name]['Entity'].append(ent)
			person_dict[sender_name]['type'].append('topic')
			person_dict[sender_name]['entityscore'].append(interest_expertise_score)


#By now you have processed all the emails.

"""
length = 0
emailcount=0
for key in person_dict:
	if person_dict[key]['Emailcount'] < 6:
		continue
	length+=1
	emailcount += person_dict[key]['Emailcount']
	print person_dict[key]['Emailcount']



print length
avg = emailcount/length

print avg
"""

DICT_FOR_DATABASE_UPD ={}
for key in person_dict:
	count = person_dict[key]['Emailcount']
	unique_entity = list(set(person_dict[key]['Entity']))
	temp_entity = {}




	for i in range(len((person_dict[key]['Entity']))):
		if person_dict[key]['Entity'][i] not in temp_entity:
			temp_entity[person_dict[key]['Entity'][i]] =[person_dict[key]['type'][i],person_dict[key]['entityscore'][i]]

		else:
			temp_entity[person_dict[key]['Entity'][i]][1] = temp_entity[person_dict[key]['Entity'][i]][1] + person_dict[key]['entityscore'][i]


	#Now Normalize

	Entity = []
	types =[]
	scores = []
	for item in temp_entity:
		Entity.append(item)
		types.append(temp_entity[item][0])
		temp_entity[item][1] = temp_entity[item][1]/count
		scores.append(temp_entity[item][1])


	#Now we have Person Entity and scores

	# Skip the ones who has sent less than 6 emails.
	if person_dict[key]['Emailcount'] < 6:
		continue

	
	DICT_FOR_DATABASE_UPD[key] = {}
	DICT_FOR_DATABASE_UPD[key]['name']=person_dict[key]['name']
	DICT_FOR_DATABASE_UPD[key]['org']=person_dict[sender_name]['org']
	DICT_FOR_DATABASE_UPD[key]['entity'] = Entity
	DICT_FOR_DATABASE_UPD[key]['type'] = types
	DICT_FOR_DATABASE_UPD[key]['scores'] = scores
	DICT_FOR_DATABASE_UPD[key]['count'] = person_dict[key]['Emailcount']


	print "************************************"

	print (DICT_FOR_DATABASE_UPD[key])


joblib.dump(DICT_FOR_DATABASE_UPD,'Enron_dict.pkl')


	#Now lets get back the original dictionary after removing duplicates.

















