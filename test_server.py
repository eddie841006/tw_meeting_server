#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 11:03:12 2020

@author: c95csy
"""

import requests
import json

 
url = "http://172.16.120.124:1111/"
# name = "subtitles_with_ASR_speaker2"
# data = {"video_name": name}
# resp = requests.post(url + "video_json", json=data)
# resp_data = json.loads(resp.text)
# print(resp_data)

resp = requests.post(url + "reload", json={"reload": True})
resp_data = json.loads(resp.text)
print(resp_data)