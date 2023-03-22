#from sklearn.metrics.pairwise import cosine_similarity
import tensorflow_hub as hub
import tensorflow as tf
import pandas as pd
import numpy as np
#import glob
import os
import urllib.request
import tarfile
import hashlib
from annoy import AnnoyIndex
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
def elmo_vectors(x):
    elmo = hub.Module("./elmo_module/", trainable=True)     
    embeddings=elmo(x, signature="default", as_dict=True)["elmo"]
    with  tf.compat.v1.Session() as sess:
        sess.run(tf.compat.v1.global_variables_initializer())
        sess.run(tf.compat.v1.tables_initializer ())
    # return average of ELMo features
        return sess.run(tf.reduce_mean(embeddings,1))
def question_csv_list():
    file="archive/question_answer_data.csv"
    data = pd.read_csv(file,header=None,names=['pdf_name','question','answer','page']) 
    data=data.dropna()
    df=data
    filename=file.split('archive/')
    filename=" ".join(filename)
    filename=filename.split('.csv')
    file_name=filename[0]
    v='archive/'+file_name+'.npy'
    if (os.path.exists(v)):
        question_set=[]
        for i in df['question']:
                    question_set.append(i)
        question_set=[question_set]
        question_set_vector=[]
        for i in range(len(question_set)):
                    question_set_vector.append(elmo_vectors(question_set[i]))
        question_set_length=len(df['question'])
        question_list=np.array(question_set_vector)
        question_list=np.reshape(question_list,(question_set_length,1024))
        np.save('archive/'+file_name,question_list)
        D=int(config['index']['D'])
        NUM_TREES=int(config['index']['Num_tree'])
        ann = AnnoyIndex(D)
        data=np.load('archive/'+file_name+'.npy')
        for index, embed in enumerate(data):
                        ann.add_item(index, embed)
        ann.build(NUM_TREES)
        search=ann.save('archive/'+file_name+'.ann')
    else:
        question_set=[]
        for i in df['question']:
                    question_set.append(i)
        question_set=[question_set]
        print(question_set)
        question_set_vector=[]
        for i in range(len(question_set)):
                    question_set_vector.append(elmo_vectors(question_set[i]))
        question_set_length=len(df['question'])
        question_list=np.array(question_set_vector)
        question_list=np.reshape(question_list,(question_set_length,1024))
        np.save('archive/'+file_name,question_list)
        D=int(config['index']['D'])
        NUM_TREES=int(config['index']['Num_tree'])
        ann = AnnoyIndex(D)
        data=np.load('archive/'+file_name+'.npy')
        for index, embed in enumerate(data):
                        ann.add_item(index, embed)
        ann.build(NUM_TREES)
        search=ann.save('archive/'+file_name+'.ann')
#question_csv_list()
def input_question(question,file_data):
    data="./archive/question_answer_index.ann"
    file_name=hashlib.md5(file_data.encode())
    file_name=file_name.hexdigest()
    question_data=[[question]]
    question_data_vector=[]
    for i in range(len(question_data)):
        question_data_vector.append(elmo_vectors(question_data[i]))
    question_input=np.array(question_data_vector)
    question_input=np.reshape(question_input,(1,1024))
    #print(question_input)
    D=int(config['index']['D'])
    NUM_TREES=int(config['index']['Num_tree'])
    u = AnnoyIndex(D)
    u.load(data)
    file="./archive/question_answer_data.csv"
    data = pd.read_csv(file,header=None,names=['pdf_file','pdf_name','question','answer','page']) 
    data=data.dropna()
    #data=data.loc[data['pdf_name'] == file_name]
    #data = data.reset_index(drop=True)
    nns= u.get_nns_by_vector(question_input[0],5)
    key=data.iloc[nns].values
    temp=[]
    for i in key:
          
         data= {"question":i[2],"ans":i[3],"page":i[4],"source_name":i[0]}
         temp.append(data)
    res = [d for d in temp if d['source_name']==file_data] 
     
    return res
         

   
    #return data_value
     
#v=input_question('what is sixth sense ?','b40f271feea9af6e03f16c95838a65e4')