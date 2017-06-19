#Create a new database for ENRON dataset.

import sqlite3

Database = sqlite3.connect('Enron_database.db')
c = Database.cursor()
c.execute("DROP TABLE IF EXISTS 'ENRON PRIME'")
c.execute("DROP TABLE IF EXISTS 'EMPLOYEE'")
c.execute("DROP TABLE IF EXISTS 'RECEIVER'")
c.execute("DROP TABLE IF EXISTS 'CC'")

SQL = "CREATE TABLE `ENRON PRIME` ('EMAIL NO' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,\
 		'sender_email','time_stamps','subject','body','full_email','Folder')"

c.execute(SQL)

# Create Employee Table
SQL ="CREATE TABLE 'EMPLOYEE' ('EMAIL ID' NOT NULL PRIMARY KEY UNIQUE,'FIRST','LAST','FULL NAME','ORGANIZATION','Position' ) "
c.execute(SQL)
#Create Receiver table
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

Database.commit()
Database.close()

