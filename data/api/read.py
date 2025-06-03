import json

file = open('data/json/api-output/art.json','r')
content = json.load(file)

count = 0
max = 0
for i in content:
    for key in i:


        # for j in range(len(i[key]['items'])):
        #     items = i[key]['items'][j]['pagemap']
        #     if not 'metatags' in items:
        #         print('no metatag')
        #     else:
        #         print(items['metatags'])
# items = content[0]['pottery']['items'][1]['pagemap']['metatags'][0]
