import json
import re
import urllib.request
from lxml import etree
import random
import requests
import time
import os

paperRecords = {}

with open('spiRecords.json','r') as fel:
    paperRecords = json.load(fel)

try:
    lastLst = paperRecords['lastLst']
except Exception as err:
    lastLst = []
dateStr = '2018-05-02'
#dateStr = time.strftime('%Y-%m-%d',time.localtime(time.time()))
toYear,toMonth,toDay = list(map(int,dateStr.split('-')))
strY = 'a' + str(toYear)
strM = 'a' + str(toMonth)
strD = 'a' + str(toDay)
try:
    if paperRecords[strY]:
        pass
    else:
        paperRecords[strY] = {}

except Exception as err:
    paperRecords[strY] = {}

try:
    if paperRecords[strY][strM]:        pass
    else:
        paperRecords[strY][strM] = {}

except Exception as err:
    paperRecords[strY][strM] = {}

try:
    if paperRecords[strY][strM][strD]:
        pass
    else:
        paperRecords[strY][strM][strD] = []

except Exception as err:
        paperRecords[strY][strM][strD] = []

headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',}


def getPaper(url):
    req = urllib.request.Request(url=url,headers=headers, method='GET')
    try:
        response = urllib.request.urlopen(req)
        html = response.read()
        selector = etree.HTML(html.decode('utf-8'))
        goodpath='/html/body/div[1]/div[1]/div[1]/div[2]/div[1]/main[1]/div[1]//div[2]/div[1]/article'
        article=selector.xpath(goodpath)
        return article
    except Exception as err:
        print(err,'getPaperError')
    finally:
        return []


def getHeadline(article):
    headline = []
    try:
        h1 = article[0].xpath('h1/span')
        for item in h1:
            headline.append(item.text)
        p1 = article[0].xpath('p[1]/text()')
        headline.append(p1[0])
    except Exception as err:
        print(err,'getHeadline')
    finally:
        return headline

def getContent(article):
    parr = []
    try:
        p = article[0].xpath('div[1]/div[3]/p/text()')
        for i in p:
            print(i)
            parr.append(i+'\n')
    except Exception as err:
        print(err,'getContent')
    finally:
        return parr

def getMain():
    #https://economist.com/latest-updates
    url = 'https://economist.com'
    req = urllib.request.Request(url=url,headers=headers, method='GET')
    response = urllib.request.urlopen(req)
    html = response.read()
    selector = etree.HTML(html.decode('utf-8'))
    goodpath='/html/body/div[1]/div[1]/div[1]/div[2]/div[1]/main[1]/div[1]/div[1]/div[1]/div[3]/ul[1]/li'
    art=selector.xpath(goodpath)
    awithtext = []
    try:
        for li in art:
            ap = li.xpath('article[1]/a[1]/div[1]/h3[1]/text()')
            a = li.xpath('article[1]/a[1]/@href')
            print(a,ap)
            awithtext.append([a[0],ap[0]])
        print(awithtext)
    except Exception as err:
        print(err,'getMain')
    finally:
        return awithtext


if __name__ == '__main__':
    linkArr = getMain()
    time.sleep(20)
    tmpLast = []
    toDayDir = './mds/' + dateStr +'/papers/'

    if not os.path.exists(toDayDir):
        os.makedirs(toDayDir)
    for item in linkArr:
        print(item)
        if item[0] not in lastLst:
            tmpLast.append(item[0])
            url = 'https://economist.com' + item[0]
            article = getPaper(url)
            headLine = getHeadline(article)
            try:
                paperRecords[strY][strM][strD].append([item[0],headLine[1]])
                content = getContent(article)
                paperName = '_'.join(item[1].split(' '))
                saveMd = toDayDir + paperName+'.md'
                result = headLine[1:]
                result.extend(content)
                output = '\n'.join(result)
                with open(saveMd,'w') as fw:
                    fw.write(output)
                time.sleep(60)
            except Exception as err:
                print(err)

    paperRecords['lastLst'] = tmpLast
    with open('spiRecords.json','w') as fwp:
        json.dump(paperRecords,fwp)
