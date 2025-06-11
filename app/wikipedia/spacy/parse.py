import spacy
import en_core_web_sm
import os
from bs4 import BeautifulSoup
import sys
import re
import json

nlp = spacy.load("en_core_web_sm")
# nltk.download('wordnet')

categories = {"accessories":{},"apparel":{},"materials": {}}

""" 
Important Spacy Method Notes:


DOC:
- doc.noun_chunks useful for finding NP


TOKEN:
- token.dep_ similar to phrase structure rules
- token.pos_ provides general POS
- token.tag_ provides additional POS information ( ex: verb is a gerund - look up key )

"""

example_words = {}
missed_words = []


def find_error_files(base_directory):
    errors = []
    for c in categories:
        directory = base_directory + c
        for file in os.listdir(directory):
            fp = os.path.join(directory,file)
            file_name = file[:-5]
            with open(fp,'r') as html:
                soup = BeautifulSoup(html, 'html.parser')

                if "may refer to" in soup.text:
                    errors.append(file_name)

    if errors != []:
        file = open('app/wikipedia/parsed/issues/errors.json','w')
        file.write(json.dumps(errors))
        file.close
 

def read_html_files_by_dir(base_directory,tag=None):
    
    for c in categories:
        res_soups_text = {}
        directory = base_directory + c
        for file in os.listdir(directory):
            fp = os.path.join(directory,file)
            file_name = file[:-5]
            res_soups_text[file_name] = []
            # file_sem = nlp(file_name)
            with open(fp,'r') as html:
                soup = BeautifulSoup(html, 'html.parser')
                categories[c][file_name] = soup.text.lower()
    

def chunk_nouns(doc_texts):
    for item in doc_texts:
        doc = nlp(item)
        for chunk in doc.noun_chunks:
            print(chunk.text, chunk.root.text, chunk.root.dep_,
                    chunk.root.head.text)

def tokenize(doc_texts):


    doc = nlp(doc_texts)
    for token in doc:

        print(token.text, token.pos_, token.dep_, token.head.text)

def information_extraction(doc_texts):
    
    for doc in nlp.pipe(doc_texts):
        for token in doc:
            print(token.ent_type_)
            # if token.ent_type_ == "MONEY":
            #     # We have an attribute and direct object, so check for subject
            #     if token.dep_ in ("attr", "dobj"):
            #         subj = [w for w in token.head.lefts if w.dep_ == "nsubj"]
            #         if subj:
            #             print(subj[0], "-->", token)
            #     # We have a prepositional object with a preposition
            #     elif token.dep_ == "pobj" and token.head.dep_ == "prep":
            #         print(token.head.head, "-->", token)

def analyze_text_for_keyword(cat,doc_texts):
    for key in doc_texts:
        all_sent = []
        item = doc_texts[key]
        doc = nlp(item)
        for sent in doc.sents:
            if key in sent.text:
                for token in sent:
                    if token.text == key:

                        all_sent.append(sent.text)
        if all_sent != []:
            example_words[key] = all_sent
        else:
            missed_words.append(key)

def work_space():
    example_file = open('app/wikipedia/parsed/json/sentences-with-word/example.json','r')
    examples = json.load(example_file)
    # for key in example_file:
    items = examples['earrings']
    # nlp.add_pipe('entity_ruler')
    for item in items:
        ents = nlp(item)
        print([e.ent_iob_ for e in ents])


"""parses all html and stores sentences"""
# read_html_files_by_dir('app/wikipedia/html/',None)   

# for c in categories:
#     analyze_text_for_keyword(c,categories[c])

# file = open('app/wikipedia/parsed/json/sentences-with-word/missing_01.json','w')
# file.writelines(json.dumps(missed_words))
# file.close
# file = open('app/wikipedia/parsed/json/sentences-with-word/example_01.json','w')
# file.writelines(json.dumps(example_words))
# file.close
