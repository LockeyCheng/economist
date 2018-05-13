import json
import time
import re
import os
import sys
from sys import argv
exclude = {}
with open('simpleWords.json','r')as fo:
    exclude = json.load(fo)
time.sleep(1)

dic = {}
records = {}
paperTitle = 'Lockey23'
keywords = None

dayArr = [31,29,31,30,31,30,31,31,30,31,30,31]
def genPaper(spidJson,origMd,genJson,nextPaper):
    global records
    global paperTitle
    global keywords
    result = []
    try:
        lastPaper = records['lastPaper']
    except Exception as err:
        lastPaper = ''
    print(lastPaper)
    with open(spidJson,'r')as fj:
       dic = json.load(fj)
    keys = list(dic.keys())
    keys = [i for i in keys if len(i)>2]

    keywords = dic['keywords']
    dic.pop('keywords')

    with open(origMd,'r')as fm:
        lineno = 0
        for line in fm:
            if lineno == 0:
                paperTitle = line
                lineno += 1
                continue
            newLine = line
            for key in keys:
                span = '<span class="fa fa-info-circle">' + key + '</span>'
                if re.search(key, newLine):
                    newLine = re.sub(key, span, newLine, flags=re.IGNORECASE)
                    continue
                word = False
                if key.endswith('ing'):
                    word = key[0:-3]

                if key.endswith('ers'):
                    word = key[0:-1]

                if key.endswith('ies') or key.endswith('ied') or key.endswith('ily'):
                    word = key[0:-3]+'y'

                if key.endswith('ded') or key.endswith('ted'):
                    word = key[0:-2]

                if key.endswith('ment') or key.endswith('ness'):
                    word = key[0:-4]


                if word and len(word) >2:    
                    span = '<span class="fa fa-info-circle">' + word + '</span>'
                    if re.search(word, newLine):
                        newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                        continue

                if key.endswith('ly'):
                    word = key[0:-2]
                    span = '<span class="fa fa-info-circle">' + word + '</span>'
                    if re.search(word, newLine) and len(word) >2:
                        newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                        continue

                if key.endswith('ed') or key.endswith('es') or key.endswith('ts'):
                    word = key[0:-1]
                    span = '<span class="fa fa-info-circle">' + word + '</span>'
                    if re.search(word, newLine) and len(word) >2:
                        newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                        continue

                if key.endswith('s'):
                    word = key[0:-1]
                    span = '<span class="fa fa-info-circle">' + word + '</span>'
                    if re.search(word, newLine) and len(word) >2:
                        newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                        continue

                if key.endswith('tion'):
                    word = key[0:-4]
                    if re.search(word, newLine) and len(word) >2:
                        span = '<span class="fa fa-info-circle">' + word + '</span>'
                        newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                        continue
                    word += 't' 
                    if re.search(word, newLine) and len(word) >2:
                        span = '<span class="fa fa-info-circle">' + word + '</span>'
                        newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                        continue
            
            result.append(newLine)

        resultStr = ' '.join(result)
        article={'date':'{} By Lockey.'.format(dateStr),'content':resultStr,'last':lastPaper,'next':nextPaper,'assistent':dic,'title':paperTitle,'keywords':keywords}
        with open(genJson,'w') as fj:
            json.dump(article,fj)


def genPaperOld(spidJson,origMd,genJson,nextPaper):
    global records
    global paperTitle
    global keywords
    result = []
    try:
        lastPaper = records['lastPaper']
    except Exception as err:
        lastPaper = ''
    print(lastPaper)
    with open(spidJson,'r')as fj:
       dic = json.load(fj)
    keywords = dic['keywords']
    dic.pop('keywords')
    with open(origMd,'r')as fm:
        lineno = 0
        for line in fm:
            if lineno == 0:
                paperTitle = line
                lineno += 1
            words = line.split(' ')
            wordstr = []
            for i in words:
                suffix = ''
                if "'" in i:
                    suffix = "'"+i.split("'")[1]
                    i = i.split("'")[0]

                if "-" in i:
                    suffix = "-"+i.split("-")[1]
                    i = i.split("-")[0]

                if "." in i:
                    suffix = "."
                    i = i.split(".")[0]

                if "/" in i:
                    suffix = "/"+i.split("/")[1]
                    i = i.split("/")[0]
                if '?' in i:
                    suffix = "?"
                    i = i.split("?")[0]
                if "," in i:
                    suffix = ","
                    i = i.split(",")[0]
                if "“" in i:
                    suffix = ""
                    i = i[1:]
                if "”" in i:
                    suffix = "”"
                    i = i[0:-1]

                try:
                    reali = i
                    if i.endswith('ing'):
                        i = i[0:-3]
                    if i.endswith('ies') or i.endswith('ied'):
                        i = i[0:-3] + 'y'
                    if i.endswith('est'):
                        i = i[0:-2]
                    if i.endswith('ily'):
                        i = i[0:-3]+'y'

                    if i.endswith('ers'):
                        i = i[0:-1]
                    if i.endswith('es') or i.endswith('ed') or i.endswith('td'):
                        i = i[0:-1]
                  
                    for item in dic:
                        if len(i) >3 and (re.search(item[0:len(i)],i) or re.search(i[0:len(item)],item)) and reali not in exclude and i not in exlude:
                            i = '<span class="fa fa-info-circle">'+reali+'</span>'+suffix
                            break
                    if len(i) < 20:
                        i = reali + suffix
                except Exception as err1:
                    try:
                        reali = i
                        if i.endswith('ing'):
                            i = i[0:-3] + 'e'
                        elif i.endswith('es') or i.endswith('ed'):
                            i = i[0:-1]
                        for item in dic:
                            if len(i) >3 and (re.search(item[0:len(i)],i) or re.search(i[0:len(item)],item)) and reali not in exclude and i not in exclude:
                                i = '<span class="fa fa-info-circle">'+reali+'</span>' + suffix
                                break
                        if len(i) < 18:
                            i = reali + suffix

                    except Exception as err2:
                        pass#print(err2,i)
                finally:
                    wordstr.append(i)
            oo = ' '.join(wordstr)
            result.append(oo)
        result = [i for i in result if i not in exclude]
        good = ' '.join(result)
        article={'date':'{} By Lockey.'.format(dateStr),'content':good,'last':lastPaper,'next':nextPaper,'assistent':dic,'title':paperTitle,'keywords':keywords}
        with open(genJson,'w') as fj:
            json.dump(article,fj)

