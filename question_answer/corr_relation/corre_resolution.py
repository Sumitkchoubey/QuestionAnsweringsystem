from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')


def resolve(corenlp_output):
    """ Transfer the word form of the antecedent to its associated pronominal anaphor(s) """
    for coref in corenlp_output['corefs']:
        mentions = corenlp_output['corefs'][coref]
        antecedent = mentions[0]  
        for j in range(1, len(mentions)):
            mention = mentions[j]
            if mention['type'] == 'PRONOMINAL':
                
                target_sentence = mention['sentNum']
                target_token = mention['startIndex'] - 1
                
                corenlp_output['sentences'][target_sentence - 1]['tokens'][target_token]['word'] = antecedent['text']


def print_resolved(corenlp_output):
     
    possessives = ['hers', 'his', 'their', 'theirs']
    for sentence in corenlp_output['sentences']:
        for token in sentence['tokens']:
            output_word = token['word']
            
            if token['lemma'] in possessives or token['pos'] == 'PRP$':
                output_word += "'s"  # add the possessive morpheme
            output_word += token['after']
            v=output_word
            #print(v)
            print(output_word, end='')
            #return output_word
#def run():
text = "Dhoni made his ODI debut in December 2004 against Bangladesh. and played his first Test a year later against Sri Lanka. Dhoni has been the recipient of many awards, including the ICC ODI Player of the Year award in 2008 and 2009 (the first player to win the award twice), the Rajiv Gandhi Khel Ratna award in 2007, the Padma Shri, India's fourth highest civilian honour, in 2009 "

output = nlp.annotate(text, properties= {'annotators':'dcoref','outputFormat':'json','ner.useSUTime':'false'})
resolve(output)
temp=[]
temp.append(resolve(output))
print(temp)
#corre_resolutionresolve(output)
#print(corre_resolution)
        #return corre_resolution
#r=run()

#corre_resolution=resolve(output)


#print('Original:', text)
print('Resolved: ', end='')
#print(v)
print_resolved(output)
tokenized_text = word_tokenize(text)
classified_text = st.tag(tokenized_text)

print(classified_text)
#return corre_resolution