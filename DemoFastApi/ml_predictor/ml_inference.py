from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
from functools import wraps
import sklearn.neural_network
import joblib
import numpy as np
import pandas as pd
import pickle
import os
import time


# Global variables
PWD = os.getcwd()
SCORE_FILE = os.path.join(PWD, "ml_predictor", "credit_score", "algo_lendingclub.pkl")


# Time spent
def spent_time(f):
    start = 0

    @wraps(f)
    def wrapper(*args):
        nonlocal start
        start = time.perf_counter()
        res = f(*args)
        finish = time.perf_counter()
        func_name = f.__name__
        time_spent = round(finish - start, 2)
        print(f"Time spent of func({func_name}): {time_spent} (s)")
        return res

    return wrapper


# Machine learning: default prediction
@spent_time
def predict_with_ml(inputs):
    algo_name = inputs["algo_name"]
    del inputs["algo_name"]
    file_path = os.path.join(
        PWD, "ml_predictor", "default_prediction", f"algo_{algo_name}.sav"
    )
    loaded_model = joblib.load(file_path)
    x_new = pd.DataFrame(inputs, index=[0])
    res = {"res": int(loaded_model.predict(x_new)[0])}
    return res


# The following model and python script
# are mainly from an excellent project:
# https://github.com/Rian021102/credit-scoring-analysis
# Define the get_points_map_dict function
@spent_time
def get_points_map_dict(scorecards):
    # Initialize the dictionary
    points_map_dict = {}
    points_map_dict["Missing"] = {}
    unique_char = set(scorecards["Characteristic"])
    for char in unique_char:
        # Get the Attribute & WOE info for each characteristic
        current_data = scorecards[scorecards["Characteristic"] == char][
            ["Attribute", "Points"]
        ]  # Filter based on characteristic, Then select the attribute & WOE
        # Get the mapping
        points_map_dict[char] = {}
        for idx in current_data.index:
            attribute = current_data.loc[idx, "Attribute"]
            points = current_data.loc[idx, "Points"]
            if attribute == "Missing":
                points_map_dict["Missing"][char] = points
            else:
                points_map_dict[char][attribute] = points
                points_map_dict["Missing"][char] = np.nan
    return points_map_dict


# Define the transform_points function
@spent_time
def transform_points(raw_data, points_map_dict):
    points_data = raw_data.copy()
    # Map the data
    for col in points_data.columns:
        map_col = col  # No need to append '_bin' here
        points_data[col] = points_data[col].map(points_map_dict[map_col])
    # Map the data if there is a missing value or out of range value
    for col in points_data.columns:
        map_col = col  # No need to append '_bin' here
        points_data[col] = points_data[col].fillna(
            value=points_map_dict["Missing"][map_col]
        )
    return points_data


# Define the predict_score function with custom score categorization
@spent_time
def predict_score(raw_data, points_map_dict):
    points_data = transform_points(raw_data, points_map_dict)
    score = sum(points_data.iloc[0, :])
    if score < 250:
        recommendation = "Very Poor"
    elif score >= 250 and score < 300:
        recommendation = "Poor"
    elif score >= 300 and score < 400:
        recommendation = "Fair"
    elif score >= 400 and score < 500:
        recommendation = "Good"
    elif score >= 500 and score < 600:
        recommendation = "Very Good"
    elif score >= 600 and score < 700:
        recommendation = "Exceptional"
    else:
        recommendation = "Excellent"
    res = {"score": score, "rating": recommendation}
    return res


# Load model and create points_map_dict
@spent_time
def get_predict_report(inputs):
    scorecards = pd.read_pickle(SCORE_FILE)
    points_map_dict = get_points_map_dict(scorecards)
    input_table = pd.DataFrame(inputs, index=[0])
    outputs = predict_score(input_table, points_map_dict)
    return outputs
