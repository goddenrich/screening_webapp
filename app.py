import os
from flask import Flask, render_template, request
from passenger_screening import train
from animation import plot_image
from multiprocessing import Pool
#from multiprocessing import Process
#import multiprocessing as mp
import threading
from threading import Thread
import time

app = Flask(__name__)

PEOPLE_FOLDER = os.path.join('static', 'people_photo')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

list1=list()
list2=list()

def func1(a, b, c):
    global list1
    list1 = [train(a, b, c)[0][0]]

def func2(x):
    global list2
    list2 = [plot_image(x)]

@app.route('/')
@app.route('/index')
def show_index():
    return render_template('index.html')

bg_clr = False

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)
    # print(f)

    #pool = Pool(processes=2)
    #prob = train(5, "passenger_screening_1512750744.82.npz", f)[0][0]
    #prob = pool.map_async(train, 5, "passenger_screening_1512750744.82.npz", f)[0][0]
    #anim = plot_image(f)
    #t = (5, "passenger_screening_1512750744.82.npz", f)
    #pool.apply_async(train, args=t)
     
    Thread(target = func1, args=(5,"passenger_screening_1512750744.82.npz", f)).start()
    Thread(target = func2, args=(f,)).start()

    while not list1 or not list2:
        time.sleep(4)
    prob = list1[0]
    
    animf = os.path.join(app.config['UPLOAD_FOLDER'], 'anim.gif')
    print(animf)
    list2[0].save(animf, writer='imagemagick', fps=3)
    if prob > 0.5:
        bg_clr = 'red'
    else:
        bg_clr = 'lightgreen'
    return render_template('index.html', upload = True, p =  prob, a = True, an = animf, bg = bg_clr)

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
