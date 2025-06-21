from data_parsing.custom_common.file_manager import CustomJSONFile
import spacy

nlp = spacy.load('en_core_web_trf')

json_dir = CustomJSONFile('app/data/google_json/google_clean_01')
my_files = json_dir.get_all_file_paths()
my_lemmas = json_dir.get_content_from_file_path('app/data/google_json/google_clean_01/lemma_items_01.json')
print(my_lemmas)
all_items_lemmas = []
tot = 0
# for item in my_files:
#     content = json_dir.get_content_from_file_path(item)
#     for obj in content:
#         for key in obj:
#             all_items_lemmas.append(key)
# json_dir.write_new_json_file(all_items_lemmas,'lemma_items')
# all_items_lemmas = []
# # print(tot)
# for c in content:
#     for key in c:
#         all_items_lemmas.append(key)
        # print(key,len(c[key]))
        # for obj in content:
        #     print(obj)
    #         for i, text in enumerate(obj[key]):
    #             doc = nlp(text)
    #             for t in doc:
    #                 print(t.ent_type_)
    #         break



# print([c.keys() for c in content])
# for category in content:
#     for word in category:
#         texts = category[word]

# doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#             token.shape_, token.is_alpha, token.is_stop)
