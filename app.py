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
seaborn_files = get_files_with_string_in_name(f"{cwd}/Notebooks/", "seaborn.ipynb")

## Get html code from note books -----------------------------------------------------------------------------##
def html_from_nbs(filenames):
    body = ''
    href_list = ''
    ## Open and convert pandas notebook files and append to body
    for idx, nx in enumerate(filenames):
        body += f'''
        <hr>
        <h2 id=section{idx} style="color:DodgerBlue;font-family:verdana;">Notebook File: {nx}</h2>
        '''
        
        href_list += f'''
        <li><a href="#section{idx}">{nx}</li>
        '''
        
        with open(f'Notebooks/{nx}', 'r', encoding='utf-8') as f:
            notebook_content = f.read()
            
        nb = nbformat.reads(notebook_content, as_version=4)     
        html_exporter = HTMLExporter()
        (body_nb, resources) = html_exporter.from_notebook_node(nb)
        
        body += body_nb
        
    body = "<h3> Contents </h3>" + f'''
    <nav>
        <ul>
            {href_list}
        </ul>
    </nav>
    ''' + body
        
    return body

# Route to generate and display HTML from Jupyter notebook content
@app.route('/')
def generate_html():
    
    ### Create Pandas Page --------------------------------------------------- # 
    html_content_start_pd = """<!-- base.html -->
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ title }}</title>
        <link rel="stylesheet" type="text/css" href="../static/styles.css">
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
    
    
    ### Create MatPlotLib Page --------------------------------------------------- # 
    html_content_start_mpl = """<!-- base.html -->
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ title }}</title>
        <link rel="stylesheet" type="text/css" href="../static/styles.css">
    </head>
    <h1> A Page of MatPlotLib Related Code </h1>
    <body>"""
    
    body_mpl1 = html_from_nbs(matplotlib_files)  
    
    body_mpl = html_content_start_mpl      
    body_mpl += body_mpl1
   
    body_mpl += html_content_end_pd    

    ## Generate HTML file from this page
    with open('templates/matplotlib.html', 'w', encoding='utf-8') as f:
        f.write(render_template_string(body_mpl))      
    
    ### Create Seaborn Page ------------------------------------------------------ # 
    html_content_start_sb = """<!-- base.html -->
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ title }}</title>
        <link rel="stylesheet" type="text/css" href="../static/styles.css">
    </head>
    <h1> A Page of Seaborn Related Code </h1>
    <body>"""    

    body_sb1 = html_from_nbs(seaborn_files)  
    
    body_sb = html_content_start_sb      
    body_sb += body_sb1
   
    body_sb += html_content_end_pd    

    ## Generate HTML file from this page
    with open('templates/seaborn.html', 'w', encoding='utf-8') as f:
        f.write(render_template_string(body_sb))     
    
    
    
    
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

    with app.open_resource('templates/pandas.html', 'r') as f:
        pandas_html = f.read()
        
    body = pandas_html
    
    return render_template_string(body)

### Generate MatPlotLib file
# Route to generate and Pandas page when viewing as Flask application
@app.route('/matplotlib')
def generate_html_matplotlib():

    with app.open_resource('templates/matplotlib.html', 'r') as f:
        matplotlib_html = f.read()
        
    body = matplotlib_html
    
    return render_template_string(body)

### Generate Seaborn file
# Route to generate and Pandas page when viewing as Flask application
@app.route('/seaborn')
def generate_html_seaborn():

    with app.open_resource('templates/seaborn.html', 'r') as f:
        matplotlib_html = f.read()
        
    body = matplotlib_html
    
    return render_template_string(body)


if __name__ == '__main__':
    app.run(debug=True)




