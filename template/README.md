<!--
 * @Author: RiderLai lyf670354671@gmail.com
 * @Date: 2024-07-24 15:51:46
 * @LastEditors: RiderLai lyf670354671@gmail.com
 * @LastEditTime: 2024-07-24 16:21:28
 * @FilePath: /TestDEV/postman2ms/template/README.md
 * @Description: 
 * 
 * Copyright (c) 2024 by RiderLai, All Rights Reserved. 
-->
# template

**desc:** 预设MeterSphere的json结构，用于后续postman数据转换成MeterSphere可导入的文件。

### MeterSphere json文件互相依赖关系

```
OutTemplate.json
-> scenarioDefinition.json
    -> httpSample.json
        -> httpHeader.json
```

#### 1. OutTemplate.json

通过程序覆盖的字段：
```
"name": "场景名2",
"scenarioDefinition": "",
```
**name:** 代表场景名
**scenarioDefinition:** 场景中调用的模块的定义，将json转换成字符串存储。具体内容则是scenarioDefinition.json。


#### 2. scenarioDefinition.json

该json包含了，场景的中的数据，例如http请求，执行脚本等。

主要字段：
```
    "hashTree": [],
```
**hashTree：** 这个字段是一个list，将存储http请求，执行脚本等实际的操作。

#### 3. httpSample.json

该json则是http请求的单一用例。
postman转换过来，主要对接的部分就是这一块。

使用字段，和postman文件的对应关系，后续程序中展示。

#### 4. httpHeader.json

该json是3中的httpHeader的一个定义。
==！！！对应在3中的header字段中==，试例如下:
```
    "headers": [
        {
            "valid": true,
            "file": false,
            "enable": true,
            "name": "Accept",
            "value": "application/json",
            "urlEncode": false,
            "required": false
        },
        {
            "valid": true,
            "file": false,
            "enable": true,
            "name": "authorization",
            "value": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbklkIjozMTgxNiwicm4iOiJBTnAySU14TjFBTHpvcnU4RTYwOTBwN0dHbFdPMkFYYiIsInVzZXJJZCI6MzE4MTYsInVzZXJuYW1lIjoiTVNyb290IiwicGxheWVySWQiOjAsInBsYXllck9yaWdpbiI6IlBMQVRGT1JNX1VTRVIiLCJyZWxhdGlvblR5cGUiOiJCQVNFIiwicmVsYXRpb25JZCI6MH0.5WMGQmGpH1Z6ywSArQt13kuxvC6Vff6m_IWmiBCyVCU",
            "urlEncode": false,
            "required": false
        }
    ],
```

