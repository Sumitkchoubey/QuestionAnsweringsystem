import os
import sys
from utils.checker  import  checker_question
from utils.pdftotext import pdftotext
#from validate import 
#from  multiprocessing  import Pool
import multiprocessing
import  ast
import sys
import logging
sys.path.append('./extractive_summery')
sys.path.append('./short_answer')
sys.path.append('./extractive_summery')
import os 
sys.path.append('./utils')
#sys.path.append('./ml')
#from core import coreml
sys.path.append('./document_ranking')
from document_ranking.create_tfidf import TfIdfModel
sys.path.append('./document_ranking')
sys.path.append('./ques_classification')
#from question_classi import question_classifi
from utils.validdate import  header_delete,remove_empty_lines,footer_delete
import multiprocessing_logging
multiprocessing_logging.install_mp_handler()
from multiprocessing_logging import install_mp_handler
#from match_question import match_question
sys.path.append('./text')

class pdfChecker:

    def __init__(self,question,words,qtype,file_name,page_number,file_dir,pdf_name,pdf_filename):
        self.question = question
        self.words=words
        self.qtype=qtype
        self.file_name=file_name
        self.page_number=page_number
        self.file_dir=file_dir
        self.pdf_name=pdf_name
        self.pdf_filename=pdf_filename
        #self.elmo=elmo

    def pdf_check(self):
        temp=[]
        for i,j in zip(self.pdf_name,self.pdf_filename):
            value='./text/' +i
            new_file1=i.split('.pdf')
            new_filename=new_file1[0]
            pdfdir='./text/'+new_filename+'/'
            if os.path.exists(pdfdir):
                pass
            else:
                os.mkdir(pdfdir)
                pdftotext2=pdftotext(value,self.page_number,new_filename) 
                remove_empty_line=remove_empty_lines(new_filename)
                header_file=header_delete(new_filename)
                footer_file=footer_delete(new_filename)
            dirName = './document_ranking/'+new_filename
            if not os.path.exists(dirName):
                os.mkdir(dirName)
                t1 = TfIdfModel(new_filename)
                t1.gen_model()
            else:
                pass
            logging.info("tfidf model created")

            tap=[self.question,self.words,self.qtype,new_filename,self.page_number,value,j]
            #answer=checker_question(question,words,qtype,new_filename,page_number,value)
            temp.append(tap)
        temp3=checker(temp)
        value = [val for sublist in temp3 for val in sublist] 
        v=len(value)
        if (v>1):
            #flatten_matrix = [val for sublist in temp3 for val in sublist] 
            flatten_matrix= ", ".join(repr(e) for e in value)
            flatten_matrix=ast.literal_eval(flatten_matrix)
            return flatten_matrix
        else:
         # flatten_matrix = [val for sublist in temp3 for val in sublist] 
          flatten_matrix= ", ".join(repr(e) for e in value)
          flatten_matrix=ast.literal_eval(flatten_matrix)
          flatten_matrix=[flatten_matrix]
          return flatten_matrix 
def checker(temp):
        v=(multiprocessing.cpu_count()-1)
        install_mp_handler()
        logging.info("going into multiprocessing")
        pool = multiprocessing.Pool(processes = 2,initargs=[...])
        answer_value=(pool.map(checker_question, temp))
        return answer_value