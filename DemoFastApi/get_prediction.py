import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
import sklearn.neural_network
import joblib
import numpy as np
import pickle
import os


# Global variables
model_file = 'models_02/model_lendingclub.pkl'
num_columns = ['annual_inc_bin', 'loan_amnt_bin', 'int_rate_bin',]
    


# Machine learning: default prediction 
def predict_with_ml(inputs):     
    model_name = inputs['model_name']
    del inputs['model_name'] 
    file_str = 'models_01/model_{}.sav'              
    loaded_model = joblib.load(file_str.format(model_name))        
    x_new = pd.DataFrame(inputs, index=[0]) 
    res = {"res": int(loaded_model.predict(x_new)[0])}       
    return res


# The following model and python script 
# are mainly from an excellent project: 
# https://github.com/Rian021102/credit-scoring-analysis
 
# Define the get_points_map_dict function
def get_points_map_dict(scorecards):
    # Initialize the dictionary
    points_map_dict = {}
    points_map_dict['Missing'] = {}
    unique_char = set(scorecards['Characteristic'])
    for char in unique_char:
        # Get the Attribute & WOE info for each characteristic
        current_data = (scorecards[scorecards['Characteristic'] == char]
                        [['Attribute', 'Points']])  # Filter based on characteristic, Then select the attribute & WOE
        # Get the mapping
        points_map_dict[char] = {}
        for idx in current_data.index:
            attribute = current_data.loc[idx, 'Attribute']
            points = current_data.loc[idx, 'Points']
            if attribute == 'Missing':
                points_map_dict['Missing'][char] = points
            else:
                points_map_dict[char][attribute] = points
                points_map_dict['Missing'][char] = np.nan
    return points_map_dict

# Define the transform_points function
def transform_points(raw_data, points_map_dict, num_cols):
    points_data = raw_data.copy()
    # Map the data
    for col in points_data.columns:
        map_col = col  # No need to append '_bin' here
        points_data[col] = points_data[col].map(points_map_dict[map_col])
    # Map the data if there is a missing value or out of range value
    for col in points_data.columns:
        map_col = col  # No need to append '_bin' here
        points_data[col] = points_data[col].fillna(value=points_map_dict['Missing'][map_col])
    return points_data


# Define the predict_score function with custom score categorization
def predict_score(raw_data, points_map_dict, num_columns):
    points_data = transform_points(raw_data=raw_data, points_map_dict=points_map_dict, num_cols=num_columns)
    score = int(points_data.sum(axis=1))    
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
    res = {'score': score, 'rating': recommendation}    
    return res


# Load model and create points_map_dict 
def get_predict_report(inputs):    
    scorecards = pd.read_pickle(model_file)
    points_map_dict = get_points_map_dict(scorecards=scorecards)
    inputs = inputs.dict()
    input_table = pd.DataFrame(inputs, index=[0])
    outputs = predict_score(
        raw_data=input_table,
        points_map_dict=points_map_dict,
        num_columns=num_columns)
    return outputs
