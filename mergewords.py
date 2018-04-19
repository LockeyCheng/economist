lst4 = []
lst6 = []
def getLst(filePath,arr):
    with open(filePath,'r') as fo:
        for line in fo:
            arr.extend(line.split(','))
        return list(set(arr))

if __name__ == '__main__':
    lst4o = getLst('cet4_finally.txt',lst4)
    lst6o = getLst('cet6_finally.txt',lst6)
    print(type(lst4o),type(lst6o))
    resultLst = lst4o+lst6o
    print(type(resultLst))
    result = ','.join(resultLst)
    with open('mergedWords.txt','w') as fm:
        fm.write(result)
