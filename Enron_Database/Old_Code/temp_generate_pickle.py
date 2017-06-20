import sqlite3
#from datetime import datetime
#import tldextract
import re
#from sklearn.externals import joblib
#import cs
#import cStringIO
import sqlite3
import json
import pickle

Database = sqlite3.connect('Enron_database.db')
c = Database.cursor()

SQL = "select distinct(msgid), raw_body,subject from `Enron Prime`"
c.execute(SQL)

msgid = []
for data in c:
	msgid.append(str(data[0]))


with open('MsgId','w') as f:
    pickle.dump(msgid,f)