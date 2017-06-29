import gensim
from gensim import corpora
import pyLDAvis
import pyLDAvis.gensim
import pickle
import logging

def gensim_output(modelfile, text_term_matrix, dictionary):
    """Displaying gensim topic models"""
    ## Load files from "gensim_modeling"
  #  corpus = corpora.MmCorpus(text_term_matrix)
    myldamodel = gensim.models.ldamodel.LdaModel.load(modelfile)
    print "read models"
    ## Interactive visualisation
    vis = pyLDAvis.gensim.prepare(myldamodel, text_term_matrix, dictionary)
    print "generated vis object"
  #  pyLDAvis.display(vis)
    pyLDAvis.save_html(vis, 'txtdata/lda.html')

logging.basicConfig(filename='txtdata/lda_vis.log', format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

with open('txtdata/text_term_matrix.p', 'rb') as handle:
    text_term_matrix = pickle.load(handle)
with open('txtdata/dictionary.p', 'rb') as handle:
    dictionary = pickle.load(handle)
print "read files"
gensim_output('txtdata/lda_35.model',text_term_matrix,dictionary)