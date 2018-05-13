import json
import re

fjson = 'Female_candidates_are_facing_a_backlash_in_Iraq.json'
fmd = 'Female_candidates_are_facing_a_backlash_in_Iraq.md'

keys =[]
with open(fjson,'r')as fj:
   dic = json.load(fj)
   keys = list(dic.keys())

print(keys)

with open(fmd,'r')as fm:
   for line in fm:
        newLine = line
        for key in keys:
            span = ' <span class="fa fa-info">' + key + '</span> '
            if re.search(key, newLine):
                newLine = re.sub(key, span, newLine, flags=re.IGNORECASE)
                continue
            word = False
            if key.endswith('ing'):
                word = key[0:-3]

            if key.endswith('ers'):
                word = key[0:-1]

            if key.endswith('ies') or key.endswith('ied') or key.endswith('ily'):
                word = key[0:-3]+'y'

            if key.endswith('ded') or key.endswith('ted'):
                word = key[0:-2]

            if key.endswith('ment') or key.endswith('ness'):
                word = key[0:-4]


            if word:    
                span = '<span class="fa fa-info">' + word + '</span>'
                if re.search(word, newLine):
                    newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                    continue

            if key.endswith('ly'):
                word = key[0:-2]
                span = '<span class="fa fa-info">' + word + '</span>'
                if re.search(word, newLine):
                    newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                    continue

            if key.endswith('ed') or key.endswith('es') or key.endswith('ts'):
                word = key[0:-1]
                span = '<span class="fa fa-info">' + word + '</span>'
                if re.search(word, newLine):
                    newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                    continue

            if key.endswith('s'):
                word = key[0:-1]
                span = '<span class="fa fa-info">' + word + '</span>'
                if re.search(word, newLine):
                    newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                    continue

            if key.endswith('tion'):
                word = key[0:-4]
                if re.search(word, newLine):
                    span = '<span class="fa fa-info">' + word + '</span>'
                    newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                    continue
                word += 't' 
                if re.search(word, newLine):
                    span = '<span class="fa fa-info">' + word + '</span>'
                    newLine = re.sub(word, span, newLine, flags=re.IGNORECASE)
                    continue
                
 
        print(newLine)
