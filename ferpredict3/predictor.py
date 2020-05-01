from __future__ import print_function

import numpy as np
import pandas as pd
from io import StringIO
from konlpy.tag import Komoran
from models.simple_cnn import SimpleCNN
from tensorflow.keras.optimizers import Adam
from textRank import textrank_keyword, textrank_keysentence
from tensorflow.keras.losses import categorical_crossentropy
from sklearn.metrics import confusion_matrix, classification_report
import os, json, pickle, sys, signal, traceback, preprocess, util, flask

# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.

class ScoringService(object):
    model = None                # Where we keep the model when it's loaded

    @classmethod
    def get_model(cls):
        """Get the model object for this instance, loading it if it's not already loaded."""
        num_features = 64
        num_labels = 7
        size = (48, 48)
        cls.model = SimpleCNN(num_features, num_labels, size)
        cls.model.load_weights('./models/sCNN.best.hdf5')
        cls.model.compile(loss=categorical_crossentropy,
                optimizer=Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7),
                metrics=['accuracy'])
        return cls.model

    @classmethod
    def predict(cls, input):
        clf = cls.get_model()
        return clf.predict(input)

# The flask app for serving predictions
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = ScoringService.get_model()  # You can insert a health check here
    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    data = None
    # Convert from CSV to pandas
    if flask.request.content_type == 'application/json':
        form = json.loads(flask.request.data.decode('utf-8'))
        # decoded = url.decode('utf-8')
        data = preprocess.video_to_npy(form["video_url"])
        
    else:
        return flask.Response(response='this predictor only recieve url', status=415, mimetype='text/plain')

    print('Invoked with {} records'.format(data.shape[0]))

    # Do the prediction
    predictions = ScoringService.predict(data)
    np.savetxt('data/emotion.csv', predictions, delimiter=",")
    filename = util.upload_file('data/emotion.csv', form, '.csv', 'mind-gitter-diary')
    audio = util.upload_file('data/audio.wav', form, '.wav', 'mind-gitter-diary')
    fulltext, text = util.speaking_to_text(audio, form)
    komoran = Komoran()
    keywords = textrank_keyword(fulltext, komoran, 2, 2, 0, df=0.85, max_iter=30, topk=30)
    keysents = textrank_keysentence(fulltext, tokenize=komoran, min_count=2)
    result = {
        "emotions": filename,
        "fulltext": text,
        "tags": keywords,
        "abb": keysents
    }

    return flask.Response(response=json.dumps(result), status=200, mimetype='application/json')