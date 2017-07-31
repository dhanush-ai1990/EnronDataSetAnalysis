import bottle
from bottle import route, run, request, template
import urllib
import urllib2
import json
from QueryWord2Vec import *

@route('/hello')
def hello():
    return "Hello World!"

@bottle.get('/')
def index():
	return bottle.redirect('index.html')

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

@route('/index.html', method='POST')
def submit_form():
	query = request.forms.get('query')
	searchArea = request.forms.get('searchArea')

	if searchArea == None:
		searchArea =[]
	else:
		searchArea = [searchArea]
	"""
	url = 'http://35.163.124.249:8080/search'
	values = { 'searchtype':'GS','query': query,'restrict': ['PERSON']}
	headers = {'content-type': 'application/json'}
	data = json.dumps(values)
	req = urllib2.Request(url, data,headers)
	response = urllib2.urlopen(req)
	data = response.read()
	print data
	"""
	result,headers = GeneralSearch(query,searchArea)
	print "**********************"
	print result
	print "**********************"
	print headers
    # process query and get the results as json file
  #  result = {"101":{"class":'V', "Name":'Rohit',  "Roll_no":7},
     #      "102":{"class":'V', "Name":'David',  "Roll_no":8},
     #      "103":{"class":'V', "Name":'Samiya', "Roll_no":12}}
   # json_data = json.dumps(result,sort_keys=True)
	return template('SearchResult.html', result =result,headers=headers)

#@route('/profile/<username>')
#def show_profile_page(username):
    #

@bottle.get('/profile/<name>')
def page_viwer(name):
    info = {'title': 'Welcome Home!',
            'content': name,
            'name': name
            }
    return template('profile.html', info)

@bottle.get('/<path:path>')
def html_pages(path):
	return bottle.static_file(path, root='')


run(host='localhost', port=8080, debug=True)