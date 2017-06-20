# This program Reads the primary Enron Database and moves information to the custom database which
# will be used for all AI and GUI purposes. We will retain only important information in the new database
# also will add fields such as sentiment analysis etc.

# Note this is a real messy code. No time to rewrite into functions here :(
import mysql.connector
import sqlite3
from datetime import datetime
import tldextract
import re

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")


def create_full_email(email_key,sender,body,time_stamps,recipient,cursor3):
	c = Database.cursor()
	full_email = []
	recipient_info = []
	for email in recipient:
 		SQL = "SELECT 'FULL NAME', 'ORGANIZATION' FROM EMPLOYEE where 'EMAIL ID' = '%s' " %(email)
 		c.execute(SQL)
 		print SQL
 		print c.fetchall()
 		# If the recipient info is not in the Employee Table, update the information to the Employee Table.
 		if len(c.fetchall()) < 1:
 			cursor1 = cnx.cursor()
			SQL = "SELECT * FROM `Enron_database`.`employeelist` Where Email_id = '%s' UNION\
			SELECT * FROM `Enron_database`.`employeelist` Where Email2 = '%s' UNION\
			SELECT * FROM `Enron_database`.`employeelist` Where Email3 = '%s' UNION\
			SELECT * FROM `Enron_database`.`employeelist` Where Email4 = '%s'"\
			%(sender,sender,sender,sender)
			cursor1.execute(SQL)
			data= cursor1.fetchone()

	full_email = " ".join(full_email)
	return full_email

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

for row in cursor:
	c = Database.cursor()
	email_key = row[0]
	sender = row[1]
	cursor1 = cnx.cursor()
	SQL = "SELECT * FROM `Enron_database`.`employeelist` Where Email_id = '%s' UNION\
	SELECT * FROM `Enron_database`.`employeelist` Where Email2 = '%s' UNION\
	SELECT * FROM `Enron_database`.`employeelist` Where Email3 = '%s' UNION\
	SELECT * FROM `Enron_database`.`employeelist` Where Email4 = '%s'"\
	%(sender,sender,sender,sender)
	cursor1.execute(SQL)
	data= cursor1.fetchone()
	flag = cursor1.fetchall()
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
		print (len(flag))
		first = data[1]
		last = data[2]
		email =data[3]
		organization = 'Enron'
		position = data[8]

	FULLNAME = first + " " + last
	#Check if this key exist in ENRON_database SQLITE.

	try:
		
		SQL = "INSERT INTO EMPLOYEE('EMAIL ID',FIRST,LAST,'FULL NAME',ORGANIZATION,POSITION)\
			VALUES ('%s','%s','%s','%s','%s','%s')" %(email,first,last,FULLNAME,organization,position)
		c.execute(SQL)
	
	except sqlite3.IntegrityError:
		pass
Database.commit()
"""

# Declare the place holder for new TABLE
# Table : ENRON PRIME
EMAIL_NO = 0
sender = ''
time_stamps = ''
subject = ''
body =''
full_email =''
folder = ''
#TABLE = EMPLOYEE

for row in cursor:
	if EMAIL_NO >50:
		break
	#row[0] = primary key with message id.
	#Query the Receiver table
	SQL = "SELECT * FROM Enron_database.recipientinfo where mid = '%s'" %(row[0])
	cursor2 = cnx.cursor()
	cursor2.execute(SQL)
	recipients = []
	CC =[]
	TO = []

	# Get data for TO and CC Table.
	for record in cursor2:
		recipients.append(record[3])
		if (record[2] == 'TO'):
			TO.append(record[3])
		if ((record[2]=='CC') or (record[2]=='BCC')):
			CC.append(record[3])

	recipients= list(set(recipients))
	TO = list(set(TO))
	CC = list(set(CC))
	print "========================================================="

	#Now we have all the recipient info
	email_key = row[0]
	sender = row[1]
	time_stamps = row[2]
	time_stamps = time_stamps.strftime("%Y-%m-%d %H:%M:%S")
	message_id = row[3]
	subject =  row[4]
	body = row[5]
	full_email = []

	# Here we create the full body for the emails
	c = Database.cursor()
	full_email = []
	recipient_info = []
	for email in recipient:
 		SQL = "SELECT 'FULL NAME', 'ORGANIZATION' FROM EMPLOYEE where 'EMAIL ID' = '%s' " %(email)
 		c.execute(SQL)
 		print c.fetchall()
 		# If the recipient info is not in the Employee Table, update the information to the Employee Table.
 		if len(c.fetchall()) < 1:
 			cursor3 = cnx.cursor()
			SQL = "SELECT * FROM `Enron_database`.`employeelist` Where Email_id = '%s' UNION\
			SELECT * FROM `Enron_database`.`employeelist` Where Email2 = '%s' UNION\
			SELECT * FROM `Enron_database`.`employeelist` Where Email3 = '%s' UNION\
			SELECT * FROM `Enron_database`.`employeelist` Where Email4 = '%s'"\
			%(sender,sender,sender,sender)
			cursor3.execute(SQL)
			data= cursor3.fetchone()

	full_email = " ".join(full_email) 


	#folder = find_folder(row[6])

	# INSERT INTO ENRON_PRIME

	# INSERT INTO RECEIVER AND CC TABLES
	EMAIL_NO+=1
"""
Database.close()
cursor.close()
cnx.close()





