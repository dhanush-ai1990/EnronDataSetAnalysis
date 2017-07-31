import bottle
import copy
import math
import os
import random
import time
from QueryWord2Vec import *
from bottle import route, error, post, get, run, static_file, abort, redirect, response, request, template
import simplejson as json



@bottle.route('/search')

def static(path):
    return bottle.static_file(path, root='static/')

@bottle.get('/')
def index():

    return {
        "Welcome to the SPAI Search Engine backend"
    }

@bottle.route('/search',method='POST')
def search():
    
    data = bottle.request.body.read()
    data = json.loads(data)


    #The data should be send in the formal :

    # Query Type - "GS" - General search NLTK related search. Should have a query String and types to return (could be null)
    # Query Type  -"DS" - This could be a post for a detailed description of a person, organization or the Entity as a part of result page
    #print "here"
    #print data
    if data == None:
        return { "message": "Invalid Search format"}
      
      

    searchtype = data['searchtype']
    query = data['query']
    print type(query)
    restrict = data['restrict']
    print type(restrict)
    if searchtype == 'GS':
    	out = GeneralSearch(query,restrict) # data[1] should be a string
    	if len(out) == 0:
    		return {
      			"message": "No results found"}
      	else:
    	    return {
    	    "message": "Results found",
    	    "out" : out }

    # TODO: Do things with data
    return {
      "message": "Invalid Search Query",
      "out": []
    }

@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }



application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))