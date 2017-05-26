#This program loads the EMPLOYEE TABLE ONLY.

import mysql.connector
import sqlite3
from datetime import datetime
import tldextract
import re


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
SQL = "SELECT * FROM `Enron_database`.`message` where folder like '%sent%' UNION \
	SELECT * FROM `Enron_database`.`message` where folder like '%inbox%' "
cursor.execute(SQL)


# Connect to new Database 
Database = sqlite3.connect('Enron_database.db')


#Create and update Employee Table
# Note Uncomment only to modify the Employee Table.
exception =0
insertions =0
for row in cursor:
	email_key = row[0]
	sender = row[1]
	emails = []
	SQL = "SELECT * FROM Enron_database.recipientinfo where mid = '%s'" %(row[0])
	cursor2 = cnx.cursor()
	cursor2.execute(SQL)
	emails.append(sender)
	# Get data for TO and CC Table.
	for record in cursor2:
		emails.append(record[3])

	emails= list(set(emails))
	cursor2.close()
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
		
Database.commit()
Database.close()
cursor.close()
cnx.close()

print "Total number of Insertions into Employee Table is : " + str(insertions)