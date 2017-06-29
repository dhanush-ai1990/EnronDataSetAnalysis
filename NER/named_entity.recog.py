#This program is mainly aimed at doing named entity recognition.


#import mysql.connector
import sqlite3
#from datetime import datetime
#import tldextract
import re
#from sklearn.externals import joblib
#import cs
#import cStringIO
import spacy
import nltk
import pickle
from nltk.corpus import stopwords
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.tag import pos_tag
from nltk.tokenize import *
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.tokenize import *
from nltk.tag import pos_tag
from collections import Counter
from spacy.en import English
nlp = spacy.load('en')

Database = sqlite3.connect('/Users/sahba/Downloads/Enron_database_2.db',timeout=10)
c = Database.cursor()

SQL = "select distinct(msgid), raw_body,subject from `Enron Prime`"
#SQL = "select msgid, raw_body, subject from 'Enron Prime' where msgid = 1335"

c.execute(SQL)
file_number = 0
count = 0
parser = English()
temp_org =[]
temp_person = []
temp_place = []
temp_others = []
temp_product = []
proper_nouns =[]
all_nouns =[]
for data in c:
	#file_to_write = file_out + str(file_number) + '.txt'
	#output = open(file_to_write, "w")
	msgid = str(data[0])
	#print msgid
	#print data[1]
	#print "*********************************"
	#print msgid
	subject = re.sub("[^a-zA-Z]", "", data[2]) 
	body =re.sub("[^a-zA-Z]", " ", data[1]) 
	blob = body
	doc = nlp(blob)



	for ent in doc.ents:
		if  (ent.label_ =='ORG'):
			#print(ent.label_, ent.text)
			temp_org.append(ent.text)
		if  (ent.label_ == 'PERSON'):
			temp_person.append(ent.text)

		if  (ent.label_ == 'GPE'):
			temp_place.append(ent.text)


	for sentence in nltk.sent_tokenize(data[1]) :
		parsed = parser(sentence)

		for token in parsed :
			if (token.tag_ == "NNP") or (token.tag_ == "NNPS") :
				all_nouns.append(token.text)
	
		#print np.text
					
	#output.write(msgid+'\n')
	#output.write(subject+'\n')
	#output.write(body+'\n')
	#file_number +=1
	count+=1


	if count % 100 == 0:
		print count
#	if count >500:
#		break
temp_place= list(set(temp_place) & set(all_nouns))
temp_org= list(set(temp_org) & set(all_nouns))
temp_person= list(set(temp_person) & set(all_nouns))

print 'Creating temp_org object: Done'

#=================================================		

words_to_count = (word for word in temp_place if word[:1].isupper())
c = Counter(words_to_count)
places= c.most_common(500)
print places
print "***********************************"


words_to_count = (word for word in temp_org if word[:1].isupper())
c = Counter(words_to_count)
org= c.most_common(500)
print org
print "***********************************"

words_to_count = (word for word in temp_person if word[:1].isupper())
c = Counter(words_to_count)
person= c.most_common(500)
print person
print "***********************************"

print 'before postprocessing'

#print org
orgs_list = set(temp_org)

### filtering the organization_list
orgs_list = [str(x) for x in orgs_list]
orgs_list = [x.replace('=','') for x in orgs_list]
orgs_list = [x.replace('(','') for x in orgs_list]
orgs_list = [x.replace(')','') for x in orgs_list]
orgs_list = [x.replace('<','') for x in orgs_list]
orgs_list = [x.replace('>','') for x in orgs_list]
orgs_list = map(str.strip,orgs_list)
# length is 294616 after removing white spaces

orgs_list = list(set(orgs_list))
filtering_item = []

print orgs_list

for org in orgs_list:
    if any(char.isdigit() for char in org):
        filtering_item.append((org))
        # length is 258010 after removing digits
    elif "@" in org:
        filtering_item.append(org)
        # length is 244233 after removing email addresses
    elif ("#" in org) or ("$" in org) or ("!" in org) or ("*" in org) or ("--" in org) or ("_" in org):
        filtering_item.append(org)
        # length is 223672 after removing special characters
    elif ("http" in org) or ("www" in org):
        filtering_item.append(org)
        #length is 221930 after removing this

print orgs_list

print len(set(orgs_list))
print len(set(filtering_item))

orgs_list = set(orgs_list) - set(filtering_item)
print filtering_item


pickle.dump(orgs_list, open("org_list_Dhanush.p", "wb"))



#print c.most_common(500)

#Now since we have all emails as text, its easier to load them and process using Spacy.

# We will do a word cloud or dictionary first and save that as pickled object.

#trying a new NLTK Entity recognizer.
