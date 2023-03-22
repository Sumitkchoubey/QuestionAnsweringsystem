import pandas as pd
import random
import nltk
import string
from nltk.corpus import stopwords 
import gensim
from gensim import corpora, models, similarities
import numpy as np
import logging
import re
#import warnings
#warnings.simplefilter('ignore')


class TfIdfPredict:

    def __init__(self,file_name):
        self.newstopwords = set(stopwords.words('english'))
        self.WNlemma = nltk.WordNetLemmatizer()
        #self.file_name=file_name
        self.file_name=file_name
         
        self.model_path = './document_ranking/'+self.file_name+'/'
        self.index = None
        self.corpus_lsi = None
        self.lsi = None
        self.corpus_tfidf = None
        self.tfidf = None
        self.corpus = None
        self.dictionary = None
        self.df = None
        self.load_model()
        #logging.info("tfidf model fetch successful")
    def pre_process(self,text):
        tokens = nltk.word_tokenize(text)
        #print(tokens)
        tokens=[self.WNlemma.lemmatize(t) for t in tokens]
        #print(tokens)
        tokens= [ t for t in tokens if t not in string.punctuation ]
        #print(tokens)
        tokens=[word for word in tokens if word.lower() not in self.newstopwords]
        #print(tokens)
        return(tokens)

    def load_model(self):
        self.df = pd.read_pickle(self.model_path+'/df.pckl')
        self.dictionary = corpora.Dictionary.load(self.model_path+'/mydict.dict')
        #logging.info("model load")
        self.corpus = corpora.MmCorpus(self.model_path+'/bow_corpus.mm')
        #logging.info("model load")
        self.tfidf = models.TfidfModel(self.corpus)
        #logging.info("model load")
        self.corpus_tfidf = self.tfidf[self.corpus]
        self.lsi = models.LsiModel.load(self.model_path+'/lsi')
        self.corpus_lsi = self.lsi[self.corpus_tfidf]
        self.index = similarities.MatrixSimilarity(self.corpus_lsi)
        logging.info("tfidf model fetch successful")
        #logging.error("false")
    
    def retrive(self,test_set_sentence):
        #qa=test_set_sentence.split()
        #q_list=[1]
        #n=q_list[0]
        #A=qa[:n]
        #qa=qa[1:]
        #test_set_sentence = " ".join(qa)
         
        tokens = self.pre_process(test_set_sentence)
        texts = " ".join(tokens) 
        vec_bow = self.dictionary.doc2bow(texts.split())
        vec_tfidf = self.tfidf[vec_bow]
        vec_lsi = self.lsi[vec_tfidf]
        sims = self.index[vec_lsi]
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        index_s =[]
        score_s = []
        for i in range(len(sims)):
            #x = sims[i][1]
            # If similarity is less than 0.5 ask user to rephrase.
            index_s.append(str(sims[i][0]))
            score_s.append(str(sims[i][1]))
            reply_indexes = pd.DataFrame({'index': index_s,'score': score_s})
           # print(reply_indexes)
        temp=[]
        index=[]
        for i in range(3):
            r_index = int(reply_indexes['index'].loc[i])
            r_score = float(reply_indexes['score'].loc[i])
            reply = str(self.df.iloc[:,1][r_index])
            #reply.strip('\n\n')
            #print(reply)
            #print(r_index)
            index.append(r_index)
            
            #print(r_score)
            temp.append(reply)
        #print(temp)
    
        #logging.error("fetch tfidf unsuccessful")
             
             
              
        return temp ,index

        
            
#t1 = TfIdfPredict()
#var=t1.retrive('what is the relation between Mike and rich dad ?')
