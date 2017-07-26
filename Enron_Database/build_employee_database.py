#This program builts the employee Table dictionary which will be used by the search engine and the relationship models

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
api_key ='AIzaSyAXSTt536rRbl4dK4pzuPs-QfuGKTT-YBk'
#dict1 = joblib.load('/Users/Dhanush/Desktop/Enron_Data/pickle/Org.pkl')
type_data= ['Corporation','Organization','GovernmentOrganization']
#print dict1



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
	try:
		response = json.loads(urllib.urlopen(url).read())
	except:
		return None
	flag = 0
	u = 'University'
	out =""
	try:
		for element in response['itemListElement']:
			out = element

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
		return [name,element]

"""
#Lets get the organizations from email domain using google Knowledge Graphs
clearbit.key = 'sk_1573a83a3cdd597a943b7a8cc50b4fcf'
Database = sqlite3.connect('Enron_database.db')
c = Database.cursor()
SQL = "select `EMAIL ID` from `EMPLOYEE`"

c.execute(SQL)
org_list ={}
for record in c:
	org =record[0]
	org = org.split('@')
	if len(org) > 1:
		org = org[1]
	try:
		if org not in org_list:
			org_list[org] = []

	except TypeError:
		continue




total = len(org_list)





organization_KG_mapped ={}
count =1
notfound=0
for record in org_list:

	print ("Processing " + str(count) +" out of " + str(total))
	flag = False
	name = None
	count+=1
	org = record.split('.')
	temp='N'
	if len(org) >2:
		flag = False
		temp ='Y'	
		if org[1] =='com' or org[1] =='net':
			print search
			search =org[0]+"."+org[1]

	else:
		org = org[0]

	if not flag:
		try:
			if temp =='Y':
				company = clearbit.Company.find(domain=search, stream=False)
			else:
				company = clearbit.Company.find(domain=record, stream=False)
		except:
			flag = True

	if not flag:
		if company != None:
			if 'legalName' in company:
				name=company['legalName']
			else:
				name=company['name']
	if not flag:
		if name==None:
			name=record

	if name != None:
		if len(name) > 1:
			organization_KG_mapped[record] = {}
			organization_KG_mapped[record]['name'] = name
			organization_KG_mapped[record]['source'] = "clearbit"
			organization_KG_mapped[record]['json'] = company
		#print (record +" : " + str(organization_KG_mapped[record]['name']))
	else:
		flag = True

	if flag:
		flag = False
		out=google_KG_search(org[0],type_data)
		if out != None:
			name= out[0]
			json = out[1]
			organization_KG_mapped[record] = {}
			organization_KG_mapped[record]['name'] = name
			organization_KG_mapped[record]['source'] = "GK"
			organization_KG_mapped[record]['json'] = json
			print (record +" : " + str(organization_KG_mapped[record]['name']))
		else:
			notfound+=1
			print "NotFound: " + str(record)
joblib.dump(organization_KG_mapped, 'organization_KG_mapped.pkl') 
raise Exception("STOP")
"""
Database = sqlite3.connect('Enron_database.db')
c = Database.cursor()

SQL = "select `EMAIL ID`, FIRST, LAST, `FULL NAME`, ORGANIZATION from `EMPLOYEE`"
c.execute(SQL)


"Processing database"
employee_dict_name = {}
employee_dict_email = {}


for record in c:
	noLastname=False
	if record[1] == '**' and record[2] == '**':
		continue
	if record[2] =='**':
		name = record[1]
	else:
		name = record[3]

	employee_dict_name[name] ={}
	employee_dict_name[name]['email'] = record[0]
	employee_dict_name[name]['org'] = record[4]

	employee_dict_email[record[0]] = {}
	employee_dict_email[record[0]]['name'] = name
	employee_dict_email[record[0]]['org'] = record[4]
print employee_dict_email
print len(employee_dict_email)
joblib.dump(employee_dict_name, 'employee_dict_name.pkl') 
joblib.dump(employee_dict_email, 'employee_dict_email.pkl') 





