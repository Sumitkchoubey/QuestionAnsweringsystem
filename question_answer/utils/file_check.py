import pandas as pd
import os
import sys
import ast 
import re
sys.path.append('./short_answer')
from short_answer.core import coreml
import hashlib
def is_exist():
    dirName = './archive/'
    if not os.path.exists(dirName):
            os.mkdir(dirName)
            print("Directory " , dirName ,  " Created ")
    else:  
         pass  
            #print("Directory " , dirName ,  " already exists")
    fn="./archive/question_answer_data.csv"
    try:
        fh = open(fn,'r')
    except:
# if file does not exist, create it
       fh = open(fn,'w')
       pass
    return fn
def check_file(question,words,file_name,page_number,pdf_pages,pdf_filename):
    file=is_exist()
    pdf_file_name=hashlib.md5(pdf_filename.encode())
    pdf_file_name=pdf_file_name.hexdigest()
    data = pd.read_csv(file,header=None,names=['pdf_name','question','answer','page']) 
    data=data.dropna()
    data=data.loc[data['pdf_name'] == pdf_file_name]
    data = data.reset_index(drop=True)
    iloc=data[data['question'] == question].index
    if (not len(iloc)) :
        answer1=coreml(question,words,file_name,page_number,pdf_pages,pdf_filename)
        for each  in answer1:
            each['page']=[each['page']]
        answer=answer1
        paragraphs = {}
        page=[]
        for i in range(len(answer)):
                  page.extend(answer[i]['page'])
        paragraphs['page']=page
        question =question
        rtn = re.split('([.!?] *)', question)
        question = ''.join([i.capitalize() for i in rtn])
        question=" ".join(question.split())
     
        question=question.lower()
        quote=[]
        for i in range(len(answer)):
                v=answer[i]['ans']
                quote.append(v)
        answer=' '.join(quote) 
        paragraphs['answer']=answer
        quote2=[]
        paragraphs['question'] = question # 2
        paragraphs['pdf_filename'] = pdf_file_name
        paragraphs['pdf_file']=pdf_filename
        output = pd.DataFrame([paragraphs],columns=['pdf_file','pdf_filename','question','answer','page'])
        output.to_csv(file,mode='a',index=False,header=False)
        return answer1
         
    else:
        arch = data.loc[iloc,'answer'].values
        page=data.loc[iloc,'page'].values
        temp=[]
        if arch:
            answer=arch[0]
            page=page[0]
            page = ast.literal_eval(page)
            text = answer
            rtn = re.split('([.!?] *)', text)
            answer = ''.join([i.capitalize() for i in rtn])
            res=[]
            temp=[]
            data = {"ans":answer,"prob":0.5214,"page":page,"source_file":pdf_filename}
            res.append(data)
            temp.append(res)
            return res
        else:
            data.drop(iloc)
       