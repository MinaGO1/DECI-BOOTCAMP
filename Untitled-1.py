# %%
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler , OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

# %% [markdown]
# #### Descriptive analysis

# %%
data = pd.read_csv(r'E:\Data science\Model_compress\Model\Traffic.csv')

# %%
data.describe(include = 'all')

# %%
# Sperate time from date
data['DateTime'] = pd.to_datetime(data['DateTime'])
hour = data['DateTime'].dt.hour
data['Date'] = pd.to_datetime(data['DateTime'].dt.date)
data.drop('DateTime' , axis =1 , inplace=True )

# %%
data.info()

# %%
data['Date'] = pd.to_datetime(data['Date'])

print(f'Min day: {data['Date'].min()}')
print(f'Max day: {data['Date'].max()}')

# %%
### Grouping the time to four groups Morning, Afternoon, Evening, Night
def period_of_day(h):
    if 5 <= h < 12: return "Morning"
    elif 12 <= h < 17: return "Afternoon"
    elif 17 <= h < 21: return "Evening"
    else: return "Night"

data['period_of_day'] =  hour.apply(period_of_day)
data['rush_hour'] = hour.apply(lambda h: 1 if h in [7, 8, 17, 18] else 0)

# %%
numerical_data = data.select_dtypes('number').drop('rush_hour',axis = 1).columns
numerical_data

# %%
zero_fix_cols = ['delay_min_per_vehicle', 'vehicle_flow_veh_hr', 'Ships_per_day', 'Closure_min']

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
    def get_feature_names_out(self , input_features = None):
        return np.array(
            self.cols if input_features is None else input_features
        )

numerical_pipeline = Pipeline(
    [
        ('zero_to_fix' , ZeroToMeanImputer(zero_fix_cols)),
        ('scaler' , StandardScaler())
    ]
)

# %%
categorical_data = data.select_dtypes('O').drop(['Bridge_Name' , 'ship_present' ] , axis = 1).columns
categorical_data

# %%
preprocessor = ColumnTransformer(
 [
     ('numerical' , numerical_pipeline , numerical_data),
     ('categorical' , OneHotEncoder() , categorical_data)
 ]   
)

# %%
pipeline = Pipeline(
    [
        ('preprocessor' , preprocessor),
        ('model', RandomForestClassifier(random_state=42 , class_weight='balanced'))
    ]
)

# %%
X = data.drop(['Bridge_Name' , 'ship_present' , 'Date' ], axis = 1) 
y = pd.get_dummies(data['ship_present'] , dtype=int)['YES']


# %%
X

# %%
X.columns

# %%
y

# %%
X_train , X_test , y_train , y_test = train_test_split(X , y , test_size = 0.2 ,
                                                      stratify=y)

from sklearn.model_selection import cross_val_score
# Checking the overfitting or underfitting

cross_val_score(pipeline , X_train , y_train)

# %%
pipeline.fit(X_train, y_train)

# %%
y_pred = pipeline.predict(X_test)

y_pred

# %%
X_test

# %%
importances = pipeline['model'].feature_importances_
feature_names = pipeline.named_steps['preprocessor'].get_feature_names_out()

pd.DataFrame({
    'Feature': feature_names,
    'importance': importances
}).sort_values('importance', ascending=False)


# %%
pipeline.named_steps['preprocessor'].get_feature_names_out()

# %%
from sklearn.metrics import accuracy_score , f1_score , classification_report

(accuracy_score(y_test , y_pred),
f1_score(y_test , y_pred))

# %%
print(classification_report(y_test ,y_pred))

# %%
import joblib 

joblib.dump(pipeline , r'E:\Data science\Model_compress\Model\Finalmodel.pki')

# %%
X_test.columns

