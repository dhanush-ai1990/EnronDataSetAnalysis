import sqlite3
import pickle

big_Database = sqlite3.connect('/Users/sahba/Downloads/Enron_database_2.db',timeout=5)

big_db_connection = big_Database.cursor()

big_db_connection.execute("SELECT * FROM `ENRON PRIME`")
all_emails = big_db_connection.fetchall()
print len(all_emails)

email_map_to = {}
email_map_cc = {}
counter = 0

for email in all_emails:
    counter += 1
    if counter % 100 == 0:
        print counter
    to_or_cc = email[16]
    sender_email = email[6]
    receiver_email = email[11]

    if to_or_cc=="TO":
        if (sender_email, receiver_email) in email_map_to:
            email_map_to[(sender_email, receiver_email)] += 1
        else:
            email_map_to[(sender_email, receiver_email)] = 1
    else:
        if (sender_email, receiver_email) in email_map_cc:
            email_map_cc[(sender_email, receiver_email)] += 1
        else:
            email_map_cc[(sender_email, receiver_email)] = 1


pickle.dump(email_map_to, open("email_map_to.p", "wb"))
pickle.dump(email_map_cc, open("email_map_cc.p", "wb"))

big_Database.close()