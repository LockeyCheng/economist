#coding=utf-8
import glob
from collections import Counter
import re
import os
#获取目录中所有txt结尾的文件名列表，因为本题条件单纯，所以也可以使用os.listdir()方法
import json

simpleWords = []
def list_txt():
    return glob.glob("./articles/mdfiles/*.md")

with open('simpleWords.txt','r')as fsimple:
    for line in fsimple:
        simpleWords.extend(line.split(','))

def wc(filename):
    print(filename)
    resultDict = []
    with open(filename, 'r') as f:
        for line in f:
            content = re.sub("\"|,>|\./'", "", line.lower())
            stripData = content.strip().split(' ')
            resultDict.extend(list(set(stripData)))

        wordlst = Counter(resultDict)

        dicLen = len(wordlst)
        allWords = wordlst.most_common(dicLen)
        lst = [item[0] for item in allWords if item[0] not in simpleWords or item[0].isalpha()]
        lst = [i for i in lst if i]
        datas = ','.join(lst)

        with open('./mdMergedWords.txt','a+') as fo:
            fo.write(datas+'\n')

if __name__ == "__main__":
    basePath = './articles/mdfiles/'
    for fileName in os.listdir(basePath):
        fullPath = os.path.join(basePath,fileName)
        wc(fullPath)
