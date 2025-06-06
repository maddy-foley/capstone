import requests
from dotenv import load_dotenv
import os
import time
import json

load_dotenv()

# google search api base url configuration
API_KEY = os.getenv('API_KEY')
CX_ID = os.getenv('CX_ID')
# BASE_URL = f"https://customsearch.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX_ID}"

json_file_path = "data/json/api-output"

def query(product_items,category):
    # prevent potential data loss and api-calls when querying
    if os.path.isfile(f"{json_file_path}/{category}.json") and category != 'test':
        return []
    else:
        product_queries = []
        for p in product_items:
            dic = {p: []}
            query_param = f"&q={p}+shop+{category}"
            print(query_param)
            full_api_url = BASE_URL + query_param
            headers = {
                'content-type':'application/json'
                }
            r = requests.get(full_api_url,headers=headers)

            time.sleep(.5)
            print(r.content)
            if r.status_code == 200:
                res = r.json()
                dic[p] = res
                product_queries.append(dic)
            else:
                return product_queries
        return product_queries

# def make_file(category,data):
#     json = json.dumps(data)
def get_all():
    with open('data/json/categorized-products.json', 'r') as file:
        product_data = json.load(file)
        # for category in product_data:
        for category in product_data:
            if category == 'art':
                continue
            res = query(product_data[category],category)
            if res != []:
                file = open(f'data/json/api-output/{category}.json','w')
                file.write(json.dumps(res))
                file.close()
            if len(res) != len(product_data[category]):
                error_file = open('data/json/error.txt','a')
                error_file.write(category + ' \n')
                error_file.close()

#         for key in product_data:
#             print(key,len(product_data[key]))

# res = query(['shoes'],'test')
# if res:
#     file = open('data/json/api-output/test-4.json','w')
#     file.write(json.dumps(res))
#     file.close()

# print(json.load(file))

# use to run pull requests
# get_all()
#
