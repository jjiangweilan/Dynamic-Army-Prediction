import json
PATH = '/Users/jiehongjiang/Desktop/Projects/Dynamic-Army-Prediction/Data/data-JJ.json'

with open(PATH) as f:
    data = json.load(f)

d = [x for x in data if len(x) != 0]
print(d)
with open('/Users/jiehongjiang/Desktop/Projects/Dynamic-Army-Prediction/Data/data.json', 'w') as f:
    f.write(json.dumps(d))