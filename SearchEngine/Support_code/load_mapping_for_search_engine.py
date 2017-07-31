
# This program reads the main email Vs entity mapping. It then creates a main mapped dictionary which should ideally contain 40K entities.

from sklearn.externals import joblib
email_entity_dict = joblib.load('/Users/Dhanush/Desktop/Enron_Data/pickle/Email_Entity_Mapping.pkl')
"""

    email_entity_dict[key]['Names'] = []
    email_entity_dict[key]['Places'] = []
    email_entity_dict[key]['Org'] = []
    email_entity_dict[key]['Entities'] = []
    email_entity_dict[key]['receiver_name'] =[]
    email_entity_dict[MSGID]['sender_Name']


"""




names = []
places =[]
orgs =[]
topics =[]
count =0
for key in email_entity_dict:
	print "processing: " + str(count)
	for name in (email_entity_dict[key]['Names']):
		names.append(name.lower())
	for name in (email_entity_dict[key]['receiver_name']):
		names.append(name.lower())
	try:
		names.append(email_entity_dict[key]['sender_Name'].lower())
	except:
		print "Not found sender_Name"
	for place in (email_entity_dict[key]['Places']):
		places.append(place.lower())
	for org in (email_entity_dict[key]['Org']):
		orgs.append(org.lower())
	for topic in (email_entity_dict[key]['Entities']):
		topics.append(topic.lower())

	count +=1



names = list(set(names))
orgs = list(set(orgs))
places = list(set(places))
topics = list(set(topics))

print 'organization of the petroleum exporting countries' in orgs

print len(names)
print len(orgs)
print len(places)
print len(topics)

mapping_to_type_dict ={}

for people in names:
	mapping_to_type_dict[people] ='PERSON'

for place in places:
	mapping_to_type_dict[place] = 'PLACE'

for org in orgs:
	mapping_to_type_dict[org] = 'ORG'

for topic in topics:
	mapping_to_type_dict[topic] ='TOPIC'

print len(mapping_to_type_dict)
print 'organization of the petroleum exporting countries' in mapping_to_type_dict
joblib.dump(mapping_to_type_dict,'mapping_to_type_dict.pkl')

	
