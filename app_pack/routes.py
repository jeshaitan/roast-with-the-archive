from flask import render_template, session
from app_pack import app
from app_pack.lineform import LineForm
from app_pack.gen import startsess, genresp

import random

# Start a Tensorflow/GPT2 session and load from checkpoint
CHECKPOINT = 'run3_med_titled_fast'
tfsess = startsess(CHECKPOINT)

@app.route('/', methods=['GET', 'POST'])
def index():
    lform = LineForm()

    # "Start Over." button pressed or empty session
    if lform.clear.data or 'acc_roast' not in session:
        session['nothingsofar'] = True
        session['acc_roast'] = ''
            
    # "Go!" button pressed
    if lform.submit.data and lform.validate_on_submit():
        if session['nothingsofar']:
            session['nothingsofar'] = False
            session['acc_roast'] = lform.lines.data + '\n'
        else:
            session['acc_roast'] += lform.lines.data + '\n'

        # Generate response from entire roast so far.
        prompt = session['acc_roast']
        resplength = max(1, len(lform.lines.data) + randint(-5, 15)) 
        response = genresp(tfsess,
                           temp=0.71,
                           pref='<|title|>' + prompt,
                           top_p=0.95,
                           length=resplength,
                           checkpoint=CHECKPOINT)
        session['acc_roast'] += response + '\n'
        
    lform.lines.data = ''
    return render_template('index.html', current_roast=session['acc_roast'], form=lform)
