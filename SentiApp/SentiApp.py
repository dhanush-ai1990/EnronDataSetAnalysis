from flask import Flask
from flask import render_template
from flask import request
from get_realtime_sentiment import *
import numpy as np
from wtforms import Form

app = Flask(__name__)

import json
import requests

def call_spacy(text):
	url = "http://localhost:8000/ent"
	message_text = text
	headers = {'content-type': 'application/json'}
	d = {'text': message_text, 'model': 'en'}

	response = requests.post(url, data=json.dumps(d), headers=headers)
	r = response.json()
	print(r)
	return r


@app.route("/")
def hello():
	return render_template("untitled.html")

@app.route('/', methods=['GET', 'POST'])

def doSentimentAnalysis():
	print ("fjhdjdjjdjdj")

	if request.method == "POST":
		text = request.form.get('textdata')

		if text == None:
			return render_template("untitled.html",result = None,text = text)
		result1 =get_activations(text)
		json = call_spacy(text)
		result = []
		result.append(result1)
		result.append(json)
		result.append(text)
		return render_template("untitled.html",result = result)

	return "Something"


if __name__ == "__main__":
    app.run()