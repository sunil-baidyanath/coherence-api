'''
Created on Dec 9, 2021

@author: sunilthakur
'''

'''
Created on Feb 27, 2021

@author: sunil.thakur
'''

import os
import string
import fnmatch
import json

from flask import Flask, session
# from flask_session import Session
from flask import flash, request, redirect, render_template, url_for, jsonify, make_response

from models import Disease

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

    
@app.route("/")
def index():
    session['disease_list'] = []
    return render_template('home.html')

@app.route("/diseases", methods = ['GET'])
def get_deseases():
    # session['disease_list'] = []
    items = list(string.ascii_uppercase) 
    return render_template('index.html', indexes = items)


@app.route("/diseases/<index>", methods = ['GET'])
def get_deseases_by_index(index):
    disease = Disease()
    items = disease.get_diseases_by_index(index)
    session['disease_list'] = items
    # print(items)
    return make_response(jsonify(items), 200)


@app.route("/diseases/<index>/<disease_id>", methods = ['GET'])
def get_disease_detail(index, disease_id):
    disease = Disease()
    print(disease_id)
    
    detail = disease.get_disease_by_id(disease_id, index)
    print(detail['diseases'])
    
    return render_template('detail.html', item=detail)

@app.route("/diseases/search/<disease_name>", methods = ['GET'])
def get_diseases_by_name(disease_name):
    disease = Disease()
    print(disease_name)
    # session.clear()
    
    items = disease.get_diseases_by_name(disease_name)
    session['disease_list'] = items
    
    return make_response(jsonify(items), 200)
    

if __name__ == '__main__':
    app.run(use_reloader=True, debug=False)