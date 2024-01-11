import sys
import os
sys.path.append("/opt/splunk/etc/apps/cimple/bin/")

import pandas as pd
import numpy as np
import joblib


from splunk.persistconn.application import PersistentServerConnectionApplication
import json
import time

def _load_model():
    # # Load the saved model
    model = joblib.load("/opt/splunk/etc/apps/cimple/bin/weights/mapping_model.pkl")
    model.probability = True
    return model

def predict_mapping(input, num_suggestion=3):
    all_field_names = pd.read_csv("/opt/splunk/etc/apps/cimple/bin/data/field_names.txt", header=None)[0].tolist()

    possible_fields_row = pd.DataFrame(
        [[False] * len(all_field_names)], columns=all_field_names
    )

    if input in all_field_names:
        possible_fields_row[input] = True

        model = _load_model()

        # proba_predictions = model.predict_proba(possible_fields_row)
        proba_predictions = model.predict(possible_fields_row)

        top_suggestions = np.argsort(proba_predictions[0])[::-1][:num_suggestion]

        top_labels = model.classes_[top_suggestions]

        datamodels_suggestions = [item.split(":")[0] for item in top_labels]
        field_suggestions = [item.split(":")[1] for item in top_labels]
        conf_scores = proba_predictions[0][top_suggestions].tolist()

        results = {
            "input": input,
            "data-model": datamodels_suggestions,
            "field": field_suggestions,
            "conf_score": conf_scores,
        }
    else:
        results = {
            "input": input,
            "data-model": None,
            "field": None,
            "conf_score": -1,
        }

    return results


class Cimple(PersistentServerConnectionApplication):
    def __init__(self, _command_line, _command_arg):
        super(PersistentServerConnectionApplication, self).__init__()

    # Handle a syncronous from splunkd.
    def handle(self, in_string):
        """
        Called for a simple synchronous request.
        @param in_string: request data passed in
        @rtype: string or dict
        @return: String to return in response.  If a dict was passed in,
                 it will automatically be JSON encoded before being returned.
        """

        decoded_string = in_string.decode('utf-8')


        # Parsing the JSON data
        data = json.loads(decoded_string)
        form_data = ""
        r_output = []
        # Accessing the form data
        if 'form' in data:
            # Extracting the form data
            form_data = data['form']
            input_string = form_data[0][0]     # need to semicomma separate it

            inputs = input_string.split(";")
            num_suggestions = 1
            for i in inputs:
                out = predict_mapping(i, num_suggestions)

                for x in range(num_suggestions):
                    r_output.append({
                        "input": out['input'],
                        "data-model": out['data-model'][x],
                        "field": out['field'][x],
                    })

        payload = r_output
        return {'payload': payload, 'status': 200}

    def handleStream(self, handle, in_string):
        """
        For future use
        """
        raise NotImplementedError(
            "PersistentServerConnectionApplication.handleStream")

    def done(self):
        """
        Virtual method which can be optionally overridden to receive a
        callback after the request completes.
        """
        pass

