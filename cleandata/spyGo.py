import urllib.request
from lxml import etree
import re
import time
from functools import reduce
import json
import random
import requests
import sys
import os
from sys import argv

replace_blank = re.compile('\n')
times = 0

ebasic = {}
emodel = {}
resultDict = {}
failed = []
failedbi = []
failedbei = []

with open('economist.json','r') as fe:
    completeDict = json.load(fe)

def get_page(myword):
    html = None
    try:
        lookurl='http://www.youdao.com/w/eng/{}/#keyfrom=dict2.index'.format(myword)
        response =  urllib.request.urlopen(lookurl)
        html = response.read()
        global times
        times += 1
    except Exception as err:
        print(err,'get html error')

    return html

def get_word_explanation(html_selector,word):
    dic = []
    goodExp = '/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]/ul[1]/li'
    try:
        exp = html_selector.xpath(goodExp)
        for li in exp:
            ex = li.text
            dic.append(ex)
    except Exception as err:
        pass#print(err,'get explanation error: ',word)

    return dic

def get_parse(html_selector,word):
    parses = {}
    hanyi_xpath='/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[5]/p'
    try:
        get_hanyi=html_selector.xpath(hanyi_xpath)
        no = 0
        for item in get_hanyi:
            enp = 'span[1]/a[1]/text()'
            aa=item.xpath(enp)
            no += 1
            cnp = './text()'
            translation = item.xpath(cnp)
            translation = (''.join(translation)).strip()
            translation = translation.replace("\n", "")
            translation = translation.replace(' ','')
            ajoin = '_'.join(aa)
            parses[ajoin]=translation
    except Exception as err:
        pass#print(err,'get parses error: ',word)
    return parses

def get_prono(html_selector,word):
    dic = {}
    goodPro='/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/h2[1]/div[1]/span'
    prono=html_selector.xpath(goodPro)
    for item in prono:
        try:
            peg = item.xpath('span[1]/text()')
            dic['peg'] = peg[0]
        except Exception as err:
            pass#print(err,word,'get pronounce of English')
        try:
            pam = item.xpath('span[1]/text()')
            dic['pam'] = pam[0]
        except Exception as err:
            pass#print(err,word,'get pronounce of American')

    return dic

def remove_blank_line(arg):
    if isinstance(arg,list):
        result1 = list(map(lambda i:i.replace("\n", ""),arg))
        result = list(map(lambda i:i.replace(" ", ""),result1))
    else:
        result = 'aaaaaaaaaa'
    return result

def get_similar_transform(html_selector,word):
    dic = {}
    ulno = 1
    def get_st(ulno):
        goodpath='/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[5]/div[1]/div[1]/ul[{}]/li'.format(ulno)
        goodli=html_selector.xpath(goodpath)
        no = 0
        for li in goodli:
            if no > 0:
                spanName = li.xpath('ul[1]/span/text()') or li.xpath('span/text()')
                if not '变形：' in spanName and not '近义词:' in spanName:
                   continue
                if '变形：' in spanName:
                    transform = li.xpath('ul[1]/p/a/text()')
                    tra = []
                    tType = li.xpath('ul[1]/p/text()')
                    tType = remove_blank_line(tType)#list(map(lambda i:i.replace("\n", ""),tType))
                    tType = [i for i in tType if i != '.' and i != '']
                    transNo = 1
                    for i in range(len(tType)):
                        pa = 'ul[1]/p[{}]/a/text()'.format(transNo)
                        transform = li.xpath(pa)
                        tra.append([tType[i],','.join(transform)])
                    dic['transform'] = tra
                  # print(','.join(transform))
                  # dic['transform'] = ','.join(transform)
                if '近义词:' in spanName:
                   similar = li.xpath('p/a/text()')
                   pass#print(','.join(similar))
                   dic['similar'] =  ','.join(similar)
            no += 1
    get_st(ulno)
    try:
        if dic['transform'] or dic['similar']:
            pass
    except Exception as err:
        pass#print(word,err)
        ulno +=1
        get_st(ulno)
    return dic

