
import json
import spacy
import os
from custom_common.file_manager import CustomFile,CustomJSONFile


nlp = spacy.load("en_core_web_sm")



BASE_SAVE_DIR = 'data/parsed/json'
FILTERED_TEXT_FILE = 'data/raw-txt/products_list_and_categories.txt'
def is_emoji(char):
    """Checks if a character is likely an emoji based on its Unicode range."""
    # This is a simplified check and may not cover all emojis or exclude non-emojis
    # For comprehensive emoji identification, consider the 'emoji' library.
    return 0x1F600 <= ord(char) <= 0x1F64F or \
           0x1F300 <= ord(char) <= 0x1F5FF or \
           0x1F900 <= ord(char) <= 0x1F9FF

product_set = set()
# my_set = set()

def consolidate_json():
    for file in os.listdir(BASE_SAVE_DIR):
        fp = f"{BASE_SAVE_DIR}/{file}"
        with open(fp,'r') as json_file:
            content = json.load(json_file)

            for key in content:
                if key != 'product' and 'misc' not in key:
                    product_set.add(key.lower())
                for item in content[key]:
                    product_set.add(item.lower())

dic = {}
def parse_filtered_data():
    with open(FILTERED_TEXT_FILE,'r') as file:
        file_line = file.readlines()
        prev = ''
        for line in file_line:
            if line[0] == '`':
                count = 0
                while not line[count].isalpha():
                    count += 1
                prev = line[count:].strip().lower()
                dic[prev] = []
            if line.count(',') > 2:
                dic[prev] += [l.strip().lower() for l in line.split(',')]
total = 0
# consolidate_json()
parse_filtered_data()
for key in dic:
    print(len(dic[key]))
    total += len(dic[key])

# json_file = CustomJSONFile(BASE_SAVE_DIR+'/all_filtered_products_by_cat')
# json_file.write_to_json_file_dir(dic)