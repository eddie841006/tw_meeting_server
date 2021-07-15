# tw_meeting_server

## Table of Contents
   * [tw_meeting_server](#tw_meeting_server)
      * [Architecture](#architecture)
      * [UI Demo](#ui-demo)
      * [Recognition Accuracy](#recognition-accuracy)
      * [server APIs](#server-apis)
         * [html (/)](#html-)
         * [video_json](#video_json)
         * [video_list](#video_list)
      * [post sample code with python](#post-sample-code-with-python)

建立一個server，提供前端與後端功能，
此server主要是用在立法院語音辨識UI上使用。

此是offline方式進行展示，裡面的影片是事先透過語音辨識模型辨識完畢，並且將辨識結果、google語音辨識結果和正確答案存成json檔，待UI要顯示時再將事先辨識好的json檔傳給前端顯示。

## Architecture
- 前端html UI
- 後端server
    - video_json
    - video_list

## UI Demo
![](https://i.imgur.com/R73wXGE.jpg)

## Recognition Accuracy
- datasets
    | Dataset | Sentences | Time  | Speaker |
    |:-------:|:---------:|:-----:|:-------:|
    |  train  |   55944   | 50.4h |   82    |
    |  test   |   6949    | 6.2h  |   11    |

- result
    | Task      | Sentences | Time  | CER (%) |
    | --------- | --------- |:-----:|:-------:|
    | Mozilla   | 3785      | 3.96h |    6    |
    | 立院測試A | 1350      | 0.79h |   14    |
    | 立院測試B | 1814      | 1.45h |   15    |

## server APIs

url = "http://172.16.120.124:1111/"

### html (/)
將DS小組寫的UI建立在server當中，這樣在同網域下就能開啟UI
前端UI界面的html掛在/中，直接在網頁上輸入
"http://172.16.120.124:1111/"
就能進入UI界面
```python=
@app.route("/")
def index():
    """html server

    Returns:
        html: [description]
    """
    return render_template(web_index_path)
```
### video_json
url = "http://172.16.120.124:1111/video_json"
type : post

Input : {"video_name": name}
> name = 影片檔名
> 格式 = json

Output : type(str)
```
[
    {
        "ASR_wer": 95,
        "speaker_wer": 75
    },
    {
        "MASR_results": "首先肯定退不會",
        "asr_wer": 0.1,
        "end_time": 19.712,
        "google_asr_results": "首先肯定退輔會",
        "labels": "首先肯定退輔會",
        "speaker": "吳斯懷",
        "speaker_wer": 0.05,
        "start_time": 16.896
    },
    {
        "MASR_results": "針對剛才",
        "asr_wer": 0.1,
        "end_time": 21.248,
        "google_asr_results": "針對剛才",
        "labels": "針對剛才",
        "speaker": "吳斯懷",
        "speaker_wer": 0.05,
        "start_time": 20.224
    },
    ...
]
```
> 格式 = str
> 回傳為此影片的辨識結果

### video_list
url = "http://172.16.120.124:1111/video_list"
type : Get

Output : type(str)
```
[
    {
        "name": "立院影片0",
        "video_name": "subtitles_with_ASR_speaker4.mp4",
        "video_time": "2:14"
    },
    {
        "name": "立院影片1",
        "video_name": "outputVideo5.mp4",
        "video_time": "2:18"
    },
    ...
]
```
> 格式 = str
> 回傳video資料夾中的影片list、影片時長與UI上要顯示的名子


## post sample code with python
```python=
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 11:03:12 2020

@author: c95csy
"""

import requests
import json

 
url = "http://172.16.120.124:1111/"
name = "subtitles_with_ASR_speaker2"
data = {"video_name": name}
resp = requests.post(url + "video_json", json=data)
resp_data = json.loads(resp.text)
print(resp_data)
```
