#This program loads the EMPLOYEE TABLE ONLY.

import mysql.connector
import sqlite3
from datetime import datetime
import tldextract
import re
from sklearn.externals import joblib


cnx = mysql.connector.connect(user='root', password='welcome@456',
                              host='127.0.0.1',
                              database='Enron_database')

cursor = cnx.cursor()

cursor.execute("select count(*) from Enron_database.message")

total_emails = cursor.fetchone()


print ("Total number of emails in this Database :%s") %(total_emails)
cursor = cnx.cursor()
sql = "SELECT COUNT(*) FROM `Enron_database`.`message` where folder like '%sent%' "
cursor.execute(sql)
Selected_emails = int(cursor.fetchone()[0])

cursor = cnx.cursor()
sql1="SELECT COUNT(*) FROM `Enron_database`.`message` where folder like '%inbox%'"
cursor.execute(sql1)
Selected_emails+= int(cursor.fetchone()[0])
print ("Total emails from Inbox and Sent :" + str(Selected_emails))

# Call a Union to get both inbox and sent emails from Enron primary Database.
cursor = cnx.cursor(buffered=True)
SQL = "SELECT sender FROM `Enron_database`.`message` where folder like '%sent%' UNION \
	SELECT sender FROM `Enron_database`.`message` where folder like '%inbox%' "
cursor.execute(SQL)
main_emails = []
for row in cursor:
	main_emails.append(row[0])

print len(main_emails)
#print main_emails[1:100]
# Connect to new Database 
#Database = sqlite3.connect('Enron_database.db')
cursor2 = cnx.cursor()
SQL = "SELECT rvalue FROM Enron_database.recipientinfo "
cursor2.execute(SQL)

for record in cursor2:
	main_emails.append(record[0])
print len(main_emails)
main_emails = list(set(main_emails))
print len(main_emails)

joblib.dump(main_emails, 'UniqueEnronEmails.pkl')
cursor.close()
cursor2.close()

Database = sqlite3.connect('Enron_database.db')
# We have all the emails in main_emails. Now lets write into the new database
count =0
exception =0
insertions =0
for email in main_emails:
	count+=1
	if (count %2000 ==0):
		print str(int(float(count)/len(main_emails) *100)) + " Percent Completed"

	cursor3 = cnx.cursor()
	c = Database.cursor()
	SQL = "SELECT * FROM `Enron_database`.`employeelist` Where Email_id = '%s' UNION\
	SELECT * FROM `Enron_database`.`employeelist` Where Email2 = '%s' UNION\
	SELECT * FROM `Enron_database`.`employeelist` Where Email3 = '%s' UNION\
	SELECT * FROM `Enron_database`.`employeelist` Where Email4 = '%s'"\
	%(email,email,email,email)
	cursor3.execute(SQL)
	data= cursor3.fetchone()

	if (data == None):
		email =email
		first ="**"
		last = "**"
		position = "**"
		organization = tldextract.extract(email).domain
		fullname =email.split("@")[0]
		fullname =re.split('[._]',fullname)
		first = fullname[0]
		
		if (len(fullname) > 1):
			last = fullname[1]
		
		if (organization =='enron'):
			organization = 'Enron'
	else:
		first = data[1]
		last = data[2]
		email =data[3]
		organization = 'Enron'
		position = data[8]

	FULLNAME = first + " " + last
	#Check if this key exist in ENRON_database SQLITE.
	#cursor1.close()
	try:
		
		SQL = "INSERT INTO EMPLOYEE('EMAIL ID',FIRST,LAST,'FULL NAME',ORGANIZATION,POSITION)\
			VALUES ('%s','%s','%s','%s','%s','%s')" %(email,first,last,FULLNAME,organization,position)
		c.execute(SQL)
		insertions+=1
	
	except sqlite3.IntegrityError:
		exception+=1

cnx.close()
print "Total Insertions " +str(insertions)
Database.commit()
Database.close()
"""
#Create and update Employee Table
# Note Uncomment only to modify the Employee Table.
exception =0
insertions =0
emails = []
cursor2 = cnx.cursor()
count = 0
for row in cursor:
	count +=1
	if (count%5000 ==0):
		print "processed emails: " +str(count)
	
	email_key = row[0]
	sender = row[1]
	
	SQL = "SELECT * FROM Enron_database.recipientinfo where mid = '%s'" %(row[0])
	
	cursor2.execute(SQL)
	emails.append(sender)
	# Get data for TO and CC Table.
	for record in cursor2:
		emails.append(record[3])


	#emails= list(set(emails))
	#cursor2.close()

	
	for email in emails:
		cursor1 = cnx.cursor()
		c = Database.cursor()
		SQL = "SELECT * FROM `Enron_database`.`employeelist` Where Email_id = '%s' UNION\
		SELECT * FROM `Enron_database`.`employeelist` Where Email2 = '%s' UNION\
		SELECT * FROM `Enron_database`.`employeelist` Where Email3 = '%s' UNION\
		SELECT * FROM `Enron_database`.`employeelist` Where Email4 = '%s'"\
		%(email,email,email,email)
		cursor1.execute(SQL)
		data= cursor1.fetchone()

		if (data == None):
			email = sender
			first ="**"
			last = "**"
			position = "**"
			organization = tldextract.extract(sender).domain
			fullname =email.split("@")[0]
			fullname =re.split('[._]',fullname)
			first = fullname[0]
			
			if (len(fullname) > 1):
				last = fullname[1]
			
			if (organization =='enron'):
				organization = 'Enron'
		else:
			first = data[1]
			last = data[2]
			email =data[3]
			organization = 'Enron'
			position = data[8]

		FULLNAME = first + " " + last
		#Check if this key exist in ENRON_database SQLITE.
		cursor1.close()
		try:
			
			SQL = "INSERT INTO EMPLOYEE('EMAIL ID',FIRST,LAST,'FULL NAME',ORGANIZATION,POSITION)\
				VALUES ('%s','%s','%s','%s','%s','%s')" %(email,first,last,FULLNAME,organization,position)
			c.execute(SQL)
			insertions+=1
		
		except sqlite3.IntegrityError:
			exception+=1
	
"""		
#Database.commit()
#Database.close()
#cursor.close()
#cnx.close()
"""
print emails[1:20]
print "Total number of emails: " +str(len(emails))

emails = list(set(emails))
print "Total number of Unique email ID: " +str(len(emails))
joblib.dump(emails, 'UniqueEnronEmails.pkl')
#print "Total number of Insertions into Employee Table is : " + str(insertions)
"""