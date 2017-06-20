#Update the Receiver and CC table.

import mysql.connector
import sqlite3
from datetime import datetime
import tldextract
import re
from sklearn.externals import joblib


cnx = mysql.connector.connect(user='root', password='welcome@456',
                              host='127.0.0.1',
                              database='Enron_database')

#cursor = cnx.cursor()
cursor = cnx.cursor(buffered=True)
SQL = "SELECT mid FROM `Enron_database`.`message` where folder like '%sent%' UNION \
	SELECT mid FROM `Enron_database`.`message` where folder like '%inbox%' "
cursor.execute(SQL)
enron_TO_dict ={}
enron_CC_dict ={}

count =0
for row in cursor:
	count +=1
	if row[0] not in enron_TO_dict:
		enron_TO_dict[row[0]] = []
		enron_CC_dict[row[0]] = []
cursor.close() 
# Now we have all the message ID's in the list. We need to query the receiver table and get the 

#Use a new cursor to query the entire receipient table.

cursor1 = cnx.cursor(buffered=True)
SQL = "SELECT mid,rtype,rvalue FROM Enron_database.recipientinfo "
cursor1.execute(SQL)
for row in cursor1:
	if row[0] not in enron_TO_dict:
		continue
	if ((row[1] == 'BCC') or (row[1] == 'CC')):
		enron_CC_dict[row[0]].append(row[2])
	if (row[1] == 'TO'):
		enron_TO_dict[row[0]].append(row[2])

cursor1.close()
cnx.close()

print "Total messages in Inbox and sent: " + str(count)
print "total CC messages keys" +str(len(enron_CC_dict))
print "Total TO messages keys" +str(len(enron_TO_dict))

# Once we have the data in python dictionaries, we can use them to update to the database

Database = sqlite3.connect('Enron_database.db')
c = Database.cursor()


Message_keys = enron_TO_dict.keys()

count = 0
for key in Message_keys:
	if count >5:
		break
	values = []
	values.append(key)
	values = values + enron_TO_dict[key]
	values = tuple(values)
	print values
	count +=1




Database.commit()
Database.close()





