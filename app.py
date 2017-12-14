import os
from flask import Flask, render_template, request
from passenger_screening import train
from animation import plot_image

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
    #file.save(f)
    # print(f)


    prob = train(5, "passenger_screening_1512750744.82.npz", f)[0][0]
    anim = plot_image(f)
    animf = os.path.join(app.config['UPLOAD_FOLDER'], 'anim.gif')
    print(animf)
    anim.save(animf, writer='imagemagick', fps=60)
    return render_template('index.html', upload = True, p =  prob, a = True, an = animf)
