'''
Author: RiderLai lyf670354671@gmail.com
Date: 2024-07-24 18:52:42
LastEditors: RiderLai lyf670354671@gmail.com
LastEditTime: 2024-07-24 19:11:23
FilePath: /TestDEV/postman2ms/test.py
Description: 

Copyright (c) 2024 by RiderLai, All Rights Reserved. 
'''
import json

def dict2str(data:dict) -> str:
    result = json.dumps(data)
    # result = repr(result)
    # result = result.replace("\"", "\\\"")
    return result



if __name__ == '__main__':
    a = {
        "padding": 1,
        "aaa": "123"
    }

    aa = dict2str(a)

    with open('aa.json', 'w+') as f:
        f.write(aa)

    b = {
        'ccc': aa
    }

    bb = dict2str(b)

    with open('test.json', 'w+') as f:
        f.write(bb)