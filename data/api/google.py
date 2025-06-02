import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

# google search api base url configuration
API_KEY = os.getenv('API_KEY')
CX_ID = os.getenv('CX_ID')
BASE_URL = f"https://customsearch.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX_ID}"

json_file_path = "data/json/api-output"
# print(BASE_URL + '&q=shoes'+ ADDITIONAL_PARAMS)
def query(product_items,category):
    # prevent potential data loss and api-calls when querying
    if os.path.isfile(f"{json_file_path}/{category}.json") and category != 'test':
        return None
    else:
        product_queries = []
        for p in product_items:
            dic = {p: []}
            query_param = f"&q={p}"
            print(query_param)
            full_api_url = BASE_URL + query_param
            headers = {
                'content-type':'application/json'
                # 'user-agent': "maddyfoley5@gmail.com"
                }
            r = requests.get(full_api_url,headers=headers)
            print(r.content)
            if r.status_code == 200:
                res = r.json()
                dic[p] = res
                product_queries.append(dic)
            else:
                return None
        return product_queries

# def make_file(category,data):
#     json = json.dumps(data)
# def get_all(total=100):
#     with open('data/json/categorized-products.json', 'r') as file:
#         product_data = json.load(file)

# res = query(['shoes'],'test')
# if res:
#     file = open('data/json/api-output/test-4.json','w')
#     file.write(json.dumps(res))
#     file.close()

# print(json.load(file))
# get_all()
#
