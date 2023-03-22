from sklearn.metrics.pairwise import cosine_similarity
import tensorflow_hub as hub
import tensorflow as tf
import pandas as pd
import numpy as np
import glob
import os
import urllib.request
import tarfile
from tqdm import tqdm
from datetime import date
import os.path,time
import os.path as path
from annoy import AnnoyIndex
from pathlib import Path
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
def download_elmo():
    elmo_folder='./elmo_module/'
    if os.path.exists(elmo_folder):
        pass
    else:
        os.mkdir(elmo_folder)
    elmo_file='./elmo_module/2.tar.gz'
    if  not os.path.exists(elmo_file):
        url="https://storage.googleapis.com/tfhub-modules/google/elmo/2.tar.gz"
        urllib.request.urlretrieve(url,elmo_file)
        my_tar = tarfile.open('./elmo_module/2.tar.gz')
        my_tar.extractall('./elmo_module/') # specify which folder to extract to
        my_tar.close()
    else:
        pass
elmo_download=download_elmo()
def elmo_vectors(x):
    elmo = hub.Module("./elmo_module/", trainable=True)     
    embeddings=elmo(x, signature="default", as_dict=True)["elmo"]
    with  tf.compat.v1.Session() as sess:
        sess.run([tf.compat.v1.global_variables_initializer()])
        sess.run([tf.compat.v1.tables_initializer ()])
    # return average of ELMo features
        return sess.run(tf.reduce_mean(embeddings,1))
def question_csv_list():
    file="./archive/question_answer_data.csv"
    data = pd.read_csv(file,header=None,names=['pdf_name','question','answer','page']) 
    data=data.dropna()
    df=data
    file_name1="question_answer_index"
    v='./archive/'+file_name1
    if (os.path.exists(v)):
        question_set_vector=[]
        BATCH_SIZE=100
        with tf.Session() as sess:
            sess.run([tf.global_variables_initializer(), tf.tables_initializer()])
            for i in tqdm(range(0, len(df['question']),BATCH_SIZE)):
                question_set_vector.append(sess.run(elmo_vectors(df["question"].iloc[i:(i+BATCH_SIZE)].tolist())))
                question_set_vector = np.concatenate(question_set_vector, axis=0)
        question_set_length=len(df['question'])
        question_list=np.array(question_set_vector)
        question_list=np.reshape(question_list,(question_set_length,1024))
        np.save('./archive/'+file_name1,question_list)
        D=int(config['index']['D'])
        NUM_TREES=int(config['index']['Num_tree'])
        ann = AnnoyIndex(D)
        data=np.load('./archive/'+file_name1+'.npy')
        for index, embed in enumerate(data):
                        ann.add_item(index, embed)
        ann.build(NUM_TREES)
        search=ann.save('./archive/'+file_name1+'.ann')
    else:
        question_set=[]
        for i in df['question']:
                    question_set.append(i)
        question_set=[question_set]
        question_set_vector=[]
        context_embed = []
        #print(len(question_set))
        BATCH_SIZE=100
        sentences = []
        with tf.Session() as sess:
            sess.run([tf.global_variables_initializer(), tf.tables_initializer()])
            for i in tqdm(range(0, len(df['question']),BATCH_SIZE)):
                question_set_vector.append(elmo_vectors(df["question"].iloc[i:(i+BATCH_SIZE)].tolist()))
                question_set_vector = np.concatenate(question_set_vector, axis=0)
        question_set_length=len(df['question'])
        question_list=np.array(question_set_vector)
        question_list=np.reshape(question_list,(question_set_length,1024))
        np.save('./archive/'+file_name1+'.npy',question_list)
        D=int(config['index']['D'])
        NUM_TREES=int(config['index']['Num_tree'])
        ann = AnnoyIndex(D)
        data=np.load('./archive/'+file_name1+'.npy')
        for index, embed in enumerate(data):
                        ann.add_item(index, embed)
        ann.build(NUM_TREES)
        search=ann.save('./archive/'+file_name1+'.ann')
###def check_file():
    #file="./archive/question_answer_data.csv"
    #file1="./archive/question_answer_data.ann"
    #if(os.path.exists(file1)):
     #   print("yes")
    #pytime = os.path.getctime(os.path.join(file))
    #txttime = os.path.getmtime(os.path.join(file))
    #print(txttime)###
def is_file_older_than_x_days(file, days=1):
    file_time = path.getmtime(file) 
    # Check against 24 hours 
    if (time.time() - file_time) / 3600 > 24*days: 
        pass
    else: 
        csv_file="./archive/question_answer_data.csv"
        model_file="./archive/question_answer_index.npy"
        if (os.path.exists(model_file)):
            pass
        else:
            question_csv_list()
        pytime = os.path.getmtime(os.path.join(csv_file))
        txttime = os.path.getmtime(os.path.join(model_file))
        if (pytime<txttime):
            pass
            #question_csv_list()
        else:
            question_csv_list()
#is_file_older_than_x_days("./archive/question_answer_data.csv")