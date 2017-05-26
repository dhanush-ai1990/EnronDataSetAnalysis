# -*- coding: utf-8 -*-
import nltk
import sys
import csv
import re
from nltk.corpus import stopwords
from nltk.tokenize import *
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
from nltk.tag import pos_tag
import string as st
#nltk.download()
"""
    Arguments to nltk_tweets:
    python nltk_tweets.py data/informalData/tweets/20000trainingdata.csv 20000trainingdata.txt
    python nltk_tweets.py data/informalData/tweets/allTweets.csv tweets.txt
    
    
    informalData/tweets/training.1600000.processed.noemotion.csv
"""

def read_contraction_wordlist():
    with open('contractions.csv', 'rb') as f:
        reader = csv.reader(f)
        contraction = [row[0] for row in reader]
    return contraction[1:]


def read_abbreviations_wordlist():
    with open('abbreviations.csv', 'rb') as f:
        reader = csv.reader(f)
        abbreviation = [row[0] for row in reader]
    return abbreviation[1:]


def twtt5_helper3(data):
    """
        Split sentences at RELEVANT times:
        "." if an uppercase letter follows.
        "!" if an uppercase letter follows.
        "?" if an uppercase letter follows.
        
        Move the boundary after following quotation marks, if any.
        
        Do not split a sentence at an abbreviation.
    """
    temp = []
    for m in re.finditer("((\!|\?|\.')[\s]*[A-Z])|((\!|\?|\.)[\s]*[A-Z])", data):
        index = m.end(0) - 1
        temp.append(index)
        #print data[index]
        #abv = data[(index-4):index]
        #print abv == "St."
        #if data[(index-4):index] == "St.":
        #    print "HERE"
        #    temp.remove(index)
    return temp


"""
['Ala.\n', 'Ariz.\n', 'Assn.\n', 'Atty.\n', 'Aug.\n', 'Ave.\n', 'Bldg.\n', 'Blvd.\n', 'Calif.\n', 'Capt.\n', 'Cf.\n', 'Ch.\n', 'Co.\n', 'Col.\n', 'Colo.\n', 'Conn.\n', 'Corp.\n', 'DR.\n', 'Dec.\n', 'Dept.\n', 'Dist.\n', 'Dr.\n', 'Drs.\n', 'Ed.\n', 'Eq.\n', 'FEB.\n', 'Feb.\n', 'Fig.\n', 'Figs.\n', 'Fla.\n', 'Ga.\n', 'Gen.\n', 'Gov.\n', 'HON.\n', 'Ill.\n', 'Inc.\n', 'JR.\n', 'Jan.\n', 'Jr.\n', 'Kan.\n', 'Ky.\n', 'La.\n', 'Lt.\n', 'Ltd.\n', 'MR.\n', 'MRS.\n', 'Mar.\n', 'Mass.\n', 'Md.\n', 'Messrs.\n', 'Mich.\n', 'Minn.\n', 'Miss.\n', 'Mmes.\n', 'Mo.\n', 'Mr.\n', 'Mrs.\n', 'Mt.\n', 'NO.\n', 'No.\n', 'Nov.\n', 'Oct.\n', 'Okla.\n', 'Op.\n', 'Ore.\n', 'Pa.\n', 'Pp.\n', 'Prof.\n', 'Prop.\n', 'Rd.\n', 'Ref.\n', 'Rep.\n', 'Reps.\n', 'Rev.\n', 'Rte.\n', 'Sen.\n', 'Sept.\n', 'Sr.\n', 'St.\n', 'Stat.\n', 'Supt.\n', 'Tech.\n', 'Tex.\n', 'Va.\n', 'Vol.\n', 'Wash.\n', 'al.\n', 'av.\n', 'ave.\n', 'ca.\n', 'cc.\n', 'chap.\n', 'cm.\n', 'cu.\n', 'dia.\n', 'dr.\n', 'eqn.\n', 'etc.\n', 'fig.\n', 'figs.\n', 'ft.\n', 'gm.\n', 'hr.\n', 'in.\n', 'kc.\n', 'lb.\n', 'lbs.\n', 'mg.\n', 'ml.\n', 'mm.\n', 'mv.\n', 'nw.\n', 'oz.\n', 'pl.\n', 'pp.\n', 'sec.\n', 'sq.\n', 'st.\n', 'vs.\n', 'yr.\n']
"""


