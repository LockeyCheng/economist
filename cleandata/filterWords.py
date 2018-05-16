#coding=utf-8
from collections import Counter
import re
import os
import json
import time
import sys
from sys import argv
import enchant
d = enchant.Dict("en_US")

toos = ['though','great','woman','much','non','even','now','never','decision','rather','writing','best','became','group','too','used','men','giving','idea','white','say','taken','something','role','two','first','without','air','second','both','visit','three','own','style','also','other','all','themselves','year','type','women','between','student','who','only','people','think','going','what','cut','case','son','into','way','these','through','out','cannot','which','home','year','than','more','new','said','was','how','from','such','but','there','not','with','about','the','this', 'that', 'tomorrow', 'yesterday', 'next', 'last', 'one', 'over', 'under', 'above', 'below', 'beyond', 'besides', 'except', 'among', 'along', 'for', 'except', 'because', 'due', 'before', 'after', 'ago', 'later', 'towards', 'since', 'give', 'teach', 'buy', 'lend', 'find', 'and','hand', 'leave', 'sell', 'show', 'read', 'pay', 'make', 'offer', 'build', 'pass', 'bring', 'cook', 'are', 'were', 'did', 'has', 'have', 'had', 'will', 'shall', 'would', 'should', 'can', 'could', 'may', 'might', 'must', 'shall', 'should', 'will', 'would', 'need', 'ought', 'look', 'sound', 'taste', 'smell', 'feel', 'listen', 'seem', 'appear', 'become', 'get', 'besides', 'furthermore', 'moreover', 'yet', 'still', 'however', 'nevertheless', 'else', 'otherwise', 'thus', 'hence', 'therefore', 'accordingly', 'consequently', 'when', 'while', 'as', 'although', 'that', 'where', 'you', 'him', 'they', 'them', 'she', 'her', 'your', 'his', 'itsour', 'your', 'their', 'mine', 'hers', 'its', 'ours', 'yours', 'theirs']
exclude = []
with open('simpleWords.json','r')as fo:
    exclude = json.load(fo)
time.sleep(1)

def notSimple(word):
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
    global allkeys
    resultDict = []
    wordlst = None
    with open(filename, 'r') as fwc:
        for line in fwc:
            #content = re.sub('[-\"\|,.)(“”]', " ",line.lower())
            #lst = content.split(' ')
            lst = re.split('\W+',line)
            lst1 = [i for i in lst if len(i)>2 and i.isalpha()]
            resultDict.extend(lst1)
            
    allLen = len(resultDict)
    wordlst = Counter(resultDict)
    dicLen = len(wordlst)

    mb = wordlst.most_common(50)
    mbai = [item[0] for item in mb if item[0].lower() not in toos and item[0].lower()[0:-1] not in toos and item[0].lower()[0:-2] not in toos]
    mbai = mbai[0:16]
    allkeys.extend(mbai)
    allWordsPre = wordlst.most_common(dicLen)
    result = []
    allwords = [item[0].lower() for item in allWordsPre if len(item[0]) >2 and notSimple(item[0].lower()) and d.check(item[0])]
    for i in allwords:
        orw = i
        if i.endswith('ting') or i.endswith('ping') or i.endswith('ning'):
            i = i[0:-3]
            if not d.check(i):
                i = i+'e'

        if i.endswith('ings'):
            i = i[0:-4]
            if not d.check(i):
                i = i+'e'

        if i.endswith('ing'):
            i = i[0:-3]
            if not d.check(i):
                i = i+'e'

        if i.endswith('ers'):
            i = i[0:-1]
        if i.endswith('ies') or i.endswith('ied'):
            i = i[0:-3]+'y'
        if i.endswith('ded'):
            i = i[0:-2]
            if not d.check(i):
                i = i+'e'
        if i.endswith('ed'):
            su = d.suggest(i)
            le = len(i)
            for wo in su:
                if ' ' in wo:
                   wo = wo.split(' ')[0]
                if '-' in wo:
                   wo = wo.split('-')[0]
                if wo[0:le-2] == i[0:le-2] and len(wo) < le:
                     i = wo
                     break
            
        if i.endswith('s'):
            su = d.suggest(i)
            le = len(i)
            for wo in su:
                if wo[0:le-2] == i[0:le-2] and len(wo) < le:
                     i = wo
                     break

        if i in exclude:
            continue
        if d.check(i):
            result.append(i)


    timeTake = str(dicLen/100 + (dicLen/allLen)*5.6 + (len(result)/dicLen)*12)[0:4] + ' Minutes'

    wordD = {'suggestedfocus':timeTake,'wordsset':dicLen,'keywords':','.join(mbai),'toughwords':len(result),'allwords':allLen}
    datas = json.dumps(wordD)+'\n\n'+','.join(list(set(result)))
    allWords.append(','.join(list(set(result))))
    print('--------------------------------'+outPath+'--------------------------')
    print(datas)
    with open(outPath,'w') as fo:
        fo.write(datas)
allkeys = []
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
        print('final all: ')
        print(','.join(allWords))
        print('all keys:')
        print(','.join(allkeys))
