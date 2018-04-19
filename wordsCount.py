#coding=utf-8
from collections import Counter
import re
import os
#获取目录中所有txt结尾的文件名列表，因为本题条件单纯，所以也可以使用os.listdir()方法
import json

simpleWords = []

with open('simpleWords.txt','r')as fsimple:
    for line in fsimple:
        simpleWords.extend(line.split(','))

def wc(filename):
    resultDict = []
    with open(filename, 'r') as f:
        for line in f:
            resultDict.extend(list(set(line.split(','))))

        wordlst = Counter(resultDict)

        dicLen = len(wordlst)
        allWords = wordlst.most_common(dicLen)
        lst = [item[0] for item in allWords if item[0] not in simpleWords or item[0].isalpha()]
        lst = [i for i in lst if i]
        datas = ','.join(lst)

        with open('./mdEnd.txt','a+') as fo:
            fo.write(datas+'\n')

if __name__ == "__main__":
    #basePath = './articles/mdfiles/'
    #for fileName in os.listdir(basePath):
        #fullPath = os.path.join(basePath,fileName)
        wc('mdMergedWords.txt')#fullPath)
