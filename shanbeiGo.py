import json
import requests

agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain','User-Agent':agent}

resultDic = {}
def getWordExplaination(word):
    try:
        getUrl = 'https://api.shanbay.com/bdc/search/?word={}'.format(word)
        print(getUrl)
        res = requests.get(getUrl)
        json_data = json.loads(res.text)
        data = json_data['data']
        filterData = {}
        filterData['pronunciations'] = data['pronunciations']
        filterData['cn_definition'] = data['cn_definition']
        filterData['en_definition'] = data['en_definition']
        wordId = data['id']
        getSentenceUrl = 'https://api.shanbay.com/bdc/example/?vocabulary_id={}'.format(wordId)
        # print(getSentenceUrl) 
        res2 = requests.get(getSentenceUrl)
        json_data2 = json.loads(res2.text)
        data2 = json_data2['data'][:1]
        egs = []
        if len(data2) >0:
            eg_cn = [data2[0]['annotation'],data2[0]['translation']]
            egs.append(eg_cn)
        filterData['eg'] = egs 
        resultDic[word] = filterData
    except Exception as err:
        print(word,err)
    finally:
        print(word)    

if __name__ == '__main__':
    with open('./result/good.txt') as fotxt:
        for line in fotxt:
            fields = line.split(',')
            for word in fields:
                getWordExplaination(word)
    with open('./result/explanation_xxx.json','a') as fojson:
        json.dump(resultDic,fojson)