import qrcode

if __name__ == '__main__':
        try:
            script_name,paperType,dateStr = argv
        except Exception as err:
            print(err)
            paperType = 'te'
            dateStr = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        if paperType == 'te':
            basedir = './The_Economist/'
        if paperType == 'mail':
            basedir = './Mail_Online/'

        toYear,toMonth,toDay = list(map(int,dateStr.split('-')))
        ayear = 'a' + str(toYear)
        amonth = 'a' + str(toMonth)
        aday = 'a' + str(toDay)
        dateDir = ayear + '/' + amonth +'/' + aday

        mdPath = basedir + dateDir +'/papers/'
        spijsonPath = basedir + dateDir +'/jsons/'
        genjsonPath = basedir + dateDir +'/results/'

        intY,intM,intD = dateStr.split('-') 
        toYear,toMonth,toDay = list(map(int,dateStr.split('-')))
        paperRecords = basedir + 'paperRecords.json'

        with open(paperRecords,'r')as fo:
            records = json.load(fo)

        paperArr = []
        ayear = 'a' + str(toYear) 
        amonth = 'a' + str(toMonth)
        aday = 'a' + str(toDay)
        if ayear not in records:
            records[ayear] = {}
        if amonth not in records[ayear]:
            records[ayear][amonth] = {}
        if aday not in records[ayear][amonth]:
            records[ayear][amonth][aday] = []

        if os.path.exists(mdPath):
            for item in os.listdir(mdPath):
                paperArr.append([mdPath+item,spijsonPath+item[0:-2]+'json',genjsonPath+item[0:-2]+'json',item])

        if len(paperArr) <= 0:
            print('NO PAPER TO FILTER!')
            sys.exit()

        if not os.path.exists(genjsonPath):
            os.makedirs(genjsonPath)
        for pp in paperArr:
            todayPush = len(records[ayear][amonth][aday])
            title = '{}_{}_{}_{}.json'.format(toYear,toMonth,toDay,todayPush+1)
            if todayPush == len(paperArr)-1:
                eyear = toYear
                emonth = toMonth
                eday = toDay + 1
                if eday > dayArr[toMonth-1]:
                    emonth = toMonth + 1
                    eday = 1

                if emonth >12:
                    eyear = toYear + 1
                    emonth = 1
                    eday = 1
                print(eyear,emonth,eday,dayArr[toMonth-1])
                nextPaper = '{}_{}_{}_{}.json'.format(eyear,emonth,eday,1)
            else:
                nextPaper = '{}_{}_{}_{}.json'.format(toYear,toMonth,toDay,todayPush+2)
            genPaper(pp[1],pp[0],genjsonPath+title,nextPaper)
            #genPaperOld(pp[1],pp[0],genjsonPath+title,nextPaper)            
            records['lastPaper'] = title
            paperId = str(intY)+str(intM)+str(intD)+str(todayPush+1)
            link = 'https://lockeycheng.github.io/iooi/index.html?paper={}'.format(paperId)
            print(link)
            img = qrcode.make(link)
            linkeTitle = '{}_{}_{}_{}'.format(toYear,toMonth,toDay,todayPush+1)
            imgFile = basedir + 'QRimages/'+linkeTitle+'.png'
            with open(imgFile,'wb') as fo:
                img.save(fo)
            thisArr = [title,paperTitle,keywords]
            records[ayear][amonth][aday].append(thisArr)

        with open(paperRecords,'w')as fa:
            json.dump(records,fa)
