import pickle
import math
import numpy as np
from matplotlib import pyplot as plt

with open('Relationships/exchange_number_map_to.p','rb') as handle:
    exchange_number_map_to = pickle.load(handle)

print len(exchange_number_map_to)

with open('Relationships/exchange_number_map_cc.p','rb') as handle:
    exchange_number_map_cc = pickle.load(handle)

print len(exchange_number_map_cc)

value_list_to = []
value_list_cc = []
for key in exchange_number_map_to:
   value_list_to.append(exchange_number_map_to[key])
for key in exchange_number_map_cc:
   value_list_cc.append(exchange_number_map_cc[key])

print min(value_list_to),max(value_list_to)
print min(value_list_cc), max(value_list_cc)
bins = np.arange(0,1000,5) # fixed bin size


fig1 = plt.figure(1)
plt.xlim([0, 200])
axes = plt.gca()
axes.set_ylim([0,30000])

plt.hist(value_list_to, bins=bins,edgecolor='black',linewidth = 1.0)
plt.title('Histogram of number of exchanges for to')
plt.xlabel('number of email exchanges')
plt.ylabel('number of pairs of people')
fig1.show()

fig2 = plt.figure(2)
plt.xlim([0, 200])
axes = plt.gca()
axes.set_ylim([0,30000])

plt.hist(value_list_cc, bins=bins,edgecolor='black',linewidth = 1.0)
plt.title('Histogram of number of exchanges for cc')
plt.xlabel('number of email exchanges')
plt.ylabel('number of pairs of people')
fig2.show()

raw_input()