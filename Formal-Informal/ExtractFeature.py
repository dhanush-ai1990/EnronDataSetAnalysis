# -*- coding: utf-8 -*-
import spacy
import nltk
import sys
import csv
import re
from nltk.corpus import stopwords
from nltk.tokenize import *
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.tag import pos_tag
import string as s
import nltk
from spacy.en import English
from csv import DictReader
parser = English()


class ExtractFeature(object):
	def __init__(self,directory =''):
		self._directory = directory
		self.formal_list = self.read_formal_wordlist("formal")
		self.informal_list = self.read_formal_wordlist("informal")
		self.contractions_list = self.read_contraction_wordlist()
		self.abbriviations_list = self.read_abbreviation_wordlist()

	def get_matching_score(self,str_tokens,word_list):
		freq_count = 0
		"""
		for sentence in nltk.sent_tokenize(str_tokens) :
			parsed = parser(sentence)
			for word in parsed:
				print str(word)
				if str(word) in word_list:
		            #print("=======" ,word)
					freq_count += 1
		"""
		parsed = str_tokens.split()
		for word in parsed:
			#print str(word)
			try:
				if word in word_list:
					freq_count += 1
			except UnicodeDecodeError:
				print ('Exception')
		return float(freq_count)/(1+len(parsed))

	def get_word_length_avg(self,str_tokens):
		parsed = str_tokens.split()
		average = sum(len(word) for word in str_tokens) / float(1+len(parsed))
		return average

	def TTR(self,str_tokens):
		parsed = str_tokens.split()
		tokens_set = set(parsed)
		return float(len(tokens_set))/(1+len(parsed)) 

	def phrasal_verb_recognizer(self,newsText) :
		temp = newsText.split()
		phrasal =0
		for sentence in nltk.sent_tokenize(newsText) :

			parsed = parser(sentence)

			for token in parsed :
				if token.dep_ == "prt" and token.head.pos_ == "VERB" :
					verb = token.head.orth_
					phrasal +=1
					particle = token.orth_

		return float(phrasal)/(1+len(temp))

	def active_passive_voice_recognizer(self,newsText) :
		temp = newsText.split()
		active = 0
		passive = 0
		for sentence in nltk.sent_tokenize(newsText) :
			parsed = parser(sentence)

			for token in parsed :
				if token.dep_ == "auxpass" and token.head.pos_ == "VERB" :
					passive+=1
					verb = token.head.orth_
	
					auxillary = token.orth_

			for token in parsed :
				if token.dep_ == "nsubj" and token.head.pos_ == "VERB" :
					verb = token.head.orth_
					nsubject = token.orth_
					active +=1
		passive = float(passive)/(1+len(temp))
		active = float(active)/(1+len(temp))			
		return passive,active


	# reads formal_informal_wordlist.csv to get a list of formal or informal words (depending on the formality parameter
	# we pass to the function
	def read_formal_wordlist(self,formality):
	    with open(self._directory +"formal-informal-wordlist.csv") as f:
	        word_list = [row[formality].lower() for row in DictReader(f)]
	    return set(word_list)

	def read_contraction_wordlist(self):
	    with open(self._directory +"contraction-fullform-wordlist.csv") as f:
	        contractions_list = [row["Contraction"].lower() for row in DictReader(f)]
	    return contractions_list

	def read_abbreviation_wordlist(self):
	    with open(self._directory +"abbriviation-fullform-wordlist.csv") as f:
	        abbreviations_list = [row["Abbreviations"].lower() for row in DictReader(f)]
	    return abbreviations_list


	def process_create_feature(self,str_tokens):

		#documents = read_data("testData.txt")
	
		self.formal_list = self.read_formal_wordlist("formal")
		self.informal_list = self.read_formal_wordlist("informal")
		self.contractions_list = self.read_contraction_wordlist()
		self.abbriviations_list = self.read_abbreviation_wordlist()
		

		#doc = u'Alex posted the video on facebook.  The picture was also posted by Ada. '
		#Feature 1 Formal
		formal_score = self.get_matching_score(str_tokens,self.formal_list)
		#Feature 2 Informal
		informal_score = self.get_matching_score(str_tokens,self.informal_list)
		#Feature 5 Contractions
		contraction_score = self.get_matching_score(str_tokens,self.contractions_list)
		#Feature 6 Abbreviation
		abbriviations_score = self.get_matching_score(str_tokens,self.abbriviations_list)
		#Feature 7 and 8, Active Passive
		passive,active =self.active_passive_voice_recognizer(str_tokens)
		#Feature 9 Phasal Verb
		phrasal = self.phrasal_verb_recognizer(str_tokens)

		#Feature 10 Word Length Average
		word_length_average = self.get_word_length_avg(str_tokens)

		# Feature 11 Type/Token Ratio
		TTR_feature =self.TTR(str_tokens)

		return [formal_score,informal_score,contraction_score,abbriviations_score,passive,active,phrasal,word_length_average,TTR_feature]

if __name__ == "__main__":
	temp = ExtractFeature('/Users/Dhanush/Desktop/EnronDataSetAnalysis/Formal-Informal/ClassificationFeatures/')
	print temp.process_create_feature(u"Tell me about it. You should break up approximately not be doing it. The Systems better were executed. etc. i will do it. can't do it")



