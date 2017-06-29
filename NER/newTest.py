import pickle

with open('freq_orgs.p','rb') as handle:
    freq_orgs = pickle.load(handle)
print len(freq_orgs)

counter = 0
for key in freq_orgs:
    if freq_orgs[key] > 5:
        counter += 1
        print key

