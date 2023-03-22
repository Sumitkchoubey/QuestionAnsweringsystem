from sklearn.metrics.pairwise import cosine_similarity
import tensorflow_hub as hub
import tensorflow as tf
import pandas as pd
import numpy as np
import glob
import os
import urllib.request
import tarfile
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
  elmo = hub.Module("elmo_module/", trainable=True)     
  embeddings=elmo(x, signature="default", as_dict=True)["elmo"]
  
  with  tf.compat.v1.Session() as sess:
    sess.run(tf.compat.v1.global_variables_initializer())
    sess.run(tf.compat.v1.tables_initializer ())
    # return average of ELMo features
    return sess.run(tf.reduce_mean(embeddings,1))
def question_csv_list(file_name):
    if (file_name==None):
        all_files = glob.glob("archive" + "/*.csv")
        #print(all_files)
        for filename in all_files:
            df = pd.read_csv(filename,  names=['question','answer','page'] )
        question_set=[]
        for i in df['question']:
             question_set.append(i)
        question_set=[question_set]
        question_set_vector=[]
        for i in range(len(question_set)):
            question_set_vector.append(elmo_vectors(question_set[i]))
        question_set_length=len(df['question'])
        return question_set_vector , question_set_length ,df['question']
    else:
         
        all_files=glob.glob("archive" +"/"+file_name+".csv")
        for filename in all_files:
            df = pd.read_csv(filename,  names=['question','answer','page'] )
        question_set=[]
        for i in df['question']:
             question_set.append(i)
        question_set=[question_set]
        print(question_set)
        question_set_vector=[]
        for i in range(len(question_set)):
            question_set_vector.append(elmo_vectors(question_set[i]))
        question_set_length=len(df['question'])
        return question_set_vector , question_set_length,df
def input_question(question):
    question_data=[[question]]
    question_data_vector=[]
    for i in range(len(question_data)):
        question_data_vector.append(elmo_vectors(question_data[i]))
    return question_data_vector
def match_question(question,file_name):
    print(file_name)
    question_data_vector=input_question(question)
    if (file_name==None):
        question_set_vector,question_set_length,df=question_csv_list(None)
        question_list=np.array(question_set_vector)
        question_input=np.array(question_data_vector)
        question_list=np.reshape(question_list,(question_set_length,1024))
        #question_list.ndim
        question_input=np.reshape(question_input,(1,1024))
        question_match_vector=cosine_similarity(question_list,question_input)
        question_match_vector=question_match_vector.tolist()

        question_value_sort = [val for sublist in question_match_vector for val in sublist]
        #print(question_value_sort)
        sorted_question=sorted(range(len(question_value_sort)), key=lambda i: question_value_sort[i])[-1:]
        print(sorted_question)
        temp=[]
        for i in sorted_question:
            r=df.iloc[[i]]
            temp.append(r.values)
        sort_question = [val for sublist in temp for val in sublist]
        return sort_question
    else:
        file_name=file_name.split()
        #print(file_name)
        value=[]
        for i in file_name:
            temp=[]
            all_files=glob.glob("archive" +"/"+i+".csv")
            if len(all_files)==0:
                data = {"question":question,"ans":"No answer","page":"Empty","source_file":i}
                value.append(data)
            else:
                question_set_vector,question_set_length,df=question_csv_list(i)
                question_list=np.array(question_set_vector)
                print(question_list)
                question_input=np.array(question_data_vector)
                question_list=np.reshape(question_list,(question_set_length,1024))
                question_input=np.reshape(question_input,(1,1024))
                question_match_vector=cosine_similarity(question_list,question_input)
                question_match_vector=question_match_vector.tolist()
                print(question_match_vector)
                question_value_sort = [val for sublist in question_match_vector for val in sublist]
                
                sorted_question=sorted(range(len(question_value_sort)), key=lambda i: question_value_sort[i])[-1:]
                print(sorted_question)
                temp2=[]
                for j in sorted_question:
                    question=df['question'].iloc[[j]]
                    question_values=question.values.tolist()
                    question_values=" ".join(question_values)
                    answer=df['answer'].iloc[[j]].isnull()
                    if (answer.values==True):
                        data = {"question":question_values,"ans":"No answer","page":"Empty","source_file":i}
                    else:
                        answer=df['answer'].iloc[[j]]
                        answer_values=answer.values.tolist()
                        answer_values=" ".join(answer_values)
                        page_number=df['page'].iloc[[j]]
                        page_number=page_number.values.tolist()
                        page_number=" ".join(page_number)
                        data = {"question":question_values,"ans":answer_values,"page":page_number,"source_file":i}
                        print(data)
                        return data
          
#match_question("who give you intelligence of reading of book ?",'hill-think-and-grow-rich')
        
