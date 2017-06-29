import sqlite3
import pickle

small_Database = sqlite3.connect('/Users/sahba/Downloads/Enron_database.db',timeout=5)
big_Database = sqlite3.connect('/Users/sahba/Downloads/Enron_database_2.db',timeout=5)

def get_name(email,db_connection):
    SQL_query = 'SELECT `FULL NAME` from EMPLOYEE where `EMAIL ID`=\"'+email+'\"'
    db_connection.execute(SQL_query)
    rows = db_connection.fetchall()

    if len(rows) == 0:
        return ""
    else:
        row = rows[0]
        return str(row[0])

small_db_connection = small_Database.cursor()
big_db_connection = big_Database.cursor()

big_db_connection.execute("SELECT * FROM `ENRON PRIME`")
all_emails = big_db_connection.fetchall()
print len(all_emails)

exchange_number_map_to = {}
exchange_number_map_cc = {}
counter = 0

for email in all_emails:
    counter += 1
    if counter % 100 == 0:
        print counter
    to_or_cc = email[16]
    sender_email = email[6]
    receiver_email = email[11]
    sender_fullname = get_name(sender_email,small_db_connection)
    receiver_fullname = get_name(receiver_email,small_db_connection)

    if sender_fullname == "":
        continue

    if to_or_cc=="TO":
        if (sender_fullname, receiver_fullname) in exchange_number_map_to:
            exchange_number_map_to[(sender_fullname, receiver_fullname)] += 1
        else:
            exchange_number_map_to[(sender_fullname, receiver_fullname)] = 1
    else:
        if (sender_fullname, receiver_fullname) in exchange_number_map_cc:
            exchange_number_map_cc[(sender_fullname, receiver_fullname)] += 1
        else:
            exchange_number_map_cc[(sender_fullname, receiver_fullname)] = 1


pickle.dump(exchange_number_map_to, open("exchange_number_map_to.p", "wb"))
pickle.dump(exchange_number_map_cc, open("exchange_number_map_cc.p", "wb"))

big_Database.close()
small_Database.close()