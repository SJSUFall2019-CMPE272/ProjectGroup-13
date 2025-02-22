#Load The Model
from keras.preprocessing.text import Tokenizer
from keras.models import model_from_json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.models import Model
from keras.layers import LSTM, Activation, Dense, Dropout, Input, Embedding
from keras.optimizers import RMSprop
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping
from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
import os
import re
import json
import mysql.connector
model_path='../model/sarcasm_detect'
h5_file_path='../model/sd_h5_file'
#file = open(model_path, 'r')
#model_json = file.read()
#file.close()
#model = model_from_json(model_json)
# load weights
#model.load_weights(h5_file_path)


#load model
from keras.models import load_model
model = load_model('../model/my_model.h5')
print(model)
#Process the input file
input_file_path='../data/input_data/data.json'
result_file_path='../data/result_data/result.json'
input_file = open (input_file_path)
json_array = json.load(input_file)
store_list = []
import mysql.connector
host_name="cmpe272.ccmlabqieyyi.us-east-1.rds.amazonaws.com"
port_number="3306"
user_name="cmpe272"
password="cmpe2722"
database="cmpe272"
mydb = mysql.connector.connect(host=host_name,user=user_name,passwd=password,database=database)
create_table_statement="create table if not exists result_table ( data TEXT ,location TEXT , retweet_count int , favorite_count int ,time_zone TEXT , is_sarcastic int);"
mycursor = mydb.cursor()
mycursor.execute(create_table_statement)
truncate_table_statement="truncate table result_tablePy;"
mycursor.execute(truncate_table_statement)


for item in json_array:
    store_details = {"text":None, "location":None, "retweet_count":None, "favorite_count":None, "time_zone":None,  "is_sarcastic":None}
    store_details['text'] = item['text']
    store_details['location'] = item['location']
    store_details['retweet_count'] = item['retweet_count']
    store_details['favorite_count'] = item['favorite_count']
    store_details['time_zone'] = item['time_zone']
    store_list.append(store_details)

#print(store_list)
for i in store_list:
    headline=[i['text']]
    tokenizer = Tokenizer(num_words=2000, split=' ')
    tokenizer.fit_on_texts(headline)
    #headline = tokenizer.fit_on_texts(headline)
    headline = tokenizer.texts_to_sequences(headline)
    headline = pad_sequences(headline, maxlen=29, dtype='int32', value=0)
    sentiment = model.predict(headline,batch_size=1,verbose = 2)[0]
    print(sentiment)
    if(np.argmax(sentiment) == 0):
        i['is_sarcastic']=0
        print('sarcastic')
    elif (np.argmax(sentiment) == 1):
        i['is_sarcastic']=1
        print('non-sarcastic')
    insert_sql="INSERT INTO result_table (data , location ,retweet_count, favorite_count, time_zone, is_sarcastic) VALUES (%s, %s, %s, %s, %s, %s)"
    values =(i['text'],i['location'],i['retweet_count'],i['favorite_count'],i['time_zone'],i['is_sarcastic'])
    #values=("test","test",1,1,"test",1)
    mycursor.execute(insert_sql,values)

#with open(result_file_path, 'w') as outfile:
#    json.dump(store_list, outfile)

mydb.commit()
