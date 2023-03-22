import configparser
import os
import sys
import re
import logging
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
sys.path.append('./document_ranking')
#sys.path.append('./bert-extractive-summarizer')
#from summarize import  *
from estra import  estract
#from summ_model import download_file
from TfIdfPredict import TfIdfPredict
import lxml.html
import re
from bs4 import BeautifulSoup
import glob
from gensim.summarization.summarizer import summarize 
from gensim.summarization import keywords 
from text_summ import text_summary

#from extract_summery import generate_summary
def file_create(question,words,file_name,page_number,delete_pages):
    pages = len(glob.glob('./text/'+file_name+'/*.txt'))
    #print(pages)
    #print(delete_pages)
    #download=download_file()
    t1 = TfIdfPredict(file_name)
    var , index=t1.retrive(question)
    #print(var)
    #print(index)
    temp=[]
    for i in range(len(index)):
                 index[i] += delete_pages - pages +1
                 temp.append(index[i])

    #print(var)
    variable=[]
    for i in var:
            #lines = i.readlines()
            #lines=''.join(lines)
            #print(lines)
            #remove_tags(fp)
            soup = BeautifulSoup(i)
            text=soup.get_text()
            variable.append(text)
    text=' '.join(variable)
    #print(text)
    v=int(words)
    dert=text_summary(text)
    temp2=[]
    temp2.append(dert)
    pattern = '[0-9]'
    dert = [re.sub(pattern, '', i) for i in temp2] 
    #dert=summarize(text,word_count=250)
    #print(dert)
    #est_sum=[]
    #est_sum.append(dert)
    #list2 = [x.replace('\n', '') for x in est_sum]
    #dert2=''.join(list2)
    #dert=[word.strip() for word in dert]
    #print(dert)
    dert=''.join(dert)
    text = dert
     
    rtn = re.split('([.!?] *)', text)
    #print(rtn)
    dert = ''.join([i.capitalize() for i in rtn])
    logging.debug("get answer")
    return dert ,temp
#print(der)