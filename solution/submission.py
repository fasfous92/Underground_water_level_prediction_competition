import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

class NumericSelector(BaseEstimator, TransformerMixin):
    """
    Custom transformer to select only numeric columns.
    """
    def fit(self, X, y=None):
        return self 
        
    def transform(self, X, y=None):
        # If the input is a Pandas DataFrame, drop the string/object columns
        if isinstance(X, pd.DataFrame):
            return X.select_dtypes(include=['number'])
        return X

def get_model():
    """
    Returns a lightweight, extremely fast Random Forest for testing.
    """
    
    preprocessor = Pipeline(steps=[
        ('selector', NumericSelector()),
        ('imputer', SimpleImputer(strategy='median'))
    ])

    # 2. Create the full pipeline with a "Fast" Random Forest
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(
            n_estimators=10,       # Reduced from 50 (Makes it 5x faster)
            max_depth=5,           # Reduced from 8 (Keeps trees shallow and quick)
            n_jobs=-1,             # CRITICAL: Forces Python to use all CPU cores!
            random_state=42
        ))
    ])
    
    return model
