#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 09:41:57 2020

@author: c95csy
"""
import os
import numpy as np
import time
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
#@cross_origin()
def index():
    """html server

    Returns:
        html: [description]
    """
    return render_template(web_index_path)

@app.route('/video_json', methods=['GET', 'POST'])
#@cross_origin()
def video_json():
    post_data = request.json
    try:
        name = post_data['video_name']
        if name in vedio_info.keys():
            return jsonify(vedio_info[name])
    
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

    vedio_info = {}
    for json_path in json_paths:

        with open(path+json_path, "r") as f:
            data = json.load(f)
        
        vedio_info[json_path[:-5]] = data
    
    return vedio_info

    
    
@app.route('/video_list', methods=['GET', 'POST'])
def video_list():
    video_list = glob.glob(video_path)
    video_name = []
    for i, v in enumerate(video_list):
        len_video = librosa.get_duration(filename=v)
        m, s = divmod(len_video, 60)
        vn = {"video_name": v.split("/")[-1],
              "video_time": str(int(m)) + ":" + str(int(s)),
              "name": "立院影片"+str(i)}
        video_name.append(vn)
    
    return jsonify(video_name)



if __name__ == "__main__":
    web_index_path = "index.html"
    path = "video_json/"
    video_path = "./static/video/*.mp4"
    vedio_info = read_json_to_dict(path)
    app.run('172.16.120.124', '1111', threaded = False)
    # app.run('127.0.0.1', '1111', threaded = False)
    
