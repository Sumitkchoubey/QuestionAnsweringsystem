import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import pickle
import os
import sys
sys.path.append('./ques_classification')
def ques_classfi(question):
    qn_df = pd.read_csv("./ques_classification/Question_Classification_Dataset.csv")
    qn_df = qn_df.iloc[:,1:]
    qn_df1 = qn_df[['Questions', 'Category0']]
    qn_df1.head()
    vect = TfidfVectorizer(ngram_range = (1,2)).fit(qn_df1['Questions'])
    input_data=[question]
    test_vector = vect.transform(input_data)
    loaded_model = pickle.load(open("./ques_classification/question_classify.pkl", 'rb'))
    pred1 = loaded_model.predict(test_vector)
    #pred1=''.join(pred1)
    #pred2=qn_df1['Category0'][pred1]
    #print(pred2)
    #print(pred1)
    temp=[]
    for i in pred1:
        v=qn_df1['Category0'][i]
        temp.append(v)
    temp1=''.join(temp)
    #print(temp1) 
    return temp1   
    #qn_df.head()
#question=ques_classfi('where dhoni lives?')