import glob
from collections import Counter
import re
import os
#获取目录中所有txt结尾的文件名列表，因为本题条件单纯，所以也可以使用os.listdir()方法
words = []
def list_txt():
    return glob.glob("./articles/*.md")


def wc(filename):
    exclude_words = ['', 'limited', 'limit', 'fares', 'help', 'lyrics', 'being', 'both', 'month', 'own', 'restore', 'human', 'battle', 'still', 'find', 'hip-hop', 'seemed', 'neither', 'public-relations', 'ads', 'also', 'third-party', 'had', 'young', 'should', 'to', 'only', 'black', 'has', 'chairman', 'team', 'then', 'them', 'good', 'saying', 'risk', 'big', 'dao', 'year,', 'were', 'facebook', 'know', 'they', 'despite', 'not', 'one', 'dr', 'killed', 'and', 'like', 'did', 'always', 'rights', 'go', 'airlines', 'hiro', 'continue', 'payments', 'including', 'went', 'discussing', 'users',  'just', 'the', 'people', 'airlines,', 'sxsw', 'some', 'up', 'platforms', 'see', 'are', 'baymax', 'year', 'time', 'best', 'techniques', 'even', 'will', 'what', 'said', 'for', 'armor', 'avoid', 'passengers', 'its', 'may', 'ftc', 'investigation', 'cambridge', 'conduct', 'shared', 'firms', 'public', 'can', 'be', 'who', 'hero', 'ability', 'business', 'healthcare', 'rock', 'attention', 'platform,', 'boss', 'zuckerberg', 'incident', 'entry\xe2\x80\x9d', 'groups', 'genre', 'from', 'his', 'by', 'after', 'panel', 'on', 'training', 'last', 'tadashi', 'where', 'could', 'grammy-nominated', 'programming', 'reason', 'experience', 'united\xe2\x80\x99s', 'dao,', 'american', 'survey', 'airline', 'however,', 'history', 'changes', 'or', 'first', 'legislators', 'control', 'incident,', 'followed', 'america\xe2\x80\x99s', 'passenger', 'him', 'political', 'into', 'within', 'classrooms', 'venues', 'hearing', 'yokai', 'put', 'because', 'been', 'another', 'artists', 'scandal', 'shakur\xe2\x80\x99s', 'disaster', 'take', 'city', 'little', 'company\xe2\x80\x99s', 'additional', 'would', 'privacy', 'there', 'apps', 'two', 'firm\xe2\x80\x99s', 'their', 'regulation', 'much', 'music', 'change', 'way', '6', 'was', 'is', 'more', 'lowest', 'himself', 'flight', 'that', 'share', 'offered', 'about', 'but', 'tadashi\xe2\x80\x99s', 'hiro\xe2\x80\x99s', 'with', 'than', 'he', 'paying', 'culture', 'these', 'inside', 'this', 'hiro,', 'karate', 'while', 'criticised', 'mr', 'making', 'shakur', 'at', 'exhibit', 'firm', 'pictured)', 'flights', 'yachty', 'san', 'stated', 'process', 'of', 'chip', 'thus', 'it', 'an', 'as', 'murder', 'promised', 'have', 'in', 'need', 'march', 'price', 'fame', 'film', 'if', 'huge', 'users\xe2\x80\x99', 'lil', 'media', 'make', 'baymax\xe2\x80\x99s', 'any', 'how', 'politicians', 'other', 'details', 'which', 'digital', 'out', 'independent', 'pain', 'users', 'congress', 'theodore', 'baymax,', 'rappers', 'fransokyo', 'most', 'united', 'portal', 'airport', 'such', 'microbots', 'data', 'recent', 'a', 'especially', 'many', 'robot', 'switch', 'without', 'tech', 'mother', 'push', 'music,', 'the', 'bumping', 'order', 'once']
    datalist = []
    print(filename)
    with open(filename, 'r') as f:
        for line in f:
            content = re.sub("\"|,>|\.", "", line.lower())
            datalist.extend(content.strip().split(' '))

    wordlst = Counter(datalist)
    for word in exclude_words:
        wordlst[word]=0
    
    resultDict = dict(wordlst.most_common(15))
    result = list(resultDict.keys())
    words.extend(result)


if __name__ == "__main__":
    basePath = './articles'
    for fileName in os.listdir(basePath):
        fullPath = os.path.join(basePath,fileName)
        wc(fullPath)
    print(set(words))
