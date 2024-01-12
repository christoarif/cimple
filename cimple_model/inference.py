import pandas as pd
import numpy as np
import joblib


def _load_model():
    # Load the saved model
    model = joblib.load("mapping_model.pkl")
    model.probability = True
    return model


def predict_mapping(input, num_suggestion=3):
    all_field_names = pd.read_csv("data/field_names.txt", header=None)[0].tolist()

    possible_fields_row = pd.DataFrame(
        [[False] * len(all_field_names)], columns=all_field_names
    )

    if input in all_field_names:
        possible_fields_row[input] = True

        model = _load_model()

        proba_predictions = model.predict_proba(possible_fields_row)

        top_suggestions = np.argsort(proba_predictions[0])[::-1][:num_suggestion]

        top_labels = model.classes_[top_suggestions]

        datamodels_suggestions = [item.split(":")[0] for item in top_labels]
        field_suggestions = [item.split(":")[1] for item in top_labels]
        conf_scores = proba_predictions[0][top_suggestions].tolist()

        print("Top predicted mappings:", top_labels)
        print("Corresponding probabilities:", proba_predictions[0][top_suggestions])

        results = {
            "input": input,
            "datamodels": datamodels_suggestions,
            "fields": field_suggestions,
            "conf_scores": conf_scores,
        }
    else:
        results = {
            "input": input,
            "datamodels": None,
            "fields": None,
            "conf_scores": -1,
        }

    return results


input_value = "obj"
num_suggestions = 3

out = predict_mapping(input_value, num_suggestions)
print("output returned by function :", out)