def twtt5_helper4(data):
    """
        Do not split a sentence at an abbreviation.
    """
    #abbreviations = ["St.", "Dr."]
    temp = []
    for m in re.finditer("St\.|Dr\.|Ala\.|Ariz\.'|Assn\.|Atty\.|Aug\.|Ave\.|Bldg\.|Blvd\.|Calif\.|Capt\.|Cf\.|Ch\.|Co\.|Col\.|Colo\.|Conn\.|Corp\.|DR\.|Dec\.|Dept\.|Dist\.|Dr.\n|Drs\.|Ed\.|Eq\.|FEB\.|Feb\.|Fig\.|Figs\.|Fla\.|Ga\.|Gen\.|Gov\.|HON\.|Ill\.|Inc\.|JR\.|Jan\.|Jr\.|Kan\.|Ky\.|La\.|Lt\.|Ltd\.|MR\.|MRS\.|Mar\.|Mass\.|Md\.|Messrs\.|Mich\.|Minn\.|Miss\.|Mmes\.|Mo\.|Mr\.|Mrs\.|Mt\.|NO\.|No\.|Nov\.|Oct\.|Okla\.|Op\.|Ore\.|Pa\.|Pp\.|Prof\.|Prop\.|Rd\.|Ref\.|Rep\.|Reps\.|Rev\.|Rte\.|Sen\.|Sept\.|Sr\.|St\.|Stat\.|Supt\.|Tech\.|Tex\.|Va\.|Vol\.|Wash\.", data):
        index = m.end(0) + 1
        temp.append(index)
    
    return temp


def remove_all_common_indeces(list1, list2):
    """
        Another twtt5() helper.
    """
    for element in list2:
        if element in list1:
            list2.remove(element)
    return list2


def twtt5(string, debug=False):
    """
        Split sentences at RELEVANT times.
    """
    temp_list = []
    do_not_split_at = twtt5_helper4(string)
    split_at = twtt5_helper3(string)
    split_at = remove_all_common_indeces(do_not_split_at, split_at)
    last_split = 0
    for new_split in split_at:
        temp_list.append(string[last_split:new_split])
        last_split = new_split
    temp_list.append(string[last_split:])
    
    big_string = ""
    for elmt in temp_list:
        big_string = big_string + elmt + '\n'
    return big_string

"""
string = "Meet me at St. George Station. OK?"
print(string)
string = twtt5(string)
print(string)
raise Exception("STOP!")
"""

def separate_puntuation_before_string(string):
    """
        Separate puntuation from words.
        """
    puntuations = re.findall("[\!|\'|\#|\$|\%|\&|\(|\)|\*|\+|\,|\-|\.|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\`|\{|\||\}|\~]\w", string)
    ready_to_replace = []
    
    for puntuation in puntuations:
        substitute = ' '.join(puntuation)
        ready_to_replace.append(substitute)
    
    for index in range(len(ready_to_replace)):
        string = string.replace(puntuations[index], ready_to_replace[index])
    
    string = ' '.join([st for st in string.split(" ") if st])

    return string

def separate_puntuation_after_string(string):
    """
        Separate puntuation from words.
        """
    puntuations = re.findall("\w[\!|\'|\#|\$|\%|\&|\(|\)|\*|\+|\,|\-|\.|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\`|\{|\||\}|\~]", string)
    ready_to_replace = []
    
    for puntuation in puntuations:
        substitute = ' '.join(puntuation)
        ready_to_replace.append(substitute)
    
    for index in range(len(ready_to_replace)):
        string = string.replace(puntuations[index], ready_to_replace[index])
    
    string = ' '.join([st for st in string.split(" ") if st])

    return string


def separate_puntuation_before_string(string):
    """
        Separate puntuation from words.
        """
    puntuations = re.findall("[\!|\'|\#|\$|\%|\&|\(|\)|\*|\+|\,|\-|\.|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\`|\{|\||\}|\~]\w", string)
    ready_to_replace = []
    
    for puntuation in puntuations:
        substitute = ' '.join(puntuation)
        ready_to_replace.append(substitute)
    
    for index in range(len(ready_to_replace)):
        string = string.replace(puntuations[index], ready_to_replace[index])
    
    string = ' '.join([st for st in string.split(" ") if st])

    return string


def unseparate_abbreviations(string):
    abbreviations = re.findall("St \.|Dr \.|Ala \.|Ariz \.'|Assn \.|Atty \.|Aug \.|Ave \.|Bldg \.|Blvd \.|Calif \.|Capt \.|Cf \.|Ch \.|Co \.|Col \.|Colo \.|Conn \.|Corp \.|DR \.|Dec \.|Dept \.|Dist \.|Drs \.|Ed \.|Eq \.|FEB \.|Feb \.|Fig \.|Figs \.|Fla \.|Ga \.|Gen \.|Gov \.|HON \.|Ill \.|Inc \.|JR \.|Jan \.|Jr \.|Kan \.|Ky \.|La \.|Lt \.|Ltd \.|MR \.|MRS \.|Mar \.|Mass \.|Md \.|Messrs \.|Mich \.|Minn \.|Miss \.|Mmes \.|Mo \.|Mr \.|Mrs \.|Mt \.|NO \.|No \.|Nov \.|Oct \.|Okla \.|Op \.|Ore \.|Pa \.|Pp \.|Prof \.|Prop \.|Rd \.|Ref \.|Rep \.|Reps \.|Rev \.|Rte \.|Sen \.|Sept \.|Sr \.|St \.|Stat \.|Supt \.|Tech \.|Tex \.|Va \.|Vol \.|Wash \.|i \. e \.|e \. g \.", string)
    ready_to_replace = []
    
    for a in abbreviations:
        substitute = a.replace(" ", "")
        ready_to_replace.append(substitute)

    for index in range(len(ready_to_replace)):
        string = string.replace(abbreviations[index], ready_to_replace[index])
    
    string = ' '.join([st for st in string.split(" ") if st])

    return string


