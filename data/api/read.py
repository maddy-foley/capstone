import json

file = open('data/json/api-output/art.json','r')
content = json.load(file)
for c in content:
    for key in c:

        items = c[key]['items']
        print(items)
    # print(item['display'])
    # print(item['metadata'])
