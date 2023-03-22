from flask import Flask, request
from flask_cors import CORS
import json, re
import tensorflow as tf
import sys
import os 
import re
import hashlib
from utils.pdf_checker import pdfChecker
from utils.qlist import  input_question
sys.path.append('./document_ranking')
sys.path.append('./text')
from utils.question_answer_list import question_csv_list,is_file_older_than_x_days
from flask_basicauth import BasicAuth
from flask import request
import configparser
import  logging
from log import log_file
import urllib.request
import shutil
app = Flask(__name__)
cors = CORS(app)
config = configparser.ConfigParser()
config.read('config.ini')
app.url_map.strict_slashes = False
ALLOWED_EXTENSIONS = set(['pdf'])
global graph
graph = tf.compat.v1.get_default_graph()
q_map = {}
#global question_answer_data
#question_answer_data=question_csv_list()
@app.route('/quans/question_list/',methods=['POST'])
def question_list():
    is_file_older_than_x_days("./archive/question_answer_data.csv")
    output_map ={}
    json_data = request.get_json(force=True)
    #question_answer_data=question_csv_list()
    question = json_data.get('question', '')
    pdf_list=request.args.get('pdf_list','')
    first_pdf=hashlib.md5("hill-think-and-grow-rich.pdf".encode())
    first_pdf=first_pdf.hexdigest()
    second_pdf=hashlib.md5("Short-stories.pdf".encode())
    second_pdf=second_pdf.hexdigest()
    third_pdf=hashlib.md5("Darigold-Travel-Policy-Final-Oct-2014.pdf".encode())
    third_pdf=third_pdf.hexdigest()
    temp=[{'_id':first_pdf,"name":"Think And Grow Rich, Napoleon Hill","source_name":"hill-think-and-grow-rich.pdf"},{'_id':second_pdf,"name":"Short Stories, O Henry","source_name":"Short-stories.pdf"},{'_id':third_pdf,"name":"Darigold Travel Policy, Darigold","source_name":"Darigold-Travel-Policy-Final-Oct-2014.pdf"}]
    res =pdf_list.split()
    temp4=[]
    for j in res:
        limited_list = [element['name'] for element in temp if element['_id'] == j]
        temp4.append(limited_list) 
    source_name = [val for sublist in temp4 for val in sublist]
    answer=[]
    for i in source_name:
        similar_question=input_question(question,i)
        answer.append(similar_question)
    question_data = [val for sublist in answer for val in sublist] 
    output_map.update({"res": question_data})
    json_string = json.dumps(output_map)
    logging.error("pdf_files")
    return json_string ,  {'Content-type': 'application/json', 'Accept': 'text/plain'}            
@app.route('/quans/',methods=['POST'])
def quans():
    start_page=1
    page_number=start_page
    file_dir=config['session']['file_dir']
    log_file()        
    with graph.as_default():
      logging.info('Started')
      output_map ={}
      json_data = request.get_json(force=True)
      question = json_data.get('question', '')
      text =question
      file_name=config['session']['file_dir']
      page_number=int(config['session']['start_page'])
      rtn = re.split('([.!?] *)', text)
      question = ''.join([i.capitalize() for i in rtn])
      question=" ".join(question.split())
      words=request.args.get('words','')
      qtype=request.args.get('qtype','')
      pdf_list=request.args.get('pdf_list','')
      first_pdf=hashlib.md5("hill-think-and-grow-rich.pdf".encode())
      first_pdf=first_pdf.hexdigest()
      second_pdf=hashlib.md5("Short-stories.pdf".encode())
      second_pdf=second_pdf.hexdigest()
      third_pdf=hashlib.md5("Darigold-Travel-Policy-Final-Oct-2014.pdf".encode())
      third_pdf=third_pdf.hexdigest()
      temp=[{'_id':first_pdf,"name":"Think And Grow Rich, Napoleon Hill","source_name":"hill-think-and-grow-rich.pdf"},{'_id':second_pdf,"name":"Short Stories, O Henry","source_name":"Short-stories.pdf"},{'_id':third_pdf,"name":"Darigold Travel Policy, Darigold","source_name":"Darigold-Travel-Policy-Final-Oct-2014.pdf"}]
      res =pdf_list.split()
      temp2=[]
      for i in res:
        limited_list = [element['source_name'] for element in temp if element['_id'] == i]
        temp2.append(limited_list)
      temp4=[]
      for j in res:
        limited_list = [element['name'] for element in temp if element['_id'] == j]
        temp4.append(limited_list)
      flatten_matrix = [val for sublist in temp2 for val in sublist]   
      flatten_matrix2 = [val for sublist in temp4 for val in sublist]
      answer1=pdfChecker(question,words,qtype,file_name,page_number,file_dir,flatten_matrix,flatten_matrix2)
      answer=answer1.pdf_check()
      output_map.update({"res": answer})
      json_string = json.dumps(output_map)
      logging.info('Finished')
      return json_string ,  {'Content-type': 'application/json', 'Accept': 'text/plain'}
@app.route('/quans/pdf_files',methods=['GET'])
def pdf_file():
    log_file()
    logging.info('list of Pdf files')
    output_map={}
    first_pdf=hashlib.md5("hill-think-and-grow-rich.pdf".encode())
    first_pdf=first_pdf.hexdigest()
    second_pdf=hashlib.md5("Short-stories.pdf".encode())
    second_pdf=second_pdf.hexdigest()
    third_pdf=hashlib.md5("Darigold-Travel-Policy-Final-Oct-2014.pdf".encode())
    third_pdf=third_pdf.hexdigest()
    temp=[{'_id':first_pdf,"name":"Think And Grow Rich, Napoleon Hill","source_name":"hill-think-and-grow-rich.pdf"},{'_id':second_pdf,"name":"Short Stories, O Henry","source_name":"Short-stories.pdf"},{'_id':third_pdf,"name":"Darigold Travel Policy, Darigold","source_name":"Darigold-Travel-Policy-Final-Oct-2014.pdf"}]
    output_map.update({"res": temp})
    json_string = json.dumps(output_map)
    logging.error("pdf_files")
    return json_string ,  {'Content-type': 'application/json', 'Accept': 'text/plain'}
@app.route('/quans/upload_files',methods=['GET'])
def upload_file():
    log_file()
    logging.info('Upload _file')
    output_map={}
    file=request.args.get('file','')
    url=file
    url_split=url.split('/')
    file_name=str(url_split[-1])
    check=file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    file_dir='./text/'+file_name
    if not  os.path.exists(file_dir):
        if (check==True):
            with urllib.request.urlopen(url) as response, open('./text/'+ file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            output_map.update({"res": "file uploaded"})
            json_string = json.dumps(output_map)
            logging.error("uploaded file")
            return json_string ,  {'Content-type': 'application/json', 'Accept': 'text/plain'}
        else:
            output_map.update({"res": "Please upload pdf file"})
            json_string = json.dumps(output_map)
            logging.error("No pdf file")
            return json_string ,  {'Content-type': 'application/json', 'Accept': 'text/plain'}
    else:
        output_map.update({"res": "file already Exists"})
        json_string = json.dumps(output_map)
        logging.error("file exists")
        return json_string ,  {'Content-type': 'application/json', 'Accept': 'text/plain'}
@app.route('/quans/ping',methods=['GET'])
def get():
    return "successsss!!"
if __name__ == '__main__':
    app.run(host=config['admin']['host'],port=config['admin']['port'],debug=True)#debug=True, port=config['admin']['port'])
     