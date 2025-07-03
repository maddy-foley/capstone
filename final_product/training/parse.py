from file_manager import FileManager, CustomJSONFile
import spacy

nlp = spacy.load('en_core_web_lg')

def get_file_1():
    KEY_CONST = ['Patterns', 'Styles', 'SubCategories']
    open_file = FileManager('final_product/training/unclean_data/raw-txt/fashion_items.txt')
    file_content = open_file.read_file()

    fashion_items_dic = {}

    key = ''
    for item in file_content:
        if item == '':
            continue
        key_pair = item.split(':')

        if '' in key_pair or len(key+key_pair[0]) == 1:
            continue
        if len(key_pair) == 1:
            key = key_pair[0].strip()
            fashion_items_dic[key] = {}
        else:
            fashion_items_dic[key][key_pair[0].strip()] = key_pair[1].strip()


    all_items = {'t-shirt':{
        
    }}
    for item in fashion_items_dic:
        un_modified_item_name = item
        if 'w/' in item:
            item = item[:item.find('w/')]
            # print(item)
        # if 't-shirt' in item.lower():
        #     for attr in fashion_items_dic[item]:
        #         if attr in all_items['t-shirt']
        #     continue
        doc = nlp(item)
        key_word = doc[-1]
        # print(key_word.text)
        if len(key_word.text) == 1:
            continue

        cleaned_key_lemma = key_word.lemma_.lower().strip()
        if cleaned_key_lemma + 's' in all_items:
            cleaned_key_lemma = cleaned_key_lemma + 's'
        elif cleaned_key_lemma[:-1] in all_items:
            cleaned_key_lemma = cleaned_key_lemma[:-1]
        if 't-shirt' in item.lower():
            cleaned_key_lemma = 't-shirt'
        if cleaned_key_lemma not in all_items:
            all_items[cleaned_key_lemma] = {}
            for attr in fashion_items_dic[un_modified_item_name]:
                all_items[cleaned_key_lemma][attr] = [fashion_items_dic[un_modified_item_name][attr]]
            # all_items[key_word.lemma_.lower()] = {attr: [fashion_items_dic[item][attr]] for attr in fashion_items_dic[item]}
        else:

            for attr in fashion_items_dic[un_modified_item_name]:
                to_add = fashion_items_dic[un_modified_item_name][attr]
                if attr not in all_items[cleaned_key_lemma]:
                    all_items[cleaned_key_lemma][attr] = []
                if ',' in to_add:
                    arr = to_add.split(',')
                    for word in arr:
                        if word.strip() not in all_items[cleaned_key_lemma][attr]:
                            all_items[cleaned_key_lemma][attr].append(str(word.strip()))
                elif to_add.strip() not in all_items[cleaned_key_lemma][attr]:
                    all_items[cleaned_key_lemma][attr].append(to_add.strip())
    return all_items

# json_item = get_file_1()
# save_file = CustomJSONFile('final_product/training/unclean_data/json_drafts')
# save_file.write_new_json_file([json_item],'fashion')

def combine_files():
    open_file = FileManager('final_product/training/unclean_data/json_drafts/all_filtered_products_by_cat_00.json')
    old_file_content = open_file.read_file()
    open_file = FileManager('final_product/training/unclean_data/json_drafts/fashion_01.json')
    new_file_content = open_file.read_file().pop()
    old_file_content['misc'] = []
    all_items = {}
    new_items = []
    for item in old_file_content.values():
        for t in item:
            all_items[t] = 1
    for item in new_file_content:
        key = item
        if item in all_items:
            all_items[item] += 1
        elif item[:-1] in all_items:
            all_items[item[:-1]] += 1
            key = item[:-1]
        elif item + 's' in all_items:
            all_items[item + 's'] += 1
            key = item + 's'
        else:
            all_items[item] = 1
            new_items.append(item)

            # print(item)
    # delete random word that got in somehow
    del all_items['on']
    return all_items,new_items

json_item,new_items = combine_files()
# print(json_item)
save_file = CustomJSONFile('final_product/training/unclean_data/json_drafts')
save_file.write_new_json_file(new_items,'new_fashion_items')
