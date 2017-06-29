import spacy
import os
import email
import pickle
import sqlite3
import re

nlp = spacy.load('en')

Database = sqlite3.connect('/Users/amplify/Downloads/Enron_database_2.db',timeout=10)
c = Database.cursor()

SQL = 'select distinct(msgid), raw_body from `Enron Prime`'
c.execute(SQL)
rows = c.fetchall()

freq_map_org = {}
freq_map_loc = {}

print len(rows)
ORGs = []
Locations = []

for row in rows:
    body = row[1]
    body = re.sub("[^a-zA-Z]", " ", body)
    doc1 = nlp(body)

    for ent in doc1.ents:
        if ent.label_ == 'ORG':
            ORGs.append(ent.text)
            if ent.text in freq_map_org:
                freq_map_org[ent.text] += 1
            else:
                freq_map_org[ent.text] = 1
        if ent.label_ == 'GPE':
            Locations.append(ent.text)
            if ent.text in freq_map_loc:
                freq_map_loc[ent.text] += 1
            else:
                freq_map_loc[ent.text] = 1

ORGs = list(set(ORGs))
Locations = list(set(Locations))

pickle.dump(ORGs, open("orgs.p", "wb"))
pickle.dump(Locations, open("locations.p", "wb"))

pickle.dump(freq_map_org, open("freq_orgs.p", "wb"))
pickle.dump(freq_map_loc, open("freq_locations.p", "wb"))

#
# for subdir, dirs, files in  os.walk(rootdir):
#     if ("inbox" not in subdir) and ("sent" not in subdir):
#         continue;
#     for file in files:
#         file_address = os.path.join(subdir,file)
#         if 'DS_Store' in file_address:
#             continue
#         with open(file_address, "r") as f:
#             data = f.read()
#             msg = email.message_from_string(data)
#             body = msg.get_payload()
#
#             doc1 = nlp(unicode(body,'utf-8'))
#             for ent in doc1.ents:
#                 if ent.label_ == 'ORG':
#                     ORGs.append(ent.text)
#                 if ent.label_ == 'GPE':
#                     Locations.append(ent.text)
