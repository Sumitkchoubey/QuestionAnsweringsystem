import natsort
import glob
import pandas as pd
import random
import nltk
import string
from nltk.corpus import stopwords
import gensim
from gensim import corpora, models, similarities
from gensim.models import LsiModel
from gensim.models import doc2vec
import numpy as np
import warnings
import os
import  sys
sys.path.append('./text')
warnings.simplefilter('ignore')
import re
import logging

class TfIdfModel:
    #print(file_name)

    def __init__(self,file_name):
        self.newstopwords = set(stopwords.words('english'))
        self.WNlemma = nltk.WordNetLemmatizer()
        self.file_name=file_name
        #print(self.file_name)

    def load_texts(self):
        dirName = './document_ranking/'+self.file_name
       # print(dirName)
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            print("Directory " , dirName ,  " Created ")
        else:    
            print("Directory " , dirName ,  " already exists")
        temp = []
        for each_text in natsort.natsorted(glob.glob('./text/'+self.file_name+'/*.txt')):
            #print("enter text")
            with open(each_text,encoding="utf-8") as fp:
                file_ = fp.read().splitlines()
                #file_=[self.WNlemma.lemmatize(t) for t in file_]                #print(file_)
                #file_=file_.decode(encoding='UTF-8',errors='strict')
            _id = each_text.split('.txt')[0].split('_')[-1]
            #file_ = file_[3:-3]
            text = ' '.join(file_)
            temp.append([int(_id), text])
        return temp

    def convert2dataframe(self):
        data = self.load_texts()
        df = pd.DataFrame(data, columns=['_id', 'text'])
        #df.text = df.text.astype(str).str.lower()
        df = df.sort_values(['_id']).reset_index(drop=True)
        return df

    def pre_process(self, text):
        tokens = nltk.word_tokenize(text)
        tokens = [self.WNlemma.lemmatize(t) for t in tokens]
        tokens = [t for t in tokens if t not in string.punctuation]
        tokens = [word for word in tokens if word.lower()
                  not in self.newstopwords]
        return(tokens)

    def gen_model(self):
        temp=[]
        df = self.convert2dataframe()
        df['processed'] = df['text'].apply(self.pre_process)
        question = df['processed']
        #df['text']=df['text'].apply(self.pre_process)
        #for i in df['text']:
                 # v=' '.join(i)
                  #temp.append(v)
       # df['text']=temp          

        dictionary = corpora.Dictionary(question)
        #print(dictionary)
        corpus = [dictionary.doc2bow(a) for a in question]
        #print(corpus)
        tfidf = models.TfidfModel(corpus)
        # Save the Dict and Corpus
        dictionary.save('./document_ranking/'+self.file_name+'/mydict.dict')  # save dict to disk
        corpora.MmCorpus.serialize(
            './document_ranking/'+self.file_name+'/bow_corpus.mm', corpus)  # save corpus to disk
        corpus_tfidf = tfidf[corpus]
        lsi =models.LsiModel(
            corpus_tfidf, id2word=dictionary, num_topics=650)  # Threshold A
        corpus_lsi = lsi[corpus_tfidf]
        _ = similarities.MatrixSimilarity(corpus_lsi)
        lsi.save('./document_ranking/'+self.file_name+'/lsi')
        df.to_pickle('./document_ranking/'+self.file_name+'/df.pckl')
        logging.info("create tfidf successful")
       # logging.error(" create  tfidf unsccessful")

#if __name__ == "__main__":
    #t1 = TfIdfModel()
    #t1.gen_model()
