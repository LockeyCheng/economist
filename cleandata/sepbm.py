import json
from sys import argv
basic = {}
model = {}
te = ['economist.json','economist_basic.json','economist_model.json']
cet46 = ['cet46.json','cet46_basic.json','cet46_model.json']

script,dic = argv

if dic == 'te':
    dicc = te
else:
   dicc = cet46

print(dicc)

with open(dicc[0],'r')as fo:
    adic = json.load(fo)
    dicLen = len(adic)
    for word in adic:
        try:
            db = {'ex':adic[word]['ex'],'pron':adic[word]['pron']}
            dm = {'eg2':adic[word]['eg2']}
            try:
               dm['wp'] = adic[word]['wp']
            except Exception as err:
               print(err)
            try:
               db['st'] = adic[word]['st']
            except Exception as err:
               print(err)
            finally:
               basic[word] = db
               model[word] = dm
        except Exception as err:
            print(err,'seperate error: ',word)

with open(dicc[1],'w')as fb:
    json.dump(basic,fb)

with open(dicc[2],'w')as fm:
    json.dump(model,fm)

print(dicLen)
