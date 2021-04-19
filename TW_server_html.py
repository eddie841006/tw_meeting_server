#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 09:41:57 2020

@author: c95csy
"""
from flask import Flask, request, jsonify, render_template
from flask_cors import cross_origin
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# app.config['debug'] = True

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



if __name__ == "__main__":
    web_index_path = "index.html"
    
    # app.run('172.16.120.247', '1111', threaded = False)
    app.run('172.16.120.124', '1112', threaded = False)
    # app.run('127.0.0.1', '1111', threaded = False)
    
