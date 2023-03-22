#!/usr/bin/env python
# coding: utf8
"""A simple example of extracting relations between phrases and entities using
spaCy's named entity recognizer and the dependency parse. Here, we extract
money and currency values (entities labelled as MONEY) and then check the
dependency tree to find the noun phrase they are referring to – for example:
$9.4 million --> Net income.

Compatible with: spaCy v2.0.0+
Last tested with: v2.2.1
"""
from __future__ import unicode_literals, print_function

import plac
import spacy
#from corre_resolution import  run

#text="Dhoni made his ODI debut in December 2004 against Bangladesh. and played his first Test a year later against Sri Lanka. Dhoni has been the recipient of many awards, including the ICC ODI Player of the Year award in 2008 and 2009 (the first player to win the award twice), the Rajiv Gandhi Khel Ratna award in 2007, the Padma Shri, India's fourth highest civilian honour, in 2009 "
#resolution=run(text)
#print(resolution)
#text=resolution.replace('.', ', ') 
#TEXTS=text.split(',')
TEXTS = [
    "To fetch a pail of water ",
    #"Revenue exceeded twelve billion dollars, with a loss of $1b."
]


@plac.annotations(
    model=("Model to load (needs parser and NER)", "positional", None, str)
)
def main(model="en_core_web_sm"):

    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
    print("Processing %d texts" % len(TEXTS))
    sen = nlp(u'')
    #for entity in sen.ents:
            #print(entity.text + ' - ' + entity.label_ + ' - ' + str(spacy.explain(entity.label_)))
    for entity in sen.ents:
         if entity.label_=='PERSON':
           print(entity.text + ' - ' + entity.label_ + ' - ' + str(spacy.explain(entity.label_)))

   # filter = {'ents': ['ORG']}
    for text in TEXTS:
        doc = nlp(text)
        #print(doc)
        relations = extract_currency_relations(doc)
        #print(relations)

        #for r1, r2 in relations:
            #print("{:<10}\t{}\t{}".format(r1.text, r2.ent_type_, r2.text))


def filter_spans(spans):
    # Filter a sequence of spans so they don't contain overlaps
    # For spaCy 2.1.4+: this function is available as spacy.util.filter_spans()
    get_sort_key = lambda span: (span.end - span.start, -span.start)
    sorted_spans = sorted(spans, key=get_sort_key, reverse=True)
    result = []
    seen_tokens = set()
    for span in sorted_spans:
        # Check for end - 1 here because boundaries are inclusive
        if span.start not in seen_tokens and span.end - 1 not in seen_tokens:
            result.append(span)
        seen_tokens.update(range(span.start, span.end))
    result = sorted(result, key=lambda span: span.start)
    return result


def extract_currency_relations(doc):
    # Merge entities and noun chunks into one token
    spans = list(doc.ents) + list(doc.noun_chunks)
    spans = filter_spans(spans)
    #print(spans)
    #temp=[]
    with doc.retokenize() as retokenizer:
        for span in spans:
            retokenizer.merge(span)
     
    relations = []
    entities = ["PERSON", "NORP",
                "FACILITY", "ORG",
                "GPE", "LOC",
                "PRODUCT", "EVENT",
                "WORK_OF_ART", "LAW",
                "LANGUAGE", "DATE",
                "TIME", "PERCENT",
                "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"]
    for entity_name in entities:
        for money in filter(lambda w: w.ent_type_ == entity_name, doc):
            print(money)
            if money.dep_ in ('attr', 'dobj', 'acomp'):
                subject = [w for w in money.head.lefts if w.dep_ == 'nsubj']
                print(subject)
                if subject:
                    subject = subject[0]
                    relations.append({"subject": subject.string.strip(), "object": money.string.strip(), "relation": entity_name})
                else:
                    subject = "N/A"
                    relations.append({"subject": "N/A", "object": money.string.strip(), "relation": entity_name})

            elif money.dep_ == 'pobj' and money.head.dep_ == 'prep':
                relations.append({"subject": money.head.head.string.strip(), "object": money.string.strip(), "relation": entity_name})
    #print( relations)
    for i in relations:
        relationSent=i['subject'],i['relation'],i['object']
        print(relationSent)
    return relations
     


if __name__ == "__main__":
    plac.call(main)