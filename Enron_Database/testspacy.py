import spacy
import nltk
from nltk.corpus import stopwords
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.tag import pos_tag
from nltk.tokenize import *
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.corpus import stopwords
from nltk.tokenize import *
from nltk.tag import pos_tag
from collections import Counter
from spacy.en import English

temp_org =[]
temp_person = []
temp_place = []
temp_others = []
temp_product = []
proper_nouns =[]
all_nouns =[]
corrected_text =[]
all_words = []


text = u'India Dabhol Creditors: Mtg In Singapore "Productive"Dow Jones Energy Service, 02/22/2002  Jeb Bush Had Profit on Enron UnitThe Washington Post, 02/22/2002  Enron unit investment made a profit for Jeb Bush                                                                                                 Houston Chronicle, 02/22/2002Enron has deal to sell wind unit / GE purchasing one of the largest assets left Houston Chronicle, 02/21/2002'  

nlp = spacy.load('en')
parser = English()

doc = nlp(text)
for ent in doc.ents:
    if  (ent.label_ =='ORG'):
        print ("Org: " + ent.text)
    if  (ent.label_ == 'PERSON'):
        print ("Person: " + ent.text)
    if  (ent.label_ == 'GPE'):
        print ("Place " + ent.text)



for sentence in nltk.sent_tokenize(text) :
    parsed = parser(sentence)
    for token in parsed :
		if (token.tag_ == "NNP") or (token.tag_ == "NNPS"):
			print ("parser output: " + str(token.text))