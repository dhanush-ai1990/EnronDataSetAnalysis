from flask import Flask
from flask import render_template
from flask import request
from get_realtime_sentiment import *
import numpy as np

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("untitled.html")

@app.route('/', methods=['GET', 'POST'])

def doSentimentAnalysis():
	if request.method == "POST":
		text = request.form.get('textdata')
		result =get_activations(text)
		print (result)
		return render_template("base.html",result = result)

	return "Something"


if __name__ == "__main__":
    app.run()