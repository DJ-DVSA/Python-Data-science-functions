from flask import Flask, render_template_string

from flask import Flask, render_template_string
from nbconvert import HTMLExporter
import nbformat
import os
import glob

app = Flask(__name__)

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

# Route to generate and display HTML from Jupyter notebook content
@app.route('/')
def generate_html():
    # Convert Jupyter notebook content to HTML
    #nb = nbformat.reads(notebook_content, as_version=4)
    with open('Notebooks/example_notebook_pandas.ipynb', 'r', encoding='utf-8') as f:
        notebook_content = f.read()
        
    # Add additional note book content
    html_content = f"<h2> Some headers and stuff</h2>"
    body = html_content
    
    ### Links
    links = """
    <ul>
        <li><a href="templates/pandas.html">Pandas</a></li>
    </ul>"""
    
        
    # Convert JuPyTer Notebook to html    
    nb = nbformat.reads(notebook_content, as_version=4)     
    html_exporter = HTMLExporter()
    (body_nb, resources) = html_exporter.from_notebook_node(nb)

    body += body_nb
    body += links
    
    ## Generate HTML file from this page
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(body)

    # Render HTML template with notebook content
    return render_template_string(body)

### Generate Pandas file
# Route to generate and display HTML from Jupyter notebook content
@app.route('/pandas')
def generate_html_pandas():
    
    
    
    # Convert Jupyter notebook content to HTML
    #nb = nbformat.reads(notebook_content, as_version=4)
    # with open('example_notebook.ipynb', 'r', encoding='utf-8') as f:
    #     notebook_content = f.read()
    
    # Open Notebook files with pandas in the file name
        
    # Add additional note book content
    html_content = "<h2> Pandas Related functions </h2>"
    body = html_content
    
    ## Open and convert pandas notebook files and append to body
    for nx in pandas_files:
        with open(f'Notebooks/{nx}', 'r', encoding='utf-8') as f:
            notebook_content = f.read()
            
        nb = nbformat.reads(notebook_content, as_version=4)     
        html_exporter = HTMLExporter()
        (body_nb, resources) = html_exporter.from_notebook_node(nb)
        
        body += body_nb          

    ## Open and convert matplotlib notebook files and append to body

    ## Generate HTML file from this page
    with open('templates/pandas.html', 'w', encoding='utf-8') as f:
        f.write(body)

    # Render HTML template with notebook content
    return render_template_string(body)

if __name__ == '__main__':
    app.run(debug=True)




# app = Flask(__name__)

# # Routes for the three different tabs
# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/matplotlib')
# def about():
#     return render_template('matplotlib.html')

# @app.route('/pandas')
# def contact():
#     return render_template('pandas.html')

# if __name__ == '__main__':
#     app.run(debug=False)
