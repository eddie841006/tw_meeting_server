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
import librosa
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)
# app.config['debug'] = True

'''
    POST data format:
    {
        'text': 'Your text'
    }
'''
    
class LoadVideoInformation():
    def __init__(self, video_dir_path, json_dir_path, sleep_time=20):
        self.video_dir_path = video_dir_path
        self.json_dir_path = json_dir_path
        self.sleep_time = sleep_time

        self.reload_video_info()

        # # load the video information thread
        # self.load_info_thread = threading.Thread(target=self.run)
        # self.load_info_thread.setDaemon(False)
        # self.load_info_thread.start()


    def read_json_to_dict(self):
        """read video json file 

        Arguments:
            path {str} -- json path

        Returns:
            list -- 
        """ 
        json_paths = os.listdir(self.json_dir_path)

        json_info = {}
        for json_path in json_paths:
            with open(os.path.join(self.json_dir_path, json_path), "r") as f:
                data = json.load(f)
            
            json_info[json_path[:-5]] = data
        
        return json_info

    def read_video_info(self):
        video_list = glob.glob(os.path.join(self.video_dir_path, "*.mp4"))
        video_list.sort()

        video_info = []

        for v in video_list:
            video_time = librosa.get_duration(filename=v)
            m, s = divmod(video_time, 60)
            v_name = v.split("/")[-1]
            vn = {
                "video_name": v_name,
                "video_time": str(int(m)) + ":" + str(int(s)),
                "name": v_name.split(".")[0]
            }

            video_info.append(vn)

        return video_info
        
    def reload_video_info(self):
        try:
                self.json_info = self.read_json_to_dict()
                self.video_info = self.read_video_info()

                print("reload info")
                print(self.video_info)

        except:
            print("unsuccess reload info")

    def run(self):
        # s = time.time()

        while True:
            # e = time.time()
            try:
                self.json_info = self.read_json_to_dict()
                self.video_info = self.read_video_info()

                print("reload info")
                print(self.video_info)

            except:
                print("unsuccess reload info")

            time.sleep(self.sleep_time)


@app.route('/video_list', methods=['GET', 'POST'])
def video_list():
    
    print(load_video_information.video_info)

    return jsonify(load_video_information.video_info)

@app.route('/video_json', methods=['GET', 'POST'])
def video_json():
    post_data = request.json
    try:
        name = post_data['video_name']
        print("name", name)
        if name in load_video_information.json_info.keys():
            print("success post video json")
            return jsonify(load_video_information.json_info[name])
    
        else:
            print(name + "don't have subline")
            return {"error": name + "don't have subline"}
        
    except:
        return {"error": """must post {'video_name': name}"""}

@app.route('/reload', methods=['GET', "POST"])
def reload():
    load_video_information.reload_video_info()

    return {"state": "success"}




if __name__ == "__main__":
    web_index_path = "index.html"
    json_dir_path = "video_json/"
    video_dir_path = "./static/video/"
    
    load_video_information = LoadVideoInformation(video_dir_path, json_dir_path)

    # app.run('172.16.120.247', '1111', threaded = False)
    app.run('172.16.120.124', '1111', threaded = False)
    # app.run('127.0.0.1', '1111', threaded = False)
    
