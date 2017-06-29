import os, sys, email,re
import numpy as np
import pandas as pd
# Plotting
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_style('whitegrid')
import wordcloud
import pickle
import glob
# Network analysis
import networkx as nx
import logging

# NLP
from nltk.tokenize.regexp import RegexpTokenizer

from subprocess import check_output

from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.lda import LDA
from sklearn.decomposition import LatentDirichletAllocation

import gensim
from gensim import corpora
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
from nltk.stem.porter import PorterStemmer

def get_text_from_email(msg):
    '''To get the content from email objects'''
    parts = []
    for part in msg.walk():
        if part.get_content_type() == 'text/plain':
            parts.append( part.get_payload() )
    return ''.join(parts)

def split_email_addresses(line):
    '''To separate multiple email addresses'''
    if line:
        addrs = line.split(',')
        addrs = frozenset(map(lambda x: x.strip(), addrs))
    else:
        addrs = None
    return addrs


def clean(text):
    stop = set(stopwords.words('english'))
    stop.update(("to", "cc", "subject", "http", "from", "sent",
                 "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    porter = PorterStemmer()

    text = text.rstrip()
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    stop_free = " ".join([i for i in text.lower().split() if ((i not in stop) and (not i.isdigit()))])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    # stem = " ".join(porter.stem(token) for token in normalized.split())

    return normalized

def generate_lda_input(path_to_corpus):

    emails_df = pd.read_csv(path_to_corpus)

    # Parse the emails into a list email objects
    messages = list(map(email.message_from_string, emails_df['message']))
    emails_df.drop('message', axis=1, inplace=True)
    # Get fields from parsed email objects
    keys = messages[0].keys()
    for key in keys:
        emails_df[key] = [doc[key] for doc in messages]
    # Parse content from emails
    emails_df['content'] = list(map(get_text_from_email, messages))
    # Split multiple email addresses
    emails_df['From'] = emails_df['From'].map(split_email_addresses)
    emails_df['To'] = emails_df['To'].map(split_email_addresses)

    # Extract the root of 'file' as 'user'
    emails_df['user'] = emails_df['file'].map(lambda x:x.split('/')[0])
    del messages

    # Set index and drop columns with two few values
    emails_df = emails_df.set_index('Message-ID')\
        .drop(['file', 'Mime-Version', 'Content-Type', 'Content-Transfer-Encoding'], axis=1)
    # Parse datetime
    emails_df['Date'] = pd.to_datetime(emails_df['Date'], infer_datetime_format=True)
    emails_df.dtypes

    analysis_df=emails_df[['From', 'To', 'Date','content']].dropna().copy()
    analysis_df = analysis_df.loc[analysis_df['To'].map(len) == 1]
    #sub_df=analysis_df.sample(1000)

    text_clean=[]
    for text in analysis_df['content']:
        text_clean.append(clean(text).split())

    print len(text_clean)

    dictionary = corpora.Dictionary(text_clean)
    print len(dictionary)
    text_term_matrix = [dictionary.doc2bow(text) for text in text_clean]

    pickle.dump(text_term_matrix, open("text_term_matrix.p", "wb"))
    pickle.dump(dictionary, open("dictionary.p", "wb"))

def generate_lda_from_txt(path_to_corpus):
    text_clean = []
    files = glob.glob(path_to_corpus)
    for file in files:
        print file
        with open(file) as f:
            text = f.read().splitlines(True)
            text = ' '.join(text[1:])
            text_clean.append(clean(text).split())

    dictionary = corpora.Dictionary(text_clean)
    print len(dictionary)
    text_term_matrix = [dictionary.doc2bow(text) for text in text_clean]

    pickle.dump(text_term_matrix, open("txtdata/text_term_matrix.p", "wb"))
    pickle.dump(dictionary, open("txtdata/dictionary.p", "wb"))

#generate_lda_input('emails.csv')
#generate_lda_from_txt('/Users/sahba/Downloads/Grammar_clean/*.txt')
logging.basicConfig(filename='txtdata/lda_35.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

with open('txtdata/text_term_matrix.p', 'rb') as handle:
    text_term_matrix = pickle.load(handle)
with open('txtdata/dictionary.p', 'rb') as handle:
    dictionary = pickle.load(handle)
print len(text_term_matrix)
print len(dictionary)
num_topics = 35

lda = gensim.models.ldamodel.LdaModel(text_term_matrix, num_topics=num_topics, id2word = dictionary, passes=30 )
lda.save('txtdata/lda_'+str(num_topics)+'.model')

print("*****************************")
print "print topics"


# TODO find doc-topic matrix. this link can be useful: https://stackoverflow.com/questions/25803267/retrieve-topic-word-array-document-topic-array-from-lda-gensim
docTopicProbMat = lda[text_term_matrix]
print("*****************************")
print(len(docTopicProbMat))
print(len(docTopicProbMat[0]))
for row in docTopicProbMat:
    print row

print("*****************************")
k = lda.num_topics
for i in range(0,k):
    print lda.print_topic(i)

