from gensim.models import Word2Vec
from sklearn.externals import joblib





#lloading : model = gensim.models.Word2Vec.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin', binary=True)






#Main Processing for creating the word2vec model.

path = '/Users/Dhanush/Desktop/Enron_Data/pickle/email_vs_entity_alone.pkl'
email_entity_dict = joblib.load(path)
sentences = []
for key in email_entity_dict:
	data = [x.lower() for x in email_entity_dict[key]]
	sentences.append(data)

print len(sentences)


model = Word2Vec(sentences, min_count=1, size=300, window=10,workers=3)
model.save('model_final')

print len(model.wv.vocab)
print model.most_similar('oil')
print model.similarity('oil', 'enron')


print ""