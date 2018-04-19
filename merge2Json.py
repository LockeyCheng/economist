import json

j1={}
j2={}
with open('economist_result.json','r')as f1:
    j1=json.load(f1)

with open('economist.json','r')as f2:
    j2 = json.load(f2)

for item in j1:
    if item not in j2:
        print item
        j2[item] = j1[item]

with open('mergeJsonResult.json','w')as fo:
    json.dump(j2,fo)
