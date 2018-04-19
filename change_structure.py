import json
dict4 = {}
dict6 = {}
result4 = {}
result6 = {}
with open('cet4_result.json','r') as fj4:
    dict4 = json.load(fj4)
    
for item in dict4:
    tmp4 = {}
    proo4 = {}
    proo4['peg'] = dict4[item]['pro_en']
    proo4['pam'] = dict4[item]['pro_am']
    tmp4['ex'] = (dict4[item]['detail']).split('||')
    tmp4['pro'] = proo4
    tmp4['eg2'] = dict4[item]['eg']
    result4[item] = tmp4
        
with open('cet4_new.json','w') as f4new:
    json.dump(result4,f4new)

with open('cet6_result.json','r') as fj6:
    dict6 = json.load(fj6)

for item6 in dict6:
    tmp6 = {}
    proo6 = {}
    proo6['peg'] = dict6[item6]['pro_en']
    proo6['pam'] = dict6[item6]['pro_am']
    tmp6['ex'] = (dict6[item6]['detail']).split('||')
    tmp6['pro'] = proo6
    tmp6['eg2'] = dict6[item6]['eg']
    result6[item6] = tmp6

with open('cet6_new.json','w') as f4new:
    json.dump(result6,f4new)

