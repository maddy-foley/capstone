import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

# google search api base url configuration
BASE_URL = os.getenv('BASE_API_URL')

ADDITIONAL_PARAMS = "&lr=lang_en&dateRestrict=y2&num=10&safe=active"
siteSearch = "&siteSearch=etsy.com&siteSearchFilter=i"

json_file_path = "data/json/api-output"

def query(product_items,category):
    # prevent potential data loss and api-calls when querying
    if os.path.isfile(f"{json_file_path}/{category}.json") and category != 'test':
        return None
    else:
        product_queries = []
        for p in product_items:
            dic = {p: []}
            query_param = f"&q={p}"

            full_api_url = BASE_URL + query_param + ADDITIONAL_PARAMS
            headers = {
                'content-type':'application/json',
                'user-agent': "maddyfoley5@gmail.com"
                }
            r = requests.get('https://api.github.com/events',headers=headers)
            if r.status_code == 200:
                res = r.json()
                dic[p] = res
                product_queries.append(dic)
            else:
                return None
        return product_queries

# def make_file(category,data):
#     json = json.dumps(data)

res = query(['shoes','new'],'test')
if res:
    file = open('data/json/api-output/test-2.json','w')
    file.write(json.dumps(res))
    file.close()
# print(json.load(file))
