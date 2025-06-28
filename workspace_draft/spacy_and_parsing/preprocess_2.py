import spacy
from spacy.tokens import DocBin,Doc
from data_parsing.custom_common.file_manager import CustomJSONFile
import re
import time
from spacy.training import Example



nlp_en = spacy.blank('en')
nlp = spacy.load("en_core_web_lg")


# doc = nlp("Laura flew to Silicon Valley.")

# gold_dict = {"entities": ["U-PERS", "O", "O", "B-LOC", "L-LOC"]}
# example = Example.from_dict(doc, gold_dict)
# files to access
json_dir = CustomJSONFile('workspace_draft/data/google_json/google_clean_01')

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
            while temp + 1 < len(main_string) and main_string[index:temp+1].isalpha():
                temp +=1
            endices.append(temp)
        return indices, endices

def make_train_data(texts):
    # db = DocBin()
    n = 0
    for example in texts:
        for key in example:
            print("building: ", key)
            # key_arr = key.split(' ')

            #help identify t-shirt
            # if '-' in key:
            #     for text in example[key]:
            #         spans = []
            #         lower_text = text.lower().strip()
            #         start_idx, end_idx = find_all_substring_indices(lower_text,key)
            #         for i, s in enumerate(start_idx):
            #             spans.append((s,end_idx[i],"PRODUCT"))
            #         if spans != []:
            #             n += 1
            #             if n % 9 == 2:
            #                 dev_data.append((text,spans))
            #             else:
            #                 training_data.append((text,spans))
            #     continue
            # else:
            key_arr = [k.lemma_ for k in nlp(key)]
            if len(example[key]) < 3:
                continue
            for text in example[key]:
                # key_lemma = key.split(' ')
                spans = []
                if text in visited:
                    continue
                doc = nlp(text)
                start_idx = []
                end_idx = []

                for i,token in enumerate(doc):
                    key_size = len(key_arr)
                    found = False
                    if token.lemma_.lower() in key_arr and token.pos_ != 'VERB':
                        if i > 0:
                            if spans[i - 1] == 'O':
                                spans.append('B-PRODUCT')
                                # token.ent_type_ = 'PRODUCT'
                                # token.ent_iob_ = 'B'
                            elif spans[i - 1] != 'O':
                                spans.append('I-PRODUCT')
                                # token.ent_type_ = 'PRODUCT'
                                # token.ent_iob_ = 'I'
                        # elif i > 0 and token.text == '_':
                        #     if spans[-1] == 'PRODUCT':
                        #         spans.append('PRODUCT')
                        #     else:
                        #         spans.append('O')
                        else:
                            spans.append('B-PRODUCT')
                            # token.ent_type_ = 'PRODUCT'
                            # token.ent_iob_ = 'B'
                    else:
                        spans.append('O')
                        # if i > 1:
                            # if spans[i - 1] == 'I-PRODUCT':
                            #     spans[i - 1] = 'L-PRODUCT'
                                # doc[i-1].ent_iob_ = 'L'
                        # token.ent_type_ = None
                    #     if found:
                    # print(token.text,i)
                if spans != []:
                    n += 1
                    if n % 9 == 2:
                        dev_data.append((doc,{"entities": spans}))
                    else:
                        training_data.append((doc,{"entities": spans}))
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

        
def test_path(file_path):
    name = file_path.split('/').pop()
    name = name [:-8]
    name.replace('_', ' ')
    test_texts =  json_dir.get_content_from_file_path(file_path=file_path)
    make_train_data(test_texts)

def train_spacy(data,file_name,total=0):
    db = DocBin()

    for item in data:
        doc = item[0]
        ents = item[1]['entities']
        # prev_ents = [(e.text, e.start_char, e.end_char, e.label_) for e in doc.ents]
        # print(prev_ents)
        words = []
        for i, token in enumerate(doc):
            words.append(token.text)
            
            # spaces.append(token.)
            if 'PRODUCT' in ents[i]:
                if len(token.text) == 1:
                    if (i == 0 and ents[i-1] == "O") or (i < len(ents)-1 and ents[i+1] == 'O'):
                        ents[i] = 'O'
                        if ents[i+1] == 'I-PRODUCT':
                            ents[i+1] == 'B-PRODUCT'
        new_doc = Doc(nlp.vocab,words=words,ents=ents)
        db.add(new_doc)

    db.to_disk(file_name)
    return total

train_all_data()
# json_dir.write_new_json_file(training_data,"train")
# json_dir.write_new_json_file(dev_data, "dev")
# test_path('workspace_draft/data/google_json/google_clean_01/clothing_10.json')
# print(len(training_data),len(dev_data))
# print(dev_data)
# for item in dev_data:
#     doc = item[0]
#     ents = item[1]['entities']
#     # prev_ents = [(e.text, e.start_char, e.end_char, e.label_) for e in doc.ents]
#     # print(prev_ents)
#     words = []
#     for i, token in enumerate(doc):
#         words.append(token.text)
        
#         # spaces.append(token.)
#         if 'PRODUCT' in ents[i]:
#             if len(token.text) == 1:
#                 if (i == 0 and ents[i-1] == "O" or ents[i+1] == 'O'):
#                     ents[i] = 'O'
#     new_doc = Doc(nlp.vocab,words=words,ents=ents)
    # print(new_doc.ents)
    # doc.set_ents(ents)
    # print(doc.ents)
# for d in dev_data:
# #     print(d[0].ents)
total_train = train_spacy(training_data,'./train_2.spacy')
total_dev = train_spacy(dev_data,'./dev_2.spacy')

# print(len(training_data))
# print(training_data)
