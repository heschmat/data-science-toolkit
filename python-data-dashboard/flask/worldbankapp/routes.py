from worldbankapp import app
from wrangling_scripts.wrangle_data import return_figures

import json
import plotly
from flask import render_template

import pandas as pd
# from wrangling_scripts.wrangling import data_wrangling


# data = data_wrangling()
# # Test to see if wrangling works
# print(data)

@app.route('/')
@app.route('/index')
def index():
    figures = return_figures()

    # Plot ids for HTML id tag
    ids = [f'figure-{i}' for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for JS in HTML template
    figures_json = json.dumps(figures, cls= plotly.utils.PlotlyJSONEncoder)
    
    return render_template('index.html', ids = ids, figuresJSON = figures_json)


@app.route('/project-one')
def project_one():
    return render_template('project_one.html')

@app.route('/flask')
def project_flask():
    return render_template('flask.html')

# To tart the web app per, follow the instructions in the instructions.md file.
