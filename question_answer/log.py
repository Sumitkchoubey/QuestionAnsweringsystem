import logging
import sys
import os
sys.path.append('./log')
def log_file():
    dirName = './log/'
    if not os.path.exists(dirName):
            os.mkdir(dirName)
            print("Directory " , dirName ,  " Created ")
    else:  
         pass  
            #print("Directory " , dirName ,  " already exists")
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    #FORMAT = '%(asctime)-15s:%(message)s'
    file_name='./log/quans.log'
    logging.basicConfig(filename =file_name,level = logging.INFO,format='%(levelname)s:%(asctime)s:%(message)s') 
    ignore=['gensim','pytorch-pretrained-bert','bert-base-uncased','short_answer/modeldir/','urlib3']
    #p#rint("dert")
    for i in ignore:
          #print(i)
          logging.getLogger(i).setLevel(logging.CRITICAL)
#logging.debug('A debug message')
#logging.info('Some information')
#logging.warning('A shot across the bows')