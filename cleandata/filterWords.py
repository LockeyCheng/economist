#coding=utf-8
from collections import Counter
import re
import os
#获取目录中所有txt结尾的文件名列表，因为本题条件单纯，所以也可以使用os.listdir()方法
import json
import time
import sys
from sys import argv

exclude = []
with open('simpleWords.json','r')as fo:
    exclude = json.load(fo)
time.sleep(1)

def getOrigianlForm(word):
    if word in exclude:
        return False
    if len(word) <=3:
        if word in exclude:
            return False
        return True
    if word.endswith('ment'):
        word = word[0:-4]
        if word not in exclude:
            return True
        return False
    if word.endswith('ing'):
        word = word[0:-3]
        if word not in exclude and word[-1] == 'y':
            return True
        word += 'e'
        if word not in exclude:
            return True
        return False
    if word.endswith('ies'):
        word = word[0:-3]
        if word not in exclude:
            word += 'y'
            if word not in exclude:
                return True
        return False
    if word.endswith('es'):
        word = word[0:-2]
        if word not in exclude:
            word += 'e'
            if word not in exclude:
                return True
        return False

    if word.endswith('ers'):
        word = word[0:-1]
        if word not in exclude:
            word = word[0:-1]
            if word not in exclude:
                word = word[0:-1]
                if word not in exclude:
                    return True
        return False

    if word.endswith('est'):
        word = word[0:-3]
        if word not in exclude:
            word = word+'e'
            if word not in exclude:
                return True
        return False

    if word.endswith('ied'):
        word = word[0:-2]
        if word not in exclude:
            word += 'y'
            if word not in exclude:
                return True
        return False

    if word.endswith('ted'):
        word = word[0:-2]
        if word not in exclude:
            return True
        return False

    if word.endswith('ed'):
        word = word[0:-2]
        if word not in exclude:
            word += 'e'
            if word not in exclude:
                return True
        return False
    if word.endswith('s'):
        word = word[0:-1]
        if word not in exclude:
            return True
        return False
    if word.endswith('ly'):
        if word.endswith('ily'):
            word = word[0:-3]+'y'
            if word not in exclude:
                return True
            return False
        
        word = word[0:-2]
        if word not in exclude:
            return True
        return False
    return True

todayAll = []
def wc(filename,outPath):
    global todayAll
    resultDict = []
    wordlst = None
    with open(filename, 'r') as fwc:
        for line in fwc:
            content = re.sub('[-\"\|,.)(“”]', " ",line.lower())
            lst = content.split(' ')
            lst1 = [i.lower() for i in lst if len(i)>2 and getOrigianlForm(i) and i.isalpha() and i not in exclude]
            resultDict.extend(lst1)
            

    wordlst = Counter(resultDict)
    dicLen = len(wordlst)

    mb = wordlst.most_common(20)
    mbai = [item[0] for item in mb]
    print('--------------------------------------------------------------most 100')
    print(','.join(mbai))

    allWordsPre = wordlst.most_common(dicLen)
    result = []
    allwords = [item[0] for item in allWordsPre if len(item[0]) >2 and item[0] not in exclude]
    for i in allwords:
        if i.endswith('ing'):
            i = i[0:-3]
        if i.endswith('ings'):
            i = i[0:-4]
        if i.endswith('ers'):
            i = i[0:-1]
        if i.endswith('ies') or i.endswith('ied'):
            i = i[0:-3]+'y'
        if i.endswith('ded'):
            i = i[0:-2]
        if i.endswith('es') or i.endswith('ts'):
            i = i[0:-1]
        if i in exclude:
            continue
        if i.isalpha():
            result.append(i)
    baiStr = ','.join(mbai)+'\n\n'
    datas = baiStr+','.join(list(set(result)))
    todayAll.append(','.join(list(set(result))))
    print('--------------------------------------------------------------all words string')
    print(datas)
    with open(outPath,'w') as fo:
        fo.write(datas)

if __name__ == "__main__":
    script_name,dateStr = argv
    if not dateStr:
        dateStr = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    toYear,toMonth,toDay = list(map(int,dateStr.split('-')))
    readPath = './mds/' + dateStr +'/papers/'
    outPath = './mds/' + dateStr +'/words/'
    readMds = []
    testGo = False
    if testGo:
        wc('todaymd.md','todaymd.txt')
        sys.exit()
    if os.path.exists(readPath):
        for item in os.listdir(readPath):
            readMds.append([readPath+item,item])
    else:
        print('Dir not found!')
        os.makedirs(readPath)
        sys.exit()
    if len(readMds) <= 0:
        print('NO PAPER TO FILTER!')
        sys.exit()
    
    if not os.path.exists(outPath):
        os.makedirs(outPath)

    for paper in readMds:
        countPaper = paper[0]
        outWords = outPath + paper[1][0:-2]+'txt'
        print(countPaper,outWords)
        wc(countPaper,outWords)
    todayallstr = ','.join(todayAll)
    todayallstr = todayallstr.split(',')
    todayallstr = list(set(todayallstr))
    todayallstr = ','.join(todayallstr)
    todayAllWords = './mds/' + dateStr + '/allWords.txt'
    with open(todayAllWords,'w')as foo:
        foo.write(todayallstr)
