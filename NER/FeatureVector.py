import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from csv import DictReader
import spacy

#nlp = spacy.load('en')

def get_matching_score(str_tokens,word_list):
    freq_count = 0
    for word in str_tokens:
        if word in word_list:
            print("=======" ,word)
            freq_count += 1
    return float(freq_count)/len(str_tokens)

"""def phrasal_verb_recognizer(str):
    doc = nlp(str)
    for sentence in doc.sents:
        parsed = spacy.en.English().parser(sentence)
        print parsed

        for token in parsed :
            if token.dep_ == "prt" and token.head.pos_ == "VERB" :
                verb = token.head.orth_
                particle = token.orth_
                print(verb)
    
    """
def get_word_length_avg(str_tokens):
    average = sum(len(word) for word in str_tokens) / float(len(str_tokens))
    return average

def TTR(str_tokens):
    tokens_set = set(str_tokens)
    return float(len(tokens_set))/len(str_tokens)

# reads the documents
# input: a text file of docs in which each document is in one line of the file
# output: a list of all of the documents in the file
def read_data(file_name):
    with open(file_name) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

# reads formal_informal_wordlist.csv to get a list of formal or informal words (depending on the formality parameter
# we pass to the function
def read_formal_wordlist(formality):
    with open("formal-informal-wordlist.csv") as f:
        word_list = [row[formality].lower() for row in DictReader(f)]
    return set(word_list)

def read_contraction_wordlist():
    with open("contraction-fullform-wordlist.csv") as f:
        contractions_list = [row["Contraction"].lower() for row in DictReader(f)]
    return contractions_list

def read_abbreviation_wordlist():
    with open("abbriviation-fullform-wordlist.csv") as f:
        abbreviations_list = [row["Abbreviations"].lower() for row in DictReader(f)]
    return abbreviations_list




documents = read_data("testData.txt")
formal_list = read_formal_wordlist("formal")
informal_list = read_formal_wordlist("informal")
contractions_list = read_contraction_wordlist()
abbriviations_list = read_abbreviation_wordlist()


str = "tell me about it."
str = str.lower()
str_tokens = str.split()
#str_tokens = word_tokenize(str)
formal_score = get_matching_score(str_tokens,formal_list)
informal_score = get_matching_score(str_tokens,informal_list)
contraction_score = get_matching_score(str_tokens,contractions_list)
abbriviations_score = get_matching_score(str_tokens,abbriviations_list)

vector = [formal_score,informal_score,contraction_score,abbriviations_score,get_word_length_avg(str_tokens),TTR(str_tokens)]

print (vector)
#phrasal_verb_recognizer(str)