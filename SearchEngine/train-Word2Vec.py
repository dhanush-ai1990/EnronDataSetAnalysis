from gensim.models import Word2Vec
from sklearn.externals import joblib





#lloading : model = gensim.models.Word2Vec.load_word2vec_format('./model/GoogleNews-vectors-negative300.bin', binary=True)






#Main Processing for creating the word2vec model.

path = '/Users/Dhanush/Desktop/Enron_Data/pickle/email_vs_entity_alone.pkl'
email_entity_dict = joblib.load(path)
sentences = []
for key in email_entity_dict:
	data = [x.lower() for x in email_entity_dict[key]]
	data = list(set(data))
	sentences.append(data)

print len(sentences)

#Lets take up an exhaustive back of entities before training because only these will be in Word2Vec Model and can be searched.

query_words ={}
for line in sentences:
	for word in line:
		if word not in query_words:
			query_words[word] = ""

joblib.dump(query_words,'SearchEngineWordList.pkl')
print len(query_words)
model = Word2Vec(sentences, min_count=1, size=150, window=20,workers=3)
model.save('model_final')

print len(model.wv.vocab)
print model.most_similar('oil')
print model.similarity('fraud', 'ferc')


print ""