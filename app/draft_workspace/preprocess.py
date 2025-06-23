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
# test_lemmas = json_dir.get_content_from_file_path('app/data/google_json/google_clean_01/lemma_items_01.json')
# print(test_lemmas)
training_data = []
dev_data = []
visited = []

def find_all_substring_indices(main_string, sub_string):
        indices = []
        endices = []
        start_index = 0
        while True:
            index = main_string.find(sub_string, start_index)
            if index == -1:
                break
            indices.append(index)
            start_index = index + len(sub_string)
            temp = start_index
            if temp + 1 < len(main_string) and main_string[index:temp+1].isalpha():
                temp +=1
            endices.append(temp)
        return indices, endices

def make_train_data(texts):
    # db = DocBin()
    n = 0
    for example in texts:
        for key in example:
            print("building: ", key)
            key_arr = key.split(' ')
            if len(example[key]) < 3:
                continue
            for text in example[key]:
                spans = []
                if text in visited:
                    continue
                # doc = nlp(text)
                lower_text = text.lower().strip()
                idx, endex = find_all_substring_indices(lower_text,key)
                for i, s in enumerate(idx):
                    spans.append((s,endex[i],"PRODUCT"))
                if spans != []:
                    n += 1
                    if n % 9 == 2:
                        dev_data.append((text,spans))
                    else:
                        training_data.append((text,spans))
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
        # time.sleep(20)
        # print(training_data)
    print('writing to file')
    return

        


def train_spacy(data,file_name,total=0):
    db = DocBin()
    for text, annotations in data:
        doc = nlp_en(text)
        ents = []

        for start_idx, end_idx, label in annotations:
            span = doc.char_span(start_idx,end_idx,label=label)
            if span == None:
                span = doc.char_span(start_idx,end_idx+1,label=label)
                if span == None:
                    continue
            ents.append(span)
        if ents == []:
            continue
        total += 1
        doc.ents = ents
        db.add(doc)

    db.to_disk(file_name)
    return total

train_all_data()
# print(len(training_data),len(dev_data))
# total_train = train_spacy(training_data,'./train.spacy')
# total_dev = train_spacy(dev_data,'./dev.spacy')
# print(training_data)
# print(len(training_data))
print(training_data)