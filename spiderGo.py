import json
import requests

agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain','User-Agent':agent}

resultDic = {}

def getWordExplaination(word):
    getUrl = 'https://api.shanbay.com/bdc/search/?word={}'.format(word)
    res = requests.get(getUrl)
    json_data = json.loads(res.text)
    data = json_data['data']
    resultDic[word] = data
    #with open('./result/explanation.json','a') as fo:
    #    fo.write(wordAll)

if __name__ == '__main__':
    with open('./result/wordsCollection.txt') as fotxt:
        for lineno, line in enumerate(fotxt, 1):
            fields = line.split(',')
            for word in fields:
                getWordExplaination(word)
    with open('./result/explanation.json','a') as fojson:
        json.dump(resultDic,fojson)
