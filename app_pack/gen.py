#import tensorflow as tf
#import gpt_2_simple as gpt2

def startsess(checkpoint):
    tfsess = gpt2.start_tf_sess()
    gpt2.load_gpt2(tfsess, run_name=checkpoint)
    return tfsess

def genresp(tfsess, temp, pref, top_p, length, checkpoint):
    response=gpt2.generate(tfsess,
                           temperature=temp,
                           prefix=pref,
                           top_p=top_p,
                           length=length,
                           truncate="<|endoftext|>",
                           run_name=checkpoint,
                           return_as_list=True)[0]
    return response