def get_eg(html_selector,word):
    dic = []
    ulno = 1#get double language
    goodpath='/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[7]/div[1]/div[1]/ul[{}]/li'.format(ulno)
    goodli=html_selector.xpath(goodpath)
    for li in goodli:
        peg = li.xpath('p[1]/span/text()')
        for i in range(len(peg)-1):
            if peg[i]==' ' and peg[i+1] == ' ':
                 peg[i] = '<b> '+word+'</b>'
        #peg = list(map(lambda i:(i if i!=' ' else '<b>'+word+'</b>'),peg))
        pcn = li.xpath('p[2]/span/text()')
        pega = ''.join(peg)
        pcna = ''.join(pcn)
        dic.append([pega,pcna])
    return dic

def get_word_info(word):
    global resultDict
    global completeDict
    global ebasic
    global emode

    wordDict = {}
    pagehtml=get_page(word)
    selector = etree.HTML(pagehtml.decode('utf-8'))
    expl = get_word_explanation(selector,word)
    pron = get_prono(selector,word)
    if expl != []:
        emodeli = {}
        wordDict['ex'] = expl
        wordDict['pron'] = pron
        webparse = get_parse(selector,word)
        eg2 = get_eg(selector,word)
        simTransform = get_similar_transform(selector,word)
        wordDict['st'] = simTransform
        ebasic[word] = wordDict

        wordDict['wp'] = webparse
        wordDict['eg2'] = eg2

        emodeli['wp'] = webparse
        emodeli['eg2'] = eg2

        emodel[word] = emodeli
        resultDict[word] = wordDict
        completeDict[word] = wordDict
    else:
        print('get explanation failed:  ',word)
        bing_get_word(word)
        print('biying spidering ',word)

def bing_get_page(myword):
    basurl='http://cn.bing.com/dict/search?q='
    searchurl=basurl+myword
    response =  urllib.request.urlopen(searchurl)  
    html = response.read()
    return html

#获得单词释义
def bing_get_chitiao(html_selector,word):
    chitiao=[]
    hanyi_xpath='/html/body/div[1]/div/div/div[1]/div[1]/ul/li'
    get_hanyi=html_selector.xpath(hanyi_xpath)
    for item in get_hanyi:
        it=item.xpath('span')
        print(it[0].text)
        chitiao.append('%s %s'%(it[0].text,it[1].xpath('span')[0].text))
    if len(chitiao)>0:
        return chitiao
    else:
        return None
def bing_get_similar(html_selector,word):
    similar=[]
    hanyi_xpath='/html/body/div[1]/div/div/div[1]/div[1]/div[3]/div[2]/div[3]/div[1]/div[2]/a'
    get_hanyi=html_selector.xpath(hanyi_xpath)
    for item in get_hanyi:
        it=item.xpath('span')
        similar.append(it[0].text)
    if len(similar)>0:
        return ','.join(similar)
    else:
        return ""


#获得例句
def bing_get_liju(html_selector,word):
    liju=[]
    get_liju_e=html_selector.xpath('//*[@class="val_ex"]')
    get_liju_cn=html_selector.xpath('//*[@class="bil_ex"]')
    get_len=len(get_liju_e)
    for i in range(get_len):
        liju.append([get_liju_e[i].text,get_liju_cn[i].text])
    if len(liju)>0:
        return liju
    else:
        return []
def bing_get_yingbiao(html_selector,word):
    yingbiao=[]
    yingbiao_xpath='/html/body/div[1]/div/div/div[1]/div[1]/div[1]/div[2]/div'
    get_yingbiao=html_selector.xpath(yingbiao_xpath)
    for item in get_yingbiao:
        it=item.xpath('div')
        if len(it)>0:
            yingbiao.append("%s"%(it[0].text))
            yingbiao.append("%s"%(it[2].text))
    if len(yingbiao)>0:
        return yingbiao
    else:
        pass#print('bing no pronounciation: ',word)
        return [0,0]
def getWordExplanation(word):
    global resultDict
    global completeDict
    global ebasic

    try:
        getUrl = 'https://api.shanbay.com/bdc/search/?word={}'.format(word)
        res = requests.get(getUrl)
        print(getUrl)
        json_data = json.loads(res.text)
        data = json_data['data']
        print('shan bei spiring',word)
        print(data)
        filterData = {}
        filterData['pam'] = data['pronunciations']
        filterData['ex'] = [data['cn_definition']]
        getSentenceUrl = 'https://api.shanbay.com/bdc/example/?vocabulary_id={}'.format(wordId)
        # print(getSentenceUrl) 
        res2 = requests.get(getSentenceUrl)
        json_data2 = json.loads(res2.text)
        data2 = json_data2['data'][:1]
        egs = []
        if len(data2) >0:
            for i in range(len(data2)):
                eg_cn = [data2[i]['annotation'],data2[i]['translation']]
                egs.append(eg_cn)
        filterData['eg2'] = egs
        resultDict[word] = filterData
        completeDict[word] = filterData
        ebasic[word] = filterData
    except Exception as err:
        print(word,err)
        failedbei.append(word)
    finally:
        print(word)

