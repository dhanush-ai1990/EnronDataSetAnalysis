from encoder import Model
import csv
import pickle
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
	print(all_emails[1])