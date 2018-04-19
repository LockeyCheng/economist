import urllib.request
from lxml import etree
import re 
import time
from functools import reduce
import json
import random

dictionary = {}
#获得页面数据
def get_page(myword):
    basurl='http://cn.bing.com/dict/search?q='
    searchurl=basurl+myword
    response =  urllib.request.urlopen(searchurl)  
    html = response.read()
    return html

#获得单词释义
def get_chitiao(html_selector,word):
    chitiao=[]
    hanyi_xpath='/html/body/div[1]/div/div/div[1]/div[1]/ul/li'
    get_hanyi=html_selector.xpath(hanyi_xpath)
    for item in get_hanyi:
        it=item.xpath('span')
        chitiao.append('%s %s'%(it[0].text,it[1].xpath('span')[0].text))
    if len(chitiao)>0:
        return reduce(lambda x, y:"%s||%s"%(x,y),chitiao)
    else:
        print('no explanation: ',word)
        return ""
def get_similar(html_selector,word):
    similar=[]
    hanyi_xpath='/html/body/div[1]/div/div/div[1]/div[1]/div[3]/div[2]/div[3]/div[1]/div[2]/a'
    get_hanyi=html_selector.xpath(hanyi_xpath)
    for item in get_hanyi:
        it=item.xpath('span')
        similar.append(it[0].text)
    if len(similar)>0:
        return ','.join(similar)
    else:
        print('no similar: ',word)
        return ""

def get_reverse(html_selector,word):
    reverse=[]
    hanyi_xpath='/html/body/div[1]/div/div/div[1]/div[1]/div[3]/div[2]/div[2]/div[1]/div[2]/a'
    get_hanyi=html_selector.xpath(hanyi_xpath)
    for item in get_hanyi:
        it=item.xpath('span')
        reverse.append(it[0].text)
    if len(reverse)>0:
        return ','.join(reverse)
    else:
        print('no similar: ',word)
        return ""

#获得单词音标和读音连接
def get_yingbiao(html_selector,word):
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
        print('no pronounciation: ',word)
        return [0,0]

#获得例句
def get_liju(html_selector,word):
    liju=[]
    get_liju_e=html_selector.xpath('//*[@class="val_ex"]')
    get_liju_cn=html_selector.xpath('//*[@class="bil_ex"]')
    get_len=len(get_liju_e)
    for i in range(get_len):
        liju.append([get_liju_e[i].text,get_liju_cn[i].text])
    if len(liju)>0:
        return liju
    else:
        print('no example: ',word)
        return []

def get_word(word):
    curWord = {}
    #获得页面
    pagehtml=get_page(word)
    selector = etree.HTML(pagehtml.decode('utf-8'))
    #单词释义
    citiao=get_chitiao(selector,word)
    #单词音标及读音
    yingbiao=get_yingbiao(selector,word) 
    #例句
    liju=get_liju(selector,word)
    #similar = get_similar(selector,word)
    #reverse = get_reverse(selector,word)

    curWord['pro_en'] = yingbiao[1]
    curWord['pro_am'] = yingbiao[0]
    curWord['detail'] = citiao
    curWord['eg'] = liju
    if citiao:
        curWord['pro_en'] = yingbiao[1]
        curWord['pro_am'] = yingbiao[0]
        curWord['detail'] = citiao
        curWord['eg'] = liju

        dictionary[word] = curWord
#dict = {}
#with open('result416.json','r') as fj:
#    dict = json.load(fj)
if __name__ == '__main__':
    with open('cet6_finally.txt','r') as fr:
        for line in fr:
            words = line.split(',')
            for word in words:
                    if not word or word == '\n':
                        continue
                    try:
                        get_word(word)
                        print('spidering ',word)
                        time.sleep(random.random()+0.5)
                    except Exception as err:
                            print(word,err)
            time.sleep(10)
    with open('cet6_result.json','a+') as fx:
        json.dump(dictionary,fx)