def bing_get_word(word):
    global resultDict
    global completeDict
    global ebasic
    wordDict = {}
    #获得页面
    pagehtml=bing_get_page(word)
    selector = etree.HTML(pagehtml.decode('utf-8'))
    #单词释义
    citiao=bing_get_chitiao(selector,word)
    #单词音标及读音
    yingbiao=bing_get_yingbiao(selector,word) 
    #例句
    liju=bing_get_liju(selector,word)
    #similar = get_similar(selector,word)
    #reverse = get_reverse(selector,word)
    wordDict['ex'] = citiao
    wordDict['pron'] = {'peg':yingbiao[1],'pam':yingbiao[0]}
    wordDict['eg2'] = liju
    if citiao != None:
        print('bing get citiao',word)
        resultDict[word] = wordDict
        completeDict[word] = wordDict
        ebasic[word] = wordDict
    else:
        failed.append(word)
        print('bing faild ',word)

def spiTxts(inputFile,outputFile):
    global resultDict
    global completeDict
    global emodel
    global ebasic
    lineno = 0
    with open(inputFile,'r')as fmd:
        for line in fmd:
            if lineno == 0:
                dic = json.loads(line)
                resultDict['paperStatistics'] = dic
                lineno += 1
                continue
            words = line.split(',')
            for word in words:
                    if len(word) <= 2:
                        continue

                    if not word or word == '\n':
                        continue
                    if word in exclude:
                        continue
                    if word in completeDict:
                        resultDict[word] = completeDict[word]
                        print(word,' in dictionary!')
                        continue
                    try:
                        if word.endswith('s') or word.endswith('ed'):
                             get_word_info(word)
                             time.sleep(2)
                             if word not in completeDict:
                                 word = word[0:-1]
                                 if d.check(word):
                                     get_word_info(word)
                        elif word.endswith('ly'):
                             get_word_info(word)
                             time.sleep(2)
                             if word not in completeDict:
                                 word = word[0:-21]
                                 if d.check(word):
                                     get_word_info(word)

                        else:
                             get_word_info(word)
                        print('youdao spidering ',word)
                        time.sleep(random.random()+1.1)
                        if times%20 == 0:
                            time.sleep(5)
                    except Exception as err:
                            print(word,err)
    print(failedbi)
    for wo in failed:
        getWordExplanation(wo)
    print('oooooooooooooooover',inputFile)
    with open(outputFile,'w') as fx:
        json.dump(resultDict,fx)

    with open('economist.json','w')as fi:
        json.dump(completeDict,fi)

    with open('economist_model.json','w')as fj:
        json.dump(emodel,fj)

    with open('economist_basic.json','w')as fk:
        json.dump(ebasic,fk)
    ebasic = {}
    emodel = {}
    resultDict = {} 
    time.sleep(5)
    print(failedbei)

exclude = []
with open('simpleWords.json','r')as fo:
    exclude = json.load(fo)

if __name__ == '__main__':
    #spiTxt = 'aaa.txt'
    #outJson = 'bbb.json'
    #spiTxts(spiTxt,outJson)
    #sys.exit()
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

        txtPath = basedir + dateDir +'/words/'
        jsonPath = basedir + dateDir +'/jsons/'

        readTxt = []

        if os.path.exists(txtPath):
            for item in os.listdir(txtPath):
                readTxt.append([txtPath+item,item])

        if len(readTxt) <= 0:
            print('NO PAPER TO FILTER!')
            sys.exit()

        if not os.path.exists(jsonPath):
            os.makedirs(jsonPath)

        for txt in readTxt:
            spiTxt = txt[0]
            outJson = jsonPath + txt[1][0:-3]+'json'
            print('spiiiiiiiiiiiing',txt[1])
            spiTxts(spiTxt,outJson)
