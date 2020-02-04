import os
#import urllib.request

from flask import Flask, flash, request, redirect, render_template, send_file
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './static/uploads'

app = Flask(__name__)
app.secret_key = "d#%d/23^"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10000 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'zip', 'app', 'deb', 'exe'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

@app.route('/')
def index():
    return "welcome test website."

@app.route('/upload')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=["POST"])
def upload_file():
    if request.method == "POST":
        if 'files[]' not in request.files:
            flash('No File Part.')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for f in files:
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                subdir = os.path.join(app.config['UPLOAD_FOLDER'], filename.split('.')[-1])

                if (not os.path.isdir(subdir)):
                    os.mkdir(subdir)

                f.save(os.path.join(subdir, filename))

        flash('File(s) successfully upload.')

    return redirect('/')

@app.route('/downloads')
def downloads():
    walk = os.walk(app.config['UPLOAD_FOLDER'])
    return render_template('downloads.html', walk=walk)

@app.route('/download_file/<path:file>')
def download_file(file):
    return send_file(file)

if '__main__' == __name__:
    app.run(host='0.0.0.0', port=10000)
