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
        lines = "\n".join(lform.lines.data.splitlines())
        print(lines)
        if session['nothingsofar']:
            session['nothingsofar'] = False
            session['acc_roast'] = lines + '\n'
        else:
            session['acc_roast'] = session['acc_roast'] + '\n' + lines + '\n'

        # Generate response from (max) 400 recent tokens.
        roast_tokens = session['acc_roast'].split(" ")
        contextlen = min(len(roast_tokens), 500)
        prompt = " ".join(roast_tokens[(-1 * contextlen):])
        resplength = min(len(lines.split(" ")) * 2, 1023)
        '''
        with graph.as_default():
            session['acc_roast'] = genresp(tfsess,
                               pref=prompt,
                               length=resplength,
                               checkpoint=CHECKPOINT)
        '''
        req = requests.post('https://gpt-jeivmljjkq-uc.a.run.app',
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
