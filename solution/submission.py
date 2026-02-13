from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_selector as selector
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

def get_model():
    """
    Returns a model that automatically filters out string columns 
    to avoid ValueErrors and fits on numeric data only.
    """
    
    # 1. Define a transformer that ONLY picks numeric columns (float64, int64)
    # This automatically ignores 'well_id_str' and 'date_dt' because they are strings/objects
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, selector(dtype_include=['float64', 'int64']))
        ],
        remainder='drop' # This explicitly drops anything that isn't a number
    )

    # 2. Create the full pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=50, max_depth=8, random_state=42))
    ])
    
    return model
