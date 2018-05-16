import json

with open('The_Economist/a2018/a5/a18/words/aa.txt','r') as fo:
     dic = None     
     no = 1
     for line in fo:
        if no == 1:
            dic = json.loads(line)
        no += 1

print(dic['total'],dic['keywords'])
