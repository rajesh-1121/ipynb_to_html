import os
from flask import Flask, request, render_template, redirect, session
from nbconvert import HTMLExporter
import nbformat

app = Flask(__name__)

# Secret key for sessions
app.secret_key = 'supersecretkey'

# Global variables for counting
visit_count = 0
conversion_count = 0

@app.route('/')
def home():
    global visit_count

    # Increment visit counter on each visit
    visit_count += 1

    # Store visit count in session (optional: per-user tracking)
    session['visit_count'] = visit_count

    # Render the homepage with the visit and conversion count
    return render_template('index.html', visit_count=visit_count, conversion_count=conversion_count)

@app.route('/convert', methods=['POST'])
def convert_ipynb():
    global conversion_count

    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400

    # Read the uploaded .ipynb file
    notebook_content = file.read().decode('utf-8')
    
    try:
        # Load the notebook content as JSON
        notebook_json = nbformat.reads(notebook_content, as_version=4)

        # Initialize nbconvert HTML exporter
        html_exporter = HTMLExporter()

        # Convert the notebook to HTML
        (html_data, resources) = html_exporter.from_notebook_node(notebook_json)

        # Increment the conversion count when conversion succeeds
        conversion_count += 1

        # Return the HTML output (you can also save it to a file if needed)
        return html_data

    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get the PORT from environment variables
    app.run(host='0.0.0.0', port=port, debug=True)
