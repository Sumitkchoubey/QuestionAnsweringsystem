import natsort
import glob
import os
import re
def header_delete(file_name):
    for each_text in natsort.natsorted(glob.glob('./text/'+file_name+'/*.txt')):
        with open(each_text, 'r+',encoding="utf-8") as f:
            data = f.readlines()
            for item in data[0:2]:
                if len(item.split())<=8:
                    with open(each_text, 'w+',encoding="utf-8") as fout:   
                        fout.writelines(data[2:])
                        p="complete"
                      
                else:
                    pass
    return p 

def footer_delete(file_name):
    for each_text in natsort.natsorted(glob.glob('./text/'+file_name+'/*.txt')):
        with open(each_text, 'r+',encoding="utf-8") as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            for item in last_line:
                if len(item.split())<=3:
                    with open(each_text, 'w+',encoding="utf-8") as fout:   
                        fout.writelines(lines[0:-1])
def check(file_name):
    temp=[]
    pages = len(glob.glob('./text/'+file_name+'/*.txt'))
    for each_text in natsort.natsorted(glob.glob('./text/'+file_name+'/*.txt')):
        with open(each_text,'r',encoding="utf-8") as fp:
                #lin=re.sub(r"[^a-zA-Z0-9]+", ' ', fp)
                lines = [line for line in fp][:1]
                search_words = ['contents']
                for line in lines:
                             if any(word in line.lower() for word in search_words):
                                            temp.append(each_text)
    return temp ,pages
def check_filedata(file_name):
    #if os.stat(file_name).st_size == 0:  
            #print(" Removing ",file_name)  
            #os.remove(file_name)
    remove_empty=remove_empty_lines(file_name) 
    each_text , pages=check(file_name)
    #print(pages)
    each_text1=len(each_text)
    #print(each_text1)
    for i in each_text:
           if len(i)== 0:
               pass
                               #print("empty")
           else:
                os.remove(i)
    return pages            
                                     #print("delete file")
    
     
def remove_empty_lines(file_name):
    #"""Overwrite the file, removing empty lines and lines that contain only whitespace."""
    for each_text in natsort.natsorted(glob.glob('./text/'+file_name+'/*.txt')):
        with open(each_text, 'r+',encoding="utf-8") as f:
                    lines = f.readlines()
                    f.seek(0)
                    f.writelines(line for line in lines if line.strip())
                    f.truncate()
        d="empty_delete"               
    return d 
                                                
