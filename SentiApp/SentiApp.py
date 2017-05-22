from flask import Flask
from flask import render_template
app = Flask(__name__)



@app.route("/")
def hello():
    return render_template("untitled.html")

@app.route('/', methods=['GET', 'POST'])

def doSentimentAnalysis():
	print ("Here")
	if request.method == "GET":
		Text = request.form.get('textdata')
		print (Text)


if __name__ == "__main__":
    app.run()