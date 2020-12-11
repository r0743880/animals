# app.py

import os
from flask import render_template
#from app import app
from flask import Flask, request, make_response, jsonify
from werkzeug.utils import secure_filename
from fastai.vision.all import *
from fastai.data.external import *
from app import app



# codeblock below is needed for Windows path #############
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
##########################################################

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

learner = load_learner('export.pkl')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")
	
@app.route("/about")
def about():
    return """ 
	<h1 style='color: red;'>I'm a red H1 heading!</h1>    <p>This is a lovely little paragraph</p>    <code>Flask is <em>awesome</em></code>    
	"""
	


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return {'error': 'no image found, in request.'}, 400

    file = request.files['image'] 
    if file.filename == '':
        return {'error': 'no image found. Empty'}, 400
 
    if file and allowed_file(file.filename): 
		
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img = PILImage.create(file)
        pred = learner.predict(img)
        #image_url = url_for('uploaded_file', filename=filename)
        print(pred)
		
        # if you want a json reply, together with class probabilities:
        #return jsonify(str(pred))
        # or if you just want the result
        #return {'This is a ': pred[0]}, 200
        return render_template('predict.html', value=pred[0], image=file, url='static/uploads/'+filename)
    return {'error': 'something went wrong.'}, 500

if __name__ == '__main__':
    port = os.getenv('PORT',5000)
    app.run(debug=True, host='0.0.0.0', port=port) 