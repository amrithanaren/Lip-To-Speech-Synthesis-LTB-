from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
import os
from model import *


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'wav', 'ogg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/upload')
# def returnHTML():
#    return render_template('index.html')
	
# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       return 'file uploaded successfully'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            transcription = readLip(filename)
            full_path = app.root_path
            print(full_path)
            return render_template("fileUpload.html", transcription = transcription)
            # return send_from_directory(path=full_path, filename="./__temp__.mp4")
            # return send_file(full_path+"/__temp__.mp4", as_attachment=True)
            # return readLip(filename)
    return render_template("./fileUpload.html")

@app.route('/download', methods=['GET', 'POST'])
def download():
    full_path = app.root_path
    # return send_from_directory(full_path, filename)
    filename="__temp__.mp4"
    return send_file(filename, as_attachment=True)

@app.route('/api', methods = ['GET'])
def returnAscii():
    d = {}
    return  { 'output': ord(str(request.args['query'])) }

if __name__ == "__main__":
    app.run(debug = True)