import json
import os
import re
from config import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import *

file = open('data/json/categorized-products.json','r')
content = json.load(file)

def insert_to_db_category():
    with Session(engine) as session:
        for c in content:
            category = Category(name=c)
            session.add(category)
        session.commit()

def insert_to_db_search_query_and_site():

    with Session(engine) as session:
        categories = session.query(Category).all()

        for c in categories:
            category = c
            category_file = json.load(open(f"./data/json/api-output/{category.name}.json",'r'))
            for f in category_file:
                for key in f:
                    query_name = key.strip()
                    rank = 0
                    search_query = SearchQuery(name=query_name,category=category)
                    res = []
                    if not check_if_query_ok(query_name):
                        continue

                    for links in f[key]['items']:
                        rank += 1
                        snippet = links.get('snippet')
                        pagemap = links.get('pagemap')
                        title = links.get('title')
                        formatted_url = links.get('formattedUrl')
                        if not snippet or not pagemap:
                            continue

                        metatags = pagemap.get('metatags')
                        if not metatags:
                            continue
                        tags = metatags[0]

                        alt_title = tags.get('og:title')
                        description = tags.get("og:description")
                        if not description:
                            for t in tags:
                                if 'description' in t:
                                    description = tags[t]
                        if not alt_title:
                            for t in tags:
                                if 'title' in t:
                                    alt_title = tags[t]

                        res.append(Site(snippet=snippet,rank=rank,search_query=search_query,formatted_url=formatted_url,title=title,description=description,alt_title=alt_title))

                    if len(search_query.site_list) < 6:
                        continue
                    else:
                        session.add(search_query)
                        session.commit()
                        

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
# convert_responses()
# test_search()
# work_on_json()
# items = content[0]['pottery']['items'][1]['pagemap']['metatags'][0]
# insert_to_db_category()
insert_to_db_search_query_and_site()
