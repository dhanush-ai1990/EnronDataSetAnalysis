import sqlite3
import wordcloud
import pandas as pd
# Plotting
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_style('whitegrid')
import nltk
from sklearn.utils import shuffle
from random import shuffle
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
import csv
from nltk.corpus import stopwords
import pickle
import logging
from collections import Counter
import codecs


def wordfreq(text):
    tokens = nltk.tokenize.word_tokenize(text)
    fd = nltk.FreqDist(tokens)
    return fd


def generate_wordcloud(text):
   # freqs = wordfreq(text)
   wc = wordcloud.WordCloud(width=1600,
                             height=800,
                             random_state=5,
                             max_words= 200,
                             stopwords=ENGLISH_STOP_WORDS).process_text(text)
   plt.figure(figsize=(20, 10))
   plt.imshow(wc)
   plt.axis("off")
   plt.savefig('subject-wordcloud.png', dpi=400)
   plt.show()

def write_csv_file(text,csv_file_name):
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    filtered_words = [word.lower().strip() for word in tokens if word.lower().strip() not in stopwords.words('english')]
    filtered_words = [word for word in filtered_words if len(word) >1]
    filtered_words = [word for word in filtered_words if not any(c.isdigit() for c in word)]

    counter = Counter(filtered_words)
    top_words = counter.most_common(200)
  #  dict = wordcloud.WordCloud(width=1600,
  #                         height=800,
  #                         random_state=5,
  #                         max_words=200,
  #                         stopwords=ENGLISH_STOP_WORDS).process_text(text)


    f = open(csv_file_name, "w")
    headers = ['words','freqs']

    writer = csv.writer(f, delimiter=",")
    writer.writerow(headers)

    for word,freq in top_words:
        writer.writerow([word,freq])
    f.close()

def pickle_to_csv(pickle_object_name,csv_file_name):
    with open(pickle_object_name, 'rb') as handle:
        word_list = pickle.load(handle)
    counter = Counter(word_list)
    top_named_entities = counter.most_common(200)
    print top_named_entities

    f = open(csv_file_name, "w")

    writer = csv.writer(f, delimiter=",")
    writer.writerow(['words','freqs'])

    for word,freq in top_named_entities:
        writer.writerow([word,freq])
    f.close()

# logging.basicConfig(filename='wordcloud_subject.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#
# database = sqlite3.connect('/Users/sahba/Downloads/Enron_database_2.db',timeout=5)
#
# emails_df = pd.read_sql_query("SELECT distinct(msgid),subject,raw_body FROM `ENRON PRIME`", database)
#
# subjects = ' '.join(emails_df['subject'])
# bodies = ' '.join(emails_df['raw_body'])
#
# write_csv_file(subjects,'subjects.csv')
# write_csv_file(bodies,'bodies.csv')

#generate_wordcloud(bodies)


#pickle_to_csv('namedEntities/ORG_dictionary.pkl','namedEntities/Org.csv')

with open('namedEntities/ORG_dictionary.pkl', 'rb') as handle:
    word_dict = pickle.load(handle)
f = open('namedEntities/Org.csv', 'w')

writer = csv.writer(f, delimiter=",")
writer.writerow(['words', 'freqs'])

for word, wordmap in word_dict.iteritems():
    count = wordmap['count']
    print word
    print count
    try:
        writer.writerow([word.encode('utf-8'), count])
    except Exception as error:
        print "unable to write"
f.close()
# pickle_to_csv('namedEntities/People.pkl','namedEntities/People.csv')
# pickle_to_csv('namedEntities/Place.pkl','namedEntities/Place.csv')