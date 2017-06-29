'''
Created on 4 Jun 2014
@author: Bleier
outputter.py
'''
import os, random, re, getopt, sys


def print_histo(rows, column_fill, labels=None, document_name=""):
    """
    rows is the number of rows the histogram is high
    column_fill is a list of numbers that determine how much of each column in the histogram is filled up
    labels for the columns
    document name for header
    """
    histo = "\n"
    for item in column_fill:
        histo += "{0: ^5}".format("_" * 5)
    histo += "\n{0}\n\n".format(document_name)
    if labels:
        for item in labels:
            histo += "{0: ^5}".format(item)
        histo += "\n"
    for row in reversed(range(rows)):
        for num in column_fill:
            if num >= row + 1:
                histo += "{0: ^5}".format("***")
            else:
                histo += "{0: ^5}".format(" ")
        histo += "\n"
    for item in column_fill:
        histo += "{0: ^5}".format("_" * 5)
    histo += "\n\n"
    return histo


def data_to_output_string(file_names=None, name_and_lst=None, print_o_lst=None):
    """
    first parameter file_names is the list of file names of the trainings corpus
    name_and_lst should a list of tuples e.g. (file_name, word_freq_list)
    print_o_lst should a list of values - values will be printed in an ordered list
    """
    output = ''
    # first print the corpus training files
    if file_names:
        output += "Training files:\n"
        for idx, name in enumerate(file_names):
            output += str(idx) + "  " + str(name) + "\n"

    if name_and_lst:
        # name_and_list is a tuple of name and a list of values, name is printed and the values in a new line
        for name, lst in name_and_lst:
            output += "\n{0}:\n".format(name)
            for item in lst:
                output += "{0}; ".format(item)

        output += "\n"

    if print_o_lst:
        # print an ordered list, e.g. list of  topics
        output += "\n"
        for idx, item in enumerate(print_o_lst):
            output += "Topic " + str(idx) + " : " + str(item) + "\n"

    return output


# Following is code for mallet2gephi transformation#

def get_percent_of_diff(lst):
    """
    given a list of values between 0 and 1, if finds the highest and lowest value, calculates the difference
    and calculates percent of the difference.
    """
    max_val = max(lst) * 100
    min_val = min(lst) * 100
    return 100 / (max_val - min_val)


def distribute_values(p, min_value, num):
    """
    in combination with get_one_per_centcent_of_diff this function distributes values between a certain range wider - e.g. in order to
    help with strong, unreadable clusters in the Gephi output.
    usually Mallet or Gensim return probability values like 0.25435, 0.3453, 0.2344, if visulized these values would cluster to strongly together in
    Gephi, therefore the they have to be distributed over 0 (0%) to 1 (100%).
    p, is a float value calculated by get_percent_of_diff
    min_value is a float between 0 and 1, the lowest value in a list of float values between 0 and 1
    num is the float (between 0 and 1) who's value should be re-calculated if the range would be 0-1
    """
    return (num * 100 - min_value * 100) * p / 100


def get_topic_comp(imp_file_comp, limit=0.1):
    with open(imp_file_comp, "r") as f:
        id2topics = {}
        for item in f.readlines()[1:]:
            try:
                topic_comp_lst = item.split("\t")
                file_name = topic_comp_lst[1]
                # print file_name
                if "//" in file_name:
                    # cut out name from file name string - used for mallet files
                    mm = re.search("txt/(\d+.0).txt", file_name)
                    if mm:
                        name = mm.group(1)
                    else:
                        print "no match found"
                else:
                    name = file_name

                topic_lst = []
                # get only edges if they have certain relevance to topic
                for num, i in enumerate(topic_comp_lst[3::2]):
                    previous_item = num * 2 + 3 - 1
                    if float(i) > float(limit):
                        topic_lst.append((topic_comp_lst[previous_item], float(i)))
                id2topics[name] = topic_lst

            except IndexError:
                print "index error"
    return id2topics


def mallet2gephi_edges(imp_file_comp, exp_file, limit=0.1, dist0to1=False):
    """
    transforms a mallet compostion txt file into a gephi edges file
    The layout of the mallet file should be as follows:
        'doc'\t'name'\t'topic'\t'proportion'\t'topic'\t'proportion'...
    topics are integer, proportion are floats between 0 and 1
    The parameter limit is the threshold below which proportions will not be included in the output
    If dist0to1 is set to 'True' the mallet proportions will be distributed from 0-1
    """
    t = get_topic_comp(imp_file_comp, limit=limit)

    value_lst = []
    for topic_lst in t.values():
        if len(topic_lst) > 0:
            for topic, value in topic_lst:
                value_lst.append(value)

    # head of gephi csv file
    write_strg = "Source,Target,Type,Id,Weight"

    if dist0to1 and len(value_lst) > 0:
        # for dist graph
        min_value = min(value_lst)
        p = get_percent_of_diff(value_lst)

    for name, topic_lst in t.items():
        # print len(topic_lst)
        if len(topic_lst) > 0:
            for topic, value in topic_lst:
                random_id = name + str(random.random())
                if dist0to1 and len(value_lst) > 0:
                    value = distribute_values(p, min_value, value)
                write_strg += "\n{0},T{1},Undirected,{2},{3}".format(name, topic, random_id, value)
    # write gephi edges data to file
    with open(exp_file, "w") as f:
        f.write(write_strg)

def outputter_main(corpus_file_path=None, attrs=None, python_expr=None, to_file=False,
                   imp_file_comp=None, exp_file=None, limit=0.1, dist0to1=False):
    mallet2gephi_edges(imp_file_comp, exp_file, limit=limit, dist0to1=dist0to1)


outputter_main(imp_file_comp="topic-compostion.txt",exp_file="gephi-input.csv")