'''
Author: RiderLai lyf670354671@gmail.com
Date: 2024-07-24 10:09:15
LastEditors: RiderLai lyf670354671@gmail.com
LastEditTime: 2024-08-05 15:31:34
FilePath: /TestDEV/postman2ms/main.py
Description: 

Copyright (c) 2024 by RiderLai, All Rights Reserved. 
'''
import os
import json
import copy
import argparse

from urllib.parse import urlparse


current_path = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_path, 'template')
groovy_path = os.path.join(template_path, 'groovy')

groovyScriptBlock_path = os.path.join(template_path, 'groovyScriptBlock.json')
initGroovy_path = os.path.join(groovy_path, 'init.groovy')
returnGroovy_path = os.path.join(groovy_path, 'return.groovy')

httpSample_path = os.path.join(template_path, 'httpSample.json')
httpHeader_path = os.path.join(template_path, 'httpHeader.json')
getHttpBody_path = os.path.join(template_path, 'getHttpBody.json')
getQuery_path = os.path.join(template_path, 'getQuery.json')
postHttpBody_path = os.path.join(template_path, 'postHttpBody.json')

scenarioDefinition_path = os.path.join(template_path, 'scenarioDefinition.json')
OutTemplate_path = os.path.join(template_path, 'OutTemplate.json')


blackList = [
    'Host',
    'host',
    'Origin',
    'Cookie',
    'Referer',
    'Connection',
    'User-Agent',
    'authorization',
]


def scenarioDefinition2str(data:dict) -> str:
    '''
    场景定义的json，转换成字符串
    json数据转换成字符串
    '''
    result = json.dumps(data)
    return result


def initSrcipt(token:str = "") -> dict:
    with open(groovyScriptBlock_path, 'r') as f:
        data = json.load(f)

    data['name'] = 'Init 依赖变量设置 & 场景变量设置'

    with open(initGroovy_path, 'r') as f:
        groovyStr = f.read()
    
    bearer = f'\nvars.put("bearer", "{token}")'
    groovyStr = groovyStr + bearer

    data['script'] = groovyStr

    return data


def returnScript() -> dict:
    with open(groovyScriptBlock_path, 'r') as f:
        data = json.load(f)

    data['name'] = 'Export None'

    with open(returnGroovy_path, 'r') as f:
        groovyStr = f.read()

    data['script'] = groovyStr

    return data


def request2httpSample(req:dict) -> tuple:
    '''
    postman的request转换成MeterSphere的http请求
    '''
    with open(httpSample_path, 'r') as f:
        httpSample = json.load(f)
    
    # other 
    httpSample['name'] = req['name']
    httpSample['method'] = req['request']['method']

    # header
    with open(httpHeader_path, 'r') as f:
        headerTemplate = json.load(f)
    
    headers = []
    token = ''
    for item in req['request']['header']:
        if item['key'] in blackList:
            if item['key'] == 'authorization':
                token = item['value']
            continue
        temp = copy.deepcopy(headerTemplate)
        temp['name'] = item['key']
        temp['value'] = item['value']
        headers.append(temp)

    httpSample['headers'] = headers

    # url
    url = req['request']['url']['raw']
    prased_url = urlparse(url)

    httpSample['path'] = prased_url.path
    httpSample['protocol'] = prased_url.scheme.upper()
    httpSample['url'] = prased_url.path
    httpSample['domain'] = f"{prased_url.scheme}://{prased_url.hostname}"

    # body
    if req['request']['method'] == 'GET':
        with open(getHttpBody_path, 'r') as f:
            getBody = json.load(f)
        httpSample['body'] = getBody
        
        queryPostman = req['request']['url'].get('query')
        if queryPostman is not None:
            with open(getQuery_path, 'r') as f:
                queryTemplate = json.load(f)
            queries = []
            for item in queryPostman:
                temp = copy.deepcopy(queryTemplate)
                temp['name'] = item['key']
                temp['value'] = item['value']
                queries.append(temp)
            httpSample['arguments'] = queries

    
    elif req['request']['method'] == 'POST':
        with open(postHttpBody_path, 'r') as f:
            postBody = json.load(f)
        postBody['raw'] = req['request']['body']['raw']
        httpSample['body'] = postBody
   

    return httpSample, token


def postman2MS(data:dict, name:str) -> dict:
    '''
    '''
    httpSamples = []

    items = data['item']
    token = ''
    for item in items:
        temp, _token = request2httpSample(item)
        httpSamples.append(temp)
        if _token != '':
            token = _token

    with open(scenarioDefinition_path, 'r') as f:
        scenario = json.load(f)
    
    scenario['hashTree'] = httpSamples

    initSrciptBlock = initSrcipt(token)
    returnScriptBlock = returnScript()
    scenario['hashTree'].insert(0, initSrciptBlock)
    scenario['hashTree'].append(returnScriptBlock)

    with open(OutTemplate_path, 'r') as f:
        out = json.load(f)
    
    out['data'][0]['scenarioDefinition'] = scenarioDefinition2str(scenario)
    out['data'][0]['name'] = name

    return out


def main():
    parser = argparse.ArgumentParser(description='APIRecoder')
    parser.add_argument('-f', '--file', type=str, required=True, help='postman导出的文件地址')
    parser.add_argument('-o', '--outfile', type=str, default='out.json', help='输出文件的地址')
    parser.add_argument('-n', '--name', type=str, required=True, help='场景名')
    args = parser.parse_args()
    
    with open(args.file, 'r') as f:
       data = json.load(f)

    outMS = postman2MS(copy.deepcopy(data), args.name)

    with open(args.outfile, 'w+') as f:
        json.dump(outMS, f, indent=4)


if __name__ == '__main__':
    main()
