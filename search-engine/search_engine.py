import bottle
from bottle import route, run, request, template

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
    name = request.forms.get('query')
    print name
    # process query and get the results as json file
    result = {"101":{"class":'V', "Name":'Rohit',  "Roll_no":7},
           "102":{"class":'V', "Name":'David',  "Roll_no":8},
           "103":{"class":'V', "Name":'Samiya', "Roll_no":12}}
    return template('SearchResult.html', result)

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