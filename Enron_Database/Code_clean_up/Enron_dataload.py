# Program : Enron_dataload.py
#This program will build the entire enron database by querying the Enron database in SQL server(raw data),
#structures it, Identify name and domain and builds a clean email text which can be used for further analysis.


import mysql.connector
import sqlite3
from datetime import datetime
import tldextract
import re
from sklearn.externals import joblib
#import cs
import cStringIO


# The below code is inserted as a bug fix where the database load failed because 
# of an error in time stamps. It looks for the already updated messages and prevents the
#same from being processed

D 


# Query the entire Enron tables messages and fetch all message Id's.
message_id_list = []
cnx = mysql.connector.connect(user='root', password='welcome@456',
                              host='127.0.0.1',
                              database='Enron_database')

cursor = cnx.cursor()
SQL = "SELECT mid FROM `Enron_database`.`message` where folder like '%sent%' UNION \
	SELECT mid FROM `Enron_database`.`message` where folder like '%inbox%' "
cursor.execute(SQL)


for row in cursor:
	message_id_list.append(row[0])

cursor.close()

temp_id = []

for message in message_id_list:
	if message not in exists:
		temp_id.append(message)
message_id_list = temp_id

print message_id_list
print ("Total number of emails for processing: ") + str(len(message_id_list))



# Table Enron_Prime 
#The below are field mapping initializations.

key = 253001 # Primary Key


#Email_data
msgid = None
time_stamp =''
subject = ''
raw_body = ''
full_text = ''


#Sender_info
sender_email = ''
sender_first_name =''
sender_last_name =''
sender_full_name =''
sender_organization =''

#receiver info
receiver_email = ''
receiver_first_name =''
receiver_last_name = ''
receiver_full_name =''
receiver_organization =''
receiver_TO_OR_CC =''

data_buffer_cache = []
processed = 1
Database = sqlite3.connect('Enron_database.db')
c = Database.cursor()
count = 0
label = '---**INSERTED INFO ---**'
for msg in message_id_list:
	msgid = msg #Field Fixed
	#query the message database and get all the informations
	cursor = cnx.cursor()
	SQL = "SELECT * FROM `Enron_database`.`message` where mid ='%s'" %(msg)
	cursor.execute(SQL)
	data= cursor.fetchone()
	#lets get the Sender information.
	sender = data[1]
	sender_email =str(sender) #field Fixed
	sender_first_name ="**"
	sender_last_name = "**"
	sender_organization = str(tldextract.extract(sender_email).domain)
	fullname =sender_email.split("@")[0]
	fullname =re.split('[._-]',fullname)
	sender_full_name= fullname #fixed
	sender_first_name = str(fullname[0]) #fixed
	
	if (len(fullname) > 1):
		sender_last_name = str(fullname[1]) #fixed
		
	if (sender_organization =='enron'):
		sender_organization = 'Enron' #fixed

	#By now we have all the available sender information, Lets move that to a Tuples to save it.
	sender_full_name = str(sender_first_name + ' ' + sender_last_name)
	sender_info = (sender_email,sender_first_name,sender_last_name,sender_full_name,sender_organization)
	cursor.close()

	#Build the receiver info by querying the receipient table.
	cursorR = cnx.cursor()
	SQL = "SELECT * FROM Enron_database.recipientinfo where mid ='%s'" %(msg)
	cursorR.execute(SQL)

	receiver_list =[]

	for receiver in cursorR:
		receiver_email = str(receiver[3]) #fixed
		receiver_first_name ='**'
		receiver_last_name = '**'
		receiver_full_name ='**'
		receiver_organization =str(tldextract.extract(receiver_email).domain) #fixed
		fullname =receiver_email.split("@")[0]
		fullname =re.split('[._-]',fullname)
		receiver_full_name = fullname #fixed

		receiver_first_name = str(fullname[0])
		receiver_TO_OR_CC =str(receiver[2]) #fixed
		
		if (len(fullname) > 1):
			receiver_last_name = str(fullname[1]) #fixed
		
		if (receiver_organization =='enron'):
			receiver_organization = 'Enron' #fixed
		receiver_full_name = str(receiver_first_name +' ' + receiver_last_name)
		#We have the receiver info, lets move it into a tuple and finally into a list.
		receiver_info =(receiver_email,receiver_first_name ,receiver_last_name,receiver_full_name,receiver_organization,receiver_TO_OR_CC)
		receiver_list.append(receiver_info)

	cursorR.close()

	#Timestamp, Subject and Body
	time_stamps = data[2]
	try:
		time_stamps = time_stamps.strftime("%Y-%m-%d %H:%M:%S") # fixed
	except ValueError:
		print msgid
		time_stamps =data[2]
	subject =  str(data[4])
	body = str(data[5])
	raw_body = str(body)
	#full_text = []
	# We need to build a Formatted Email Which has expanded Entity such as Names and Organization embedded in each emails
	# Using expanded Entities makes the work of tools like Textacy and Spacy much better

	"""
		---**INSERTED INFO ---**
		DATA TIME FROM TIME STAMP

		FULL NAME OF RECEIVERS, ORGANIZATION, EMAIL

		SUBJECT

		---**INSERTED INFO ---**

		BODY

		---**INSERTED INFO ---**

		FULL NAME OF SENDER, ORGANIZATION,EMAIL

		---**INSERTED INFO ---**

	"""
	output = cStringIO.StringIO()

	output.write(label+'\n')
	output.write(time_stamps+'\n')
	
	for record in receiver_list:
		string = record[0] + str(", ") + record[3] + str(", ") + record[4] +'\n'
		output.write(string)

	subject_string = "SUBJECT: " + subject+'\n'
	output.write(subject_string)
	output.write(label+'\n')
	output.write(body+'\n')
	output.write(label+'\n')
	string = sender_info[0] + str(", ") + sender_info[3] + str(", ") + sender_info[4]+'\n'
	output.write(string)
	output.write(label+'\n')
	full_text = output.getvalue()
	output.close()
	#os.remove("ChangedFile.csv")
	Email_data = (msgid,time_stamps,subject,raw_body,full_text)

	#print key
	#print sender_info
	#print receiver_list
	#print Email_data

	#Now we have all the info we needed. Lets Build the databuffer tuples. These will be inserted as
	#records in the database.
	Total_msg_this_instance = len(receiver_list)
	for record in receiver_list:
		key+=1
		count +=1
		temp =[] # done to fix python error of int not iterable
		temp.append(key)
		buffer_record =  temp +list(Email_data) + list(sender_info) + list(record)
		data_buffer_cache.append(tuple(buffer_record))
		values = ', '.join(map(str, data_buffer_cache))
		data_buffer_cache =[]
		#Insert the buffer into the SQL TABLE

		SQL = "INSERT INTO 'ENRON PRIME' VALUES {}".format(values)
		c.execute(SQL)
		Database.commit()
		processed +=1

		#print ("Processed " + str(processed) +" out of " + str(len(message_id_list))) 
		#print ("Percent completed :" + str(int((float(processed)/len(message_id_list))* 100))

		#print SQL
		if (count == 1000):
			Database.commit()
			count = 0
#print data_buffer_cache[67]


Database.commit()
Database.close()
cursor.close()
cnx.close()



print " "






