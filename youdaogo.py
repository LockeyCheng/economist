import urllib.request
from lxml import etree
import re
import time
from functools import reduce
import json
import random

replace_blank = re.compile('\n')

def get_page(myword):
    html = None
    try:
        lookurl='http://www.youdao.com/w/eng/{}/#keyfrom=dict2.index'.format(myword)
        response =  urllib.request.urlopen(lookurl)
        html = response.read()
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
        print(err,'get explanation error: ',word)

    return dic

def get_parse(html_selector,word):
    parses = {}
    hanyi_xpath='/html/body/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[5]'
    try:
        get_hanyi=html_selector.xpath(hanyi_xpath)
        for item in get_hanyi:
            pp = item.xpath('p/text()')
            no = 1
            for ptext in pp:
              if ';' in ptext:
                  faa = 'p[{}]/span/a/text()'.format(no)
                  aa=item.xpath(faa)
                  translation = ptext.strip()
                  translation = translation.replace("\n", "")
                  translation = translation.replace(' ','')
                  ajoin = '_'.join(aa)
                  parses[ajoin]=translation
                  no += 1
    except Exception as err:
        print(err,'get parses error: ',word)

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
            print(err,word,'get pronounce of English')
        try:
            pam = item.xpath('span[1]/text()')
            dic['pam'] = pam[0]
        except Exception as err:
            print(err,word,'get pronounce of American')

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
                   print(','.join(similar))
                   dic['similar'] =  ','.join(similar)
            no += 1
    get_st(ulno)
    try:
        if dic['transform'] or dic['similar']:
            pass
    except Exception as err:
        print(word,err)
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
        pcn = li.xpath('p[2]/span/text()')
        pega = ''.join(peg)
        pcna = ''.join(pcn)
        dic.append([pega,pcna])
    return dic

resultDict = {} 
failed = []
def get_word_info(word):
    wordDict = {}
    pagehtml=get_page(word)
    selector = etree.HTML(pagehtml.decode('utf-8'))
    expl = get_word_explanation(selector,word)
    pron = get_prono(selector,word)
    if expl != []:
        wordDict['ex'] = expl
        wordDict['pron'] = pron
        webparse = get_parse(selector,word)
        eg2 = get_eg(selector,word)
        simTransform = get_similar_transform(selector,word)
        wordDict['wp'] = webparse
        wordDict['st'] = simTransform
        wordDict['eg2'] = eg2
        resultDict[word] = wordDict
    else:
        failed.append(word)
        print('get explanation failed:  ',word)

if __name__ == '__main__':
    with open('economist_419.txt','r')as fmd:
        for line in fmd:
            words = line.split(',')
            for word in words:
                    if not word or word == '\n':
                        continue
                    try:
                        get_word_info(word)
                        print('spidering ',word)
                        time.sleep(random.random()+1)
                    except Exception as err:
                            print(word,err)
            time.sleep(10)
    print(failed)
    with open('economist_419.json','w') as fx:
        json.dump(resultDict,fx)
