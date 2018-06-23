import json
import re
import urllib.request
from lxml import etree
import random
import requests
import time
import os
from sys import argv

paperRecords = {}

headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',}

def getEP(url):
    req = urllib.request.Request(url=url,headers=headers, method='GET')
    try:
        response = urllib.request.urlopen(req)
        html = response.read()
        pout = []
        hout = []
        selector = etree.HTML(html.decode('utf-8'))
        headline = '//h1[@class="flytitle-and-title__body"]'
        head = selector.xpath(headline)
        for item in head:
#            a = item.xpath('span[1]/text()')[0]
            b = item.xpath('span[2]/text()')[0]
            hout.append(b)
#            hout.append(a)
        des = '//p[@class="blog-post__rubric"]/text()'
        desa = selector.xpath(des)
        for de in desa:
            hout.append(de)
        print(hout)
        ps = '//div[@class="blog-post__text"]'
        p=selector.xpath(ps)
        for item in p:
            pt = item.xpath('p/text()')
            for po in pt:
               pout.append(po)
        print(pout)
        img = '//img/@src' 
        srcs = selector.xpath(img)
        result = {'head':hout,'ps':pout,'imgsrc':srcs[0]}
        print(result)
        return result
    except Exception as err:
        print(err,url)

def getEA():
    url = 'https://economist.com/latest-updates'
    #url = 'https://economist.com'
    req = urllib.request.Request(url=url,headers=headers, method='GET')
    response = urllib.request.urlopen(req)
    html = response.read()
    selector = etree.HTML(html.decode('utf-8'))
    aa='//a[@class="teaser__link"]/@href'
    ahref = selector.xpath(aa)
    arr = []
    for a in ahref:
        arr.append(a)
        print(a)
    return arr

def getMA():
    url = 'http://www.dailymail.co.uk/home/latest/index.html'
    req = urllib.request.Request(url=url,headers=headers, method='GET')
    response = urllib.request.urlopen(req)
    html = response.read()
    selector = etree.HTML(html.decode('utf-8'))
    liss ='//li[@class="dynArticle"]'
    lis = selector.xpath(liss)
    awithtext = []
    for li in lis:
        lia = li.xpath('div[1]/div[1]/h3[1]/a[1]/@href')
        awithtext.append(lia)
    return awithtext
    
if __name__ == '__main__':
    try:
        script_name,paperType,dateStr = argv
    except Exception as err:
        print(err)
        paperType = 'te'
        dateStr = time.strftime('%Y-%m-%d',time.localtime(time.time()))

    intY,intM,intD = dateStr.split('-')
    toYear,toMonth,toDay = list(map(int,dateStr.split('-')))
    ayear = 'a' + str(toYear) 
    amonth = 'a' + str(toMonth)
    aday = 'a' + str(toDay)
    dateDir = ayear + '/' + amonth +'/' + aday

    if paperType == 'te':
        linkArr = getEA()
        basedir = './The_Economist/'
    if paperType == 'mail':
        linkArr = getMA()
        basedir = './Mail_Online/'
    spiRecords = basedir+'spiRecords.json'
    with open(spiRecords,'r') as fel:
        paperRecords = json.load(fel)

    try:
        lastLst = paperRecords['lastLst']
    except Exception as err:
        lastLst = []

    if ayear not in paperRecords:
        paperRecords[ayear] = {}
    if amonth not in paperRecords[ayear]:
        paperRecords[ayear][amonth] = {}
    if aday not in paperRecords[ayear][amonth]:
        paperRecords[ayear][amonth][aday] = []
    
    time.sleep(12)
    tmpLast = []
    toDayDir = basedir + dateDir + '/papers/'
    if not os.path.exists(toDayDir):
        os.makedirs(toDayDir)
    for item in linkArr:
        print(item)
        if item not in lastLst:
            paperRecords['lastLst'].append(item)
            if paperType == 'te':
                url = 'https://economist.com' + item
                article = getEP(url)
            if paperType == 'mail':
                url = 'http://www.dailymail.co.uk' + item
                article = getMP(url)

            try:
                paperName = '_'.join(article['head'][0].split(' '))
                saveMd = toDayDir + paperName+'.md'
                result = article['head']+[article['imgsrc']]+article['ps']
                output = '\n\n'.join(result)
                if len(output) < 100:
                    continue
                paperRecords[ayear][amonth][aday].append([item,article['head'][0]])
                with open(saveMd,'w') as fw:
                    fw.write(output)
                time.sleep(30)
            except Exception as err:
                print(err)

    paperRecords['lastLst'] = paperRecords['lastLst'][-30:]
    with open(spiRecords,'w') as fwp:
        json.dump(paperRecords,fwp)
