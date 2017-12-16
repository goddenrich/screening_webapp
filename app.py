import os
from flask import Flask, render_template, request
from passenger_screening import train
from animation import plot_image
from multiprocessing import Process

app = Flask(__name__)

PEOPLE_FOLDER = os.path.join('static', 'people_photo')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/')
@app.route('/index')
def show_index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)
    # print(f)


    prob = train(5, "passenger_screening_1512750744.82.npz", f)[0][0]
    anim = plot_image(f)
    animf = os.path.join(app.config['UPLOAD_FOLDER'], 'anim.gif')
    print(animf)
    anim.save(animf, writer='imagemagick', fps=3)
    return render_template('index.html', upload = True, p =  prob, a = True, an = animf)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
