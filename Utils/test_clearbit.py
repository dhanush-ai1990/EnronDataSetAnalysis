import clearbit

clearbit.key = 'sk_1573a83a3cdd597a943b7a8cc50b4fcf'

company = clearbit.Company.find(domain='wapa.gov', stream=True)
if company != None:
  print "Name: " + company['name']