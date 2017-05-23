

# external modules
import pandas as pd
import numpy as np
#import gensim
from keras.utils import np_utils
import re
import numpy as np
import pandas as pd
import string
#import os
import gensim

formal_dataset = "/Users/Dhanush/Documents/Deeplearn/generating-reviews-discovering-sentiment/data_formal_informal/en_US.news.txt"
informal_dataset ="/Users/Dhanush/Documents/Deeplearn/generating-reviews-discovering-sentiment/data_formal_informal/en_US.blogs.txt"


''' 
prepares data for network 
in order to run a training session, use the code in network_elements.py and train.py
tweak the hyperparameters and run '''
def cleanup_str(st, numbers=False):
    
    st=str(st)

    if numbers == True:
        keep=set(string.letters + string.digits + ' ')    
    else: 
        keep=set(string.letters + ' ')
    
    # clean string
    st=''.join(x if x in keep else ' ' for x in st)
    # rem multiple spaces
    st=re.sub(' +',' ', st)

    return st.strip().lower()   

# mapper: cleanup a pd column or list of strings
def cleanup_col(col, numbers=False):
    
    col=map(lambda x: cleanup_str(x, numbers=numbers), col)
    return col
    

# perform cleanup on a pandas dataframe or dict
def cleanup_frame(dat, collist=['user1_string', 'user2_string'], numbers=False):
    for col in collist:
        dat[col]=cleanup_col(dat[col], numbers=False)
        
    return dat

# shorten strings in list
def reduce_strings(stringlist, maxlength, return_arrays=True):
    
    # if type(stringlist) != list:
    #    stringlist=list(stringlist)
    
    splitsreduce=[x[0:maxlength] for x in [x.split(' ') for x in stringlist]]
    
    if return_arrays:
        return splitsreduce
    
    shortstrings=[' '.join(x) for x in splitsreduce]
    return shortstrings



def vec2pad(doc, max_length):
    
    doclength, embdim=np.shape(doc)
    # add zeros up the decided sequence length 
    if doclength < max_length:
        s=np.zeros([max_length - doclength, embdim]) 
        doc=np.concatenate((doc,s), axis=0)
        
        return doc
    elif doclength == max_length:
        
        return doc
    else: 
        print("document is longer that the set max_length")
        
        return doc


            
def str_length_distr(string_arrays, max_length=40):
    # strings of usererdata and their respective lengths

    stringlengths=[len(x.split(' ')) for x in string_arrays]
    
    # maximum length of user string
    maxstringlength=max(stringlengths)
    print("maximum string length: {}".format(maxstringlength))
    numchanged=len([x for x in stringlengths if x >= max_length])
    print("number docs changed with cap at {}: {} of total {} ({}%)".format(
        max_length, numchanged, len(string_arrays), np.round(100.0*numchanged/len(string_arrays), 2)))
    # plot length distribution
    plt.hist(stringlengths)  


def genwordvecs(docs, emb_size, try_load=False, minc=1):

    vmodel_name='embedding_dim_{}_c_{}'.format(emb_size, minc)
    if try_load == True:
        try: 
            vmodel=gensim.models.Word2Vec.load('vmodels/'+vmodel_name)
            print('model loaded from disk')
            
            return vmodel
        except IOError:
            print('error loading model..')
            print('training word embeddings')

    vmodel=gensim.models.Word2Vec(docs, min_count=minc, size=emb_size, workers=4)
    vmodel.save('vmodels/'+vmodel_name)
    
    return vmodel        


def w2v_transform(string_arrays, model, max_length=None):
    
    # removes words that not in vocabulary and then transforms to vector form
    v2w_arrays=map(lambda x: model[[y for y in x if y in model]], string_arrays)
    # sets length limit and zero-vectors as padding
    if max_length != None:
        v2w_arrays=map(lambda x: vec2pad(x, max_length), v2w_arrays)
        
    return np.array(v2w_arrays)

def loaddata():
# set parameters ------------------------------------
# ---------------------------------------------------

	MAXLENGTH=50
	EMBEDDING_SIZE=64
	MIN_COUNT=1


	# read data -----------------------------------------
	# ---------------------------------------------------

	# i mport csvtable of the form: 
	# |other stuff|user1_string|user2_string|other stuff|

	formal_data_text_list = []
	formal_data_label_list =[]
	f = open(formal_dataset,'r')
	num_chars = 0
	text = []
	for line in f:
		num_chars += len(line)
		text.append(line)
		if num_chars > 1000:
			text = "".join(text)
			text = re.sub("[^a-zA-Z]", " ", text) 
			formal_data_text_list.append(text)
			formal_data_label_list.append(0)
			num_chars = 0
			text = []

	print (" ")
	#print formal_data_text_list[4567]

	# Process for Informal dataset

	informal_data_text_list = []
	informal_data_label_list =[]
	f = open(informal_dataset,'r')
	num_chars = 0
	text = []

	for line in f:
		num_chars += len(line)
		text.append(line)
		if num_chars > 1000:
			text = "".join(text)
			text = re.sub("[^a-zA-Z]", " ", text) 
			informal_data_text_list.append(text)
			informal_data_label_list.append(1)
			num_chars = 0
			text = []
	print ("The number of samples for formal data: " + str(len(formal_data_text_list)))
	print ("The number of labels for formal data: " + str(len(formal_data_label_list)))
	print ("The number of samples for informal data: " + str(len(informal_data_text_list)))
	print ("The number of samples for informal data: " + str(len(informal_data_label_list)))

# combine and create a common training set. We will use CV and split into train and test later.
	Combined_training_data = formal_data_text_list + informal_data_text_list
	Combined_training_label = formal_data_label_list +informal_data_label_list
	print ("Total training data samples " + str(len(Combined_training_data)))
	print ("Total training data labels " + str(len(Combined_training_label)))
	
	X1=np.array(Combined_training_data)
	
	Y = np.array(Combined_training_label)
	Y = np_utils.to_categorical(Y, 2)
	# X1 data
	X1=reduce_strings(X1, MAXLENGTH)
	# preprocess vocab data -----------------------------
	# ---------------------------------------------------

	# generate word2vec - model
	vmodel=genwordvecs(X1, 
	                     emb_size=EMBEDDING_SIZE, 
	                     try_load=False, 
	                     minc=1)

	# perform transformation
	X1=w2v_transform(X1, vmodel, MAXLENGTH) 
	print X1.shape
	print Y.shape  

	# final dataset object
	data=Dataset(X1, Y, testsize=0.2,  shuffle=False)
	#pickle.dump(data,open('data.pickle','wb'))
	
	
loaddata()






