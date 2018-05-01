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
    keywords = dic['keywords']

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
                        if len(reali) >3 and (re.search(item[0:len(i)],i) or re.search(i[0:len(item)],item)) and reali not in exclude:
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
                            if len(reali) >3 and (re.search(item[0:len(i)],i) or re.search(i[0:len(item)],item)) and reali not in exclude:
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
        script_name,dateStr = argv
        if not dateStr:
            dateStr = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        mdPath = './mds/' + dateStr +'/papers/'
        spijsonPath = './mds/' + dateStr +'/jsons/'
        genjsonPath = './mds/' + dateStr +'/results/'
        intY,intM,intD = dateStr.split('-') 
        toYear,toMonth,toDay = list(map(int,dateStr.split('-')))

        with open('paperRecords.json','r')as fo:
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
            nextPaper = '{}_{}_{}_{}.json'.format(toYear,toMonth,toDay,todayPush+2)
            print('curretTitle: ',title)
            print('currentPaper: ',pp[0])
            genPaper(pp[1],pp[0],genjsonPath+title,nextPaper)            
            records['lastPaper'] = title
            paperId = str(intY)+str(intM)+str(intD)+str(todayPush+1)
            link = 'https://lockeycheng.github.io/economist/index.html?paper={}'.format(paperId)
            print(link)
            img = qrcode.make(link)
            linkeTitle = '{}_{}_{}_{}'.format(toYear,toMonth,toDay,todayPush+1)
            imgFile = './economistQrcode/'+linkeTitle+'.png'
            with open(imgFile,'wb') as fo:
                img.save(fo)
            thisArr = [title,paperTitle,keywords]
            records[ayear][amonth][aday].append(thisArr)

        with open('paperRecords.json','w')as fa:
            json.dump(records,fa)
