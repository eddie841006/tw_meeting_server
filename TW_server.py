#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 09:41:57 2020

@author: c95csy
"""
import os
import numpy as np
from flask import Flask, request, jsonify, render_template
import json
import glob
from flask_cors import cross_origin
from flask_cors import CORS
import librosa


app = Flask(__name__)
CORS(app)
app.config['debug'] = True

'''
    POST data format:
    {
        'text': 'Your text'
    }
'''


@app.route("/")
def index():
    """html server

    Returns:
        html: [description]
    """
    return render_template(web_index_path)

@app.route('/video_json', methods=['GET', 'POST'])
def video_json():
    post_data = request.json
    try:
        name = post_data['video_name']
        if name in json_info.keys():
            return jsonify(json_info[name])
    
        else:
            return {"error", name + "don't have subline"}
        
    except:
        return {"error", """must post {'video_name': name}"""}
    
def read_json_to_dict(path):
    """read video json file 

    Arguments:
        path {str} -- json path

    Returns:
        list -- 
    """ 
    json_paths = os.listdir(path)

    json_info = {}
    for json_path in json_paths:
        with open(path+json_path, "r") as f:
            data = json.load(f)
        
        json_info[json_path[:-5]] = data
    
    return json_info

def read_video_info(path, name=None):
    video_list = glob.glob(path)
    video_list.sort()

    if not name:
        name = {}
        for i, v in enumerate(video_list):
            v_name = v.split("/")[-1]
            name[v_name] = "立院影片測試" + str(i+1)
    
    video_info = []
    for v in video_list:
        video_time = librosa.get_duration(filename=v)
        m, s = divmod(video_time, 60)
        v_name = v.split("/")[-1]
        vn = {
            "video_name": v_name,
            "video_time": str(int(m)) + ":" + str(int(s)),
            "name": name[v_name]
        }

        video_info.append(vn)

    return video_info

@app.route('/video_list', methods=['GET', 'POST'])
def video_list():
    
    print(video_info)

    return jsonify(video_info)



if __name__ == "__main__":
    web_index_path = "index.html"
    json_path = "video_json/"
    video_path = "./static/video/*.mp4"
    with open("video_info.json", "r") as f:
        name = json.load(f)
    json_info = read_json_to_dict(json_path)
    video_info = read_video_info(video_path, name)
    app.run('172.16.120.124', '1111', threaded = False)
    # app.run('127.0.0.1', '1111', threaded = False)
    
