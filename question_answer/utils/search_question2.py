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
import sys
sys.path.append('./archive/')
from annoy import AnnoyIndex
def download_elmo():
    elmo_folder='elmo_module/'
    if os.path.exists(elmo_folder):
        pass
    else:
        os.mkdir(elmo_folder)
    elmo_file='elmo_module/2.tar.gz'
    if  not os.path.exists(elmo_file):
        url="https://storage.googleapis.com/tfhub-modules/google/elmo/2.tar.gz"
        urllib.request.urlretrieve(url,elmo_file)
        my_tar = tarfile.open('elmo_module/2.tar.gz')
        my_tar.extractall('elmo_module/') # specify which folder to extract to
        my_tar.close()
    else:
        pass
#elmo_download=download_elmo()
def elmo_vectors(x):
    elmo = hub.Module("elmo_module/", trainable=True)     
    embeddings=elmo(x, signature="default", as_dict=True)["elmo"]
    with  tf.compat.v1.Session() as sess:
        sess.run(tf.compat.v1.global_variables_initializer())
        sess.run(tf.compat.v1.tables_initializer ())
    # return average of ELMo features
        return sess.run(tf.reduce_mean(embeddings,1))
def input_question(question,file_data):
    data="archive/question_answer_data.ann"
    if (os.path.exists(data)):
        print("yes")
    
#v=input_question('what is sixth felling ?','b40f271feea9af6e03f16c95838a65e4')