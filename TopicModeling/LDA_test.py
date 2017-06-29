import gensim
from gensim import corpora
from nltk.corpus import stopwords


# later on, load trained model from file
model =  gensim.models.LdaModel.load('lda_50.model')

# print all topics
for i in range(0,50):
    print model.print_topic(i)