import pickle
import csv

def get_relation_csv(pickle_object):
    with open(pickle_object, 'rb') as handle:
        relationships = pickle.load(handle)
    f = open('relationships.csv', 'w')

    writer = csv.writer(f, delimiter=",")

    for msgid, msg_info_list in relationships.iteritems():
        sender_name = msg_info_list[1]
        receiver_name = msg_info_list[2]
        heuristic_score = msg_info_list[6]

        writer.writerow([sender_name,receiver_name, heuristic_score])
    f.close()