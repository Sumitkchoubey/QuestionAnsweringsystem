import sys
import os
import logging.handlers
sys.path.append('./extractive_summery')
sys.path.append('./short_answer')
sys.path.append('./extractive_summery')
from extractive_summery.test1 import file_create
import os 
sys.path.append('./utils')
sys.path.append('./document_ranking')
from document_ranking.create_tfidf import TfIdfModel
sys.path.append('./document_ranking')
sys.path.append('./ques_classification')
from ques_classification.question_classification import ques_classfi
sys.path.append('./text')
import logging
from PyPDF2 import PdfFileReader
from utils.file_check import check_file
def upload_file(file_location,page_number):

      for i in file_location:

          new_file1=i.split('.pdf')
          new_filename=new_file1[0]
          page_number=int(page_number)
          dirName = './document_ranking/'+new_filename
          if not os.path.exists(dirName):
                os.mkdir(dirName)
                t1 = TfIdfModel(new_filename)
                t1.gen_model()
                logging.info("tfidf model created")
          else:
                pass
def removeElements(A, B): 
       for i in range(len(B)-len(A)+1): 
            for j in range(len(A)): 
                if B[i + j] != A[j]: 
                       break
                else: 
                      return True
       return False
 
#def checker_question(question,words,qtype,file_name,page_number,file_dir):
def checker_question(temp):
    question=temp[0]
    words=temp[1]
    qtype=temp[2]
    file_name=temp[3]
    page_number=temp[4]
    file_dir=temp[5]
    pdf_filename=temp[6]
     
    #print(dirName)
    #if   os.path.exists(dirName):
       # print("yes")
        #similar_question=match_question(question,file_name)
        #similar_question_data.append(similar_question)
        #return similar_question_data
    #else:
     #   pass       
    if question.strip():
                  pass
        #print("it's not an empty or blank string")
    else:
        res=[]
        data = {"ans":"Please Select Question"}
        res.append(data)
        return res
    inputpdf = PdfFileReader(open(file_dir, "rb"))
    pdf_pages=inputpdf.numPages
    new_filename=file_name
    if words:
            words=words
    else:
        words=200
    
    question=question.lower()
    question_type=ques_classfi(question)
    if (question_type=='DESCRIPTION'):
        if (qtype=='short'):
            answer1=check_file(question,words,new_filename,page_number,pdf_pages,pdf_filename)
            v=answer1
            logging.info('short answer')
            return v
        else:
            v,index=file_create(question,words,new_filename,page_number,pdf_pages)
            res=[]
            data = {"ans":v,"prob":0.512,"page":index,"source_file":pdf_filename}
            res.append(data)
            logging.info('extract summery')
            return res
    else:
        if (qtype=='long'):
            v,index=file_create(question,words,new_filename,page_number,pdf_pages)
            #print(v)
           
            res=[]
            data = {"ans":v,"prob":0.5234,"page":index,"source_file":pdf_filename}
            res.append(data)
            logging.info('extract summery')
            return  res
        else:
            answer1=check_file(question,words,new_filename,page_number,pdf_pages,pdf_filename)
            logging.info('short answer')
            return answer1
 