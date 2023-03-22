from sklearn.metrics.pairwise import cosine_similarity
import tensorflow_hub as hub
import tensorflow as tf
import pandas as pd
import numpy as np
import glob
import os
import urllib.request
import tarfile
import hashlib
from annoy import AnnoyIndex
def download_elmo():
    elmo_folder='./elmo_module/'
    if os.path.exists(elmo_folder):
        pass
    else:
        os.mkdir(elmo_folder)
    elmo_file='./elmo_module/2.tar.gz'
    if  not os.path.exists(elmo_file):
        url="https://storage.googleapis.com/tfhub-modules/google/elmo/2.tar.gz"
        urllib.request.urlretrieve(url,elmo_folder)
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
    sess.run(tf.compat.v1.global_variables_initializer())
    sess.run(tf.compat.v1.tables_initializer ())
    # return average of ELMo features
    return sess.run(tf.reduce_mean(embeddings,1))

def question_csv_list():
    all_files = glob.glob(("./archive" +"/*.csv"))
     
     
    for filename in all_files:
            
            df = pd.read_csv(filename,  names=['question','answer','page'] )
            filename=filename.split('archive\\')
            filename=" ".join(filename)
            filename=filename.split('.csv')
            file_name=filename[0]
            v=file_name+'.npy'
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
                np.save(file_name,question_list)
                D=1024
                NUM_TREES=10
                ann = AnnoyIndex(D)
                data=np.load(file_name+'.npy')
                for index, embed in enumerate(data):
                        ann.add_item(index, embed)
                ann.build(NUM_TREES)
                search=ann.save(file_name+'.ann')
            else:
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
                np.save(file_name,question_list)
                D=512
                NUM_TREES=512
                ann = AnnoyIndex(D)
                data=np.load(file_name+'.npy')
                for index, embed in enumerate(data):
                        ann.add_item(index, embed)
                ann.build(NUM_TREES)
                search=ann.save(file_name+'.ann')

#question_csv_list()
def input_question(question):
    data="archive/ question_answer_data.ann"
    if(os.path.exists(data)):
        print("yes")
    question_data=[[question]]
    question_data_vector=[]
    for i in range(len(question_data)):
        question_data_vector.append(elmo_vectors(question_data[i]))
    question_input=np.array(question_data_vector)
    question_input=np.reshape(question_input,(1,1024))
    print(question_input)
    D=1024
    u = AnnoyIndex(D)
    u.load(data)
    temp=pd.read_csv('hill-think-and-grow-rich.csv',  names=['question','answer','page'] )
    nns= u.get_nns_by_vector(question_input[0],1)
    key=temp.iloc[nns].values
    d=key.tolist()
    flatten_matrix = [val for sublist in d for val in sublist]
    data= {"question":flatten_matrix[0],"ans":flatten_matrix[1],"page":flatten_matrix[2]}
    print(data)
     
    
v=input_question(('what is sixth sense ?'))