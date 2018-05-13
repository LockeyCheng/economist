#coding=utf-8
from collections import Counter
import re
import os
#获取目录中所有txt结尾的文件名列表，因为本题条件单纯，所以也可以使用os.listdir()方法
import json
import time
import sys
from sys import argv
import enchant
d = enchant.Dict("en_US")


exclude = []
with open('simpleWords.json','r')as fo:
    exclude = json.load(fo)
time.sleep(1)

def getOrigianlForm(word):
    if not word.isalpha():
        return False
    if word in exclude:
        return False
    if word.endswith('ment') or word.endswith('ness'):
        word = word[0:-4]
        if word in exclude:
            return False
    if word.endswith('tion'):
        word = word[0:-4]
        if word in exclude:
            return False
        word += 't'
        if word in exclude:
            return False
        word = word[0:-1] +'e'
        if word in exclude:
            return False

    if word.endswith('ing'):
        word = word[0:-3]
        if word in exclude:
            return False
        word += 'e'
        if word in exclude:
            return False
    if word.endswith('ies'):
        word = word[0:-3]
        if word in exclude:
            return False
        word += 'y'
        if word in exclude:
            return False
    if word.endswith('es'):
        word = word[0:-2]
        if word in exclude:
            return False
        word += 'e'
        if word in exclude:
            return False
        word += 's'

    if word.endswith('ers'):
        word = word[0:-1]
        if word in exclude:
            return False
        word = word[0:-1]
        if word in exclude:
            return False
        word = word[0:-1]
        if word in exclude:
            return False
        return True

    if word.endswith('est'):
        word = word[0:-3]
        if word in exclude:
            return False
        word = word[0:-1]
        if word in exclude:
            return False

    if word.endswith('ied'):
        word = word[0:-2]
        if word in exclude:
            return False
        word += 'y'
        if word in exclude:
            return False
        return True

    if word.endswith('ted') or word.endswith('ded'):
        word = word[0:-2]
        if word in exclude:
            return False
        word = word[0:-1]
        if word in exclude:
            return False
        return True

    if word.endswith('ed'):
        word = word[0:-2]
        if word in exclude:
            return False
        word += 'e'
        if word in exclude:
            return False
        return True

    if word.endswith('s') and len(word)>3:
        word = word[0:-1]
        if word in exclude:
            return False

    if word.endswith('ly'):
        if word.endswith('ily'):
            word = word[0:-3]+'y'
            if word in exclude:
                return False
        word = word[0:-2]
        if word in exclude:
            return False
    return True

allWords = []
def wc(filename,outPath):
    global allWords
    resultDict = []
    wordlst = None
    with open(filename, 'r') as fwc:
        for line in fwc:
            #content = re.sub('[-\"\|,.)(“”]', " ",line.lower())
            #lst = content.split(' ')
            lst = re.split('\W+',line)
            lst1 = [i.lower() for i in lst if len(i)>2 and d.check(i) and getOrigianlForm(i)]
            resultDict.extend(lst1)
            

    wordlst = Counter(resultDict)
    dicLen = len(wordlst)

    mb = wordlst.most_common(15)
    mbai = [item[0] for item in mb]
    print('--------------------------------------------------------------most 100')
    print(','.join(mbai))

    allWordsPre = wordlst.most_common(dicLen)
    result = []
    allwords = [item[0] for item in allWordsPre if len(item[0]) >2 and item[0] not in exclude]
    for i in allwords:
        if i.endswith('ting') or i.endswith('ping') or i.endswith('ning'):
            i = i[0:-3]
        if i.endswith('ings'):
            i = i[0:-4]
        if i.endswith('ing'):
            i = i[0:-3]+'e'
        if i.endswith('ers'):
            i = i[0:-1]
        if i.endswith('ies') or i.endswith('ied'):
            i = i[0:-3]+'y'
        if i.endswith('ded'):
            i = i[0:-2]
        if i.endswith('es') or i.endswith('ts') or i.endswith('tions') or i.endswith('ments'):
            i = i[0:-1]
        if i in exclude:
            continue
        if i.isalpha():
            result.append(i)
    baiStr = ','.join(mbai)+'\n\n'
    datas = baiStr+','.join(list(set(result)))
    allWords.append(','.join(list(set(result))))
    print('--------------------------------------------------------------all words string')
    print(datas)
    with open(outPath,'w') as fo:
        fo.write(datas)

if __name__ == "__main__":
    try:
        script_name,paperType,dateStr = argv
    except Exception as err:
        print(err)
        paperType = 'te'
        dateStr = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    basedir = './The_Economist/'
    if paperType == 'mail':
        basedir = './Mail_Online/'
    dateArr = [dateStr]
    #dateArr = ['2018-04-18', '2018-04-19', '2018-04-20', '2018-04-21', '2018-04-22', '2018-04-23', '2018-04-24', '2018-04-25', '2018-04-26', '2018-04-27', '2018-04-28', '2018-04-29', '2018-04-30','2018-05-01', '2018-05-02', '2018-05-03', '2018-05-04', '2018-05-05', '2018-05-06', '2018-05-07', '2018-05-08', '2018-05-09', '2018-05-10', '2018-05-11']
    
    for dateStr in dateArr:
        toYear,toMonth,toDay = list(map(int,dateStr.split('-')))
        ayear = 'a' + str(toYear) 
        amonth = 'a' + str(toMonth)
        aday = 'a' + str(toDay)
        dateDir = ayear + '/' + amonth +'/' + aday
        readPath = basedir + dateDir +'/papers/'
        baseOut = basedir + dateDir +'/words/'
        readMds = []
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

        if not os.path.exists(baseOut):
            os.makedirs(baseOut)
        todayAll = []
        for paper in readMds:
                countPaper = paper[0]
                outWords = baseOut + paper[1][0:-2]+'txt'
                print(countPaper,outWords)
                wc(countPaper,outWords)

        print(','.join(allWords))
