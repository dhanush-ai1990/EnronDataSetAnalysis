from encoder import Model
import csv

model=Model()
def get_activations(text):
	activations = []
	new_text = []

	for i in range(len(text)):
		new_text.append(text[i])
		new_text = ''.join(new_text)
		temp2 = []
		temp2.append(new_text)
		print(temp2)
		
		text_features = model.transform(temp2)
		print (text_features.shape)
		print (text_features)

		#17.660 seconds to transform 8 examples
		for i in range(len(temp2)):
			sentiment = text_features[i, 2388]
		print(temp2[i],sentiment)
		activations.append(sentiment)
		new_text = list(temp2)

	list1 = []
	for i in range(len(text)):
		list1.append([text[i], activations[i]])

	with open('sentiment.csv', 'w') as csvfile:
	    fieldnames = ['new_character', 'neuron_activation']
	    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	    writer.writeheader()
	    for i in range(len(text)):
		    writer.writerow({'new_character': text[i], 'neuron_activation': activations[i]})

	return list1



