import json
PATH = '/Users/jiehongjiang/Desktop/Projects/Dynamic-Army-Prediction/Data/data-JJ.json'

with open(PATH) as f:
    data = json.load(f)

tags = {'protoss': set(), 'zerg': set(), 'terran' : set()}
for game in data:
    race = game.keys()[0].split('_')[0].lower()
    tags[race].update(game.keys())

print(tags)