#coding=utf-8
from collections import Counter
import re
import os
#获取目录中所有txt结尾的文件名列表，因为本题条件单纯，所以也可以使用os.listdir()方法
import json

exclude = ['read','small''height','width','picture', 'writer','improv','themselves','','decide','new', 'video', 'call', 'why', 'late', 'post', 'end', 'gay', 'off', 'week','manner', 'bid', 'piece', 'feed', 'led', 'age', 'high', 'type', 'job', 'long', 'ink', 'ten', 'clever', 'you', 'live', 'page',  'view', 'simply', 'wish', 'taste', 'mean', 'day', 'men', 'under', 'wide', 'mark', 'fan', 'later', 'star', 'car', 'code', 'value', 'offer', 'horn','all', 'chinese', 'focus', 'month', 'go', 'follow', 'technique', 'young', 'to', 'program', 'microbot', 'risk', 'facebook', 'fall', 'trouble', 'did', 'dig', 'list', 'try', 'subway', 'team', 'quick', 'past', 'even', 'will', 'what', 'conduct', 'shared', 'public', 'hero', 'wuhan', 'slow', 'china', 'groups', 'meet', 'sing', 'strong', 'change', 'shift', 'experience', 'airport', 'survey', 'changes', 'campaign', 'criticise', 'app', 'yokai', 'scandal', 'crisis', 'use', 'from', 'would', 'give', 'two', 'few', 'music', 'more', 'company', 'effort', 'this', 'baymax', 'can', 'mr', 'making', 'history', 'control', 'compare', 'stated', 'process', 'chip', 'share', 'tao', 'rescue', 'huge', 'united', 'american', 'how', 'hot', 'stand', 'fare', 'tried', 'may', 'after', 'tied', 'produce', 'such', 'data', 'grow', 'classroom', 'third', 'whenever', 'robot', 'switch', 'healthcare', 'order', 'help', 'over', 'trade', 'including', 'still', 'its', 'thank', 'better', 'platform', 'then', 'them', 'good', 'return', 'dao', 'they', 'not', 'now', 'term', 'always', 'rock', 'went', 'economy', 'woes', 'year', 'our', 'out', 'armor', 'since', 'ftc', 'investigation', 'sxsw', 'million', 'given', 'zuckerberg', 'reason', 'put', 'bleed', 'training', 'tadashi', 'where', 'could', 'keep', 'filter', 'turn', 'shakur', 'first', 'economy.', 'one', 'another', 'open', 'city', 'little', 'privacy', 'their', 'regulation', 'too', 'murder', 'that', 'than', 'steel', 'war', 'karate', 'matter', 'were', 'exhibit', 'bridge', 'yachty', 'san', 'say', 'buy', 'have', 'need', 'seem', 'any', 'lid', 'lil', 'also', 'take', 'which', 'pain', 'trace', 'price', 'who', 'reach', 'unused', 'most', 'america', 'especially', 'alarm', 'tech', 'clean', 'saying', 'show', 'find', 'decade', 'busy', 'less', 'should', 'only', 'black', 'factor', 'announce', 'local', 'his', 'get', 'capital', 'nearly', 'despite', 'report', 'him', 'artist', 'borrow', 'whether', 'river', 'discussing', 'culture', 'see', 'are', 'fail', 'close', 'best', 'project', 'said', 'neither', 'we', 'ability', 'extend', 'attention', 'weak', 'however', 'boss', 'incident', 'cities', 'come', 'both', 'last', 'outflows', 'many', 'and', 'supply', 'period', 'debt', 'political', 'three', 'been', 'quickly', 'much', 'firm', 'controlled', 'offered', 'paying', 'unsold', 'politician', 'these', 'aim', 'while', 'property', 'at', 'almost', 'is', 'thus', 'it', 'in', 'fame', 'if', 'develop', 'media', 'make', 'same', 'theodore', 'portal', 'user', 'recent', 'kepp', 'without', 'mother', 'yangtze', 'the', 'gdp', 'just', 'heavily', 'kill', 'human', 'ads', 'had', 'combine', 'has', 'march', 'government', 'big', 'digital', 'early', 'know', 'like', 'continue', 'payments', 'because', 'crowd', 'people', 'some', 'growth', 'export', 'home', 'for', 'avoid', 'leader', 'be', 'business', 'by', 'earlier', 'panel', 'on', 'about', 'of', 'airline', 'or', 'own', 'into', 'within', 'right', 'additional', 'area', 'there', 'start', 'way', 'was', 'strict', 'lowest', 'himself', 'but', 'construction', 'hear', 'line', 'with', 'he', 'made', 'hiro', 'inside', 'up', 'limit', 'problem', 'passenger', 'qin', 'an', 'as', 'promised', 'flight', 'film', 'detail', 'other', 'income', 'test', 'poor', 'ago', 'rule', 'time', 'push', 'once']


