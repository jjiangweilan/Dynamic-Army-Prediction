"""
Extracts data from replay files and creates a JSON in this format:
Dictionary: { “Player 1” : ..., “Player 2” : ... } <string> : <list>
Where <list> is a list of all units seen by each player
"""

import os
import json
import argparse
import collections
from pkg_resources import resource_filename

def __nameUnits(collectUnits, idUnit):
    saveNames = collections.OrderedDict()
    for idUnit2, iterate1 in collectUnits.items():
        label = idUnit[int(idUnit2)]
        saveNames[label] = iterate1
    return saveNames

def __unitAdd(times, types):
    addUnits = collections.OrderedDict()
    for temp1 in times:
        for temp2 in state['Armies'][types]:
            if not temp2 in addUnits.keys():
                addUnits[temp2] = temp1['Step']
    return addUnits

def updateBuildInfo(times, idUnit):
    player1 = __unitAdd(times, 'Player1')
    player2 = __unitAdd(times, 'Player2')
    namePlayer1 = __nameUnits(player1, idUnit)
    namePlayer2 = __nameUnits(player2, idUnit)
    return { "Player1 " : list(namePlayer1.keys()), "Player2" : list(namePlayer2.keys()) }

def __createJSON():
    with open(resource_filename(__name__, '../Desktop/replay.json')) as data:
        units = json.load(data)
        unit_ids = { int(unit_id) : name for unit_id, name in units.items()}
    return unit_ids

def buildInfo(stateDir='./states', buildInfoDir='./build_orders'):
    os.makedirs(buildInfoDir)
    files = []
    unitNameJson = __createJSON()

    for file in os.listdir(states_dir):
        if file.endswith(".json"):
            files.append(os.path.join(stateDir, file))

    for file in files:
        replayData = json.load(open(file))
        buildData = updateBuildInfo(replayData['States'], unitNameJson)
        playerData = replayData
        del playerData['States']
        playerData['ArmyBuildOrder'] = buildData

        fileName = os.path.basename(file)
        playerFileName = os.path.join(buildInfoDir, "Player1" + file)

        with open(playerFileName, 'w') as json_file:
            json.dump(playerData, json_file)

def getData():
    parser = argparse.ArgumentParser()
    parser.add_argument('--states_dir', dest='s_dir', action='store', default='./states', required=False)
    parser.add_argument('--buildInfoDir', dest='bo_dir', action='store',
                        default='./build_orders',required=False)

    return parser.getData()

def main():
    ordersData = getData()
    buildInfo(ordersData.s_dir, ordersData.bo_dir)

if __name__ == '__main__':
    main()