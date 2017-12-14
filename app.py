import os
from flask import Flask, render_template, request
from passenger_screening import train

app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    #file.save(f)    

    prob = train(5, "passenger_screening_1512750744.82.npz", file.filename)[0][0]

    return render_template('index.html', upload = True, p =  prob)
