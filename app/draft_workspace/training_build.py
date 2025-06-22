import spacy
from spacy.tokens import DocBin
from data_parsing.custom_common.file_manager import CustomJSONFile
import re
import time
from spacy.training import Example


nlp_en = spacy.blank('en')
nlp = spacy.load("en_core_web_trf")
# files to access
json_dir = CustomJSONFile('app/data/google_json/google_clean_01')

my_files = json_dir.get_all_file_paths()
# test_lemmas = json_dir.get_content_from_file_path('app/data/google_json/google_clean_01/accessories_01.json')
training_data = []

def make_train_data(texts):
    # db = DocBin()
    for example in texts:
        for key in example:
            key_lemmas = key.split(' ')
            key_lemmas.append(key.replace(' ',''))
            if len(example[key]) < 4:
                continue
            for text in example[key]:
                doc = nlp(text)
                for token in doc:
                    if token.lemma_ in key_lemmas:
                        print('building: ',key)
                        start_idx = token.idx
                        end_idx = start_idx+ len(token.text)

                        training_data.append((text,[(start_idx,end_idx,'PRODUCT')]))
    return

def train_all_data():
    name = ''
    for file in my_files:
        if 'lemma_items' in file:
            continue
        name = file.split('/').pop()
        name = name [:-8]
        name.replace('_', ' ')
        test_texts =  json_dir.get_content_from_file_path(file)
        make_train_data(test_texts)
        time.sleep(20)
    train_spacy(training_data)

        


def train_spacy(training_data):
    db = DocBin()
    for text, annotations in training_data:
        doc = nlp_en(text)
        ents = []
        for start_idx, end_idx, label in annotations:
            span = doc.char_span(start_idx,end_idx,label=label)
            ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk('./train.spacy')

train_all_data()