from flask import Flask, render_template_string

from flask import Flask, render_template_string
from nbconvert import HTMLExporter
import nbformat

app = Flask(__name__)


# Route to generate and display HTML from Jupyter notebook content
@app.route('/')
def generate_html():
    # Convert Jupyter notebook content to HTML
    #nb = nbformat.reads(notebook_content, as_version=4)
    with open('example_notebook.ipynb', 'r', encoding='utf-8') as f:
        notebook_content = f.read()
        
    # Add additional note book content
    html_content = "<h2> Some headers and stuff </h2>"
    body = html_content
        
    # Convert JuPyTer Notebook to html    
    nb = nbformat.reads(notebook_content, as_version=4)     
    html_exporter = HTMLExporter()
    (body_nb, resources) = html_exporter.from_notebook_node(nb)

    body += body_nb
    
    ## Generate HTML file from this page
    with open('index.html', 'w', encoding='utf-8') as f:
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