def unseparate_abbreviations(string):
    """
        Leave abbreviations alone!!
    """
    
    abbreviation_list = read_abbreviations_wordlist()
    new_list = []
    for abbreviation in abbreviation_list:
        abbreviation = re.sub("\.", " .", abbreviation)
        new_list.append(abbreviation)
    for index in range(len(new_list)):
        if new_list[index] in string:
            string = re.sub(new_list[index], abbreviation_list[index], string)
                     
    return string


def sort_of_works(string):
    """
        Separate puntuation from words.
    """
    
    puntuations = re.findall("[\!|\'|\#|\$|\%|\&|\(|\)|\*|\+|\,|\-|\.|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\`|\{|\||\}|\~][\!|\'|\#|\$|\%|\&|\(|\)|\*|\+|\,|\-|\.|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\`|\{|\||\}|\~[\s]+\!|\'|\#|\$|\%|\&|\(|\)|\*|\+|\,|\-|\.|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\`|\{|\||\}|\~]*", string)
    
    ready_to_replace = []
    
    for puntuation in puntuations:
        substitute = puntuation.replace(" ", "")
        ready_to_replace.append(substitute)
    
    for index in range(len(ready_to_replace)):
        string = string.replace(puntuations[index], ready_to_replace[index])
    
    string = ' '.join([st for st in string.split(" ") if st])

    return string


def do_all_things(string):
    """
        Separate puntuation after string.
        Separate punctuation before string.
        Unseparate abbreviations.
    """
    
    string = separate_puntuation_after_string(string)
    string = separate_puntuation_before_string(string)
    string = unseparate_abbreviations(string)
    string = sort_of_works(string)

    return string


def unseparate_contractions(string):
    """
        Leave contractions alone!!
    """
    
    contraction_list = read_contraction_wordlist()
    new_list = []
    for contraction in contraction_list:
        contraction = re.sub("\'", " \' ", contraction)
        new_list.append(contraction)

    for index in range(len(new_list)):
        if new_list[index] in string:
            string = re.sub(new_list[index], contraction_list[index], string)
                     
    return string


def cleanText(review):
    nltk.data.path.append('/home/mchopra/nltk_data')
    # "[\!|\'|\#|\$|\%|\&|\(|\)|\*|\+|\,|\-|\.|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\`|\{|\||\}|\~]\w"
    # remove Digits
    review = re.sub("[0-9]", " ", review)
    review = re.sub("[@|#]", " ", review)

    string = review.split()
    #review = re.sub("http", " ", review)
    ns = []
    for s in string:
        if s.startswith('http') or s.startswith('www'):
            continue
        else:
            ns.append(s)
    review = " ".join(str(x) for x in ns)

    review = do_all_things(review)

    review = unseparate_contractions(review)

    #print review
    # Separate puntuation from words.
    # review = regexp_tokenize(review, pattern='(?:(?!\d)\w)+|\S+')
    
    # Split sentences
    #review = twtt5(review)
    # change to lower case
    #review = review.lower()

    #review = " ".join(review)
    #print review
    #raise Exception("STOP!")
    #review = nltk.word_tokenize(review)
    #review = nltk.pos_tag(review)
    
    
    #newcorpus = PlaintextCorpusReader(review,'.*')
    #dir(newcorpus)
    #newcorpus.words()
    #pos_tag(review)
    #print review
    
    return review


def tokenize(string):
    """
        Tokenize and separate punctuation.
    """
    return regexp_tokenize(string, pattern='(?:(?!\d)\w)+|\S+')



if __name__ == "__main__":
    args = sys.argv
    FILE = args[1]
    SAVEFILE = args[2]
    DATA = []

    with open(FILE) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            tweet = row[5]
            
            tweet = cleanText(tweet)
            
            print row[5]
            print tweet
            DATA.append(tweet)




    with open(SAVEFILE, 'w') as train_file:
        for i in range(len(DATA)):
            train_file.write(DATA[i] + '\n')


    file = open(SAVEFILE, 'r')
    #print file.read()


    #print(DATA)