from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import sys, getopt
import shutil
from PyPDF2 import PdfFileWriter, PdfFileReader
import time
class split:
    
    def __init__(self, filename,input_setence,file_name):
        self.filename = filename
        self.file_name=file_name
        self.input_setence=input_setence   
    def splitpdf(self):
        temp=[]
        inputpdf = PdfFileReader(open(self.filename, "rb"))
        x=inputpdf.numPages
        dirName = './text/'+ self.file_name+'/temp/'
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            print("Directory " , dirName ,  " Created ")
        else:    
            print("Directory " , dirName ,  " already exists")
        for i in range(x):
            temp.append(i)
        while(self.input_setence<len(temp)):
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(self.input_setence))
            self.input_setence = self.input_setence + 1 
            new_filename = self.filename.split('/')[-1]
            new_filename = new_filename.split(".")[0]+'_{}'.format(self.input_setence)+'.pdf'
            with open('./text/'+ self.file_name+'/temp/'+new_filename, "wb") as outputStream:
                    output.write(outputStream)
class pdftotext(split):
    
        
    
    def __init__(self, filename,input_setence,file_name):
        split.__init__(self,filename,input_setence,file_name)
        split.splitpdf(self)
        self.pdfDir ='./text/'+file_name+'/temp/'
        self.txtDir='./text/'+file_name+ '/'
        self.createDir()
        self.convertMultiple()
        shutil.rmtree(self.pdfDir)# delete temp folder

    def createDir(self):
        if not os.path.exists(self.txtDir):
            os.mkdir(self.txtDir)
            print("Directory " , self.txtDir ,  " Created ")
        else:    
            print("Directory " , self.txtDir ,  " already exists")
        
    
    def convert(self,fname, pages=None):
        if not pages:
            pagenums = set()
        else:
            pagenums = set(pages)

        output = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)
        infile = open(fname, 'rb')
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
        infile.close()
        converter.close()
        text = output.getvalue()
        output.close
        return text 
    
    def convertMultiple(self):
        #print(self, 'convertMultiple')
        t1=time.time()
        #p = multiprocessing.Pool()
        if self.pdfDir == "": self.pdfDir = os.getcwd() + "\\" #if no pdfDir passed in 
        for pdf in os.listdir(self.pdfDir):#iterate through pdfs in pdf directory
            #temp.append(pdf)
            #print(temp)
        #for pdf in glob.glob(self.pdfDir):
            fileExtension = pdf.split(".")[-1]
            if fileExtension == "pdf":
                pdfFilename = self.pdfDir + pdf 
                text = self.convert(pdfFilename) #get string of text content of pdf
                new_filename = self.txtDir + pdf
                new_filename = new_filename.split('.pdf')[0]
                textFilename = new_filename + ".txt"
                textFile = open(textFilename, "w",encoding='utf-8') #make text file
                textFile.write(text) #write text to text file
        #print("the timw",time.time()-t1)
#pdftotext('Rich-Dad-Poor-Dad-eBook.pdf',6)