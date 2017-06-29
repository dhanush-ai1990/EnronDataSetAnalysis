__author__ = 'Sahba'
import os
from email.parser import Parser
import email
import traceback
import pickle
import types
from types import *


def print_map(a,b):
    for i in range(0,min(len(a),len(b))):
        print a[i]+" -> "+b[i]

# returns mapping from email address to the full name for sender of the emails
def get_from_mapping(msg,mapping):
    email_address = msg['From']
    x_from = msg['X-From']

    if '<' in x_from:
        x_from = x_from.split('<')[0]
    if "\"" in x_from:
        x_from = x_from.replace("\"","")
    if ',' in x_from:
        full_name = x_from.split(',')
        first_name = full_name[1].strip()
        if ' ' in first_name:
            first_name = first_name.split(' ')[0]
        last_name = full_name[0]
    else:
        x_from = x_from.strip()
        if ' ' in x_from:
            full_name = x_from.split(' ')
            first_name = full_name[0]
            last_name = full_name[-1]
        else:
            first_name = x_from
            last_name = ""
    full_name = first_name.strip()+" "+last_name.strip()
    full_name = full_name.replace('(E-mail)', '').replace('\\(E-mail\\)', '').replace('email','').replace('e-mail','')
    mapping[email_address] = full_name

def get_to_mapping(to_part, x_to,mapping):
  #  email_address = msg['To']
    email_address = to_part
    if email_address == None:
        return
    email_address = email_address.replace('\r\n','')
    email_address = email_address.replace('\t','')
    email_address = email_address.split(',')
#    x_to = msg['X-To']
    x_to = x_to.replace('\r\n','')
    x_to = x_to.replace('\t','')
    full_names = []

    if '<' in x_to:
        if '>,' in x_to:
            people_list = x_to.split(">,")
        else:
            # if there is only one person in the list
            people_list = [x_to]
        for p in people_list:
            name_str = p.split("<")[0]
            if "\"" in name_str:
                name_str = name_str.replace("\"", "")
            if "," in name_str:
                first_name = name_str.split(",")[1].strip()
                last_name = name_str.split(",")[0].strip()
            else:
                first_name = name_str.strip()
                last_name = ""
            full_name = first_name+" "+last_name
            full_name = full_name.replace('(E-mail)', '').replace('\\(E-mail\\)', '').replace('email','').replace('e-mail','')
            full_names.append(full_name)
    else:
        # if there is no email address in the list
        if "," in x_to:
            people_list = x_to.split(",")
        else:
            people_list = [x_to]
        for p in people_list:
            if "\"" in p:
                p = p.replace("\"", "")
            if ' ' in p:
                full_name = p.split(' ')
                first_name = full_name[0].strip()
                last_name = full_name[-1].strip()
            else:
                first_name = p.strip()
                last_name = ""
            full_name = first_name + " " + last_name
            full_name = full_name.replace('(E-mail)', '').replace('\\(E-mail\\)', '').replace('email','').replace('e-mail','')
            full_names.append(full_name)

    #print '*****************'
    #print len(full_names)
    #print email_address
    #print full_names
    #print len(email_address)
    try:
        for i,val in enumerate(email_address):
            mapping[val.strip()] = full_names[i]
    except:
        print "******"
        print_map(email_address,full_names)
        print len(full_names)
        print(len(email_address))
      #  raise Exception('not working')


rootdir = "/Users/amplify/Downloads/maildir"
email_to_name_mapping = {}

for subdir, dirs, files in  os.walk(rootdir):
    if ("inbox" not in subdir) and ("sent" not in subdir):
        continue;
    for file in files:
        file_address = os.path.join(subdir,file)
        if 'DS_Store' in file_address:
            continue
        with open(file_address, "r") as f:
            data = f.read()
         #   emailData = Parser().parsestr(data)
            msg = email.message_from_string(data)
     #   print("\n From: ", msg['from'])
     #   print("\n X-From: ", msg['X-From'])


        try:
            get_to_mapping(msg['To'],msg['X-To'],email_to_name_mapping)
            get_from_mapping(msg,email_to_name_mapping)
            get_to_mapping(msg['Cc'], msg['X-cc'], email_to_name_mapping)
        except:
            print file_address
            print traceback.print_exc()
            raise Exception('Damn')

print email_to_name_mapping
print len(email_to_name_mapping)

#pickle.dump(email_to_name_mapping, open("mapping.p", "wb"))



#


  #  print msg
  #  print emailData.is_multipart()
  #  for part in msg.walk():
  #      print part.get_content_type()
  #      print part
   #     print '*******'
    #body = msg.get_payload()
    #print body.__len__()

#

#print("\nTo: " , msg['to'])

#print("\n Subject: " , msg['subject'])
#print("\n Date: ",msg['Date'])


#print("\n X-To: ",msg['X-To'])
#body = msg.get_payload()

#doc1 = nlp(unicode(body,'utf-8'))
#for ent in doc1.ents:
#    print ent
