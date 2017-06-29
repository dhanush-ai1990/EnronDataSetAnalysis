import pickle

with open('mapping.p','rb') as handle:
    my_dictionary = pickle.load(handle)
print len(my_dictionary)

#print(unserialize_data)
#print unserialize_data['mark.guzman@enron.com']
#print(unserialize_data['ryan.slinger@enron.com'])

#print(unserialize_data['mark.guzman@enron.com, ryan.slinger@enron.com'])


import sqlite3

Database = sqlite3.connect('/Users/sahba/Downloads/Enron_database.db',timeout=10)
Database.text_factory = str
c = Database.cursor()
print "hi"

SQL = 'SELECT * from EMPLOYEE where last="**"'
c.execute(SQL)
rows = c.fetchall()

common_emails = 0
for row in rows:
  if row[0] in my_dictionary:
      full_name = my_dictionary[row[0]].strip()
      if ' ' in full_name:
          print row[0]
          name_parts = full_name.split(' ')
          if len(name_parts)==2:
              first_name = name_parts[0]
              last_name = name_parts[1]
          else:
              first_name = name_parts[0]
              last_name = name_parts[-1]
      else:
          first_name = full_name.split('@')[0]
          last_name = '**'
      full_name= first_name + ' ' + last_name

      c.execute('UPDATE EMPLOYEE SET `FIRST` =?, `LAST` =?, `FULL NAME`=? WHERE `EMAIL ID`=?',
                (str(first_name),str(last_name),str(full_name),str(row[0])))
print len(my_dictionary)
print (len(rows))
print common_emails
print "do it"
Database.commit()
Database.close()



