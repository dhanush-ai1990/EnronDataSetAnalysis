from sklearn.externals import joblib
from collections import Counter
import requests
from bs4 import BeautifulSoup
import json
import urllib2
from HTMLParser import HTMLParser


from sklearn.externals import joblib
from collections import Counter
import requests
from bs4 import BeautifulSoup
import json
import urllib2
import urllib
from HTMLParser import HTMLParser

type_data= ['Corporation','Organization','GovernmentOrganization','EducationalOrganization','LocalBusiness','SportsTeam']
place_stop_list =[]
place_file = open ('/Users/Dhanush/Desktop/Enron_Data/org.txt','r')
dict1 = {}
for line in place_file:
	line = line.replace('\n','')
	line = line.replace('\t','')
	line=line.strip()
	line=line.strip()
	line = line.split("-")
	key = line[0]
	key=key.strip()
	key=key.strip()
	key = key.lower()

	name = line[1]
	name = name.strip()
	name=name.strip()
	dict1[key] = name
	place_stop_list.append(line)
api_key ='AIzaSyAXSTt536rRbl4dK4pzuPs-QfuGKTT-YBk'

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
		return []

	else:
		return [name,description,detailed_description]


def check_noise(word):
    caps = sum(1 for c in word if c.isupper())
    word_list = word.split(" ")
    for word in word_list:
        word = word.lower()
        if word in place_stop_list:
            return False 
    return True

data= joblib.load('/Users/Dhanush/Desktop/Enron_Data/pickle/Org.pkl')

data =[element.lower() for element in data]
print (len(data))

counter = Counter(data)

counter_selected = 	counter.most_common(10000)
list_selected = []

res = 0
dictionary_of_places = {}
tag_vs_name = {}
mandatory =['rbcds.com','rbc.com','rbcinvestments.com','rbcdain.com','rbc confirm','rbc capital partners telecom fund','rbc capital markets','rbc capital markets vice']
for i in counter_selected:

	word = i[0].lower()
	word = word.strip()
	word = word.strip()
	word = word.strip()
	word = word.strip()
	if res >2000:
		if word not in mandatory:
			continue

	if word in dict1:
		if dict1[word] not in dictionary_of_places:
			dictionary_of_places[dict1[word]] = {}
			dictionary_of_places[dict1[word]]['name'] = dict1[word]
			dictionary_of_places[dict1[word]]['description'] = ""
			dictionary_of_places[dict1[word]]['detailed'] = ""
			dictionary_of_places[dict1[word]]['tag'] = [i[0]]
			dictionary_of_places[dict1[word]]['count'] = i[1]
		else:
			dictionary_of_places[dict1[word]]['tag'].append(i[0])
			dictionary_of_places[dict1[word]]['count']+= int(i[1])

		tag_vs_name[i[0]] = dict1[word]

		print (dictionary_of_places[dict1[word]]['name'])
	word = i[0]
	out= google_KG_search(word,type_data)
	if len(out) > 0:
		if out[0] not in dictionary_of_places:
			dictionary_of_places[out[0]] = {}
			dictionary_of_places[out[0]]['name'] = out[0]
			dictionary_of_places[out[0]]['description'] = out[1]
			dictionary_of_places[out[0]]['detailed'] = out[2]
			dictionary_of_places[out[0]]['tag'] = [i[0]]
			dictionary_of_places[out[0]]['count'] = i[1]

		else:
			dictionary_of_places[out[0]]['tag'].append(i[0])
			dictionary_of_places[out[0]]['count']+= int(i[1])

		tag_vs_name[i[0]] = out[0]
	res+=1

		#print (dictionary_of_places[out[0]]['name'])
		


print (len(tag_vs_name))

print (len(dictionary_of_places))


dump ='/Users/Dhanush/Desktop/Enron_Data/pickle/'
joblib.dump(dictionary_of_places, dump+'ORG_dictionary.pkl')
joblib.dump(tag_vs_name, dump+'ORG_datatag.pkl')

