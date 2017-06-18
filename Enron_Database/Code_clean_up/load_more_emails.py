import re

dictionary = {}


def getItem(names):
    for name in names:
        for (pos,item) in enumerate(name):
            yield item

def get_matched(name,emails):
	return_dict = {}

	itembase = getItem(name)
	for i in enumerate(name):
	    element = itembase.next()
	    if len(element) == 4: firstName = element+" "+itembase.next()
	    else: firstName = element
	    element = itembase.next()
	    if len(element) == 4: mName = element+" "+itembase.next()
	    else: mName = element
	    element = itembase.next()
	    if len(element) == 4: lastName = element+" "+itembase.next()
	    else: lastName = element
	    print firstName, mName, lastName

		


def update_global_data(temp_list):
	global dictionary
	name = []
	emails =[]
	"""
	nlp = spacy.load('en')
	doc = nlp(news)
	"""
	for email in temp_list:
		temp=email.split('->')
		#temp[0]= re.sub("[^a-zA-Z0-9@]", " ", temp[0])
		temp[1]= re.sub("[^a-zA-Z0-9@]", " ", temp[1])
		emails.append(temp[0])
		name.append(temp[1])

	mapped_dict = get_matched(name,emails)
	print emails
	print name

	return
f = open('output.txt','r')

email =[]
tag ='******'
count = 0
main = []
for line in f:
	if line[0:6] == tag:
		count+=1
		main.append(email)
		email = []
	else:
		email.append(line)



print len(main)
count = 0
for emails in main:
	temp_list = []
	for i in range(len(emails) -2):
		temp_list.append(emails[i])
	update_global_data(temp_list)
	if count >3:
		break


 