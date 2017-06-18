#Create a new database for ENRON dataset.

import sqlite3

Database = sqlite3.connect('Enron_database.db')
c = Database.cursor()
c.execute("DROP TABLE IF EXISTS 'ENRON PRIME'")
c.execute("DROP TABLE IF EXISTS 'EMAIL'")
c.execute("DROP TABLE IF EXISTS 'EMPLOYEE'")
c.execute("DROP TABLE IF EXISTS 'TO'")

SQL = "CREATE TABLE `ENRON PRIME` ('key' INTEGER NOT NULL PRIMARY KEY UNIQUE,'msgid',\
 		'time_stamps','subject','raw_body','full_text','sender_email','sender_first_name',\
 		'sender_last_name','sender_full_name','sender_organization','receiver_email','receiver_first_name',\
 		'receiver_last_name','receiver_full_name','receiver_organization','receiver_TO_OR_CC')"

c.execute(SQL)

# Create Employee Table
SQL ="CREATE TABLE 'EMPLOYEE' ('EMAIL ID' NOT NULL PRIMARY KEY UNIQUE,'FIRST','LAST','FULL NAME','ORGANIZATION','Position' ) "
#Sentiment Score,Intrest, expertise,mailing groups, busy days, stress maps, avg response time,direct/broadcaster,avg emails per day. 
c.execute(SQL)
#Create Receiver table
"""
l = []
for i in range(1,51):
    l.append("'CC_{}'".format(i))

SQL ="CREATE TABLE 'CC' ('EMAIL NO' INTEGER NOT NULL PRIMARY KEY,%s)" %(",".join(l))
c.execute(SQL)
# Create CC table
l = []
for i in range(1,51):
    l.append("'to_{}'".format(i))
SQL ="CREATE TABLE 'TO' ('EMAIL NO' INTEGER NOT NULL PRIMARY KEY,%s)" %(",".join(l))
c.execute(SQL)
"""
SQL = "CREATE TABLE 'EMAIL' ('MSGID' NOT NULL PRIMARY KEY,'sentiment','Formality','Cluster Entity','Named Entity')"
c.execute(SQL)
Database.commit()
Database.close()

