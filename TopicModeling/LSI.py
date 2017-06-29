from gensim import models, corpora, similarities
import pickle
import random
import string

def id_generator(size=9, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def docs2topics(vector_corpus, dictionary, num_topics):
    """
    Parameters are a vector corpus file, a dictionary that can be used to translate the vector corpus,
    and an integer for num_topics
    the function returns a document to topic list, with as many topics as requested by num_topics.
    """
    tfidf = models.TfidfModel(vector_corpus)
    corpus_tfidf = tfidf[vector_corpus]

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=num_topics, onepass=False, power_iters=5)
    #returns lsi, a list of topics and a list of distribution of topics over the corpus documents
    doc2topics = lsi[corpus_tfidf]
    return doc2topics

def make_lsi_topics(vector_corpus, dictionary, num_topics):
    """
    Given a vector corpus and a dictionary to translate the vector corpus the function returns a list of topics.
    The number of topics generated is specified with the parameter num_topics.
    """
    # corpus = corpora.MmCorpus(corpus_path)
    tfidf = models.TfidfModel(vector_corpus)
    corpus_tfidf = tfidf[vector_corpus]

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=num_topics, onepass=False, power_iters=5)
    topics_str = lsi.show_topics(num_topics)
    """
        the topics are returned in a list of topic strings:

        [u'0.703*"trees" + 0.538*"graph" + 0.402*"minors" + 0.187*"survey" + 0.061*"system" + 0.060*"time" + 0.060*"response" + 0.058*"user" + 0.049*"computer" + 0.035*"interface"', 
        u'0.460*"system" + 0.373*"user" + 0.332*"eps" + 0.328*"interface" + 0.320*"response" + 0.320*"time" + 0.293*"computer" + 0.280*"human" + 0.171*"survey" + -0.161*"trees"']
    """
    topics = []
    print topics_str
    for item in topics_str:
        print "*******"
        print item
        topic = []
        for strg in item[1].split(" + "):
            strg = strg.strip()
            t = []
            for item in tuple(strg.split("*")):
                item = item.strip("\"").strip("'").strip()
                t.append(item)
            topic.append((float(t[0]), t[1]))
        topics.append(topic)
        print topic

    return topics


with open('text_term_matrix.p','rb') as handle:
    vector_corpus = pickle.load(handle)
with open('dictionary.p', 'rb') as handle:
    dictionary = pickle.load(handle)
num_topics = 10

print "---------------"
print "before lsi"
topics_lst = make_lsi_topics(vector_corpus, dictionary, num_topics)
print "after LSI"
print_str = ""
for idx, t in enumerate(topics_lst):
    sum_prop = sum([abs(x[0]) for x in t])
    words = [x[1] for x in t]
    print_str += "{0}\t{1}\t{2}\n".format(idx, sum_prop, " ".join(words))

# key_file = corpus_dir + os.sep +
with open("topic-keys.txt", "w") as f:
    f.write(print_str)

print_str = "doc\tname\ttopic\tproportion..."
docs2topics_lst = docs2topics(vector_corpus, dictionary, num_topics)

with open("topic-compostion.txt", "w") as f:
    for idx, item in enumerate(docs2topics_lst):
        if idx == 0:
            print_str = "doc\tname\ttopic\tproportion..."
        else:
            print_str = ""
        prop_lst = []
        for topic, value in item:
            prop_lst.append("{0}\t{1}".format(topic, abs(value)))
        print_str += "\n{0}\t{1}\t{2}".format(idx, id_generator(), "\t".join(prop_lst))
        f.write(print_str)