resultDict=[]
outFile=[]
def getOrigianlForm(word):
    if word in exclude:
        return False
    if len(word) <=3:
        if word in exclude:
            return False
        return True
    if word.endswith('ing'):
        word = word[0:-3]
        if word not in exclude:
            word += 'e'
            if word not in exclude:
               word = word[0:-2]
               if word not in exclude:
                    return True
        return False
    if word.endswith('ies'):
        word = word[0:-3]
        if word not in exclude:
            word += 'y'
            if word not in exclude:
                return True
        return False
    if word.endswith('es'):
        word = word[0:-2]
        if word not in exclude:
            word += 'e'
            if word not in exclude:
                return True
        return False

    if word.endswith('s'):
        word = word[0:-1]
        if word not in exclude:
            return True
        return False

    if word.endswith('ers'):
        word = word[0:-2]
        if word not in exclude:
            word += 'e'
            if word not in exclude:
                return True
        return False

    if word.endswith('est'):
        word = word[0:-3]
        if word not in exclude:
            word = word[0:-1]
            if word not in exclude:
                return True
        return False

    if word.endswith('ied'):
        word = word[0:-3]
        if word not in exclude:
            word += 'y'
            if word not in exclude:
                return True
        return False

    if word.endswith('ed'):
        word = word[0:-2]
        if word not in exclude:
            word += 'e'
            if word not in exclude:
                return True
        return False

    if word.endswith('ly'):
        word = word[0:-2]
        if word not in exclude:
            word += 'e'
            if word not in exclude:
                return True
        return False

common100 = []
def wc(filename):
    with open(filename, 'r') as fwc:
        for line in fwc:
            content = re.sub("\"|,>|\.", "",line.lower())
            lst = content.split(' ')
            lst1 = [i.lower() for i in lst if len(i)>2 and getOrigianlForm(i)]
            common100.extend(lst1)
            lst2 = ' '.join(lst1)
            lst3 = lst2.split("'")
            lstx = ' '.join(lst3)
            lsty = lstx.split(',')
            lstz = ' '.join(lsty)
            lst3 = lstz.split(' ')
            resultDict.extend(lst3)
            

    wordlst = Counter(resultDict)
    dicLen = len(wordlst)

    m100 = Counter(common100)
    mb = m100.most_common(100)
    mbai = [item[0] for item in mb]
    print('--------------------------------------------------------------mbai')
    print(','.join(mbai))

    allWords = wordlst.most_common(dicLen)
    allwords = [item[0] for item in allWords if item[0].isalpha()]
    resultWords = []
    for word in allwords:
        tmp = word
        if len(word)<=5:
            continue
        if word.endswith('ing'):
            tmp = word[0:-3]
        if word.endswith('ies'):
            tmp = word[0:-3]+'y'
        if word.endswith('es'):
            tmp = word[0:-1]
        if word.endswith('ers'):
            tmp = word[0:-1]
        if word.endswith('est'):
            tmp = word[0:-3]
        if word.endswith('ied'):
            tmp = word[0:-3]+'y'
        if word.endswith('ed'):
            tmp = word[0:-1]
        if word.endswith('ly'):
            tmp = word[0:-2]
        resultWords.append(tmp)
    datas = ','.join(resultWords)
    print('--------------------------------------------------------------all str')
    print(datas)
    with open('todaymd.txt','w') as fo:
        fo.write(datas)

if __name__ == "__main__":
    wc('todaymd.md')
