# This program loads the pickled feature matrix as implmented using the linguistic paper and uses various classifiers to
# to classify as formal and informal. 
#Linguistic Paper : http://journals.linguisticsociety.org/elanguage/lilt/article/download/2844/2844-5756-1-PB.pdf


from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
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
from scipy.sparse import coo_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

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
    classifier= GridSearchCV(estimator=clf, cv=5 ,param_grid=param_grid)
    classifier.fit(X_train, y_train)
    return classifier.cv_results_

def MyExtraTreeClassifier(X_train, y_train):
    clf = ExtraTreesClassifier(min_samples_split=2, random_state=0,max_depth = 10)
    param_grid = {'n_estimators': [10,20,30,50,75,100],'max_depth': [1,5,10,25,50,75,100]}
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
    classifier= GridSearchCV(estimator=linear_svc, cv=5 ,param_grid=param_grid)
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


if __name__ == "__main__":
    feature_matrix = joblib.load('feature_matrix.pkl')
    X = feature_matrix[0]
    y = feature_matrix[1]
    #print X[1:100]
    X_train, X_test, y_train, y_test=train_test_split(X,y ,test_size=0.2, random_state=5677)
    """
    output = MyExtraTreeClassifier(X_train,y_train)
    #print output
    print "Mean Train score"
    print output['mean_train_score']
    print "Mean Test score"
    print output['mean_test_score']
    """
    #clf = ExtraTreesClassifier(min_samples_split=2, random_state=0,max_depth=70,n_estimators=50)
    #clf = DecisionTreeClassifier(min_samples_split=2,random_state=0,max_depth =10)
    clf = RandomForestClassifier(n_estimators =500)
    #clf =svm.SVC(kernel='linear',C=10000)
    clf.fit(X_train, y_train)
    out =clf.predict(X_test)
    print "Accuracy:" +str(accuracy_score(y_test,out))
    print "F1 score: "+str(f1_score(y_test,out, average='macro'))
    print "Percision: " + str(precision_score(y_test,out, average='macro'))
    print "Recall: " +str(recall_score(y_test,out, average='macro'))
    joblib.dump(clf, 'randomforests.pkl')
    #print (X[1:100])
    #print (y[1:100])
