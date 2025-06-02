import json

file = open('data/json/api-output/test-2.json','r')
content = json.load(file)
items = content[0]['shoes']['items']
for item in items:
   print(item['snippet'])
    # print(item['display'])
    # print(item['metadata'])
