import re
from collections import defaultdict
 
 
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
 
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer

from nltk.corpus import stopwords
stop_words = stopwords.words('english')

def text_summary(data):
    language="english"
    parser = PlaintextParser(data, Tokenizer(language))
    sentence_count=6
    summarizer_2 = LsaSummarizer(Stemmer(language))
    summarizer_2.stop_words = get_stop_words(language)
    summary_2 = summarizer_2(parser.document, sentence_count)
    temp=[]
    for sentence in summary_2:
          temp.append(sentence)
    summ=' '.join(map(str, temp))
    return summ
