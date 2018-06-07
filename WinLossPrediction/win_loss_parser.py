import json

count = 1
zerg1 = zerg2 = protoss1 = protoss2 = 0
zergHealth1 = zergHealth2 = protossHealth1 = protossHealth2 = 0
zerg1Win = zerg2Win = protoss1Win = protoss2Win = 0
f = open('parsed.txt','w')

with open('predictionData.txt') as json_file:  
    data = json.load(json_file)
    for j in data:
        for i in data[str(count)]:
            if(i == 'zerg 1'):
                for j in data[str(count)]['zerg 1']:
                    if (j == 'ZERG_ROACH' or j == 'ZERG_LARVA'):
                        zerg1 = zerg1 + len(data[str(count)]['zerg 1'][j])
                        for elem in data[str(count)]['zerg 1'][j]:
                            zergHealth1 = zergHealth1 + elem
                    if j == 'W':
                        for elem in data[str(count)]['zerg 1'][j]:
                            zerg1Win = elem
            if(i == 'zerg 2'):
                for j in data[str(count)]['zerg 2']:
                    if (j == 'ZERG_ROACH' or j == 'ZERG_LARVA'):
                        zerg2 = zerg2 + len(data[str(count)]['zerg 2'][j])
                        for elem in data[str(count)]['zerg 2'][j]:
                            zergHealth2 = zergHealth2 + elem
                    if j == 'W':
                        for elem in data[str(count)]['zerg 2'][j]:
                            zerg2Win = elem
            if(i == 'protoss 1'):
                for j in data[str(count)]['protoss 1']:
                    if (j == 'PROTOSS_PYLON' or j == 'PROTOSS_PROBE'):
                        protoss1 = protoss1 + len(data[str(count)]['protoss 1'][j])
                        for elem in data[str(count)]['protoss 1'][j]:
                            protossHealth1 = protossHealth1 + elem
                    if j == 'W':
                        for elem in data[str(count)]['protoss 1'][j]:
                            protoss1Win = elem
            if(i == 'protoss 2'):
                for j in data[str(count)]['protoss 2']:
                    if (j == 'PROTOSS_PYLON' or j == 'PROTOSS_PROBE'):
                        protoss2 = protoss2 + len(data[str(count)]['protoss 2'][j])
                        for elem in data[str(count)]['protoss 2'][j]:
                            protossHealth2 = protossHealth2 + elem
                    if j == 'W':
                        for elem in data[str(count)]['protoss 2'][j]:
                            protoss2Win = elem
        for i in data[str(count)]:
            if(i == 'zerg 1'):
                f.write('{TEAM:[Zerg,Zerg],WIN:['+str(zerg1Win)+','+str(zerg2Win)+'],UNITS:['+str(zerg1)+','+str(zerg2)+'],HEALTH:['+str(zergHealth1)+','+str(zergHealth2)+']}')
            if(i == 'protoss 1'):
                f.write('{TEAM:[Protoss,Protoss],WIN:['+str(protoss1Win)+','+str(protoss2Win)+'],UNITS:['+str(protoss1)+','+str(protoss2)+'],HEALTH:['+str(protossHealth1)+','+str(protossHealth2)+']}')
            f.write('\n')
        zerg1 = zerg2 = protoss1 = protoss2 = 0
        zergHealth1 = zergHealth2 = protossHealth1 = protossHealth2 = 0
        zerg1Win = zerg2Win = protoss1Win = protoss2Win = 0
        count = count + 1
f.close()                       