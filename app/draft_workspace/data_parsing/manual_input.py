import json
import os
from custom_common.file_manager import CustomJSONFile,CustomHTMLFile
from bs4 import BeautifulSoup


BASE_SAVE_DIR = 'data/raw-html/google'

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
save_path_google = f"data/raw-html/google/"
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





def get_queries(key,item,enginge_name):
    engine = search_engines[enginge_name]
    all_urls = [engine['url']] * (len(engine['dir_pattern']) + len(engine['item_patterns']))

    for i,pattern in enumerate(engine['dir_pattern']):
        all_urls[i] += pattern
    
    all_urls = [url + "&".join([p + item.replace('_','+')+f"+{key.lower().replace('/','+').replace(' ','+')}" for p in engine['search_prefix']])for url in all_urls]
    # all_urls[-1] += f"+{key.lower().replace('/','+').replace(' ','+')}"

    return all_urls  
        
def build_path(base,cat,item):
    return f"{base}{cat.replace(' ','_').replace('/','_or_').lower()}/{item.lower().strip().replace(' ','_')}"


def make_files():
    for key in content:
        curr_save_page = f"{save_path_google}{key.replace(' ','_').replace('/','_or_')}"

        for item in content[key]:

            save_path = build_path(save_path_google,key,item)
            # first_page = f"{save_path}_00.html"
            page = f"{save_path}_01.html"
            # print(save_path)
            if not os.path.exists(page):
                html = CustomHTMLFile(save_path)
                html.write_to_html_file_dir('')

            # if not os.path.exists(second_page):
            #     html = CustomHTMLFile(first_page)
            #     html.write_to_html_file_dir('')


def manual_input_tracker(engine_name: str):
    for key in content:
        # if key in visited:
        #     continue
        for item in sorted(content[key]):
            if item == '':
                continue
            curr_dir = build_path(save_path_google,key,item)
         
            print(f"key: {key}\n",f"item: {item}\n")
            all_urls = get_queries(key,item,engine_name)
            for url in all_urls:
                print(url,'\n')
            print('------------------------------------------\n')
            save = input("press enter to continue")
        
            if save == 'stop':
                break
            else:
                
                continue

# manual_input_tracker(etsy)
manual_input_tracker('google')

# html = CustomHTMLFile('data/raw-html/google/clothing')
# html.prettify_all_html_versions('blouse')
# with open('data/raw-html/google/clothing/trousers' + '_01.html') as file:
#     soup = BeautifulSoup(file)
#     print(soup.text)
# make_files()