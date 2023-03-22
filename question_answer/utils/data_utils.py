import sys
sys.path.append('./document_ranking')
from document_ranking.TfIdfPredict import TfIdfPredict
from bs4 import BeautifulSoup
import  glob
def para_convert(question,file_name,page_number,delete_pages):
        pages = len(glob.glob('./text/'+file_name+'/*.txt'))
        t1 = TfIdfPredict(file_name)
        var, var2=t1.retrive(question)
        variable=[]
        for i in var:
            soup = BeautifulSoup(i)
            text=soup.get_text()
            #print(text)
            variable.append(text)
        temp=[]
        for i in range(len(var2)):
                 var2[i] +=delete_pages - pages +1
                 temp.append(var2[i])
        question_data=[]
        input_data=[]
        question_data.append(question)
        i=0
        para_list = map(lambda s: s.strip('\n\n'), variable)
        #print(para_list)
        for i in range(len(temp)):
         for para in para_list :
          
            if para:
                paragraphs = {}
                #splits = para.split('\nQuestions:')
                paragraphs['id'] = var2[i] # 2
                #print(paragraphs['id'])
                paragraphs['text'] = para # 2
                #print(paragraphs['text'] )
                #question=input("enter question")
                paragraphs['ques']=question_data # 1
               # print(paragraphs)
                input_data.append(paragraphs) 
            i+=1      
        return var2 ,input_data  
#fert=para_convert("who is mike")      
