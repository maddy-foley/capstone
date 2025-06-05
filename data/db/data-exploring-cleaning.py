import json
import os
import re
# from config import engine
# from sqlalchemy.orm import Session
# from sqlalchemy import select
# from models import *

file = open('data/json/categorized-products.json','r')
content = json.load(file)

def insert_to_db(test=False):
    count = 0
    for c in content:
        response = ResponseModel()
        site = SiteModel()

        result_file_name =f"./data/json/api-output/{c}.json"
        if not os.path.isfile(result_file_name):
            continue
        result_file = open(result_file_name,'r')
        results = json.load(result_file)
        if test and count == 2:
            break
        else:
            count += 1
            # print(c)

def convert_product_data():
    with Session(engine) as session:
        count = 0
        arr = []
        for category_name in content:
            category = CategoryModel(name=category_name)
            arr.append(category)
        session.add_all(input)
        session.commit()

# def convert_search_queries():

#     with Session(engine) as session:
#         search = []
#         for category_name in content:
#             stmt = select(CategoryModel).where(CategoryModel.name == category_name)
#             category = session.scalars(stmt).one()
#             for item in content[category_name]:
#                 query_name = item.strip()
#                 search.append(SearchQueryModel(name=query_name,category=category))

#         session.add_all(search)
#         session.commit()


# ## FIX - look into filtering
def convert_responses():
    removed = {}
    # with Session(engine) as session:
    responses = []
    count = 0
    for c in content:
        result_file = json.load(open(f"./data/json/api-output/{c}.json",'r'))
        for f in result_file:
            # print(f.get('formattedUrl'))
            for key in f:
                query_name = key.strip()
                removed[query_name] = 0
                rank = 0

                if not check_if_query_ok(query_name):
                    removed[query_name] = 10
                    continue
                for links in f[key]['items']:
                    rank += 1
                    snippet = links.get('snippet')
                    pagemap = links.get('pagemap')
                    title = links.get('title')
                    formatted_url = links.get('formattedUrl')
                    if not snippet or not pagemap:
                        removed[query_name] += 1
                        continue

                    metatags = pagemap.get('metatags')
                    if not metatags:
                        removed[query_name] += 1
                        continue
                    tags = metatags[0]
                    # formatted_url = tags.get('formattedUrl')
                    # if 'url' in [key.lower() for key in tags]:
                    #     print(tags)

                    og_title = tags.get('og:title')
                    description = tags.get("og:description")
                    if not description:
                        for t in tags:
                            if 'description' in t:
                                description = tags[t]
                    if not og_title:
                        for t in tags:
                            if 'title' in t:
                                og_title = tags[t]
    # remove any query w/ responses with less than half of the data requested
    remove_arr = [ r for r in removed if removed[r] > 5]
    # if not og_title:
    #     print(query_name)
    # print(len(remove_arr))
    # save_file = open('data/json/products-to-remove.json','w')
    # save_file.write(json.dumps(remove_arr))
    # save_file.close()

def check_if_query_ok(query_name):
    # remove (potentially) missing context queries
    if 'these' in query_name or re.match('^other ',query_name) or 'those' in query_name:
        return False
    # remove sentences that start with an awkward preposition - FIX check remaining data for more prepositions later
    if re.match('^to ', query_name) or re.match('^for ', query_name):
        return False
    return True

def test_search():
    removed = {}
    # with Session(engine) as session:
    responses = []
    for c in content:

        result_file = json.load(open(f"./data/json/api-output/{c}.json",'r'))
        for f in result_file:
            # print(f.get('formattedUrl'))
            for row in f:

                """AVAILABLE KEYS for f[row]:
                kind
                url
                queries
                context
                searchInformation
                items
                """


                for item in f[row].get('items'):
                    # print([key for key in item])

                    """AVAILABLE KEYS for item:
                        kind
                        title
                        htmlTitle
                        link
                        displayLink
                        snippet
                        htmlSnippet
                        formattedUrl
                        htmlFormattedUrl
                        pagemap
                    """
                    pagemap = item.get('pagemap')
                    # if pagemap:
                    #     if pagemap.get('website'):
                    #         print(pagemap)
# def work_on_json():
#     for c in content:
#         result_file = json.load(open(f"./data/json/api-output/{c}.json",'r'))
#         for line in result_file:
#             for key in line:
#                 query_name = key.strip()




#DONE
# convert_product_data()
# convert_search_queries()
convert_responses()
# test_search()
# work_on_json()
# items = content[0]['pottery']['items'][1]['pagemap']['metatags'][0]
