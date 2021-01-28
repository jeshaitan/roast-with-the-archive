from flask import render_template, session
from app_pack import app
from app_pack.lineform import LineForm
from app_pack.gen import startsess, genresp
from random import randint
import tensorflow as tf

# Start a Tensorflow/GPT2 session and load from checkpoint
CHECKPOINT = 'run3_med_titled_fast'
tfsess = startsess(CHECKPOINT)
graph = tf.get_default_graph()

@app.route('/', methods=['GET', 'POST'])
def index():
    lform = LineForm()    
    
    # "Start Over." button pressed or empty session
    if lform.cbutton.data or 'acc_roast' not in session:
        session['nothingsofar'] = True
        session['acc_roast'] = ''
        
    # "Go!" button pressed
    if lform.sbutton.data and lform.validate_on_submit():
        if session['nothingsofar']:
            session['nothingsofar'] = False
            session['acc_roast'] = '<|title|>' + lform.lines.data + '\n'
        else:
            session['acc_roast'] = '<|title|>' + session['acc_roast'] + '\n' + lform.lines.data + '\n'

        # Generate response from entire roast so far.
        prompt = session['acc_roast']
        resplength = max(1, len(lform.lines.data) + randint(-1, 10)) 
        with graph.as_default():
            response = genresp(tfsess,
                               temp=0.70,
                               pref=prompt,
                               top_p=0.95,
                               length=resplength,
                               checkpoint=CHECKPOINT)
            # Remove title token
            session['acc_roast'] = response[9:]

    lform.sbutton.disabled = False
    lform.cbutton.disabled = False
    lform.lines.data = ''
    return render_template('index.html', current_roast=session['acc_roast'], form=lform)
