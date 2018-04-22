import json

dic = {}
result=[]
title = None
with open('todaymd.json')as fj:
   dic = json.load(fj)

with open('todaymd.md','r')as fm:
    lineno = 0
    for line in fm:
        if lineno == 0:
            title = line
            lineno += 1
        words = line.split(' ')
        wordstr = []
        for i in words:
            try:
                reali = i
                if i.endswith('ing') or i.endswith('ies') or i.endswith('est') or i.endswith('ied'):
                    i = i[0:-3]
                elif i.endswith('es') or i.endswith('er') or i.endswith('ed') or i.endswith('ly'):
                    i = i[0:-2]
                elif i.endswith('s'):
                    i = i[0:-1]
                if dic[i]:
                    i = '<span class="fa fa-info-circle">'+i+'</span>'
                else:
                    i = reali
            except Exception as err1:
                try:
                    reali = i
                    if i.endswith('ing'):
                        i = i[0:-3] + 'e'
                    elif i.endswith('ies') or i.endswith('ied'):
                        i = i[0:3] + 'y'
                    elif i.endswith('es') or i.endswith('er') or i.endswith('ed'):
                        i = i[0:-1]
                    elif i.endswith('ly'):
                        i = i[0:-2]+'e'
                    if dic[i]:
                        i = '<span class="fa fa-info-circle">'+i+'</span>'
                    else:
                        i = reali
                except Exception as err2:
                    pass#print(err2,i)
            finally:
                wordstr.append(i)
        oo = ' '.join(wordstr)
        result.append(oo)
        good = ' '.join(result)
        article={'date':'Lockey 2018-04-21','content':good,'last':'2018_4_20.json','next':'2018_4_22.json','assistent':dic,'title':title}
        with open('fimd.md','w')as fo:
            fo.write(good)
        with open('fijson.json','w') as fj:
            json.dump(article,fj)
