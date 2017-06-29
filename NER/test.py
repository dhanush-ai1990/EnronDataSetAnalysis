import pickle
import re

with open('orgs.p','rb') as handle:
    orgs_list = pickle.load(handle)
# prints 298083
print len(orgs_list)
with open('locations.p','rb') as handle:
    locations_list = pickle.load(handle)

#[x.encode('UTF8') for x in orgs_list]
orgs_list = [str(x) for x in orgs_list]
orgs_list = [x.replace('=','') for x in orgs_list]
orgs_list = [x.replace('(','') for x in orgs_list]
orgs_list = [x.replace(')','') for x in orgs_list]
orgs_list = [x.replace('<','') for x in orgs_list]
orgs_list = [x.replace('>','') for x in orgs_list]
orgs_list = map(str.strip,orgs_list)
# length is 294616 after removing white spaces

orgs_list = list(set(orgs_list))
filtering_item = []

for org in orgs_list:
    if any(char.isdigit() for char in org):
        filtering_item.append((org))
        # length is 258010 after removing digits
    elif "@" in org:
        filtering_item.append(org)
        # length is 244233 after removing email addresses
    elif ("#" in org) or ("$" in org) or ("!" in org) or ("*" in org) or ("--" in org) or ("_" in org):
        filtering_item.append(org)
        # length is 223672 after removing special characters
    elif ("http" in org) or ("www" in org):
        filtering_item.append(org)
        #length is 221930 after removing this

orgs_list = set(orgs_list) - set(filtering_item)
print len(orgs_list)

pickle.dump(orgs_list, open("org_list_v2.p", "wb"))
