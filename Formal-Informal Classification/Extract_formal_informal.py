# This program is written to extract the Blog and News data and label them as formal and informal.
# The dataset source are two text files. We use 500 characters limit per sample which are delimited by a new line.

import os
import tldextract
import numpy as np
import re
import nltk
import nltk.tokenize
from scipy.sparse import coo_matrix
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from nltk.tokenize import TreebankWordTokenizer
from sklearn.model_selection import cross_val_score
from sklearn.cross_validation import ShuffleSplit
# from sklearn.grid_search import GridSearchCV
from sklearn.learning_curve import learning_curve
from sklearn.model_selection import GridSearchCV
from matplotlib import pyplot as pl
from matplotlib.backends.backend_pdf import PdfPages
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_blobs
import gc
from sklearn import svm
from sklearn.datasets import fetch_20newsgroups
formal_dataset = "/Users/Dhanush/Documents/Deeplearn/generating-reviews-discovering-sentiment/data_formal_informal/en_US.news.txt"
informal_dataset ="/Users/Dhanush/Documents/Deeplearn/generating-reviews-discovering-sentiment/data_formal_informal/en_US.blogs.txt"

# 

def MyRandomForest(X_train, y_train):
	clf = RandomForestClassifier()
	#param_grid = {'n_estimators': [10,20,30,50,70,100,200,500,1000,2000,2500]}
	param_grid = {'n_estimators': [75]}
	classifier= GridSearchCV(estimator=clf, cv=3 ,param_grid=param_grid)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def MyDecisionTree(X_train, y_train):
	clf = DecisionTreeClassifier(min_samples_split=2,random_state=0)
	param_grid = {'max_depth': [1,5,10,25,50,75,100,500]}
	classifier= GridSearchCV(estimator=clf, cv=3 ,param_grid=param_grid)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def MyExtraTreeClassifier(X_train, y_train):
	clf = ExtraTreesClassifier(min_samples_split=2, random_state=0,max_depth = 10)
	param_grid = {'n_estimators': [10,20,30,50]}
	#param_grid = {'max_depth': [1,5,10,25,50,75,100,500,1000,2000]}
	classifier= GridSearchCV(estimator=clf, cv=3 ,param_grid=param_grid)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def MyMultiNomialNB(X_train, y_train):
	clf = MultinomialNB()
	param_grid = {'alpha': [0.000000001,0.00000001,0.0000001,0.0000001] }
	#param_grid = {'alpha': [0.000001] }
	# Ten fold Cross Validation
	classifier= GridSearchCV(estimator=clf, cv=10 ,param_grid=param_grid)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def Mylinear_svm(X_train, y_train):
	linear_svc = svm.SVC(kernel='linear')#,decision_function_shape ='ovo'/'ovr'
	param_grid = {'C': np.logspace(-3, 2, 6)}
	#param_grid = {'C': [ 0.1]}
	classifier= GridSearchCV(estimator=linear_svc, cv=3 ,param_grid=param_grid)
	y_train= np.array(y_train)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def rbf_svm(X_train, y_train):
	rbf_svc = svm.SVC(kernel='rbf')#,max_iter = 10000,cache_size =1024,decision_function_shape ='ovo'/'ovo'
	param_grid = {'C': np.logspace(-3, 2, 6), 'gamma': np.logspace(-3, 2, 6)}
	classifier= GridSearchCV(estimator=rbf_svc, cv=10 ,param_grid=param_grid)
	y_train= np.array(y_train)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_
#Process for formal dataset

formal_data_text_list = []
formal_data_label_list =[]
f = open(formal_dataset,'r')
num_chars = 0
text = []
for line in f:
	num_chars += len(line)
	text.append(line)
	if num_chars > 1000:
		text = "".join(text)
		text = re.sub("[^a-zA-Z]", " ", text) 
		formal_data_text_list.append(text)
		formal_data_label_list.append(0)
		num_chars = 0
		text = []

print (" ")
#print formal_data_text_list[4567]

# Process for Informal dataset

informal_data_text_list = []
informal_data_label_list =[]
f = open(informal_dataset,'r')
num_chars = 0
text = []

for line in f:
	num_chars += len(line)
	text.append(line)
	if num_chars > 1000:
		text = "".join(text)
		text = re.sub("[^a-zA-Z]", " ", text) 
		informal_data_text_list.append(text)
		informal_data_label_list.append(1)
		num_chars = 0
		text = []
#print ("The number of samples for formal data: " + str(len(formal_data_text_list)))
#print ("The number of labels for formal data: " + str(len(formal_data_label_list)))
print ("The number of samples for informal data: " + str(len(informal_data_text_list)))
print ("The number of samples for informal data: " + str(len(informal_data_label_list)))


# Loading the Twenty news group articles

categories = [
        'sci.med',
        'sci.space',
    ]
remove = ('headers', 'footers', 'quotes')

data_train = fetch_20newsgroups(subset='train', categories=categories,
                                shuffle=True, random_state=42,
                                remove=remove)

data_test = fetch_20newsgroups(subset='test', categories=categories,
                               shuffle=True, random_state=42,
                               remove=remove)

print('data loaded')

twent_y_train, y_test = data_train.target, data_test.target
twenty_X_train =data_train.data




# combine and create a common training set. We will use CV and split into train and test later.
Combined_training_data = formal_data_text_list + informal_data_text_list
Combined_training_label = formal_data_label_list +informal_data_label_list

print ("Total training data samples " + str(len(Combined_training_data)))
print ("Total training data labels " + str(len(Combined_training_data)))
# Train Decision Trees.
#cv = CountVectorizer(input ='total_feature_list',stop_words = {'english'},lowercase=True,analyzer ='word',binary =binary,max_features =15000)#,non_negative=True)#,)
#Get the Vocabulary from the file for both formal and informal.
f = open("/Users/Dhanush/Documents/Deeplearn/generating-reviews-discovering-sentiment/Formal_Informal_vocab/temp.txt",'r')
Vocabulary = f.read().split()
Vocabulary = list(set(Vocabulary))
#print (data)

cv = TfidfVectorizer(input ='Combined_training_data',lowercase=True,analyzer ='word',binary =False,min_df = 0.3,max_features =5000)#,non_negative=True)#,)
#cv = TfidfVectorizer(input ='Combined_training_data',lowercase=True,analyzer ='word',binary =False,vocabulary =Vocabulary)#,non_negative=True)#,)
X = cv.fit_transform(Combined_training_data).toarray()
#print ("Total Features used: " +str(len(cv.vocabulary_)))
vocab = np.array(cv.get_feature_names())
y = (np.array(Combined_training_label))
X_train, X_test, y_train, y_test = train_test_split(X,y ,test_size=0.2, random_state=5677)
results_DTC = MyRandomForest(X_train,y_train)
print "Maximum Train accuracy: " 
print results_DTC['mean_train_score']

print "Maximum Test accuracy: " 
print results_DTC['mean_test_score']

#Best performance for random forest at 100 trees, CV accuracy 90% and features 5000 using TDIF


print ""


#Train the most Successful model and pickle both the classifier and the Vectorizer.


cv = TfidfVectorizer(input ='Combined_training_data',lowercase=True,analyzer ='word',binary =False,min_df = 0.3,max_features =5000)#,non_negative=True)#,)
X = cv.fit_transform(Combined_training_data).toarray()
clf = RandomForestClassifier(n_estimators =70)
clf.fit(X_train, y_train)
joblib.dump(clf, 'randomforests.pkl')
joblib.dump(cv, 'tdif.pkl')
