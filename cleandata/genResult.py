import json
import time
import re
import os
import sys
from shutil import copyfile

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
def genPaper(spidJson,origMd,genJson,nextPaper,fileName):
    global records
    global latestPapers
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
    paperStatistics = dic['paperStatistics']
    keywords = paperStatistics['keywords']
    dic.pop('paperStatistics')

    with open(origMd,'r')as fm:
        lineno = 0
        for line in fm:
            if lineno == 0:
                paperTitle = line
                paperStatistics['title'] = line
                lineno += 1
                continue
            if lineno == 2:
                paperStatistics['desc'] = line
            lineno += 1
            if line.startswith('https://'):
                paperStatistics['img'] = line
                continue
            newLine = line
            for key in keys:
                span = '<span class="word-wrap-span">' + key + '</span>'
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
                    span = '<span class="word-wrap-span">' + word + '</span>'
                    if re.search(word, newLine):
                        newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                        continue

                if key.endswith('ly'):
                    word = key[0:-2]
                    span = '<span class="word-wrap-span">' + word + '</span>'
                    if re.search(word, newLine) and len(word) >2:
                        newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                        continue

                if key.endswith('ed') or key.endswith('es') or key.endswith('ts'):
                    word = key[0:-1]
                    span = '<span class="word-wrap-span">' + word + '</span>'
                    if re.search(word, newLine) and len(word) >2:
                        newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                        continue

                if key.endswith('s'):
                    word = key[0:-1]
                    span = '<span class="word-wrap-span">' + word + '</span>'
                    if re.search(word, newLine) and len(word) >2:
                        newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                        continue

                if key.endswith('tion'):
                    word = key[0:-4]
                    if re.search(word, newLine) and len(word) >2:
                        span = '<span class="word-wrap-span">' + word + '</span>'
                        newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                        continue
                    word += 't' 
                    if re.search(word, newLine) and len(word) >2:
                        span = '<span class="word-wrap-span">' + word + '</span>'
                        newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                        continue
            
            result.append('<p>'+newLine+'</p>')

        resultStr = ' '.join(result)
#time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        genDate = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))#dateStr+' 00:06:36'
        paperStatistics['date'] = genDate
        paperStatistics['link'] = fileName
        latestPapers['papers'].append(paperStatistics)
        article={'Date':genDate,'content':resultStr,'Last':lastPaper,'Next':nextPaper,'assistent':dic,'Title':paperTitle,'paperStatistics':paperStatistics}
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
        gitPath = '/root/LockeyCheng.github.io/iledu/The_Economist'
        latestPapers = {'papers':[],'more':None}
        toYear,toMonth,toDay = list(map(int,dateStr.split('-')))
        ayear = 'a' + str(toYear)
        amonth = 'a' + str(toMonth)
        aday = 'a' + str(toDay)
        dateDir = ayear + '/' + amonth +'/' + aday

        mdPath = basedir + dateDir +'/papers/'
        spijsonPath = basedir + dateDir +'/jsons/'
        genjsonPath = basedir + dateDir +'/results/'
        outcomePath = './outcome'

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
            genPaper(pp[1],pp[0],genjsonPath+title,nextPaper,title)
            records['lastPaper'] = title
            paperId = str(intY)+str(intM)+str(intD)+str(todayPush+1)
            link = 'https://lockeycheng.github.io/iledu/article.html?paper={}'.format(paperId)
            print(link)
            img = qrcode.make(link)
            linkTitle = '{}_{}_{}_{}'.format(toYear,toMonth,toDay,todayPush+1)
            imgFile = os.path.join(gitPath+'/QRimages',linkTitle+'.png')
            with open(imgFile,'wb') as fo:
                img.save(fo)
            thisArr = [title,paperTitle,keywords]
            records[ayear][amonth][aday].append(thisArr)
        more = 'a'+''.join(dateStr.split('-'))
        latestPaperFile = basedir+'latestPapers.json'
        
        try:
            morefile = more+'.json'
            latestPapers['more'] = morefile
            os.rename(latestPaperFile,basedir+morefile)
            desppp = os.path.join(gitPath,'amore/'+morefile)
            copyfile(basedir+morefile, desppp)
            with open(latestPaperFile,'w')as fa:
                json.dump(latestPapers,fa)
            desppp = os.path.join(gitPath,'amore/latestPapers.json')
            copyfile(latestPaperFile, desppp)
        except Exception as err:
           print(err)
           
        with open(paperRecords,'w')as fa:
            json.dump(records,fa)
        gitPath_ym = os.path.join(gitPath,ayear+'/'+amonth)
        copyfile(paperRecords, os.path.join(gitPath,'paperRecords.json'))
        for res in os.listdir(genjsonPath):
            f1 = os.path.join(genjsonPath,res)
            f2 = os.path.join(gitPath_ym,res)
            copyfile(f1, f2)
