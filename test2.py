'''
Author: RiderLai lyf670354671@gmail.com
Date: 2024-07-25 16:25:30
LastEditors: RiderLai lyf670354671@gmail.com
LastEditTime: 2024-07-25 16:38:17
FilePath: /TestDEV/postman2ms/test2.py
Description: 

Copyright (c) 2024 by RiderLai, All Rights Reserved. 
'''
import json

from main import scenarioDefinition2str


def main():
    
    with open('./template/groovy/init.groovy', 'r') as f:
        initStr = f.read()

    # print(initStr)

    with open('./template/initScript.json', 'r') as f:
        data = json.load(f)
    
    data['script'] = initStr

    # print(data)

    with open('./template/scenarioDefinition.json', 'r') as f:
        sd = json.load(f)
    
    sd['hashTree'] = [data]


    with open('./template/OutTemplate.json', 'r') as f:
        out = json.load(f)
    
    out['data'][0]['scenarioDefinition'] = scenarioDefinition2str(sd)


    with open('./test2.json', 'w+') as f:
        json.dump(out, f, indent=4)




if __name__ == '__main__':
    main()
