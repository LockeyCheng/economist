import json
dict = {}
with open('result1.json','r') as fj:
    dict = json.load(fj)
    print(dict['embody'])
