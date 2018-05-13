import json
import re
import enchant
d = enchant.Dict("en_US")

words = []
with open('asimple.txt','r')as fo:
    for line in fo:
        word = re.split('\W+',line)
        word = [i for i in word if len(i)>1 and i.isalpha() and d.check(i)]
        words.extend(word)

print(list(set(words)))
