from sklearn.externals import joblib
from collections import Counter
import requests
from bs4 import BeautifulSoup
import json
import urllib2
from HTMLParser import HTMLParser


place_stop_list =[]
place_file = open ('/Users/Dhanush/Desktop/Enron_Data/list_Places.txt','r')
for line in place_file:
    line = line.replace('\n','')
    place_stop_list.append(line)
place_stop_list = list(set(place_stop_list)) + ['ECT','Enron']
place_stop_list =[element.lower() for element in place_stop_list]

def check_noise(word):
    caps = sum(1 for c in word if c.isupper())
    word_list = word.split(" ")
    for word in word_list:
        word = word.lower()
        if word in place_stop_list:
            return False 
    return True



def check_for_babelnet_entry(word):
    #URL = 'http://live.babelnet.org/search?word='+word+'&lang=EN'
    #URL ='http://babelnet.org/search?word='+word+'&lang=EN'
    URL = 'https://babelnet.io/v4/getSenses?word='+word+'&lang=EN&source=WIKI&key=eeb2340a-5060-4770-8a80-cc306222ab31'
    session = requests.session()
    login_response = session.get(URL)
    soup = BeautifulSoup(login_response.text, "html.parser")
    Output=json.loads(str(soup))
    if len(Output) <1:
        return False
    else:
        return True

data= joblib.load('/Users/Dhanush/Desktop/Enron_Data/pickle/place.pkl')
data =[element.lower() for element in data]
print (len(data))

counter = Counter(data)

counter_selected_all = counter.most_common(2000)
counter_selected = 	counter.most_common(880)


list_selected = []
for i in counter_selected_all:

	if i[1] < 25:
		print (count)
		break

	word = i[0]
	word = word.strip()
	word = word.strip()
	if len(word) < 3:
		continue

	if check_for_babelnet_entry(word):
		if check_noise(word):
			list_selected.append(word)





list_all = []
for i in counter_slected_all:
	word = i[0]
	word = word.strip()
	word = word.strip()
	if len(word) < 3:
		continue

	if check_for_babelnet_entry(word):
		if check_noise(word):
			list_all.append(word)

print (len(list_all))
print (len(list_selected))




"""
dump ='/Users/Dhanush/Desktop/Enron_Data/pickle/'
joblib.dump(list_selected, dump+'Place_selected.pkl')
joblib.dump(list_all, dump+'Place_all_final.pkl')
"""