import json

def getJson():
    with open('./result/explanation.json') as fo:
        data = json.load(fo)
        return data

if __name__ == '__main__':
    data = getJson()
    print(data['household'])
