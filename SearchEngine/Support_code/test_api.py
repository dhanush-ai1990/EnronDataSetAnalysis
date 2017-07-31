import urllib
import urllib2
import json
url = 'http://35.163.124.249:8080/search'
values = { 'searchtype':'GS','query': 'Who is interested in oil ?','restrict': ['PERSON']}
#r = requests.post(url, data = json.dumps(payload), headers = headers)
headers = {'content-type': 'application/json'}
data = json.dumps(values)
req = urllib2.Request(url, data,headers)
response = urllib2.urlopen(req)
data = response.read()
data = json.loads(data)

print type(data)