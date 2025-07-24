import streamlit as st
import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class ZeroToMeanImputer(BaseEstimator, TransformerMixin):
    def __init__(self, cols):
        self.cols = cols
        self.means_ = {}

    def fit(self, X, y=None):
        X = X.copy()
        for col in self.cols:
            non_zero = X[col].replace(0, np.nan)
            self.means_[col] = non_zero.mean()
        return self

    def transform(self, X):
        X = X.copy()
        for col in self.cols:
            X[col] = X[col].replace(0, np.nan)
            X[col] = X[col].fillna(self.means_[col])
        return X

    def get_feature_names_out(self, input_features=None):
        return np.array(self.cols if input_features is None else input_features)

# Load the trained model
@st.cache_resource
def load_model():
    with open('Finalmodel.pki', 'rb') as f:
        model = joblib.load(f)
    return model

model = load_model()

st.title('🚢 Ship Prediction App')
st.write('Enter the following features to predict if a ship is present:')

# Categories mapping
bridge_type_map = {'Floating': 0, 'Pontoon': 1, 'Swing': 2}
period_map = {'Morning': 0, 'Afternoon': 1, 'Evening': 2, 'Night': 3}
rush_time_map = {'Yes': 1, 'No': 0}

# User inputs with descriptive tooltips
bridge_type = st.selectbox(
    'Bridge Type',
    list(bridge_type_map.keys()),
    help='Type of bridge: Floating, Pontoon, or Swing. Influences how ship crossings affect traffic.'
)

closure_min = st.number_input(
    'Closure (min)',
    min_value=0, max_value=1440, value=0,
    help='Duration in minutes the bridge remains closed for ship passage.'
)

vehicle_flow = st.number_input(
    'Vehicle flow (veh/hr)',
    min_value=0, max_value=100000, value=0,
    help='Average number of vehicles passing per hour while the bridge is open.'
)

ships_per_day = st.number_input(
    'Ships per Day',
    min_value=0, max_value=1000, value=0,
    help='Average number of ships passing per day.'
)

delay_per_vehicle = st.number_input(
    'Delay (min) per Vehicle',
    min_value=0.0, max_value=60.0, value=0.0,
    help='Average delay in minutes per vehicle caused by bridge closure.'
)


rush_hour = st.selectbox(
    'Rush Time',
    list(rush_time_map.keys()),
    help='Indicates whether the data was recorded during peak traffic hours.'
)

period_of_day = st.selectbox(
    'Period of Day',
    list(period_map.keys()),
    help='Time of day the data refers to: Morning, Afternoon, Evening, or Night.'
)

def encode_inputs():
    return [
        bridge_type,
        closure_min,
        vehicle_flow,
        rush_time_map[rush_hour],
        period_of_day,
        ships_per_day,
        delay_per_vehicle
    ]


if st.button('Predict'):
    columns = [
        'Bridge_Type',
        'Closure_min',
        'vehicle_flow_veh_hr',
        'rush_hour',
        'period_of_day',
        'Ships_per_day',
        'delay_min_per_vehicle'
    ]

    features = pd.DataFrame([encode_inputs()], columns=columns)

    prediction = model.predict(features)
    if prediction[0] == 1:
        st.success('✅ There is a ship.')
    else:
        st.info('ℹ️ No ship detected.')