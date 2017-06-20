from encoder import Model
import csv
import pickle
import time
from sklearn.externals import joblib
model=Model()

def get_activations(text):
	text_features = model.transform(text)
	for i in range(len(text)):
		sentiment = text_features[i, 2388]
		return (text[i],sentiment)

    
if __name__ == "__main__":
	text = ["Happy"]
	print(get_activations(text))

	all_emails = pickle.load(open('myPickles', 'rb'))
	all_emails_label = pickle.load(open('MsgId', 'rb'))
	print (type(all_emails))
	print (len(all_emails))
	print (len(all_emails_label))

	get_data_transform = []
	get_data_labels =[]
	count = 0
	batch = 0
	Total_batch = 0
	activations = []
	for email in all_emails:
		if batch < 500:
			get_data_transform.append(" ".join(email))
			get_data_labels.append(all_emails_label[count])
			count+=1
			batch +=1
			continue
		a = time.time()
		Total_batch +=1
		batch = 0
		text_features = model.transform(get_data_transform)
		get_data_transform = []
		b = time.time()
		for i in range(len(text_features)):
			sentiment = text_features[i, 2388]
			activations.append(sentiment)
		print ("Completed Batch: " +str(Total_batch))
		c = b - a

	joblib.dump(activations, 'activations.pkl')
	joblib.dump(get_data_labels, 'labels.pkl')




