#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 09:41:57 2020

@author: c95csy
"""
import os
import numpy as np
import time
from flask import Flask, request, jsonify
import json


app = Flask(__name__)
#app.config['debug'] = True

'''
    POST data format:
    {
        'text': 'Your text'
    }
'''

@app.route('/video_json', methods=['GET', 'POST'])
def video_json():
    post_data = request.json
    
    name = post_data['video_name']
    if name in vedio_info.keys():
        return jsonify(vedio_info[name])

    else:
        return {"error", name + "don't have subline"}
    
def read_json_to_dict(path):
    json_paths = os.listdir(path)

    vedio_info = {}
    for json_path in json_paths:

        with open(path+json_path, "r") as f:
            data = json.load(f)
        
        vedio_info[json_path[:-5]] = data
    
    return vedio_info



if __name__ == "__main__":

    path = "video_json/"
    vedio_info = read_json_to_dict(path)
    app.run('172.16.120.124', '1111', threaded = False)
    # app.run('127.0.0.1', '1111', threaded = False)
    
