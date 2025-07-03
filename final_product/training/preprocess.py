import spacy
from spacy.tokens import DocBin,Doc
from file_manager import FileManager, HTMLFileManager
from directory_manager import DirectoryManager
import re
import time
from spacy.training import Example


# get what all the html files we want to parse
directory = DirectoryManager('final_product/training/unclean_data/google_html')
file_paths = directory.get_all_dir_file_names(sub_dir=True)

#load spacy
nlp_en = spacy.blank('en')
nlp = spacy.load("en_core_web_sm")
dev_data = []
training_data = []
visited = []

def make_train_data(chunk,key_arr):
    spans = []
    doc = nlp(chunk)

    for i,token in enumerate(doc):
        if token.lemma_.lower() in key_arr and token.pos_ != 'VERB':
            if i > 0:
                if spans[i - 1] == 'O':
                    spans.append('B-PRODUCT')
                elif spans[i - 1] != 'O':
                    spans.append('I-PRODUCT')
            else:
                spans.append('B-PRODUCT')
        else:
            spans.append('O')
    return (doc,{"entities": spans})

def parse_html(test=None):
    i = 0
    products_seen = []
    if test:
        open_file_path = HTMLFileManager(file_path=test)
        file = open_file_path.parse_html(test)
        name = open_file_path.get_file_name()
        key_arr = name.split('_')
        for chunk in file:
            i += 1
            curr_annotated_span = make_train_data(chunk,key_arr)
            if i % 9 == 2:
                dev_data.append(curr_annotated_span)
            else:
                training_data.append(curr_annotated_span)
    else:
        for file_path in file_paths:
            print(file_path)
            open_file_path = HTMLFileManager(file_path=file_path)
            file = open_file_path.parse_html(file_path)
            name = open_file_path.get_file_name()
            key_arr = name.split('_')
            for chunk in file:
                i += 1
                curr_annotated_span = make_train_data(chunk,key_arr)
                if i % 9 == 2:
                    dev_data.append(curr_annotated_span)
                else:
                    training_data.append(curr_annotated_span)
    pass


def make_spacy_file(data,file_name):
    db = DocBin()

    for item in data:
        doc = item[0]
        ents = item[1]['entities']
        words = []
        spaces = []
        for i, token in enumerate(doc):
            words.append(token.text)
            has_ws = token.whitespace_ == ' '
            spaces.append(has_ws)
            
            if 'PRODUCT' in ents[i]:
                if len(token.text) == 1:
                    if (i == 0 and ents[i-1] == "O") or (i < len(ents)-1 and ents[i+1] == 'O'):
                        ents[i] = 'O'
                        if ents[i+1] == 'I-PRODUCT':
                            ents[i+1] == 'B-PRODUCT'
                
        new_doc = Doc(nlp.vocab,words=words,ents=ents,spaces=spaces)
        db.add(new_doc)

    db.to_disk(file_name)

parse_html()
# print(dev_data,training_data)


# total_train = make_spacy_file(training_data,'./train.spacy')
# total_dev =  make_spacy_file(dev_data,'./dev.spacy')