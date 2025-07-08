import json
import os
from project.file_manager import CustomHTMLFile, FileManager
from bs4 import BeautifulSoup

# not allowed to scrape google so this file helps make links to copy and paste
BASE_SAVE_DIR = 'product/training/unclean_data/google_html'

search_engines = {
    'etsy':{
        'url':'https://www.etsy.com/',
        'dir_pattern': ['','clothing/','accessories/','jewelry/'],
        'search_prefix': ['search?q='],
        'item_patterns': ''
    },
    'google':{
        'url':'https://www.google.com/',
        'dir_pattern': [''],
        'search_prefix': ['search?q=','oq='],
        'item_patterns': '+'
        }
}
save_path_google = f"product/training/unclean_data/google_html"
# os.listdir(BASE_SAVE_DIR)


content = {
    'accessories': ['suspenders'],
    'footwear': ['socks'],
    'clothing': ['skirt','shorts','pants','overalls','suit','jeans','gowns'],
    'headwear': ['baseball_cap','cap']
}

# base_html = "data/raw-html/google"
# total = 0
# for item in os.listdir(base_html):
#     clean_item = item.replace('_or_','+').replace('_','+')
#     content[clean_item] = []
#     for file in os.listdir(base_html + '/' + item):
#         file_path = base_html + '/' + item + '/' + file
#         content[clean_item].append(file[:-8])
#         total += 1
# visited = ['clothing','accessories','headwear','footwear']
# to_visit = []

# for dir in os.listdir(save_path_google):
#     for file in os.listdir(save_path_google+dir):
#         with open(file) as text:
#             if len(text) < 4:
#                 to_visit.append(file[:-8])
# print(to_visit)




# get query for search url
def get_queries(item,enginge_name,key=''):
    engine = search_engines[enginge_name]
    all_urls = [engine['url']] * (len(engine['dir_pattern']) + len(engine['item_patterns']))

    for i,pattern in enumerate(engine['dir_pattern']):
        all_urls[i] += pattern
    if key:
        all_urls = [url + "&".join([p + item.replace('_','+')+f"+{key.lower().replace('/','+').replace(' ','+')}" for p in engine['search_prefix']])for url in all_urls]
    else:
        all_urls = [url + "&".join([p + item.replace('_','+')+f"{key.lower().replace('/','+').replace(' ','+')}" for p in engine['search_prefix']])for url in all_urls]
    # all_urls[-1] += f"+{key.lower().replace('/','+').replace(' ','+')}"

    return all_urls  
    
# build search url
def build_path(base,item,cat='new'):
    return f"{base}{cat.replace(' ','_').replace('/','_or_').lower()}/{item.lower().strip().replace(' ','_')}"

# create files for manual input
def make_files(content,dir):
        for item in content:

            save_path = build_path(dir,item)
            # first_page = f"{save_path}_00.html"
            page = f"{save_path}_01.html"
            # print(save_path)
            if not os.path.exists(page):
                html = CustomHTMLFile(save_path)
                html.write_to_html_file_dir('')

            # if not os.path.exists(second_page):
            #     html = CustomHTMLFile(first_page)
            #     html.write_to_html_file_dir('')

# help track input and build urls
def manual_input_tracker(content,engine_name: str):

    for item in sorted(content):

        curr_dir = build_path(save_path_google,item)
        
        # print(f"key: {key}\n",f"item: {item}\n")
        all_urls = get_queries(item.strip(),engine_name)
        for url in all_urls:
            print(url,'\n')
        print('------------------------------------------\n')
        save = input("press enter to continue")
    
        if save == 'stop':
            break
        else:
            
            continue

# json_file_input = FileManager('product/training/unclean_data/json_drafts/new_fashion_items_01.json')
# content = json_file_input.read_file()

# make_files(content,'product/training/unclean_data/google_html/')
# manual_input_tracker(etsy)

json_file_input = FileManager('product/training/unclean_data/json_drafts/new_fashion_items_01.json')
content = json_file_input.read_file()
manual_input_tracker(content,'google')

# html = CustomHTMLFile('data/raw-html/google/clothing')
# html.prettify_all_html_versions('blouse')
# with open('data/raw-html/google/clothing/trousers' + '_01.html') as file:
#     soup = BeautifulSoup(file)
#     print(soup.text)
# make_files()