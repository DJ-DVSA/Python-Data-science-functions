from flask import Flask, render_template_string

from flask import Flask, render_template_string
from nbconvert import HTMLExporter
import nbformat
import os
import glob

app = Flask(__name__)

## Function to get file names containing string (used for finding notebooks)----------------------------------##
def get_files_with_string_in_name(directory, string):
    fileMatch = []
    
    for pth in glob.iglob(f"{directory}/*"):
        if os.path.isfile(pth):
            fn = os.path.basename(pth)
            if string in fn:
                fileMatch.append(os.path.relpath(pth, directory))

    return fileMatch

cwd = os.getcwd()
pandas_files = get_files_with_string_in_name(f"{cwd}/Notebooks/", "pandas.ipynb")
matplotlib_files = get_files_with_string_in_name(f"{cwd}/Notebooks/", "matplotlib.ipynb")

## Get html code from note books -----------------------------------------------------------------------------##
def html_from_nbs(filenames):
    body = ''
    ## Open and convert pandas notebook files and append to body
    for nx in filenames:
        body += f'<h2>Notebook File: {nx}</h2>'
        
        with open(f'Notebooks/{nx}', 'r', encoding='utf-8') as f:
            notebook_content = f.read()
            
        nb = nbformat.reads(notebook_content, as_version=4)     
        html_exporter = HTMLExporter()
        (body_nb, resources) = html_exporter.from_notebook_node(nb)
        
        body += body_nb
        
    return body

# Route to generate and display HTML from Jupyter notebook content
@app.route('/')
def generate_html():
    
    ### Create Pandas Page
    html_content_start_pd = """<!-- base.html -->
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ title }}</title>
        <link rel="stylesheet" type="text/css" href="static/styles.css">
    </head>
    <h1> A Page of Pandas Related Code </h1>
    <body>"""
    
    html_content_end_pd = """</body>
        </html>"""
    
    body_pd = html_content_start_pd
    
    ## Open and convert pandas notebook files and append to body
    body_pd1 = html_from_nbs(pandas_files)        
    body_pd += body_pd1
    
    body_pd += html_content_end_pd

    ## Generate HTML file from this page
    with open('templates/pandas.html', 'w', encoding='utf-8') as f:
        f.write(render_template_string(body_pd))    
    
    
    ### Create MatPlotLib Page
    
    
    
    
    ### Create Main page
        
    # Add additional note book content
    # Top of HTML page
    html_content_start = """<!-- base.html -->
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ title }}</title>
        <link rel="stylesheet" type="text/css" href="static/styles.css">
    </head>
    <h1> A place to store Python data analysis/science code that I want to remember! </h1>
    <body>"""
    
    html_content_end = """</body>
        </html>"""
    
    
    body = html_content_start
    
    ### Links
    links = """
    <ul>
        <li><a href="templates/pandas.html">Pandas</a></li>
        <li><a href="templates/matplotlib.html">MatPlotLib</a></li>
        <li><a href="templates/seaborn.html">Seaborn</a></li>
    </ul>"""

    body += links
    body += html_content_end
    
    ## Generate HTML file from this page
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(render_template_string(body))

    # Render HTML template with notebook content
    return render_template_string(body)

### Generate Pandas file
# Route to generate and Pandas page when viewing as Flask application
@app.route('/pandas')
def generate_html_pandas():

    html_content = "<h2> Pandas Related functions </h2>"
    body = html_content
    
    with app.open_resource('templates/pandas.html', 'r') as f:
        pandas_html = f.read()
        
    body += pandas_html
    
    return render_template_string(body)

if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/matplotlib')
# def about():
#     return render_template('matplotlib.html')


