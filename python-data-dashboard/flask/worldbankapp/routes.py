from worldbankapp import app

from flask import render_template

import pandas as pd
from wrangling_scripts.wrangling import data_wrangling


data = data_wrangling()
# Test to see if wrangling works
print(data)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    
@app.route('/project-one')
def project_one():
    return render_template('project_one.html')

@app.route('/flask')
def project_flask():
    return render_template('flask.html')

# To tart the web app per, follow the instructions in the instructions.md file.
