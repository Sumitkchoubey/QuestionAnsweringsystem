from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.tokenizabledoc.simple_tokenizer import SimpleTokenizer
from pysummarization.abstractabledoc.top_n_rank_abstractor import TopNRankAbstractor
import logging
def estract(document):
      auto_abstractor = AutoAbstractor()
# Set tokenizer.
      auto_abstractor.tokenizable_doc = SimpleTokenizer()
# Set delimiter for making a list of sentence.
      auto_abstractor.delimiter_list = [".", "\n"]
# Object of abstracting and filtering document.
      abstractable_doc = TopNRankAbstractor()
# Summarize document.
      result_dict = auto_abstractor.summarize(document, abstractable_doc)
      temp=[]
      if result_dict:
# Output result.
           for sentence in result_dict["summarize_result"]:
                  temp.append(sentence)
           logging.debug("find long answer")
      else:
            loggging.error ("can not find answer")           
      #print(temp)

      return temp