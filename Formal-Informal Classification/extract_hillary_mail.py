#!/usr/bin/python
# -*- coding: utf-8 -*-

# code to create test data for Formal and Informal.
import sqlite3 as lite
import sys
import re

con = None

try:
    con = lite.connect('/Users/Dhanush/Downloads/hillary-clinton-emails/database.sqlite')
    cur = con.cursor() 
    cur.execute('SELECT ExtractedBodyText from Emails ')
    data = cur.fetchall()
    #print "SQLite version: %s" % data  


except lite.Error, e:
    
    print "Error %s:" % e.args[0]
    sys.exit(1)
    
finally:
    
    if con:
        con.close()
informal_text = []
c= 0
num_chars = 0
print data[51]
for text in data:

	text = re.sub("[^a-zA-Z]", " ", text[0]) 
	num_chars += len(text)
	if (num_chars < 200) or (num_chars > 1000):
		num_chars = 0
		continue
	num_chars = 0
	c +=1
	if c > 100:
		break
	informal_text.append(text)

print "--------------------------------------------------"
