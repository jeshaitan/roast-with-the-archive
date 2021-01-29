from flask import render_template, session
from app_pack import app
from app_pack.lineform import LineForm
from app_pack.gen import startsess, genresp
from random import randint
#import tensorflow as tf

import requests

'''
# Start a Tensorflow/GPT2 session and load from checkpoint
CHECKPOINT = 'eot_small'
tfsess = startsess(CHECKPOINT)
graph = tf.get_default_graph()
'''

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
            session['acc_roast'] = lform.lines.data + '\n'
        else:
            session['acc_roast'] = session['acc_roast'] + '\n' + lform.lines.data + '\n'

        # Generate response from entire roast so far.
        prompt = session['acc_roast']
        resplength = min(len(lform.lines.data.split()) * 3, 1023)
        
        '''
        with graph.as_default():
            session['acc_roast'] = genresp(tfsess,
                               pref=prompt,
                               length=resplength,
                               checkpoint=CHECKPOINT)
        '''
        req = requests.post('https://gpt2-api-jeivmljjkq-nn.a.run.app',
                    json={'length': resplength,
                          'temperature': 0.7,
                          'top_p': 0.95,
                          'prefix': prompt,
                          'truncate': '<|endoftext|>'})
        session['acc_roast'] = req.json()['text']

    lform.sbutton.disabled = False
    lform.cbutton.disabled = False
    lform.lines.data = ''
    return render_template('index.html', current_roast=session['acc_roast'], form=lform)
