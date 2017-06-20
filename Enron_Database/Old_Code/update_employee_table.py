#Fill in the Missing information in the Employee Table by loading the information from the mined Pickle object.
from sklearn.externals import joblib

name_email_dict = joblib.load('Mapping.p') 

print type(name_email_dict)
list1 = name_email_dict.keys()
print list1[2]

print name_email_dict['scott.wohlander@enron.com']