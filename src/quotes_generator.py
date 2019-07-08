import gpt_2_simple as gpt2

model = None
session = None


def load_model(name):
    global model, session
    session = gpt2.start_tf_sess()
    model = gpt2.load_gpt2(session,
                           run_name=name)


def generate(length=50, temperature=0.8, prefix='<|startoftext|>', truncate='<|endoftext|>',
             nsamples=1, include_prefix=False, return_as_list=True, top_k=40, run_name='model'):
    text = gpt2.generate(session,
                         run_name=run_name,
                         length=length,
                         temperature=temperature,
                         prefix=prefix,
                         truncate=truncate,
                         nsamples=nsamples,
                         include_prefix=include_prefix,
                         return_as_list=return_as_list,
                         top_k=top_k)

    return text