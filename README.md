# Quote Me AI

Quote Me AI is quotes generating bot whose the only purpose is to generate unique quotes. Generated quotes are drawn onto the image and posted to facebook page [Quote Me AI facebook page](https://www.facebook.com/quotemeai).

## Samples

![alt text](docs/20190704225727.png "Quote Me AI 1")

![alt text](docs/20190704225936.png "Quote Me AI 2")

## Libraries used
* GPT-2-simple - text generation
* Unsplash API - photos search
* spacy - NLP tasks (word embeddings, similarity search)
* Facebook SDK - posting quotes images to Facebook page

## Workflow diagram
![alt text](docs/workflow.png "Workflow")

## How to use
* Install libraries `pip install -r requirements.txt`
* Rename `config_tempalte.py` into `config,py` and fill unsplash and facebook and Google Drive API keys.
* Use `Quote_model_train.ipynb` to train GPT-2 model.
* Copy trained checkpoint to root path.
* Execute `python quote_me_ai.py`